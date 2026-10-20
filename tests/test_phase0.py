import json

import pytest
from fastapi.testclient import TestClient

from frontier import ingest, matcher, store
from frontier.matcher import Link, Req
from frontier.requirements import Requirement, store_candidates
from frontier.web import create_app


@pytest.fixture
def conn(tmp_path):
    return store.connect(tmp_path / "f.db")


def test_migrations_are_idempotent(tmp_path):
    store.connect(tmp_path / "f.db")
    conn = store.connect(tmp_path / "f.db")
    assert conn.execute("PRAGMA user_version").fetchone()[0] == len(store.MIGRATIONS)


def test_split_spans_classifies_and_merges_fragments():
    page = (
        "A real paragraph about influence functions, which ends with a full stop.\n\n"
        "Figure 2: Influence scores by layer.\n\n"
        "Method\n\nRanking\n\n12.5 10.0 7.5\n\n"
        "3 of 86\n\n"
        "Another paragraph that is long enough to count as prose, also ending with a stop."
    )
    spans, warnings = ingest.split_spans([page])
    kinds = [s.kind for s in spans]
    assert kinds == ["paragraph", "caption", "fragments", "paragraph"]
    assert spans[2].text == "Method | Ranking | 12.5 10.0 7.5"
    assert not any("3 of 86" in s.text for s in spans)
    assert any("figure and table contents" in w for w in warnings)


def test_identify_prefers_arxiv_identity(tmp_path):
    assert ingest.identify(tmp_path / "ed09f796-2502.03407v1.pdf") == (
        "arxiv:2502.03407",
        "arxiv",
        "v1",
    )
    assert ingest.identify(tmp_path / "c11823fb-Neural_Networks_Are_Already_Clean.pdf")[0] == (
        "doc:neural-networks-are-already-clean"
    )


def seed_revision(conn, n_spans=5):
    with conn:
        conn.execute("INSERT INTO sources (source_id, kind) VALUES ('arxiv:1', 'arxiv')")
        conn.execute(
            "INSERT INTO revisions (revision_id, source_id, content_hash, raw_path,"
            " parser_version, coverage_warnings) VALUES ('r1', 'arxiv:1', 'h', 'x', 'p', '[]')"
        )
        conn.executemany(
            "INSERT INTO spans VALUES ('r1', ?, ?, 1, 'paragraph', 'text')",
            [(f"S{i}", i) for i in range(n_spans)],
        )
        conn.execute(
            "INSERT INTO artifacts (artifact_id, stage, requested_model, prompt_hash,"
            " schema_name, params, path, outcome) VALUES ('a1','s','m','h','S','{}','p','ok')"
        )


def req(spans):
    return Requirement(
        label="KL",
        sense="divergence",
        capability="explain KL",
        depth="explain",
        required_elements=["asymmetric"],
        served_span_ids=spans,
        centrality="background",
        why_needed="eq 3",
    )


def test_store_candidates_drops_invalid_spans_and_rejects_mostly_invalid(conn):
    seed_revision(conn)
    valid = ingest.span_ids(conn, "r1")
    (cid,) = store_candidates(
        conn, "r1", "guide", "a1", [req(["S1", "S2", "S3", "S4", "S99"])], valid
    )
    stored = conn.execute(
        "SELECT served_span_ids FROM requirement_candidates WHERE candidate_id = ?", (cid,)
    ).fetchone()[0]
    assert json.loads(stored) == ["S1", "S2", "S3", "S4"]
    with pytest.raises(ValueError):
        store_candidates(conn, "r1", "guide", "a1", [req(["S98", "S99", "S1"])], valid)


def link(pred, relation, elements):
    return Link(predicted=pred, relation=relation, covered_elements=elements, evidence="")


def test_coverage_needs_all_elements_and_ignores_non_covering_relations():
    gold = Req("G", "IF", "s", "c", "derive", ["a", "b", "c"])
    assert (
        matcher.coverage(gold, [link("P1", "covers_part", [0]), link("P2", "covers_part", [1, 2])])
        == 1
    )
    assert matcher.coverage(gold, [link("P1", "equivalent", [])]) == 1
    assert matcher.coverage(gold, [link("P1", "broader_but_not_explicit", [0, 1, 2])]) == 0
    assert matcher.coverage(gold, [link("P1", "covers_part", [0, 0])]) == pytest.approx(1 / 3)


