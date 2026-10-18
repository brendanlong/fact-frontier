"""Run the fact reviewer over an existing pool with several models and write a side-by-side
HTML comparison. Read-only on the pool; spend is recorded in its llm_calls table."""

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor
from html import escape
from pathlib import Path

from frontier.db import connect
from frontier.extract import Candidate
from frontier.llm import LLM
from frontier.review import Verdict, review

TEMPLATE = Path(__file__).parent.parent / "frontier" / "report_template.html"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", type=Path, default=Path("data/pool.db"))
    parser.add_argument("--out", type=Path, default=Path("reports/review-comparison.html"))
    parser.add_argument(
        "--models",
        nargs="+",
        default=["anthropic/claude-haiku-5.5", "anthropic/claude-sonnet-5.5"],
    )
    args = parser.parse_args()
    conn = connect(args.db)
    llm = LLM(conn)

    jobs = []
    for s in conn.execute("SELECT id, title, text FROM sources ORDER BY id").fetchall():
        cands = [
            Candidate(
                key=f"f{r['id']}",
                statement=r["statement"],
                kind=r["kind"],
                role=r["role"],
                importance=r["importance"],
                prerequisites=[],
                evidence=r["evidence"],
            )
            for r in conn.execute(
                "SELECT f.id, f.statement, f.kind, fs.role, fs.importance, fs.evidence"
                " FROM facts f JOIN fact_sources fs ON fs.fact_id = f.id"
                " WHERE fs.source_id = ? AND fs.source_id = (SELECT min(source_id)"
                " FROM fact_sources WHERE fact_id = f.id) ORDER BY f.id",
                (s["id"],),
            )
        ]
        for model in args.models:
            jobs.append((model, s["title"], s["text"], cands))

    with ThreadPoolExecutor(8) as pool:
        results = list(pool.map(lambda j: (j[0], j[3], review(llm, *j)), jobs))
    llm.flush_log()

    verdicts: dict[str, dict[str, Verdict]] = {m: {} for m in args.models}
    order: list[Candidate] = []
    for model, cands, vs in results:
        verdicts[model] |= vs
        if model == args.models[0]:
            order += cands

    out = [
        "<style>td{vertical-align:top;font-size:0.85rem} td ul{padding-left:1rem;margin:0}"
        ".v{font-weight:600}</style>"
    ]
    out.append("<h2>Verdict counts</h2><table><tr><th>Model</th>")
    kinds = ["keep", "rewrite", "split", "drop"]
    out += [f"<th>{k}</th>" for k in kinds] + ["<th>pieces out</th><th>cost</th></tr>"]
    for m in args.models:
        vs = verdicts[m].values()
        cost = conn.execute(
            "SELECT sum(cost) FROM llm_calls WHERE purpose='review' AND model=?", (m,)
        ).fetchone()[0]
        pieces = sum(1 if v.verdict == "keep" else len(v.replacements) for v in vs)
        out.append(
            f"<tr><td>{m}</td>"
            + "".join(f"<td>{sum(v.verdict == k for v in vs)}</td>" for k in kinds)
            + f"<td>{pieces}</td><td>${cost:.3f}</td></tr>"
        )
    out.append(
        "</table><h2>Per fact</h2><table><tr><th>Fact</th>"
        + "".join(f"<th>{m.split('/')[-1]}</th>" for m in args.models)
        + "</tr>"
    )
    for c in order:
        cells = []
        for m in args.models:
            v = verdicts[m].get(c.key)
            if v is None:
                cells.append("<td>—</td>")
                continue
            reps = "".join(f"<li>{escape(r.statement)}</li>" for r in v.replacements)
            cells.append(
                f'<td><span class="v">{v.verdict}</span> {", ".join(v.problems)}'
                f"<ul>{reps}</ul><i>{escape(v.reason)}</i></td>"
            )
        out.append(f"<tr><td>#{c.key[1:]} {escape(c.statement)}</td>{''.join(cells)}</tr>")
    out.append("</table>")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        TEMPLATE.read_text()
        .replace("{{TITLE}}", "Fact review: model comparison")
        .replace("{{BODY}}", "\n".join(out))
    )
    print(f"wrote {args.out}")


if __name__ == "__main__":
    sys.exit(main())
