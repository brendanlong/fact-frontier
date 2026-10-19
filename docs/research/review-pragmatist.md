# Review of PLAN.md: a pragmatist's view

Reviewer stance: one user, an experienced engineer, agents do the building, money is no
object, and the owner's time and attention are the scarce resources. The question for every
section is "does this help us find out, soon and honestly, whether the core idea works?"

Overall: the *diagnosis* in the plan is right. Concepts instead of atomic facts, the paper as
the spine, diagnosis before teaching, models judge and code decides, and a frozen exam
against a "read it with Claude" baseline. The *sequencing* is wrong for this owner. It puts
four gated phases and roughly 4–5 hours of up-front annotation between him and the first time
he uses the thing on a paper he actually wants to read. And the reading companion, which is
both the product and the best source of labels, is held back until Phase 3. Most of the fixes
below are reorderings, not cuts.

---

## Issues, in priority order

### 1. Blocker: the first useful thing arrives at Phase 3, behind three gates
**Section:** §8 (Phases).
**Problem:** The owner first reads a real paper with the tool in Phase 3, after Phase 0
(harness + 4–5 h of annotation), Phase 1 (LaTeX ingest, citation resolution, multi-family
extraction, concept store, typed edges, target exam) and Phase 2 (diagnosis, item pipeline,
grader, web UI), each of which must pass its exit test. Realistically that is weeks of agent
work plus several owner review sessions, while he is still reading papers the old way. The
plan's own risk list (#1 over-teaching, #9 the tool replacing the paper) and the research
mentor's warning ("adults who are already researchers drop tools that feel like homework they
didn't choose") both point at motivation, and this schedule spends it.
**Change:** Ship a **v0 reading guide in the first days**: paper map, the requirement list with
spans and provenance badges, and an inline gloss or short explainer per gap, as one static HTML
page per paper. The plan already specifies this as the Phase 0 "one-shot baseline". Promote it
to the first product. He uses it on the next paper he was going to read anyway. Keep the
measurement honest by generating and sealing the target exam *before* he opens the guide (see
the alternative sequencing below).

### 2. Blocker: the reading companion is both the product and the label source, so it can't wait for Phase 3
**Section:** §4.4 (step 3), §6 gold set C, §8 Phase 3.
**Problem:** "I got stuck here", "ask about this paragraph" and "already knew" clicks are
gold set C. They are the cheapest, most honest recall labels the plan has, because they come
from real reading and not from recollection. Phase 1's exit needs recall against "the stuck
points", but the instrument that collects stuck points isn't built until Phase 3. So Phase 0
falls back to one scheduled 1–2 h stuck-point session.
**Change:** Build a *minimal* companion in Phase 0/1: the paper's text split by section, with
a "stuck here" button per paragraph (with an optional note) and an "ask" box that calls a model
and logs the question. No learner model, no items. Every paper he reads after that adds stuck
points for free, and it is the first useful thing from issue 1.

### 3. Major: the gold-set ask is the wrong shape. It costs a lot, it's written from memory, and its scoring is under-specified
**Section:** §6 gold set A, §8 Phase 0, §9 decision 1.
**Problems:**
- *Expert blind spot.* "Write what a strong SWE + general ML person would need" for papers he
  already understands asks him to remember what he didn't know before. Experts are poor at
  this, and the result will lean toward what is salient now. Recall against it will be
  measured against a biased list.
- *Generation vs. recognition.* Writing a requirement list from a blank page takes 15–20
  minutes per paper. Ticking or crossing a candidate list that the models have already produced
  takes about 2 minutes per 50 items, by the plan's own estimate (§4.3). The plan uses
  recognition for triage but generation for gold.