def test_label_api_appends_and_sealed_exams_are_hidden(conn, tmp_path):
    seed_revision(conn)
    store_candidates(conn, "r1", "gold_draft", "a1", [req(["S1"])], ingest.span_ids(conn, "r1"))
    cid = conn.execute("SELECT candidate_id FROM requirement_candidates").fetchone()[0]
    with conn:
        conn.execute(
            "INSERT INTO exams (exam_id, revision_id, artifact_id, content_hash, sealed)"
            " VALUES ('a1', 'r1', 'a1', 'h', 1)"
        )
    client = TestClient(create_app(tmp_path / "f.db"))
    assert client.post("/api/label", json={"candidate_id": cid, "label": "know"}).status_code == 200
    assert (
        client.post("/api/label", json={"candidate_id": cid, "label": "partly"}).status_code == 200
    )
    assert client.post("/api/label", json={"candidate_id": cid, "label": "meh"}).status_code == 400
    labels = [r[0] for r in conn.execute("SELECT label FROM owner_labels ORDER BY label_id")]
    assert labels == ["know", "partly"]
    assert "review exam" not in client.get("/").text
    assert client.get("/exam/a1").status_code == 404
    assert "<span id='done'>1</span>/1 labelled" in client.get("/label/r1").text


def test_label_and_review_posts_reject_unknown_or_sealed_targets(conn, tmp_path):
    seed_revision(conn)
    with conn:
        conn.execute(
            "INSERT INTO exams (exam_id, revision_id, artifact_id, content_hash, sealed)"
            " VALUES ('a1', 'r1', 'a1', 'h', 1)"
        )
    client = TestClient(create_app(tmp_path / "f.db"))
    assert (
        client.post("/api/label", json={"candidate_id": "nope", "label": "know"}).status_code == 404
    )
    review = {"exam_id": "a1", "question_id": "q1", "verdict": "good"}
    assert client.post("/api/exam_review", json=review).status_code == 404
    assert client.post("/api/missing", json={"revision_id": "nope", "text": "x"}).status_code == 404


def test_load_exam_refuses_a_changed_artifact(conn, tmp_path):
    from frontier import generate

    seed_revision(conn)
    exam = generate.Exam(questions=[])
    path = tmp_path / "exam.json"
    path.write_text(
        json.dumps({"response": {"choices": [{"message": {"content": exam.model_dump_json()}}]}})
    )
    with conn:
        conn.execute(
            "INSERT INTO artifacts (artifact_id, stage, requested_model, prompt_hash,"
            " schema_name, params, path, outcome) VALUES ('e1','exam','m','h','Exam','{}',?,'ok')",
            (str(path),),
        )
        conn.execute(
            "INSERT INTO exams (exam_id, revision_id, artifact_id, content_hash)"
            " VALUES ('e1', 'r1', 'e1', 'not-the-hash')"
        )
    with pytest.raises(ValueError):
        generate.load_exam(conn, "e1")
    with pytest.raises(KeyError):
        generate.load_exam(conn, "missing")


def test_dehyphenation_keeps_suspended_hyphens():
    spans, _ = ingest.split_spans(
        ["We use first- and second-order methods, which were con- tinued later in training."]
    )
    assert spans[0].text == (
        "We use first- and second-order methods, which were continued later in training."
    )


def test_label_page_hides_details_until_labelled_and_records_blindness(conn, tmp_path):
    seed_revision(conn)
    store_candidates(conn, "r1", "gold_draft", "a1", [req(["S1"])], ingest.span_ids(conn, "r1"))
    cid = conn.execute("SELECT candidate_id FROM requirement_candidates").fetchone()[0]
    with conn:
        conn.execute("UPDATE requirement_candidates SET self_test = 'Why is KL odd?'")
    client = TestClient(create_app(tmp_path / "f.db"))
    page = client.get("/label/r1").text
    assert "Why is KL odd?" in page
    assert "<div class='hidden-details' hidden>" in page
    client.post("/api/label", json={"candidate_id": cid, "label": "know", "revealed": False})
    client.post("/api/label", json={"candidate_id": cid, "label": "partly", "revealed": True})
    assert conn.execute(
        "SELECT label, revealed FROM owner_labels ORDER BY label_id"
    ).fetchall() == [
        ("know", 0),
        ("partly", 1),
    ]
    assert "<div class='hidden-details'>" in client.get("/label/r1").text
