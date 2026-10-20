"""Owner labelling pages: requirement triage per paper and exam validation.

Labels are appended, never edited; the latest label per candidate wins when scoring.
"""

import json
import random
import sqlite3
from html import escape
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from frontier import generate, store

TEMPLATE = Path(__file__).with_name("report_template.html")
VERDICTS = [("good", "Good"), ("fix", "Fix"), ("drop", "Drop")]
LABELS = [
    ("know", "Know it"),
    ("partly", "Partly"),
    ("dont_know", "Don't know"),
    ("not_needed", "Not needed"),
    ("wrong", "Wrong"),
]

STYLE = """
<style>
.req { border-top: 1px solid var(--grid); padding: .6rem 0; }
.req .meta { color: var(--ink-2); font-size: .85rem; }
.req ul { margin: .3rem 0; font-size: .9rem; }
.btns { display: flex; flex-wrap: wrap; gap: .3rem; margin-top: .3rem; }
.btns button, .vbtn { font: inherit; font-size: .85rem; padding: .25rem .6rem; border-radius: 6px;
  border: 1px solid var(--grid); background: var(--surface); color: var(--ink); cursor: pointer; }
.btns button.on, .vbtn.on { background: var(--link); color: var(--page);
  border-color: var(--link); }
input.note, textarea { font: inherit; width: 100%; box-sizing: border-box; margin-top: .3rem;
  background: var(--surface); color: var(--ink); border: 1px solid var(--grid); border-radius: 6px;
  padding: .3rem; }
details.spans { font-size: .8rem; color: var(--ink-2); }
.progress { position: sticky; top: 0; background: var(--page); padding: .4rem 0; z-index: 5; }
</style>
<script>
async function post(url, body) {
  const r = await fetch(url, {method: "POST", headers: {"Content-Type": "application/json"},
    body: JSON.stringify(body)});
  if (!r.ok) { alert("Save failed: " + await r.text()); throw new Error(); }
}
async function label(btn) {
  const box = btn.closest(".req");
  await post("/api/label", {candidate_id: box.dataset.cid, label: btn.dataset.value,
    note: box.querySelector("input.note").value});
  box.querySelectorAll(".btns button").forEach(b => b.classList.toggle("on", b === btn));
  box.dataset.done = "1";
  const done = document.querySelectorAll(".req[data-done='1']").length;
  const p = document.getElementById("done"); if (p) p.textContent = done;
}
async function review(btn) {
  const box = btn.closest(".req");
  await post("/api/exam_review", {exam_id: box.dataset.exam, question_id: box.dataset.qid,
    verdict: btn.dataset.value,
    note: box.querySelector("input.note").value});
  box.querySelectorAll(".vbtn").forEach(b => b.classList.toggle("on", b === btn));
}
async function missing(btn) {
  const t = document.getElementById("missing-text");
  if (!t.value.trim()) return;
  await post("/api/missing", {revision_id: btn.dataset.rev, text: t.value});
  t.value = ""; document.getElementById("missing-saved").textContent = "Saved.";
}
</script>
"""


def page(title: str, body: str) -> HTMLResponse:
    html = TEMPLATE.read_text().replace("{{TITLE}}", escape(title))
    return HTMLResponse(html.replace("{{BODY}}", STYLE + body))


class LabelIn(BaseModel):
    candidate_id: str
    label: str
    note: str = ""


class MissingIn(BaseModel):
    revision_id: str
    text: str


class ExamReviewIn(BaseModel):
    exam_id: str
    question_id: str
    verdict: str
    note: str = ""


