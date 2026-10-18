import argparse
import re
import sys
import time
from pathlib import Path

from frontier import cluster, merge, report, review, sources
from frontier.db import connect
from frontier.extract import extract
from frontier.llm import LLM


def ingest(args: argparse.Namespace) -> None:
    conn = connect(args.db)
    llm = LLM(conn)
    profile = args.profile.read_text()
    for arg in args.sources:
        ref, pdf = sources.resolve(arg, args.db.parent / "pdfs")
        if conn.execute("SELECT 1 FROM sources WHERE ref = ?", (ref,)).fetchone():
            print(f"{ref}: already ingested, skipping")
            continue
        print(f"{ref}: extracting facts...", flush=True)
        start = time.monotonic()
        text = sources.pdf_text(pdf)
        try:
            extraction = extract(llm, profile, text)
            print(f"{ref}: reviewing {len(extraction.facts)} candidates...", flush=True)
            verdicts = review.review(
                llm, llm.models.review, extraction.title, text, extraction.facts
            )
            extracted = len(extraction.facts)
            extraction.facts = review.apply(extraction.facts, verdicts)
            print(f"{ref}: {len(extraction.facts)} facts; merging into pool...", flush=True)
            source_id = conn.execute(
                "INSERT INTO sources (ref, title, text) VALUES (?, ?, ?)",
                (ref, extraction.title, text),
            ).lastrowid
            assert source_id is not None
            stats = merge.add_candidates(conn, llm, source_id, extraction)
            stats.extracted = extracted
            print(f"{ref}: reclustering...", flush=True)
            cluster.recluster(conn, llm, args.resolution)
            conn.execute(
                "INSERT INTO ingests VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    source_id,
                    stats.extracted,
                    stats.candidates,
                    stats.new,
                    stats.duplicates,
                    stats.edges,
                    stats.cycles_skipped,
                    llm.pending_cost(),
                    time.monotonic() - start,
                ),
            )
            conn.commit()
        except BaseException:
            conn.rollback()
            raise
        finally:
            llm.flush_log()
        print(
            f"{ref}: {stats.new} new, {stats.duplicates} merged, {stats.edges} links"
            f" ({stats.cycles_skipped} skipped as cycles)"
        )
        n = conn.execute("SELECT count(*) FROM sources").fetchone()[0]
        slug = re.sub(r"[^A-Za-z0-9.]+", "-", ref)
        write_report(conn, args.report_dir / f"{n:02d}-{slug}.html", f"Fact pool after {n} sources")
    write_report(conn, args.report_dir / "index.html", "Fact pool")


def write_report(conn, path: Path, title: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report.render(conn, title))
    print(f"wrote {path}")


def recluster(args: argparse.Namespace) -> None:
    conn = connect(args.db)
    llm = LLM(conn)
    try:
        cluster.recluster(conn, llm, args.resolution)
        conn.commit()
    finally:
        llm.flush_log()
    write_report(conn, args.report_dir / "index.html", "Fact pool")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="frontier")
    parser.add_argument("--db", type=Path, default=Path("data/pool.db"))
    parser.add_argument("--report-dir", type=Path, default=Path("reports"))
    parser.add_argument(
        "--resolution",
        type=float,
        default=1.0,
        help="Louvain resolution; higher = smaller clusters",
    )
    sub = parser.add_subparsers(required=True)

    p = sub.add_parser("ingest", help="add papers to the pool, one at a time, in order")
    p.add_argument("sources", nargs="+", help="arXiv IDs or URLs, or local PDF paths")
    p.add_argument("--profile", type=Path, default=Path("profile.md"))
    p.set_defaults(func=ingest)

    p = sub.add_parser("recluster", help="recompute clusters and the report")
    p.set_defaults(func=recluster)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())
