"""Canary papers: short, plausible, invented papers with planted traps and an answer key.

They test whether the pipeline explains things from the text in front of it, or from what a
familiar-sounding name suggests. The owner checks each one before it's used.
"""

import hashlib
import json
import re
import sqlite3
from pathlib import Path

from pydantic import BaseModel, Field

from frontier.calls import Client


class Trap(BaseModel):
    kind: str = Field(
        description="invented_method | name_collision | altered_standard_result | "
        "undefined_term | unresolvable_citation | standard_control"
    )
    term: str
    truth: str = Field(description="What the paper actually says, or what is wrong, for the key.")
    expected_behaviour: str = Field(
        description="What a correct pipeline should do with it (e.g. 'explain from the text, not "
        "from the name', 'flag as unknown', 'flag the sign error')."
    )


class CanaryPaper(BaseModel):
    title: str
    text: str = Field(description="The full paper as plain text with section headings.")
    traps: list[Trap]


SYSTEM = """\
You write test fixtures for a system that reads research papers and teaches their
prerequisites. Write a short, realistic ML research paper (about 2,500 words: abstract,
introduction, background, method, experiments, discussion, references) that a careful reader
could not tell apart from a real workshop paper. Plant these traps, and list each one in
`traps` with the truth and the behaviour a correct system should show:

1. Three invented methods with familiar-sounding names whose definitions differ from what the
   name suggests (e.g. a "gradient echo" that has nothing to do with echoes of gradients). Define
   each clearly in the text.
2. One name collision: an existing well-known term redefined to mean something different in
   this paper, defined explicitly.
3. One standard result restated with a subtle error (a dropped minus sign or a missing
   condition) in the background section. The key gives the correct version.
4. One term used repeatedly but never defined anywhere in the paper or its references.
5. One method attributed to a citation that does not exist (an invented author and year).
6. Two standard concepts used correctly, as controls that a correct system should treat
   normally.

Don't mark the traps in the text itself."""


def generate(client: Client, topic: str) -> tuple[CanaryPaper, str]:
    return client.structured(
        "canary",
        client.roles.canary,
        CanaryPaper,
        SYSTEM,
        f"Topic area for this paper: {topic}",
        subject=topic,
        effort="high",
    )


def ingest_text(
    conn: sqlite3.Connection, paper: CanaryPaper, artifact_id: str, raw_dir: Path
) -> str:
    """Store a canary as a revision with one span per paragraph, plus its answer key."""
    digest = hashlib.sha256(paper.text.encode()).hexdigest()
    slug = re.sub(r"[^a-z0-9]+", "-", paper.title.lower()).strip("-")[:50]
    source_id = f"canary:{slug}"
    revision_id = f"{source_id}@{digest[:8]}"
    raw_dir.mkdir(parents=True, exist_ok=True)
    raw_path = raw_dir / f"{digest[:16]}.json"
    raw_path.write_text(json.dumps({"artifact_id": artifact_id, **paper.model_dump()}, indent=1))
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", paper.text) if p.strip()]
    with conn:
        conn.execute(
            "INSERT INTO sources (source_id, kind, title) VALUES (?, 'canary', ?)",
            (source_id, paper.title),
        )
        conn.execute(
            "INSERT INTO revisions (revision_id, source_id, external_version, content_hash,"
            " raw_path, parser_version, coverage_warnings) VALUES (?, ?, NULL, ?, ?, ?, '[]')",
            (revision_id, source_id, digest, str(raw_path), "canary-text-1"),
        )
        conn.executemany(
            "INSERT INTO spans (span_id, revision_id, ord, page, kind, text) VALUES (?,?,?,1,?,?)",
            [
                (f"S{i}", revision_id, i, "heading" if len(p) < 80 else "paragraph", p)
                for i, p in enumerate(paragraphs)
            ],
        )
    return revision_id