def create_app(db_path: Path) -> FastAPI:
    app = FastAPI()

    def db() -> sqlite3.Connection:
        return store.connect(db_path)

    @app.get("/", response_class=HTMLResponse)
    def index():
        conn = db()
        rows = conn.execute(
            "SELECT r.revision_id, s.title,"
            " (SELECT count(*) FROM requirement_candidates c WHERE c.revision_id = r.revision_id"
            "   AND c.system = 'gold_draft') AS n,"
            " (SELECT count(DISTINCT l.candidate_id) FROM owner_labels l"
            "   JOIN requirement_candidates c ON c.candidate_id = l.candidate_id"
            "   WHERE c.revision_id = r.revision_id AND c.system = 'gold_draft') AS done,"
            " (SELECT exam_id FROM exams e WHERE e.revision_id = r.revision_id AND NOT e.sealed"
            "   ORDER BY frozen_at DESC LIMIT 1) AS exam"
            " FROM revisions r JOIN sources s ON s.source_id = r.source_id ORDER BY r.added_at"
        ).fetchall()
        items = []
        for r in rows:
            links = []
            if r["n"]:
                links.append(
                    f'<a href="/label/{r["revision_id"]}">label requirements</a> '
                    f"({r['done']}/{r['n']})"
                )
            if r["exam"]:
                links.append(f'<a href="/exam/{r["exam"]}">review exam</a>')
            title = escape(r["title"] or r["revision_id"])
            items.append(
                f"<li><b>{title}</b> <code>{escape(r['revision_id'])}</code><br>"
                f"{' · '.join(links) or '<i>nothing to label yet</i>'}</li>"
            )
        return page("fact-frontier labelling", f"<ul>{''.join(items)}</ul>")

    @app.get("/label/{revision_id:path}", response_class=HTMLResponse)
    def label_page(revision_id: str):
        conn = db()
        cands = conn.execute(
            "SELECT * FROM requirement_candidates WHERE revision_id = ? AND system = 'gold_draft'",
            (revision_id,),
        ).fetchall()
        if not cands:
            raise HTTPException(404, "no drafted requirements for this paper")
        cands = list(cands)
        random.Random(revision_id).shuffle(cands)
        latest = dict(
            conn.execute(
                "SELECT candidate_id, label FROM owner_labels ORDER BY label_id"
            ).fetchall()
        )
        spans = dict(
            conn.execute(
                "SELECT span_id, 'p' || page || ': ' || text FROM spans WHERE revision_id = ?",
                (revision_id,),
            ).fetchall()
        )
        out = [
            f"<p class='progress'><span id='done'>{sum(c['candidate_id'] in latest for c in cands)}"
            f"</span>/{len(cands)} labelled. Label each by whether <b>you</b> already understand "
            "it at the depth shown. <i>Not needed</i>: the paper doesn't really require it. "
            "<i>Wrong</i>: incorrect or misleading.</p>"
        ]
        for c in cands:
            cur = latest.get(c["candidate_id"])
            elements = "".join(f"<li>{escape(e)}</li>" for e in json.loads(c["required_elements"]))
            span_text = "".join(
                f"<p>{escape(spans.get(s, s)[:400])}</p>"
                for s in json.loads(c["served_span_ids"])[:3]
            )
            buttons = "".join(
                f"<button class='{'on' if cur == v else ''}' data-value='{v}' "
                f"onclick='label(this)'>{t}</button>"
                for v, t in LABELS
            )
            out.append(
                f"<div class='req' data-done='{1 if cur else 0}' "
                f"data-cid='{escape(c['candidate_id'], quote=True)}'><b>{escape(c['label'])}</b> "
                f"<span class='meta'>· {c['depth']} · {c['centrality'].replace('_', ' ')}</span>"
                f"<div>{escape(c['capability'])}</div><ul>{elements}</ul>"
                f"<div class='meta'>Why needed: {escape(c['why_needed'])}</div>"
                f"<details class='spans'><summary>Where the paper uses it</summary>{span_text}"
                f"</details><div class='btns'>{buttons}</div>"
                "<input class='note' placeholder='Optional note (saved with the next click)'></div>"
            )
        out.append(
            "<h2>Missing</h2><p>Anything you'd need for this paper that isn't listed above?</p>"
            "<textarea id='missing-text' rows='4'></textarea>"
            f"<button class='vbtn' data-rev='{escape(revision_id, quote=True)}' "
            "onclick='missing(this)'>Save</button> "
            "<span id='missing-saved'></span>"
        )
        title = conn.execute(
            "SELECT s.title FROM revisions r JOIN sources s USING (source_id)"
            " WHERE revision_id = ?",
            (revision_id,),
        ).fetchone()[0]
        return page(f"Requirements: {title or revision_id}", "".join(out))

    @app.get("/exam/{exam_id}", response_class=HTMLResponse)
    def exam_page(exam_id: str):
        conn = db()
        sealed = conn.execute("SELECT sealed FROM exams WHERE exam_id = ?", (exam_id,)).fetchone()
        if sealed is None or sealed[0]:
            raise HTTPException(404, "no such reviewable exam")
        exam = generate.load_exam(conn, exam_id)
        latest = dict(
            conn.execute(
                "SELECT question_id, verdict FROM exam_reviews WHERE exam_id = ?"
                " ORDER BY review_id",
                (exam_id,),
            ).fetchall()
        )
        out = [
            "<p>Is each question one an expert colleague would ask, with a correct and "
            "complete key? <i>Fix</i>: right idea, wrong key or wording (say what).</p>"
        ]
        for q in exam.questions:
            cur = latest.get(q.question_id)
            keys = "".join(f"<li>{escape(k)}</li>" for k in q.key_points)
            buttons = "".join(
                f"<button class='vbtn {'on' if cur == v else ''}' data-value='{v}' "
                f"onclick='review(this)'>{t}</button> "
                for v, t in VERDICTS
            )
            out.append(
                f"<div class='req' data-exam='{escape(exam_id, quote=True)}' "
                f"data-qid='{escape(q.question_id, quote=True)}'><b>{escape(q.question_id)}</b> "
                f"<span class='meta'>· {q.kind} · {q.use}"
                f"</span><div>{escape(q.question)}</div><ul>{keys}</ul>"
                f"<div class='meta'>Also acceptable: {escape(q.acceptable_variants)}</div>"
                f"<div class='btns'>{buttons}</div>"
                "<input class='note' placeholder='What to fix (saved with the next click)'></div>"
            )
        return page(f"Exam review: {exam_id}", "".join(out))

    @app.post("/api/label")
    def post_label(body: LabelIn):
        if body.label not in dict(LABELS):
            raise HTTPException(400, "bad label")
        conn = db()
        if not conn.execute(
            "SELECT 1 FROM requirement_candidates WHERE candidate_id = ? AND system = 'gold_draft'",
            (body.candidate_id,),
        ).fetchone():
            raise HTTPException(404, "no such draft requirement")
        with conn:
            conn.execute(
                "INSERT INTO owner_labels (candidate_id, label, note) VALUES (?, ?, ?)",
                (body.candidate_id, body.label, body.note),
            )
        return {"ok": True}

    @app.post("/api/missing")
    def post_missing(body: MissingIn):
        conn = db()
        if not conn.execute(
            "SELECT 1 FROM revisions WHERE revision_id = ?", (body.revision_id,)
        ).fetchone():
            raise HTTPException(404, "no such paper")
        with conn:
            conn.execute(
                "INSERT INTO owner_missing (revision_id, text) VALUES (?, ?)",
                (body.revision_id, body.text),
            )
        return {"ok": True}

    @app.post("/api/exam_review")
    def post_exam_review(body: ExamReviewIn):
        if body.verdict not in dict(VERDICTS):
            raise HTTPException(400, "bad verdict")
        conn = db()
        sealed = conn.execute(
            "SELECT sealed FROM exams WHERE exam_id = ?", (body.exam_id,)
        ).fetchone()
        if sealed is None or sealed[0]:
            raise HTTPException(404, "no such reviewable exam")
        with conn:
            conn.execute(
                "INSERT INTO exam_reviews (exam_id, question_id, verdict, note) VALUES (?,?,?,?)",
                (body.exam_id, body.question_id, body.verdict, body.note),
            )
        return {"ok": True}

    return app
