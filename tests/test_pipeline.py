import numpy as np
import pytest

from frontier import cluster, merge
from frontier.db import connect
from frontier.extract import Candidate, Extraction, Role, drop_dangling
from frontier.llm import Models, strict_schema


class FakeLLM:
    """Embeds by keyword so similarity is predictable, and answers merge calls from a script."""

    VOCAB = ("influence", "hessian", "kl", "sae", "feature", "loss")

    def __init__(self, conn, decisions=None):
        self.conn = conn
        self.models = Models()
        self.decisions = decisions or {}
        self.calls = []

    def embed(self, texts):
        rows = []
        for t in texts:
            v = np.array([1.0 if w in t.lower() else 0.0 for w in self.VOCAB] + [0.1])
            rows.append(v / np.linalg.norm(v))
        return np.array(rows, dtype=np.float32)

    def structured(self, purpose, model, schema, system, user, effort="medium"):
        self.calls.append((purpose, user))
        if schema is merge.Decisions:
            return merge.Decisions(
                decisions=[d for k, d in self.decisions.items() if f"key={k!r}" in user]
            )
        if schema is cluster.ClusterName:
            return cluster.ClusterName(name="Topic", summary="About a topic.")
        raise AssertionError(schema)


def cand(key, statement, prereqs=(), role: Role = "prerequisite"):
    return Candidate(
        key=key,
        statement=statement,
        kind="definition",
        role=role,
        importance=2,
        prerequisites=list(prereqs),
        evidence="",
    )


@pytest.fixture
def conn(tmp_path):
    return connect(tmp_path / "pool.db")


def add_source(conn, ref):
    return conn.execute("INSERT INTO sources (ref, text) VALUES (?, '')", (ref,)).lastrowid


def test_first_source_adds_everything_with_internal_links(conn):
    llm = FakeLLM(conn)
    s = add_source(conn, "a")
    stats = merge.add_candidates(
        conn,
        llm,  # type: ignore[arg-type]
        s,
        Extraction(
            title="A",
            facts=[cand("f1", "The Hessian of the loss"), cand("f2", "Influence uses it", ["f1"])],
        ),
    )
    assert (stats.new, stats.duplicates, stats.edges) == (2, 0, 1)
    assert not llm.calls, "nothing to merge against, so no merge call"


def test_duplicate_attaches_source_and_upgrades_role(conn):
    llm = FakeLLM(conn)
    s1 = add_source(conn, "a")
    merge.add_candidates(
        conn,
        llm,  # type: ignore[arg-type]
        s1,
        Extraction(title="A", facts=[cand("f1", "KL divergence is asymmetric")]),
    )
    existing = conn.execute("SELECT id FROM facts").fetchone()[0]

    llm.decisions = {
        "g1": merge.Decision(
            key="g1",
            action="duplicate",
            duplicate_of=existing,
            prerequisite_ids=[],
            dependent_ids=[],
            reason="same",
        )
    }
    s2 = add_source(conn, "b")
    stats = merge.add_candidates(
        conn,
        llm,  # type: ignore[arg-type]
        s2,
        Extraction(
            title="B",
            facts=[cand("g1", "Relative entropy (KL) is not symmetric", role="contribution")],
        ),
    )
    assert (stats.new, stats.duplicates) == (0, 1)
    roles = dict(
        conn.execute("SELECT source_id, role FROM fact_sources WHERE fact_id = ?", (existing,))
    )
    assert roles == {s1: "prerequisite", s2: "contribution"}


def test_merge_ignores_ids_it_was_not_shown(conn):
    llm = FakeLLM(conn)
    s1 = add_source(conn, "a")
    merge.add_candidates(
        conn,
        llm,  # type: ignore[arg-type]
        s1,
        Extraction(title="A", facts=[cand("f1", "SAE feature")]),
    )
    llm.decisions = {
        "g1": merge.Decision(
            key="g1",
            action="duplicate",
            duplicate_of=999,
            prerequisite_ids=[999],
            dependent_ids=[],
            reason="hallucinated",
        )
    }
    stats = merge.add_candidates(
        conn,
        llm,  # type: ignore[arg-type]
        add_source(conn, "b"),
        Extraction(title="B", facts=[cand("g1", "SAE feature, again")]),
    )
    assert (stats.new, stats.duplicates, stats.edges) == (1, 0, 0)


def test_links_that_would_make_a_cycle_are_skipped(conn):
    llm = FakeLLM(conn)
    s1 = add_source(conn, "a")
    merge.add_candidates(
        conn,
        llm,  # type: ignore[arg-type]
        s1,
        Extraction(
            title="A",
            facts=[cand("f1", "Hessian"), cand("f2", "Influence via Hessian", ["f1"])],
        ),
    )
    hessian, influence = (r[0] for r in conn.execute("SELECT id FROM facts ORDER BY id"))
    # A new fact claiming to need `influence` while being needed by `hessian` closes a loop.
    llm.decisions = {
        "g1": merge.Decision(
            key="g1",
            action="new",
            duplicate_of=None,
            prerequisite_ids=[influence],
            dependent_ids=[hessian],
            reason="",
        )
    }
    stats = merge.add_candidates(
        conn,
        llm,  # type: ignore[arg-type]
        add_source(conn, "b"),
        Extraction(title="B", facts=[cand("g1", "Influence and Hessian loss")]),
    )
    assert (stats.edges, stats.cycles_skipped) == (1, 1)


def test_drop_dangling_removes_unknown_self_and_repeated_keys():
    e = drop_dangling(
        Extraction(title="", facts=[cand("a", "x", ["a", "b", "zz", "b"]), cand("b", "y")])
    )
    assert e.facts[0].prerequisites == ["b"]


def test_clusters_keep_identity_when_membership_mostly_survives():
    previous = {7: {1, 2, 3, 4}, 8: {5, 6}}
    assert cluster.match_previous([{1, 2, 3, 4, 9}, {10, 11}], previous) == {0: 7}


def test_recluster_names_only_new_clusters(conn):
    llm = FakeLLM(conn)
    merge.add_candidates(
        conn,
        llm,  # type: ignore[arg-type]
        add_source(conn, "a"),
        Extraction(
            title="A",
            facts=[cand("a", "influence hessian"), cand("b", "sae feature", ["a"])],
        ),
    )
    cluster.recluster(conn, llm)  # type: ignore[arg-type]
    named = sum(1 for p, _ in llm.calls if p == "name_cluster")
    cluster.recluster(conn, llm)  # type: ignore[arg-type]
    assert sum(1 for p, _ in llm.calls if p == "name_cluster") == named


def test_keyword_query_quotes_terms_and_drops_stopwords():
    assert merge.keyword_query("The EK-FAC approximation and the Hessian") == (
        '"approximation" OR "ek-fac" OR "hessian"'
    )
    assert merge.keyword_query("of to a") is None


def test_strict_schema_requires_every_property_and_keeps_title_fields():
    schema = strict_schema(Extraction)
    assert schema["required"] == ["title", "facts"]
    assert schema["additionalProperties"] is False
    candidate = schema["$defs"]["Candidate"]
    assert candidate["additionalProperties"] is False
    assert set(candidate["required"]) == set(Candidate.model_fields)
