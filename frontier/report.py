import sqlite3
from collections import defaultdict
from html import escape
from pathlib import Path

TEMPLATE = Path(__file__).with_name("report_template.html")

STYLE = """
<style>
.stats { display: flex; flex-wrap: wrap; gap: 0.6rem 1.6rem; margin: 1rem 0 1.5rem; }
.stats div { display: flex; flex-direction: column; }
.stats b { font-size: 1.4rem; }
.stats span, .muted { color: var(--ink-2); font-size: 0.85rem; }
details.cluster { border-top: 1px solid var(--grid); padding: 0.5rem 0; }
details.cluster > summary { font-weight: 600; }
ol.facts { padding-left: 0; list-style: none; }
ol.facts li { margin: 0.6rem 0; padding: 0.4rem 0.6rem; border-radius: 6px;
              background: var(--surface); }
ol.facts li:target { outline: 2px solid var(--link); }
.chip { display: inline-block; font-size: 0.72rem; padding: 0 0.45em; margin-right: 0.3em;
        border-radius: 999px; border: 1px solid var(--grid); color: var(--ink-2); }
.chip.contribution { border-color: var(--series-3); }
.chip.prerequisite { border-color: var(--series-1); }
.meta { font-size: 0.8rem; color: var(--ink-2); margin-top: 0.2rem; }
td.num { text-align: right; }
</style>
<script>
// Fact links point into collapsed clusters; open the cluster so the target is visible.
function openTarget() {
  const el = location.hash && document.querySelector(location.hash);
  if (el) { el.closest("details")?.setAttribute("open", ""); el.scrollIntoView(); }
}
addEventListener("hashchange", openTarget);
addEventListener("DOMContentLoaded", openTarget);
</script>
"""