- *Scoring is a hidden third judge.* Gold A is free text. Scoring recall means matching his
  phrases to extracted concepts, which is another LLM judgment with no rubric, threshold or
  validation in the plan. Granularity mismatches ("Gauss-Newton Hessian" against "K-FAC
  curvature") will move recall by ±0.2, which is enough to decide the 0.8 gate on its own.
- *The exit test "the owner trusts the gold labels"* can't be tested.

**Change:** Do it in three cheaper steps:
1. **Use the four papers already ingested** (Bae, Grosse, Soligo, Der). Run the new
   extraction plus the one-shot guide, union the concept lists, and have him triage the union:
   keep / already know / irrelevant / wrong. Then he adds anything missing and picks the "3
   things that matter most". That is about 10 minutes per paper, roughly 45 minutes in total. The
   devil's advocate's 37 graded facts and its list of missing concepts (LLM judge and
   thresholds, LoRA, rank-1 adapters, linear representation hypothesis) are already labels.
   Convert them before asking him for anything.
2. **Stuck points come from natural reading** (issue 2), one paper at a time. Don't schedule a
   separate session.
3. **Add more "already understood" papers only if** recall numbers look unstable across the
   first four. Start with 4. Go to 8–10 only if needed.

Make the gold format explicit: per paper, a list of `{concept name, needed depth, must-know
(y/n), notes}`. Make matching a recorded human step: during triage he ticks which extracted
concept covers each of his items, so recall needs no model.

### 4. Major: rubric validation hides a large owner-labelling bill
**Section:** §5 (κ ≥ 0.6 against ~30–50 owner labels *per criterion*), §6 gold set D.
**Problem:** The §5 table has roughly 35–40 criteria across 9 decisions. At 30–50 labels each,
that is over a thousand owner judgments, plus 100 labelled items and 50 self-graded answers in
gold set D. None of this appears in §9's time estimate, which only mentions 3 + 1–2 hours.
This is where the owner's time would actually go.
**Change:** Validate only the criteria that **gate a decision or touch the learner** right now.
In Phase 1 that is requirement necessary/grounded (covered by triage) and provenance/canary
(covered by the canary set, with no owner labels). In Phase 2 it is the grade (his disputes and
overrides *are* the labels) and item defects (his "bad question" clicks). Every other
criterion starts as a judge whose disagreements get logged, and is validated only when a
metric suggests it is causing harm. Put a total owner-hours budget per phase into §9.

### 5. Major: the exit thresholds are arbitrary, absolute and statistically meaningless at this n, and most gates have no failure plan
**Section:** §8 exit tests.
**Problems:**
- Recall ≥ 0.8 and precision ≥ 0.5 have no stated basis, and both depend on the matching
  method and granularity (issue 3). With 4–10 papers, the confidence interval on recall is
  roughly ±0.1.
- The Phase 3 exit ("target-exam scores beat the read-with-Claude papers… over 3–4 real
  papers") compares about 2 papers against 2. Paper difficulty and prior familiarity swamp the
  effect, and each paper can only be read once, so there is no way to rerun it.
- Only Phase 1 says what happens on failure (fall back to the reading guide). Phases 0, 2 and 3
  just stop the project.

**Changes:**
- Make gates **relative to the baseline** wherever possible: "the pipeline's recall beats the
  one-shot guide's by a margin larger than its own run-to-run variance (§6 asks for 3 runs)".
  That is sounder than 0.8 and costs nothing extra.
- Treat absolute numbers as **alarms, not gates**: "already knew" > 30%, disputes > 5%,
  confident errors on canaries > 0. These are good, keep them.
- For Phase 3, rely on **within-paper** comparisons: the 20% withheld-teaching holdout,
  pre-test vs. post-test on the same exam, and his rating of whether each gap explanation
  unblocked him. Present paper-vs-paper results as descriptive only.
- Give every gate a **pre-registered fallback**, and allow the next phase to start in parallel
  when the failure is in a component it doesn't depend on. For example:
  - Phase 2 grader κ < 0.6: ship with self-grading plus a model's suggested grade, and keep
    collecting disputes.
  - Item defect rate > 10%: show items with a "bad question" button and log every click.
  - Diagnosis removes < 60% of candidates: show the triage screen only.

  None of these should block the teaching loop.

### 6. Major: Phase 1 is too big, and parts of it serve later phases
**Section:** §4.1, §4.2, §8 Phase 1.
**Problem:** Phase 1 bundles the parts needed to *decide what to teach* with infrastructure
that only pays off later or for other domains:
- Six edge types and `encompasses` weights. These only matter for FIRe credit flow in Phase 4.
- Facets and Elo + FSRS per (concept, facet).
- Replaying evidence against graph versions.
- §4.8 language-learning requirements, such as 10⁵-item scale and "no LLM in the planning
  loop".
- Citation resolution to Semantic Scholar, with full-text fetching of central references.

**Change:** Phase 1 = LaTeX ingest (keep it: equations and definitions matter, and the sweep
depends on it), paper map, multi-run cross-family requirement extraction with spans, provenance
classes using the paper-internal and collision signals, concept resolution against the store,
`requires` edges only (proposer + blind verifier), dispositions, the sealed target exam.
Defer to when they are first used:
- the other edge types (store `contrasts` if extraction produces it for free);
- citation full-text fetching. Start with arXiv IDs and dates from the .bbl, which are enough
  for the date signal;
- facets;
- graph-versioned replay. Store the graph version on each evidence row now, since that costs
  nothing, and build the replay later.

Keep §4.8 as a *design review checklist*, not build work. Multiple model families and multiple
runs cost only money, so keep them.

### 7. Major: the target exam isn't independent of the pipeline it evaluates
**Section:** §1, §4.2 step 1 ("[the paper map] is what the target exam is written against"),
step 6.
**Problem:** The plan says the exam "never sees the teaching plan", but it is written against
the paper map, and the paper map also drives teaching. If the map misses or misstates a
load-bearing claim, the exam and the teaching share the error, and the scores look fine. This
is the plan's own risk #6 (compounding errors) applied to its north-star metric.
**Change:** Generate the exam from the **paper alone**, in a separate call on a different model
family with its own rubric ("questions an expert colleague would ask after a reading group").
Seal it before any other stage runs. Let the owner add or veto questions *after* he finishes
the paper (2 minutes), since he is the only judge of "is this what matters". Log map/exam
disagreement as a metric on the map.

### 8. Major: not actionable enough for an agent to start Phase 0/1 tomorrow
**Sections:** §4, §6, §8.
**Ambiguities an implementing agent will hit:**
1. **Repo transition.** §9 recommends reworking in place, but there's no migration plan. Is
   there a new DB file or a new schema in `pool.db`? What happens to `facts`, `fact_sources`,
   `merge_log`, `clusters` and `review.py`? Are the four ingested papers re-ingested? Suggest:
   new schema, new DB, old modules deleted once replaced, and the four papers re-ingested as the
   first regression set.
2. **No schema.** §4.1 is a diagram and prose. An agent needs table definitions for goal,
   requirement, concept (with depth-level definitions, aliases, provenance), edge, item and
   evidence, or explicit permission to design them and record them in DESIGN.md.
3. **Canary papers.** How many, in what format (LaTeX or text), who writes them, and how
   invented methods are made plausible yet different from what their names suggest. Suggest
   2 canaries, written by a model from a real paper with one method replaced and renamed, and
   checked by the owner in 5 minutes.
4. **Scoring script.** It needs a gold format, a matching method (issue 3) and an output
   format. And how is a *prose* reading guide scored for recall against a concept list? It
   needs its own concept-extraction step, which the plan doesn't mention.
5. **Granularity anchors** ("matches the anchor examples", §5) are referenced but don't exist.
   Someone has to write 10–15 good/bad examples. Suggest drawing them from the devil's
   advocate grades (A-graded facts 132, 136, 43 as positives; 48, 109, 153 as negatives) plus
   PBRF informal/formal as one concept with two depths.
6. **Model choices.** "Opus-class" and "different family" need named OpenRouter model IDs,
   and the cutoff date used by the provenance date signal needs to be stated per model.
7. **Tension between the candidate cap and recall.** §4.2 caps candidates at 30–60 per paper,
   but extraction is a union of multiple runs, "for recall". Say whether the cap applies before
   or after the union, and whether exceeding it fails the run or just triggers an alarm.
8. **"Few minutes" vs. "about two minutes for 50"** of triage, plus probes. Fine, but say what
   the Phase 1 triage page *is*: a static HTML page with a form that writes to a JSON file?
   That choice decides whether Phase 1 needs a server at all.
9. **No output contract for Phase 1.** Name the file per paper (e.g.
   `reports/<arxiv-id>/guide.html`) and the CLI command (`frontier ingest`, `frontier score`).

### 9. Minor: "alternate papers between tool and read-with-Claude" costs real papers for little signal
**Section:** §6 causal checks, §8 Phase 3.
**Problem:** He reads perhaps a few papers a week in his area. Putting every other one in a
control arm halves his use of the tool, and as issue 5 shows, the comparison is too noisy to
be decisive at this n.
**Change:** Run the control arm rarely: one or two papers, *after* the tool is decent, as a
sanity check. Use within-paper holdouts as the main causal evidence. Also log, during normal
tool use, how often he opens a Claude chat anyway, and why. That gap is a direct signal of what
the tool misses.

### 10. Minor: the item pipeline and grader belong to the teaching loop, not before it
**Section:** §4.5, §8 Phase 2.
**Problem:** Phase 2 builds a 5-stage item pipeline (spec → candidates → solver → leak check →
ambiguity check → code gate) and a validated cross-family grader before any teaching exists to
use them. Until the teaching loop runs, item defect rate and κ are measured on items nobody
needs yet.
**Change:** Start with a solver + leak check only, one item per gap, and self-grading against
the key points with a model's suggested grade. Add ambiguity checks, multi-sample grading and
κ validation once dispute and "bad question" clicks show where the defects actually are.

### 11. Minor: maintenance has nothing to maintain until there are several papers
**Section:** §4.7, §8 Phase 4.
**Problem:** None. Phase 4 is correctly last. Mentioned only to say that "one optional homework
item", audio and spoken answers should stay in "Later", and that FSRS should not creep forward.
**Change:** None, beyond keeping it last. At most, record the paper's one-line claim and key
figure per paper from day one, since that is the plan's retention unit and costs nothing.

---

## What must not be cut

These are the parts of the plan that are right and cheap relative to their value. A
simplification pass might try to remove them:

1. **The frozen target exam, sealed before teaching, plus a pre-test.** Without it, every other
   number measures the pipeline against itself. (Fix its independence per issue 7, but keep it.)
2. **The "read with Claude chat" bar.** It is the honest baseline, and it keeps the project
   from building something that loses to a chat window.
3. **The one-shot reading guide as a competitor, with a pre-committed fallback.** "If it
   doesn't beat the guide, the guide becomes the core" is the single best decision rule in
   the plan.
4. **Triage clicks as evidence and as labels.** One action yields both diagnosis and an
   extraction-precision label. This is the template for all owner time: labels should come
   from use.
5. **An append-only evidence log, and "a model never writes 'user knows X'".** It is cheap to
   do from the start and impossible to retrofit. The same goes for logging predicted
   P(correct) before each answer and pinning model and prompt versions on every row.
6. **Provenance classes, an `unknown` state, and canaries.** This is the owner's explicit
   requirement, the devil's advocate found that all 3 wrong facts were prerequisites written
   from model memory, and the cost is small.
7. **Spans on every requirement and explanation sentence.** This makes faithfulness checkable
   and lets every activity point back into the paper (risk #9).
8. **The "already knew" alarm (> 30%), and the 2–3 new concepts per session cap.** These are
   the direct guards against over-teaching, the most likely way this product fails.
9. **Value-weighted retention with paper-local detail allowed to decay.** It prevents review
   debt and keeps the product from drilling trivia.

---

## Proposed alternative sequencing

The principle: **every paper he reads through the tool both helps him and produces labels.**
The app grows only as fast as measurement allows, but measurement grows from use, not from
annotation sessions held in advance.

**Step A: days 1–3 (agent build; about 45 min of owner time)**
- New schema and DB. Re-ingest the four existing papers through: LaTeX ingest → paper map →
  multi-run cross-family requirement extraction with spans and provenance → concept
  resolution → `requires` edges with a verifier → dispositions. Separately, from the paper
  alone, a sealed target exam.
- Build the one-shot Opus reading guide for the same four papers.
- Build a static triage page per paper over the union of both concept lists. **Owner:** about
  10 min per paper triaging, adding misses and picking the top 3. Convert the devil's advocate
  grades into labels.
- Build the scoring script: recall and precision for pipeline vs. guide, with variance over
  3 runs. Build 2 canaries.
- **Decision point (not a gate):** if the pipeline doesn't beat the guide, the guide becomes
  the per-paper core (the plan's own fallback). Either way, Step B goes ahead with whichever
  wins.

**Step B: end of week 1 (first real use; owner time is his normal reading time + 15 min)**
- **Reading guide v0** for the next paper he actually wants to read: map first, then the
  paper by section with glosses, a "stuck here" button and an "ask" box that logs questions.
  A tiny FastAPI + SQLite app, or static HTML posting to a local endpoint.
- Before he opens it: a 2-minute triage, plus 3 pre-test questions from the sealed exam.
  After: the full exam, and his additions or vetoes to it.
- Every stuck point, question and "already knew" click goes into gold set C automatically.

**Step C: weeks 2–3 (diagnosis and JIT teaching, still inside the companion)**
- One discriminating probe for central "know it" concepts. Top-down inference.
- For the 1–3 gaps blocking each section: a short grounded explanation and one item (solver +
  leak check). Self-grading with a suggested model grade, plus a dispute button.
- A 20% withheld-teaching holdout on diagnosed gaps, starting on the first paper.
- Alarms: "already knew" rate, stuck points that map to no concept, disputes.

**Step D: once 3–5 papers have gone through (hardening where the data says to)**
- Grader validation from accumulated disputes. Fuller item pipeline if "bad question" rate is
  high.
- One "read with Claude" control paper as a sanity check.
- Delayed (2–4 week) exam on the first papers.

**Step E: maintenance**
- FSRS on reusable concepts, a review budget, decay of paper-local detail.

This gets him a useful tool on a real paper in about a week instead of several, cuts up-front
owner time from about 4–5 hours to under 1, and keeps every honest measure in the plan: the
sealed exam, the baseline comparison, canaries, holdouts and logged predictions.
