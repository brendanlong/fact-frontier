"""The v2 store: sources as span-addressable revisions, model-call artifacts, and the
requirement candidates and owner labels that Phase 0 measurement runs on.

Tables only ever gain rows through explicit events: owner labels are appended, never edited.
"""

import sqlite3
from pathlib import Path

MIGRATIONS = [
    """
    CREATE TABLE sources (
        source_id TEXT PRIMARY KEY,
        kind TEXT NOT NULL,
        title TEXT
    );

    CREATE TABLE revisions (
        revision_id TEXT PRIMARY KEY,
        source_id TEXT NOT NULL REFERENCES sources(source_id),
        external_version TEXT,
        content_hash TEXT NOT NULL UNIQUE,
        raw_path TEXT NOT NULL,
        parser_version TEXT NOT NULL,
        coverage_warnings TEXT NOT NULL,
        added_at TEXT NOT NULL DEFAULT (datetime('now'))
    );

    -- Span IDs ("S12") are local to a revision; prompts and citations use them that way.
    CREATE TABLE spans (
        revision_id TEXT NOT NULL REFERENCES revisions(revision_id),
        span_id TEXT NOT NULL,
        ord INTEGER NOT NULL,
        page INTEGER NOT NULL,
        kind TEXT NOT NULL,
        text TEXT NOT NULL,
        PRIMARY KEY (revision_id, span_id)
    );

    CREATE TABLE artifacts (
        artifact_id TEXT PRIMARY KEY,
        stage TEXT NOT NULL,
        subject TEXT,
        requested_model TEXT NOT NULL,
        served_model TEXT,
        provider TEXT,
        prompt_hash TEXT NOT NULL,
        schema_name TEXT NOT NULL,
        params TEXT NOT NULL,
        path TEXT NOT NULL,
        outcome TEXT NOT NULL,
        error TEXT,
        prompt_tokens INTEGER,
        completion_tokens INTEGER,
        cost REAL,
        seconds REAL,
        created_at TEXT NOT NULL DEFAULT (datetime('now'))
    );

    -- Requirements proposed by any system (the reading-guide baseline, a model-drafted gold
    -- list, later the extractor) in one comparable shape, so all are scored the same way.
    CREATE TABLE requirement_candidates (
        candidate_id TEXT PRIMARY KEY,
        revision_id TEXT NOT NULL REFERENCES revisions(revision_id),
        system TEXT NOT NULL,
        artifact_id TEXT NOT NULL REFERENCES artifacts(artifact_id),
        label TEXT NOT NULL,
        sense TEXT NOT NULL,
        capability TEXT NOT NULL,
        depth TEXT NOT NULL,
        required_elements TEXT NOT NULL,
        served_span_ids TEXT NOT NULL,
        centrality TEXT NOT NULL,
        why_needed TEXT NOT NULL
    );

    CREATE TABLE owner_labels (
        label_id INTEGER PRIMARY KEY,
        candidate_id TEXT NOT NULL REFERENCES requirement_candidates(candidate_id),
        label TEXT NOT NULL CHECK (label IN ('know', 'partly', 'dont_know', 'not_needed', 'wrong')),
        note TEXT NOT NULL DEFAULT '',
        created_at TEXT NOT NULL DEFAULT (datetime('now'))
    );

    -- Requirements the owner says are missing from everything he was shown.
    CREATE TABLE owner_missing (
        missing_id INTEGER PRIMARY KEY,
        revision_id TEXT NOT NULL REFERENCES revisions(revision_id),
        text TEXT NOT NULL,
        created_at TEXT NOT NULL DEFAULT (datetime('now'))
    );

    CREATE TABLE exams (
        exam_id TEXT PRIMARY KEY,
        revision_id TEXT NOT NULL REFERENCES revisions(revision_id),
        artifact_id TEXT NOT NULL REFERENCES artifacts(artifact_id),
        content_hash TEXT NOT NULL,
        frozen_at TEXT NOT NULL DEFAULT (datetime('now'))
    );

    CREATE TABLE exam_reviews (
        review_id INTEGER PRIMARY KEY,
        exam_id TEXT NOT NULL REFERENCES exams(exam_id),
        question_id TEXT NOT NULL,
        verdict TEXT NOT NULL CHECK (verdict IN ('good', 'fix', 'drop')),
        note TEXT NOT NULL DEFAULT '',
        created_at TEXT NOT NULL DEFAULT (datetime('now'))
    );

    CREATE TABLE matches (
        match_id INTEGER PRIMARY KEY,
        gold_id TEXT NOT NULL REFERENCES requirement_candidates(candidate_id),
        predicted_id TEXT NOT NULL REFERENCES requirement_candidates(candidate_id),
        relation TEXT NOT NULL,
        covered_elements TEXT NOT NULL,
        artifact_id TEXT NOT NULL REFERENCES artifacts(artifact_id)
    );
    """,
    # Sealed exams are measurement instruments for a paper the owner hasn't read yet: they are
    # never shown for review, only administered.
    """
    ALTER TABLE exams ADD COLUMN sealed INTEGER NOT NULL DEFAULT 0;
    """,
    # Whether the owner had seen the requirement's details (its elements, which give away the
    # answer) when he chose the label. The first, blind label measures what he knew; a revised
    # label after seeing the details is usually more accurate, and the revision rate itself says
    # how much blind self-assessment over- or under-claims.
    """
    ALTER TABLE owner_labels ADD COLUMN revealed INTEGER NOT NULL DEFAULT 1;
    """,
    # A question that tests the requirement without stating its answer, shown to the owner
    # before he self-assesses (the capability statement often contains the claim itself).
    """
    ALTER TABLE requirement_candidates ADD COLUMN self_test TEXT;
    """,
    # Owner notes, saved as he types, independent of any label or verdict. The latest note per
    # target is current; earlier ones are kept.
    """
    CREATE TABLE owner_notes (
        note_id INTEGER PRIMARY KEY,
        target_kind TEXT NOT NULL CHECK (target_kind IN ('candidate', 'exam_question')),
        target_id TEXT NOT NULL,
        note TEXT NOT NULL,
        created_at TEXT NOT NULL DEFAULT (datetime('now'))
    );
    """,
    # Whether each self-test question passed the blind "makes sense with no other context"
    # check (`ok`), or still failed after rewrites (`flagged`, with the reader's complaint).
    """
    ALTER TABLE requirement_candidates ADD COLUMN self_test_status TEXT;
    ALTER TABLE requirement_candidates ADD COLUMN self_test_issue TEXT;
    """,
]


def connect(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")
    migrate(conn)
    return conn


def migrate(conn: sqlite3.Connection) -> None:
    version = conn.execute("PRAGMA user_version").fetchone()[0]
    for i, script in enumerate(MIGRATIONS[version:], start=version + 1):
        # executescript commits any open transaction first, so the migration and its version
        # bump go in one explicit transaction of their own.
        conn.executescript(f"BEGIN IMMEDIATE; {script}; PRAGMA user_version = {i}; COMMIT;")
