import re
import sqlite3
from dataclasses import dataclass
from typing import Literal

import networkx as nx
import numpy as np
from pydantic import BaseModel

from frontier.db import from_blob, to_blob
from frontier.extract import Candidate, Extraction
from frontier.llm import LLM

EMBED_NEIGHBORS = 6
KEYWORD_NEIGHBORS = 3
CHUNK = 25


class Decision(BaseModel):
    key: str
    action: Literal["new", "duplicate"]
    duplicate_of: int | None
    prerequisite_ids: list[int]
    dependent_ids: list[int]
    reason: str


class Decisions(BaseModel):
    decisions: list[Decision]


SYSTEM = """\
You maintain a pool of atomic facts that a learner studies over months. New candidate facts \
were just extracted from a paper. For each candidate you see the most similar facts already in \
the pool. Decide how each candidate joins the pool.

action:
- duplicate: the candidate and an existing fact are the same knowledge — anyone who knows one \
knows the other, even if worded differently or using different names for the same thing \
("relative entropy" / "KL divergence"). Set duplicate_of to that fact's ID. Missing a duplicate \
splits the learner's history in two; that is the main failure this step exists to prevent.
- new: anything else, including candidates that are more specific than, more general than, or a \
consequence of an existing fact. Those are distinct facts; connect them with links instead.

Links, for both actions, using only IDs of the existing facts shown with that candidate:
- prerequisite_ids: existing facts that understanding the candidate directly requires.
- dependent_ids: existing facts whose understanding directly requires the candidate.
Only direct, genuine dependencies; leave them empty when none apply. For a duplicate, give the \
links the candidate brings that the existing fact may lack.

reason: one short sentence, mainly useful for duplicates and borderline calls.

Return exactly one decision per candidate key.
"""


@dataclass
class PoolFact:
    id: int
    statement: str
    embedding: np.ndarray


def load_pool(conn: sqlite3.Connection) -> list[PoolFact]:
    return [
        PoolFact(r["id"], r["statement"], from_blob(r["embedding"]))
        for r in conn.execute("SELECT id, statement, embedding FROM facts ORDER BY id")
    ]


def keyword_query(text: str) -> str | None:
    words = {w.lower() for w in re.findall(r"[A-Za-z][A-Za-z0-9-]{2,}", text)}
    words -= STOPWORDS
    return " OR ".join(f'"{w}"' for w in sorted(words)) or None


def neighbors(
    conn: sqlite3.Connection, pool: list[PoolFact], matrix: np.ndarray, cand: Candidate, vec
) -> list[int]:
    """Indexes into `pool` of the facts most likely to duplicate or link to `cand`."""
    found = list(np.argsort(-(matrix @ vec))[:EMBED_NEIGHBORS])
    query = keyword_query(cand.statement)
    if query:
        index_of = {f.id: i for i, f in enumerate(pool)}
        rows = conn.execute(
            "SELECT rowid FROM facts_fts WHERE facts_fts MATCH ? ORDER BY bm25(facts_fts) LIMIT ?",
            (query, KEYWORD_NEIGHBORS),
        )
        found += [index_of[r[0]] for r in rows if r[0] in index_of]
    return list(dict.fromkeys(int(i) for i in found))


def judge(llm: LLM, batch: list[tuple[Candidate, list[PoolFact]]]) -> dict[str, Decision]:
    parts = []
    for cand, near in batch:
        lines = "\n".join(f"  [{f.id}] {f.statement}" for f in near)
        parts.append(
            f"<candidate key={cand.key!r}>\n{cand.statement}\nExisting:\n{lines}\n</candidate>"
        )
    result = llm.structured(
        "merge", llm.models.merge, Decisions, SYSTEM, "\n\n".join(parts), effort="low"
    )
    return {d.key: d for d in result.decisions}


@dataclass
class IngestStats:
    extracted: int = 0
    candidates: int = 0
    new: int = 0
    duplicates: int = 0
    edges: int = 0
    cycles_skipped: int = 0


def add_candidates(
    conn: sqlite3.Connection, llm: LLM, source_id: int, extraction: Extraction
) -> IngestStats:
    stats = IngestStats(candidates=len(extraction.facts))
    cands = extraction.facts
    vecs = llm.embed([c.statement for c in cands])
    pool = load_pool(conn)

    decisions: dict[str, Decision] = {}
    shown: dict[str, set[int]] = {}
    if pool:
        matrix = np.stack([f.embedding for f in pool])
        batch = []
        for cand, vec in zip(cands, vecs, strict=True):
            near = [pool[i] for i in neighbors(conn, pool, matrix, cand, vec)]
            shown[cand.key] = {f.id for f in near}
            batch.append((cand, near))
        for i in range(0, len(batch), CHUNK):
            decisions |= judge(llm, batch[i : i + CHUNK])

    graph = nx.DiGraph(
        [(r[0], r[1]) for r in conn.execute("SELECT prereq_id, fact_id FROM fact_edges")]
    )
    fact_of: dict[str, int] = {}
    pending_links: list[tuple[int, int]] = []

    for cand, vec in zip(cands, vecs, strict=True):
        d = decisions.get(cand.key)
        allowed = shown.get(cand.key, set())
        if d and d.action == "duplicate" and d.duplicate_of in allowed:
            fact_id = d.duplicate_of
            action, reason = "duplicate", d.reason
            stats.duplicates += 1
        else:
            fact_id = conn.execute(
                "INSERT INTO facts (statement, kind, embedding) VALUES (?, ?, ?)",
                (cand.statement, cand.kind, to_blob(vec)),
            ).lastrowid
            assert fact_id is not None
            action = "new"
            reason = d.reason if d else ("empty pool" if not pool else "no decision returned")
            stats.new += 1
        fact_of[cand.key] = fact_id
        conn.execute(
            "INSERT INTO fact_sources (fact_id, source_id, role, importance, evidence)"
            " VALUES (?, ?, ?, ?, ?) ON CONFLICT DO UPDATE SET"
            " importance = max(importance, excluded.importance),"
            " role = CASE WHEN excluded.role = 'contribution' THEN 'contribution' ELSE role END",
            (fact_id, source_id, cand.role, cand.importance, cand.evidence),
        )
        conn.execute(
            "INSERT INTO merge_log (source_id, candidate, action, fact_id, reason)"
            " VALUES (?, ?, ?, ?, ?)",
            (source_id, cand.statement, action, fact_id, reason),
        )
        if d:
            pending_links += [(p, fact_id) for p in d.prerequisite_ids if p in allowed]
            pending_links += [(fact_id, q) for q in d.dependent_ids if q in allowed]

    for cand in cands:
        pending_links += [(fact_of[p], fact_of[cand.key]) for p in cand.prerequisites]

    for prereq, fact in dict.fromkeys(pending_links):
        if prereq == fact or graph.has_edge(prereq, fact):
            continue
        if fact in graph and prereq in graph and nx.has_path(graph, fact, prereq):
            stats.cycles_skipped += 1
            continue
        graph.add_edge(prereq, fact)
        conn.execute(
            "INSERT INTO fact_edges (prereq_id, fact_id, source_id) VALUES (?, ?, ?)",
            (prereq, fact, source_id),
        )
        stats.edges += 1
    return stats


_STOPWORD_TEXT = """
the and for are but not you all any can had her was one our out has have this that with from
they will would there their what about which when make like than then them these some into more
other such only also over very just most well both each does doing done being been were where
while whose through between during before after above below under same its used using use uses
because however therefore thus
"""
STOPWORDS = frozenset(_STOPWORD_TEXT.split())
