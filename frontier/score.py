import json
import sqlite3
from html import escape
from pathlib import Path

from frontier import matcher
from frontier.calls import Client
from frontier.matcher import Req

TEMPLATE = Path(__file__).with_name("report_template.html")
EXCLUDED = ("not_needed", "wrong")
GAPS = ("dont_know", "partly")


def bucket(fraction: float) -> str:
    return "full" if fraction >= 1 else "partial" if fraction > 0 else "none"


def check_matcher(client: Client, path: Path) -> list[tuple[str, str, str]]:
    """(case, expected, got) for every challenge case."""
    out = []
    for case in json.loads(path.read_text()):
        gold = Req(
            "G1",
            **{k: case["gold"][k] for k in ("label", "sense", "capability", "depth")},
            elements=case["gold"]["elements"],
        )
        preds = [
            Req(f"X{i}", p["label"], p["sense"], p["capability"], p["depth"], p["elements"])
            for i, p in enumerate(case["predicted"])
        ]
        links, _ = matcher.judge(client, [gold], preds, subject=f"challenge:{case['name']}")
        out.append((case["name"], case["expect"], bucket(matcher.coverage(gold, links["G1"]))))
    return out


def latest_labels(conn: sqlite3.Connection, revision_id: str) -> dict[str, str]:
    rows = conn.execute(
        "SELECT l.candidate_id, l.label FROM owner_labels l"
        " JOIN requirement_candidates c ON c.candidate_id = l.candidate_id"
        " WHERE c.revision_id = ? AND l.label != 'unclear' ORDER BY l.label_id",
        (revision_id,),
    )
    return dict(rows.fetchall())


def score_paper(
    conn: sqlite3.Connection,
    client: Client,
    revision_id: str,
    predicted: str,
    gold_system: str,
    include_unlabelled: bool = False,
) -> dict:
    """Gold is the owner-labelled draft minus what he marked not needed or wrong. Unlabelled
    draft items are model output nobody has vetted, so they're left out unless asked for."""
    labels = latest_labels(conn, revision_id)
    gold = [
        g
        for g in matcher.load(conn, revision_id, gold_system)
        if labels.get(g.rid) not in EXCLUDED and (include_unlabelled or g.rid in labels)
    ]
    preds = matcher.load(conn, revision_id, predicted)
    if not gold or not preds:
        raise SystemExit(
            f"need labelled {gold_system} and {predicted} candidates for {revision_id}"
            " (or --include-unlabelled)"
        )
    links, judged_by = matcher.judge(
        client, gold, preds, subject=f"score:{revision_id}:{predicted}"
    )
    with conn:
        conn.executemany(
            "INSERT INTO matches (gold_id, predicted_id, relation, covered_elements, artifact_id)"
            " VALUES (?, ?, ?, ?, ?)",
            [
                (g, link.predicted, link.relation, json.dumps(link.covered_elements), judged_by[g])
                for g, ls in links.items()
                for link in ls
            ],
        )
    cov = {g.rid: matcher.coverage(g, links.get(g.rid, [])) for g in gold}
    used = {
        link.predicted
        for ls in links.values()
        for link in ls
        if link.relation == "equivalent"
        or (link.relation == "covers_part" and link.covered_elements)
    }
    missing = [
        r[0]
        for r in conn.execute(
            "SELECT text FROM owner_missing WHERE revision_id = ? ORDER BY missing_id",
            (revision_id,),
        )
    ]
    gaps = [g for g in gold if labels.get(g.rid) in GAPS]
    return {
        "revision_id": revision_id,
        "predicted": predicted,
        "gold_system": gold_system,
        "labelled": sum(1 for g in gold if g.rid in labels),
        "gold": gold,
        "preds": preds,
        "links": links,
        "coverage": cov,
        "labels": labels,
        "recall": sum(1 for v in cov.values() if v >= 1) / len(gold),
        "partial_recall": sum(cov.values()) / len(gold),
        "gap_recall": (sum(1 for g in gaps if cov[g.rid] >= 1) / len(gaps)) if gaps else None,
        "n_gaps": len(gaps),
        "matched_precision": len(used) / len(preds),
        "unmatched": [p for p in preds if p.rid not in used],
        "owner_missing": missing,
        "judge_artifacts": sorted(set(judged_by.values())),
    }


def render_report(result: dict) -> str:
    pct = lambda x: "—" if x is None else f"{x:.0%}"  # noqa: E731
    pred_by_id = {p.rid: p for p in result["preds"]}
    out = [
        "<style>td{vertical-align:top;font-size:.85rem} .full{color:var(--series-3)}"
        " .none{color:var(--series-2)}</style>",
        f"<p>Predicted: <code>{escape(result['predicted'])}</code> ({len(result['preds'])}). "
        f"Gold: <code>{escape(result['gold_system'])}</code> ({len(result['gold'])} after removing "
        f"owner-labelled not-needed/wrong; {result['labelled']} labelled).</p>",
        "<table><tr><th>Full recall</th><th>Element recall</th><th>Gap recall</th>"
        "<th>Predictions matching a gold entry</th></tr>"
        f"<tr><td>{pct(result['recall'])}</td><td>{pct(result['partial_recall'])}</td>"
        f"<td>{pct(result['gap_recall'])} (of {result['n_gaps']})</td>"
        f"<td>{pct(result['matched_precision'])}</td></tr></table>",
        "<p class='muted'>Gap recall counts only gold entries the owner labelled don't know or "
        "partly. Unmatched predictions are not necessarily wrong; they are listed for review.</p>",
        "<h2>Gold entries</h2><table><tr><th>Gold</th><th>Owner</th><th>Coverage</th>"
        "<th>By</th></tr>",
    ]
    for g in sorted(result["gold"], key=lambda g: result["coverage"][g.rid]):
        c = result["coverage"][g.rid]
        by = "<br>".join(
            f"{escape(pred_by_id[link.predicted].label)} <i>({link.relation}, "
            f"{link.covered_elements})</i>"
            for link in result["links"].get(g.rid, [])
            if link.predicted in pred_by_id
        )
        out.append(
            f"<tr><td><b>{escape(g.label)}</b> ({g.depth})<br>{escape(g.capability)}</td>"
            f"<td>{escape(result['labels'].get(g.rid, ''))}</td>"
            f"<td class='{bucket(c)}'>{c:.0%}</td><td>{by}</td></tr>"
        )
    out.append(
        f"</table><h2>Missing from the draft ({len(result['owner_missing'])})</h2>"
        "<p class='muted'>Requirements the owner said were missing. They aren't in the recall "
        "denominator yet, so recall overstates coverage by up to this many entries.</p><ul>"
        + "".join(f"<li>{escape(m)}</li>" for m in result["owner_missing"])
        + "</ul>"
    )
    out.append("<h2>Unmatched predictions</h2><ul>")
    out += [
        f"<li><b>{escape(p.label)}</b>: {escape(p.capability)}</li>" for p in result["unmatched"]
    ]
    out.append("</ul>")
    out.append(
        "<p class='muted'>Judge calls: "
        + ", ".join(f"<code>{escape(a)}</code>" for a in result["judge_artifacts"])
        + "</p>"
    )
    title = (
        f"Requirement coverage: {result['predicted']} vs {result['gold_system']}, "
        f"{result['revision_id']}"
    )
    return (
        TEMPLATE.read_text().replace("{{TITLE}}", escape(title)).replace("{{BODY}}", "\n".join(out))
    )