def render(conn: sqlite3.Connection, title: str) -> str:
    facts = {r["id"]: r for r in conn.execute("SELECT id, statement, kind FROM facts")}
    sources = {r["id"]: r for r in conn.execute("SELECT id, ref, title FROM sources")}
    short = {sid: f"S{sid}" for sid in sources}
    links: dict[int, list] = defaultdict(list)
    for r in conn.execute("SELECT * FROM fact_sources ORDER BY source_id"):
        links[r["fact_id"]].append(r)
    prereqs: dict[int, list[int]] = defaultdict(list)
    dependents: dict[int, list[int]] = defaultdict(list)
    for p, f in conn.execute("SELECT prereq_id, fact_id FROM fact_edges"):
        prereqs[f].append(p)
        dependents[p].append(f)
    clusters = conn.execute(
        "SELECT c.id, c.name, c.summary, count(*) n FROM clusters c"
        " JOIN fact_clusters fc ON fc.cluster_id = c.id GROUP BY c.id ORDER BY n DESC"
    ).fetchall()
    members: dict[int, list[int]] = defaultdict(list)
    for f, c in conn.execute("SELECT fact_id, cluster_id FROM fact_clusters ORDER BY fact_id"):
        members[c].append(f)
    total_cost = conn.execute("SELECT coalesce(sum(cost), 0) FROM llm_calls").fetchone()[0]
    shared = [f for f in facts if len(links[f]) > 1]

    def ref(f: int) -> str:
        return f'<a href="#f{f}">#{f}</a>'

    def fact_item(f: int) -> str:
        chips = "".join(
            f'<span class="chip {lk["role"]}" title="{escape(lk["evidence"])}">'
            f"{short[lk['source_id']]} {lk['role'][:6]} {'★' * lk['importance']}</span>"
            for lk in links[f]
        )
        meta = []
        if prereqs[f]:
            meta.append("needs " + ", ".join(ref(p) for p in sorted(prereqs[f])))
        if dependents[f]:
            meta.append(f"needed by {len(dependents[f])}")
        return (
            f'<li id="f{f}"><span class="chip">#{f} {facts[f]["kind"]}</span>{chips}<br>'
            f'{escape(facts[f]["statement"])}<div class="meta">{" · ".join(meta)}</div></li>'
        )

    out = [STYLE]
    stats = [
        (len(facts), "facts"),
        (len(clusters), "clusters"),
        (sum(len(v) for v in prereqs.values()), "prerequisite links"),
        (len(shared), "facts shared by 2+ sources"),
        (f"${total_cost:.2f}", "spent"),
    ]
    out.append(
        '<div class="stats">'
        + "".join(f"<div><b>{v}</b><span>{k}</span></div>" for v, k in stats)
        + "</div>"
    )

    out.append(
        "<h2>Sources, in ingest order</h2><table><tr><th></th><th>Source</th>"
        "<th>Candidates</th><th>New</th><th>Merged</th><th>Links</th><th>Cost</th></tr>"
    )
    for r in conn.execute("SELECT * FROM ingests ORDER BY source_id"):
        s = sources[r["source_id"]]
        out.append(
            f"<tr><td>{short[s['id']]}</td><td>{escape(s['title'] or s['ref'])}<br>"
            f'<span class="muted">{escape(s["ref"])}</span></td>'
            f'<td class="num">{r["candidates"]}</td><td class="num">{r["new"]}</td>'
            f'<td class="num">{r["duplicates"]}</td><td class="num">{r["edges"]}</td>'
            f'<td class="num">${r["cost"]:.2f}</td></tr>'
        )
    out.append(
        '</table><p class="muted">Merged = candidates judged to be a fact already in '
        "the pool. Chips on each fact show which sources use it, in which role, and how "
        "important it is to that source (★ to ★★★); hover for the evidence.</p>"
    )

    out.append("<h2>Clusters</h2>")
    for c in clusters:
        out.append(
            f'<details class="cluster"><summary>{escape(c["name"])} '
            f'<span class="muted">({c["n"]})</span></summary>'
            f'<p class="muted">{escape(c["summary"])}</p><ol class="facts">'
            + "".join(fact_item(f) for f in members[c["id"]])
            + "</ol></details>"
        )

    out.append(f"<h2>Facts shared by several sources ({len(shared)})</h2>")
    out.append('<p class="muted">Where the pool is paying off: one fact, several papers.</p>')
    out.append(
        '<ol class="facts">'
        + "".join(fact_item(f).replace(' id="f', ' data-f="') for f in shared)
        + "</ol>"
    )

    dups = conn.execute(
        "SELECT * FROM merge_log WHERE action = 'duplicate' ORDER BY source_id, id"
    ).fetchall()
    out.append(f"<h2>Merge decisions ({len(dups)})</h2>")
    out.append(
        '<p class="muted">Each candidate the merger folded into an existing fact. '
        "A wrong merge here loses a distinct idea.</p><table><tr><th>Source</th>"
        "<th>Candidate</th><th>Merged into</th><th>Why</th></tr>"
    )
    for d in dups:
        out.append(
            f"<tr><td>{short[d['source_id']]}</td><td>{escape(d['candidate'])}</td>"
            f"<td>{ref(d['fact_id'])} {escape(facts[d['fact_id']]['statement'])}</td>"
            f'<td class="muted">{escape(d["reason"])}</td></tr>'
        )
    out.append("</table>")

    out.append(
        "<h2>Model spend</h2><table><tr><th>Step</th><th>Model</th><th>Calls</th>"
        "<th>Input tokens</th><th>Output tokens</th><th>Cost</th></tr>"
    )
    for r in conn.execute(
        "SELECT purpose, model, count(*) n, sum(prompt_tokens) i, sum(completion_tokens) o,"
        " sum(cost) c FROM llm_calls GROUP BY purpose, model ORDER BY c DESC"
    ):
        out.append(
            f'<tr><td>{r["purpose"]}</td><td>{r["model"]}</td><td class="num">{r["n"]}</td>'
            f'<td class="num">{r["i"]:,}</td><td class="num">{r["o"]:,}</td>'
            f'<td class="num">${r["c"]:.3f}</td></tr>'
        )
    out.append("</table>")

    page = TEMPLATE.read_text()
    return page.replace("{{TITLE}}", escape(title)).replace("{{BODY}}", "\n".join(out))
