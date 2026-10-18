import sqlite3
from pathlib import Path

import numpy as np

SCHEMA = """
CREATE TABLE IF NOT EXISTS sources (
    id INTEGER PRIMARY KEY,
    ref TEXT NOT NULL UNIQUE,
    title TEXT,
    text TEXT NOT NULL,
    added_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS facts (
    id INTEGER PRIMARY KEY,
    statement TEXT NOT NULL,
    kind TEXT NOT NULL,
    embedding BLOB NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Keyword index alongside the embeddings: catches matches on rare technical terms
-- ("EK-FAC", "PBRF") that embeddings can rank below looser paraphrases.
CREATE VIRTUAL TABLE IF NOT EXISTS facts_fts USING fts5(
    statement, content='facts', content_rowid='id'
);
CREATE TRIGGER IF NOT EXISTS facts_ai AFTER INSERT ON facts BEGIN
    INSERT INTO facts_fts(rowid, statement) VALUES (new.id, new.statement);
END;

-- A fact can matter to many sources, in a different role for each: the same fact is a
-- contribution of the paper that introduced it and a prerequisite of the papers that build on it.
CREATE TABLE IF NOT EXISTS fact_sources (
    fact_id INTEGER NOT NULL REFERENCES facts(id),
    source_id INTEGER NOT NULL REFERENCES sources(id),
    role TEXT NOT NULL CHECK (role IN ('prerequisite', 'contribution')),
    importance INTEGER NOT NULL,
    evidence TEXT NOT NULL,
    PRIMARY KEY (fact_id, source_id)
);

CREATE TABLE IF NOT EXISTS fact_edges (
    prereq_id INTEGER NOT NULL REFERENCES facts(id),
    fact_id INTEGER NOT NULL REFERENCES facts(id),
    source_id INTEGER NOT NULL REFERENCES sources(id),
    PRIMARY KEY (prereq_id, fact_id)
);

CREATE TABLE IF NOT EXISTS merge_log (
    id INTEGER PRIMARY KEY,
    source_id INTEGER NOT NULL REFERENCES sources(id),
    candidate TEXT NOT NULL,
    action TEXT NOT NULL,
    fact_id INTEGER REFERENCES facts(id),
    reason TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS clusters (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    summary TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fact_clusters (
    fact_id INTEGER PRIMARY KEY REFERENCES facts(id),
    cluster_id INTEGER NOT NULL REFERENCES clusters(id)
);

CREATE TABLE IF NOT EXISTS ingests (
    source_id INTEGER PRIMARY KEY REFERENCES sources(id),
    candidates INTEGER NOT NULL,
    new INTEGER NOT NULL,
    duplicates INTEGER NOT NULL,
    edges INTEGER NOT NULL,
    cycles_skipped INTEGER NOT NULL,
    cost REAL NOT NULL,
    seconds REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS llm_calls (
    id INTEGER PRIMARY KEY,
    at TEXT NOT NULL DEFAULT (datetime('now')),
    purpose TEXT NOT NULL,
    model TEXT NOT NULL,
    prompt_tokens INTEGER NOT NULL,
    completion_tokens INTEGER NOT NULL,
    cached_tokens INTEGER NOT NULL,
    cost REAL NOT NULL,
    seconds REAL NOT NULL
);
"""


def connect(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    conn.executescript(SCHEMA)
    return conn


def to_blob(vec: np.ndarray) -> bytes:
    return np.asarray(vec, dtype=np.float32).tobytes()


def from_blob(blob: bytes) -> np.ndarray:
    return np.frombuffer(blob, dtype=np.float32)
