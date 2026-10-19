"""Turn a source document into an immutable revision of addressable spans.

Models cite spans by ID, and code checks every cited ID exists, so nothing downstream can
invent a source location. PDF text extraction loses equations and figure contents; those losses
are recorded as coverage warnings on the revision rather than silently dropped.
"""

import hashlib
import json
import re
import shutil
import sqlite3
import subprocess
from dataclasses import dataclass
from pathlib import Path

from frontier.sources import ARXIV_ID

PARSER_VERSION = "pdftotext-paragraphs-2"

# Lines a browser adds when printing a web page to PDF ("3 of 86", the URL, a timestamp).
PRINT_NOISE = [
    re.compile(r"^\d+ of \d+$"),
    re.compile(r"^https?://\S+$"),
    re.compile(r"^\d{1,2}/\d{1,2}/\d{2,4},? \d{1,2}:\d{2}\s*(AM|PM)?$"),
]
CAPTION = re.compile(r"^(Figure|Fig\.|Table|Algorithm)\s+\d+[.:]")
MATH_CHARS = set("∑∫∂∇θλεαβγδσμπ≈≤≥∈⊆⊂→←↦·∥⟨⟩\u00d7")


@dataclass
class Span:
    page: int
    kind: str
    text: str


def identify(pdf: Path) -> tuple[str, str, str | None]:
    """(source_id, kind, external_version) from a filename, preferring arXiv identity."""
    m = ARXIV_ID.search(pdf.name)
    if m:
        return f"arxiv:{m.group(1)}", "arxiv", m.group(2)
    stem = re.sub(r"^[0-9a-f]{8}-", "", pdf.stem)
    return f"doc:{re.sub(r'[^a-z0-9]+', '-', stem.lower()).strip('-')}", "document", None


def pdf_pages(pdf: Path) -> list[str]:
    out = subprocess.run(["pdftotext", str(pdf), "-"], check=True, capture_output=True, text=True)
    return out.stdout.split("\f")


def is_mathy(text: str) -> bool:
    if not text:
        return False
    symbols = sum(1 for ch in text if ch in MATH_CHARS)
    return symbols / len(text) > 0.04


def split_spans(pages: list[str]) -> tuple[list[Span], list[str]]:
    spans: list[Span] = []
    warnings: list[str] = []
    for page_no, page in enumerate(pages, start=1):
        lines = [
            ln for ln in page.splitlines() if not any(p.match(ln.strip()) for p in PRINT_NOISE)
        ]
        paragraphs = re.split(r"\n\s*\n", "\n".join(lines))
        page_chars = 0
        for para in paragraphs:
            text = re.sub(r"\s*\n\s*", " ", para).strip()
            text = re.sub(r"(\w)- (\w)", r"\1\2", text)
            if len(text) < 3:
                continue
            page_chars += len(text)
            if CAPTION.match(text):
                kind = "caption"
            elif is_mathy(text):
                kind = "math"
            elif len(text) < 80 and not text.endswith("."):
                kind = "heading"
            else:
                kind = "paragraph"
            spans.append(Span(page_no, kind, text))
        if page.strip() and page_chars < 300:
            warnings.append(f"page {page_no}: little extractable text (figure or scanned content?)")
    spans = merge_fragments(spans)
    math = sum(1 for s in spans if s.kind == "math")
    if math:
        warnings.append(
            f"{math} spans look like equations; PDF extraction garbles maths, so check the PDF "
            "for exact notation"
        )
    warnings.append("figure and table contents are not extracted; only their captions")
    return spans, warnings


def merge_fragments(spans: list[Span]) -> list[Span]:
    """Collapse runs of three or more short lines on one page (figure axis labels, table cells,
    chat transcripts) into one `fragments` span, so they don't drown out the prose."""
    out: list[Span] = []
    run: list[Span] = []

    def flush():
        if len(run) >= 3:
            out.append(Span(run[0].page, "fragments", " | ".join(s.text for s in run)))
        else:
            out.extend(run)
        run.clear()

    for s in spans:
        if s.kind == "heading" and (not run or run[-1].page == s.page):
            run.append(s)
            continue
        flush()
        if s.kind == "heading":
            run.append(s)
        else:
            out.append(s)
    flush()
    return out


def ingest_pdf(conn: sqlite3.Connection, pdf: Path, raw_dir: Path, title: str | None = None) -> str:
    """Store `pdf` as a revision (idempotent on content) and return its revision ID."""
    content = pdf.read_bytes()
    digest = hashlib.sha256(content).hexdigest()
    existing = conn.execute(
        "SELECT revision_id FROM revisions WHERE content_hash = ?", (digest,)
    ).fetchone()
    if existing:
        return existing[0]
    source_id, kind, version = identify(pdf)
    revision_id = f"{source_id}{version or ''}@{digest[:8]}"
    raw_path = raw_dir / f"{digest[:16]}.pdf"
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(pdf, raw_path)
    spans, warnings = split_spans(pdf_pages(pdf))
    with conn:
        conn.execute(
            "INSERT INTO sources (source_id, kind, title) VALUES (?, ?, ?)"
            " ON CONFLICT DO UPDATE SET title = coalesce(excluded.title, title)",
            (source_id, kind, title),
        )
        conn.execute(
            "INSERT INTO revisions (revision_id, source_id, external_version, content_hash,"
            " raw_path, parser_version, coverage_warnings) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                revision_id,
                source_id,
                version,
                digest,
                str(raw_path),
                PARSER_VERSION,
                json.dumps(warnings),
            ),
        )
        conn.executemany(
            "INSERT INTO spans (span_id, revision_id, ord, page, kind, text) VALUES (?,?,?,?,?,?)",
            [(f"S{i}", revision_id, i, s.page, s.kind, s.text) for i, s in enumerate(spans)],
        )
    return revision_id


def render(conn: sqlite3.Connection, revision_id: str) -> str:
    """The revision as text with a span marker before each span, for prompts."""
    rows = conn.execute(
        "SELECT span_id, page, kind, text FROM spans WHERE revision_id = ? ORDER BY ord",
        (revision_id,),
    )
    return "\n\n".join(f"[{r['span_id']}|p{r['page']}|{r['kind']}] {r['text']}" for r in rows)


def span_ids(conn: sqlite3.Connection, revision_id: str) -> set[str]:
    return {
        r[0]
        for r in conn.execute("SELECT span_id FROM spans WHERE revision_id = ?", (revision_id,))
    }
