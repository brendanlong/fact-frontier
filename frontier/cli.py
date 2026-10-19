import argparse
import re
import sys
import time
from pathlib import Path

from frontier import canary, cluster, generate, merge, report, review, score, sources, store
from frontier import ingest as ingest_mod
from frontier.calls import Client
from frontier.db import connect
from frontier.extract import extract
from frontier.llm import LLM


def legacy_ingest(args: argparse.Namespace) -> None:
    conn = connect(args.legacy_db)
    llm = LLM(conn)
    profile = args.profile.read_text()
    for arg in args.sources:
        ref, pdf = sources.resolve(arg, args.legacy_db.parent / "pdfs")
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


def legacy_recluster(args: argparse.Namespace) -> None:
    conn = connect(args.legacy_db)
    llm = LLM(conn)
    try:
        cluster.recluster(conn, llm, args.resolution)
        conn.commit()
    finally:
        llm.flush_log()
    write_report(conn, args.report_dir / "index.html", "Fact pool")


def open_store(args: argparse.Namespace):
    conn = store.connect(args.db)
    return conn, Client(args.db, args.db.parent / "artifacts")


def resolve_paper(conn, ref: str) -> str:
    """A revision ID, or the latest revision of a source ID or unique substring of one."""
    rows = conn.execute(
        "SELECT revision_id FROM revisions WHERE revision_id = ? OR source_id = ?"
        " OR source_id LIKE ? ORDER BY added_at DESC",
        (ref, ref, f"%{ref}%"),
    ).fetchall()
    sources_hit = {r[0].split("@")[0] for r in rows}
    if not rows or len(sources_hit) > 1:
        raise SystemExit(f"{ref!r} matches {len(sources_hit)} sources: {sorted(sources_hit)}")
    return rows[0][0]


def cmd_ingest(args: argparse.Namespace) -> None:
    conn, _ = open_store(args)
    for path in args.pdfs:
        revision_id = ingest_mod.ingest_pdf(conn, path, args.db.parent / "raw", args.title)
        print(revision_id)


def cmd_generate(args: argparse.Namespace) -> None:
    conn, client = open_store(args)
    for ref in args.papers:
        revision_id = resolve_paper(conn, ref)
        if args.kind == "guide":
            artifact = generate.guide(client, conn, revision_id, args.profile.read_text())
        elif args.kind == "draft":
            artifact = generate.gold_draft(client, conn, revision_id)
        else:
            artifact = generate.exam(client, conn, revision_id, sealed=args.sealed)
        print(f"{revision_id}: {args.kind} -> {artifact}")


def cmd_matcher_check(args: argparse.Namespace) -> None:
    _, client = open_store(args)
    results = score.check_matcher(client, args.cases)
    for name, expected, got in results:
        print(f"{'ok ' if expected == got else 'BAD'} {name}: expected {expected}, got {got}")
    print(f"{sum(e == g for _, e, g in results)}/{len(results)} correct")


def cmd_score(args: argparse.Namespace) -> None:
    conn, client = open_store(args)
    revision_id = resolve_paper(conn, args.paper)
    result = score.score_paper(conn, client, revision_id, args.predicted, args.gold)
    slug = revision_id.replace(":", "-").replace("@", "-")
    path = args.report_dir / f"score-{slug}-{args.predicted}.html"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(score.render_report(result))
    gap = result["gap_recall"]
    print(
        f"recall {result['recall']:.0%}, element recall {result['partial_recall']:.0%}, "
        f"gap recall {'n/a' if gap is None else f'{gap:.0%}'}, "
        f"matched precision {result['matched_precision']:.0%} -> {path}"
    )


def cmd_serve(args: argparse.Namespace) -> None:
    import uvicorn

    from frontier.web import create_app

    store.connect(args.db)
    uvicorn.run(create_app(args.db), host=args.host, port=args.port)


def cmd_canary(args: argparse.Namespace) -> None:
    conn, client = open_store(args)
    for topic in args.topics:
        paper, artifact_id = canary.generate(client, topic)
        revision_id = canary.ingest_text(conn, paper, artifact_id, args.db.parent / "raw")
        print(f"{revision_id}: {paper.title} ({len(paper.traps)} traps)")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="frontier")
    parser.add_argument("--db", type=Path, default=Path("data/frontier.db"))
    parser.add_argument("--legacy-db", type=Path, default=Path("data/pool.db"))
    parser.add_argument("--report-dir", type=Path, default=Path("reports"))
    parser.add_argument(
        "--resolution",
        type=float,
        default=1.0,
        help="Louvain resolution; higher = smaller clusters",
    )
    sub = parser.add_subparsers(required=True)

    p = sub.add_parser("ingest", help="store PDFs as span-addressable revisions")
    p.add_argument("pdfs", nargs="+", type=Path)
    p.add_argument("--title")
    p.set_defaults(func=cmd_ingest)

    for kind, help_text in [
        ("guide", "one-shot reading guide baseline (learner-specific)"),
        ("draft", "recall-oriented requirement draft for owner labelling"),
        ("exam", "sealed exam, written from the paper alone"),
    ]:
        p = sub.add_parser(kind, help=help_text)
        p.add_argument("papers", nargs="+", help="revision ID, source ID, or part of one")
        p.add_argument("--profile", type=Path, default=Path("profile.md"))
        p.add_argument("--sealed", action="store_true", help="exam: never show for review")
        p.set_defaults(func=cmd_generate, kind=kind)

    p = sub.add_parser("matcher-check", help="run the matcher on its challenge set")
    p.add_argument("--cases", type=Path, default=Path("tests/data/matcher_challenge.json"))
    p.set_defaults(func=cmd_matcher_check)

    p = sub.add_parser("score", help="score one system's requirements against the gold draft")
    p.add_argument("paper")
    p.add_argument("--predicted", default="guide")
    p.add_argument("--gold", default="gold_draft")
    p.set_defaults(func=cmd_score)

    p = sub.add_parser("canary", help="generate canary papers with planted traps")
    p.add_argument(
        "topics",
        nargs="*",
        default=[
            "training data attribution for fine-tuned language models",
            "probing and steering internal representations for model safety",
        ],
    )
    p.set_defaults(func=cmd_canary)

    p = sub.add_parser("serve", help="owner labelling pages")
    p.add_argument("--host", default="0.0.0.0")
    p.add_argument("--port", type=int, default=8787)
    p.set_defaults(func=cmd_serve)

    p = sub.add_parser("legacy-ingest", help="v1 fact-pool pipeline")
    p.add_argument("sources", nargs="+", help="arXiv IDs or URLs, or local PDF paths")
    p.add_argument("--profile", type=Path, default=Path("profile.md"))
    p.set_defaults(func=legacy_ingest)

    p = sub.add_parser("legacy-recluster", help="v1: recompute clusters and the report")
    p.set_defaults(func=legacy_recluster)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())
