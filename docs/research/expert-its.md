# Expert opinion: intelligent tutoring / educational data mining perspective

Author's stance: I've built knowledge-component (KC) models, BKT/DKT-style tracers, adaptive item
selection, and mastery-learning systems, and I know how ALEKS (knowledge space theory) and Math
Academy (hand-built knowledge graph, diagnostic placement, "fractional implicit repetition") work.
I'm reasoning from the brief alone, without looking at the current implementation.

The short version: **this is a placement and attribution problem more than a teaching problem.**
The learner is an expert. Most of the time a naive system wastes goes into teaching him things he
already knows, and most of the modelling error comes from crediting evidence to the wrong unit.
Build the system to (a) find the edge of what he knows quickly, (b) expand the domain model only
where he fails, and (c) keep an append-only event log so that any learner state can be recomputed
when the LLM-generated graph inevitably changes.

---

## 1. How I would approach this

### Core idea

Use a **goal-anchored, lazily expanded prerequisite graph of knowledge components**, with an
**ALEKS-style "outer fringe"** (KCs whose prerequisites are mastered but which are not yet
mastered themselves) as the teaching frontier. Add a **Math Academy-style implicit-repetition
layer** so that practising advanced KCs counts as review of the KCs they build on. All learner
state is a pure function of an **event log** plus the **current graph version**.

Concretely, for a paper:

1. **Ingest and anchor.** Split the paper into passages (sections, equations, figures,
   algorithm boxes). For each passage an LLM lists what a reader must know to understand it.
   Each item on that list becomes a candidate KC with a pointer back to the passage, so every KC
   comes with "why you need this": the paper spans that depend on it. Importance is mostly the
   count and centrality of those spans.
2. **Classify every candidate KC by provenance:** `well-known` (textbook/pre-cutoff, the model is
   confident), `paper-local` (defined in this paper: its own notation, method, or results),
   `cited` (defined in a referenced paper, so fetch that paper's abstract or relevant section),
   or `unknown/unverified` (the model can't ground it). Unknown KCs are shown to the user as such
   and get no generated explanation until a source is retrieved. This meets the "flag rather
   than guess" requirement in a way you can check: every explanation must cite a source span,
   or carry an explicit "from model knowledge, well-known" tag.
3. **Diagnose top-down before teaching anything.** Start with probes on the *highest* KCs the
   paper needs (closest to the paper), not the foundations. A pass on a high KC implies its
   prerequisites, as in knowledge space theory. Drill down only below failures. For an
   experienced ML engineer this typically removes 60–80% of a naive prerequisite list in
   10–15 minutes of questions. This is the largest efficiency gain available to you.
4. **Expand lazily.** Only decompose a KC into finer prerequisites when the learner fails it, and
   the grader's diagnosis says the failure came from something underneath it. The graph grows
   where the learner needs it, not where an LLM thinks a textbook would.
5. **Teach the fringe, anchored to the paper.** Each lesson opens with the paper passage that
   needs this KC (that's the "blurry" frame), then gives a brief ADEPT-style explanation, then a
   question that requires *using* the KC.
6. **Guided reading as the main goal activity.** The deliverable isn't "KCs mastered". It's
   reading the paper. Once a section's required KCs are on track, unlock a guided read of that
   section with inline just-in-time pop-outs. Comprehension questions on the paper itself are
   both the goal check and the main evaluation signal.
7. **Maintain with a value-weighted review budget.** Schedule reviews per KC (not per card) with
   an FSRS-style memory model. Implicit credit from practising downstream KCs reduces how many
   explicit reviews are needed. Each KC's target retention scales with how much active goals
   still need it.

### Why this shape

- ALEKS's and Math Academy's real advantage is not the tracing algorithm. It's (i) a good graph,
  (ii) aggressive placement, and (iii) learning only at the fringe. With an LLM-generated graph,
  (i) is your weakest component, so (ii) and lazy expansion matter even more: they confine graph
  errors to regions the learner actually touches, where evidence can expose them.
- With one learner you **cannot fit** BKT parameters, IRT item parameters, or a DKT network in
  any meaningful sense. Use simple, interpretable update rules whose predictions you log, and
  replace them later if the logs justify it.

---

## 2. Learner model and domain model

### Unit of knowledge (KC)

A KC is **the smallest thing the learner can independently know or not know and that you can
ask at least three distinct questions about**. Practical size test for this user: one sentence
states it; one 5–15 minute lesson teaches it; failing it has a recognisable signature.

Each KC has a type, because the types behave differently:

| Type | Example | Typical items | Memory behaviour |
|---|---|---|---|
| term/notation | "what $\nabla_\theta \mathcal{L}(z)$ means in TracIn" | recognition, short recall | fast decay, cheap review |
| concept | "influence function as a first-order effect of upweighting a point" | explain, apply to scenario, contrast | slow decay once understood |
| method/procedure | "computing TRAK scores with random projections" | worked steps, "what goes wrong if…" | decays as a procedure; homework is the best evidence |
| result/claim | "EK-FAC approximates the GGN better than diagonal" | "would you expect X?" | depends on whether its *reason* is known |
| misconception | "influence ≠ leave-one-out retraining for deep nets" | discrimination items | needs explicit refutation |
| contrast | "when to use TracIn vs. influence functions" | choose-between-methods | an edge, but worth items of its own |

Treat **contrast** ("choose between methods") as a first-class unit. It is exactly the item type
the owner asked for, and its evidence must not be split across the two sibling KCs.

**Paper-local** KCs (this paper's notation and contributions) belong to the goal. They are
reviewed heavily while the paper is active and allowed to decay afterwards. **Global** KCs live
in a shared registry that persists across goals, and that registry is where value compounds over
months.

### Granularity

Granularity is *learner-relative*, which is why lazy expansion is the right policy. "Hessian" is
one KC for this user. For a novice it would be ten. Rules:

- Default granularity is "what this paper's author assumes the reader knows, at the level the
  author assumes it".
- Split a KC only on evidence: repeated failure with a diagnosis that points to a sub-part, or a
  grader that keeps needing to mention two distinct ideas.
- Merge KCs when they are always tested together and always pass and fail together (this shows up
  in the logs).
- Cap the number of KCs extracted per paper (e.g. 30–60 candidates, most of them pruned by the
  diagnostic). If an extraction proposes 200, the granularity prompt is wrong.

### Prerequisite structure

Edges are typed and weighted:

- `requires(A → B)`: B can't be understood without A. Used for the fringe. Keep these few and
  strict.
- `helps(A → B)`: knowing A makes B easier, but B is learnable without it. Used for ordering
  preference only, never for gating.
- `encompasses(B ⊇ A, w)`: practising B exercises A with weight w ∈ [0,1]. This is Math
  Academy's implicit-repetition weight, and it is how practice on a downstream KC counts as
  review of upstream ones.
- `contrasts(A, B)`: sources of discrimination items.

The LLM proposes edges. A *separate* LLM call, with the KC definitions only and no paper context,
verifies each `requires` edge with the question "could a competent learner understand B while
genuinely not knowing A?" Keep edges where both agree. Downgrade disagreements to `helps`.
Gating on a false `requires` edge costs the learner time. A missing `requires` edge is
self-correcting, because the learner fails and the system drills down.

### Maintaining the graph as it grows and gets restructured

This is the most important engineering decision. Make it now.

1. **Event sourcing.** The source of truth is an append-only log of
   `(timestamp, item_id, item_version, response, grade, grader_rationale, kc_tags_at_time, …)`.
   Learner state (mastery, memory stability) is a *derived cache*, recomputed by replaying the
   log against the current graph. Restructuring the graph then re-attributes the old evidence
   correctly instead of corrupting state.
2. **Stable IDs and never delete.** KCs are only ever *merged* (old ID becomes an alias of the
   survivor), *split* (old ID becomes a parent with a mapping of which items go to which child;
   the LLM re-tags old items), or *deprecated* (hidden, evidence kept). Every graph change is
   itself a logged event with a graph version number.
3. **Canonicalisation on insert.** Before adding a KC from a new paper, retrieve near-duplicates
   from the registry (embedding search over name and definition) and have an LLM decide whether
   it is the same KC, a specialisation, or new. This is how the second paper on influence
   functions benefits from the first. Expect to tune this: under-merging fragments evidence, and
   over-merging (treating "influence function (classical stats)" and "influence function
   (Koh & Liang deep-net approximation)" as one KC) hides real gaps.
4. **Item-to-KC tagging (the Q-matrix) is stored per item version and re-validated** by a
   separate call when items are generated and when the graph around them changes.

### How evidence updates mastery

Keep two quantities per KC and keep them separate:

- **Acquisition**: has the learner *ever understood* this? Track it as a logit ability θ_k with
  an Elo-style update against item difficulty b_i: P(correct) = σ(θ_k − b_i); after a response,
  θ_k += K·(outcome − P). K starts large (fast placement) and shrinks with the number of
  observations. Item difficulty b_i starts from an LLM-predicted tier (calibrated per item type)
  and is updated slowly from responses. (Item difficulty can be learned a little from one user,
  because the same items recur across reviews.)
- **Memory**: will he recall it *now*? Use an FSRS-style stability S_k and retrievability
  R_k(t) once the KC is acquired. Feed in only items that genuinely test recall, not the
  explanations he has just read.

Predicted success on item i for KC k ≈ σ(θ_k − b_i) adjusted down by R_k(t). **Log this
prediction before every response.** That one decision makes the whole system evaluable later
(§5).

**Evidence weight by modality:**

| Modality | Updates acquisition? | Updates memory? | Weight |
|---|---|---|---|
| read/listen | no (record as exposure only) | no | 0 |
| self-graded flashcard | weakly | yes | low; self-grades are optimistic |
| LLM-graded short answer / spoken answer | yes | yes | normal |
| application / contrast question | yes, strongly | yes | high |
| worked homework (verified, ideally by code) | yes, strongly, for the method KC | yes | highest |
| guided-reading comprehension question on the paper | yes, for the KCs the passage depends on | yes | high, and it is also the goal metric |

**Partial credit across related KCs:**

- **Success flows down.** Success on B gives implicit credit to each A with `encompasses(B ⊇ A, w)`
  in proportion to w, both to acquisition (small) and memory (counts as a fractional review, as
  in Math Academy's FIRe). A strong pass on a high KC during diagnosis sets its `requires`
  ancestors to "inferred known", a distinct state that is cheap to spot-check later.
- **Failure is attributed, not propagated by default.** On a wrong answer, the grader must output
  a *diagnosis*: which KC (primary, a prerequisite, or a careless slip/item defect) the error
  shows a gap in. Debit only that KC. Downstream KCs that require the failed KC get "doubt": a
  confidence reduction that makes them eligible for re-probing, but not a mastery penalty.
- **Multi-KC items** carry one primary KC and at most two secondary ones. The primary gets full
  weight, secondaries about a third. If an item needs more than three KCs, it is a homework
  problem: grade it by rubric, step by step, with each step tagged to a KC.

This "LLM-diagnosed blame" is the one place where LLMs genuinely beat classical ITS: a
free-text answer plus a diagnosing grader gives you per-KC attribution that classical systems
needed hand-built bug libraries to approximate. It is also the main source of misattribution
risk (§4), so log the rationale.

---

## 3. What to teach next, when to review, effort levels, goals

### Selecting the next activity

Each candidate activity gets a score; take the top one subject to the session's effort budget.

```
value(k) = goal_weight(k) · need(k) · readiness(k) · generality_bonus(k)
```

- `goal_weight`: sum over active goals of (goal weight × how much the goal's passages depend on k).
- `need`: for new KCs, 1 − P(known). For acquired KCs, expected loss from forgetting
  (1 − R_k(t)) weighted by how soon a goal needs it.
- `readiness`: 1 if every `requires` parent is acquired or inferred, otherwise 0. This is the
  fringe.
- `generality_bonus`: modest, based on how many KCs and goals in the *registry* depend on k. This
  is where the owner's "general first" belongs: as a tie-breaker, not as the primary order.

Session rules borrowed from mastery learning:

- At most 2–3 *new* KCs per session, and avoid introducing two similar KCs in the same session
  (interference). Introduce contrasts only once both sides are acquired.
- Interleave reviews with new material. Prefer reviewing an acquired KC *through* a downstream
  item that encompasses it, rather than through an isolated card.
- Diagnostic phase first for any new goal, using the information-maximising choice: probe the
  KC whose answer resolves the most uncertainty in the candidate set (typically mid-depth KCs
  on long chains).

### When to review

- Per KC, FSRS-style scheduling with a **per-KC target retention**: about 0.9 for KCs active goals
  need soon, 0.8 for registry KCs still in use, and "let it lapse to recognition" (about 0.6, or
  no reviews at all) for paper-local KCs of finished goals.
- **Hard daily review budget** (e.g. 10 minutes). When due reviews exceed the budget, drop the
  lowest-value ones. Never let the queue grow without bound, because that is how SRS users quit.
- Fold implicit repetition into the schedule: a successful downstream item that encompasses A at
  weight w pushes A's due date as if it were a review of weight w.
- Each review should use a **new item variant** from a pool generated around the KC (§4 covers
  the problem this creates). FSRS was fitted on repeated identical cards, so expect it to be
  miscalibrated for varied items. The prediction log tells you by how much.

### Effort levels

Effort level is **a constraint the user picks for a session**, not a property of the KC. Given
"10 minutes, low effort", the scheduler picks the highest-value activities that can be done as
flashcard-style items. Map effort to item formats:

- **No effort (read/listen):** use it for *advance organisers* (a 3-minute "what this paper is
  doing and why" audio), for *previews* of fringe KCs before a quiz, and for *refreshers* on
  lapsed paper-local KCs. It produces **no mastery evidence**. Tell the user this; it
  isn't a cheat.
- **Low effort (flashcards):** best for term/notation KCs and for keeping acquired concepts warm.
  Prefer "type one line" over "reveal and self-grade", or at least spot-check self-grades
  against an LLM grade now and then.
- **Higher effort (quiz, written or spoken):** the workhorse. Application, contrast, and "predict
  what happens if…" items with 1–3 sentence answers, graded by an LLM against a rubric of key
  points.
- **Very high effort (homework):** for method KCs where the user wants to *use and extend* the
  method, which is his stated goal. Make these small coding tasks verified by executing code (e.g.
  "compute TracIn scores for this toy logistic regression; the test checks your values"). They
  are the strongest evidence you have and the most transferable to research. They aren't MVP,
  but design item schemas so they fit.

If the user always picks low effort, the model starves: concepts never get application evidence.
Track the effort mix and nudge ("3 KCs have only flashcard evidence; a 5-minute quiz would
confirm them").

### Goal changes and stale goals

- A goal = {target (paper or project), weight, created_at, last_engaged_at, status}.
- Goal weight **decays** with time since the user last engaged with it (e.g. half-life of 3–4
  weeks), unless he pins it. When weight falls below a threshold, ask once: "Still working on
  paper X? Keep / archive / keep just the general ideas." Don't silently drop goals and don't
  silently keep them.
- Archiving a goal lowers the retention target of its paper-local KCs. Global KCs keep whatever
  weight other goals give them. A KC that no goal supports any more drops to "recognition only"
  maintenance and then to none, which is correct. Memory is not free and the brief's "keep it
  over time" should be value-weighted.
- A new goal that overlaps the registry gets a cheap diagnostic: inferred-known KCs from earlier
  goals are spot-checked, not retaught.

---

## 4. What is most likely to go wrong (ranked)

| # | Failure | Early warning sign | Mitigation |
|---|---|---|---|
| 1 | **Wasting the expert's time on things he knows** (graph too foundational, diagnostic too timid). This is the failure that makes him stop using it. | First-attempt success on newly taught KCs > 85%. "I know this" clicks. Sessions that end before reaching anything paper-specific. | Top-down diagnosis; inferred-known state; a one-click "I know this" that schedules a single hard spot-check instead of a lesson; a time-to-first-paper-content metric. |
| 2 | **Bad items**: wrong answer key, ambiguous wording, answerable from the wording alone, or a difficulty far from the intended tier. LLM item variance is large, and with varied items it is *uncontrolled*. | User disputes or "bad question" flags; one item variant failed while the KC is otherwise passing; grader rationale contradicts the key. | Generate → independent solve by a second model (it must reach the key without seeing it) → reject on disagreement. Discount evidence from an item's first uses (it is uncalibrated). Keep one stable "anchor" item per KC for measurement and vary the others. A "this question is broken" button that voids the evidence retroactively (easy with event sourcing). |
| 3 | **Misattributed evidence**: an item tagged to KC A actually hinges on B, or the grader blames the wrong KC, so the model teaches the wrong thing. | A KC fails repeatedly despite reteaching; reteaching doesn't change the error type; grader diagnoses point outside the item's tags. | Independent Q-matrix check per item; diagnosis output constrained to the item's tags plus their direct prerequisites plus "slip" plus "item defect"; when diagnoses keep pointing elsewhere, re-tag or split the KC. |
| 4 | **Grader leniency or drift**: LLM graders are generous with fluent near-misses, especially on spoken answers. Mastery inflates. | Success rates creep up while comprehension of the actual paper doesn't; self-reported confidence lower than grades. | Rubrics with explicit required key points and a "must not say" misconception list; grade with a different model from the generator; pin grader model and prompt versions in the log; monthly audit of 20 random gradings by the user (2 minutes). |
| 5 | **Hallucinated or post-cutoff prerequisites**: confident, wrong explanations of new methods; invented prerequisite edges. | Explanations with no source citation; the user spots errors; terms not found in the paper or its references. | Provenance class on every KC; explanations must quote source spans; fetch cited papers; render "unverified" visibly; never auto-generate explanations for `unknown` KCs. |
| 6 | **Graph churn corrupting state**: merges and splits lose history, duplicates fragment evidence, re-extraction for a new paper produces near-duplicate KCs. | Registry growing faster than the number of KCs actually taught; two KCs with near-identical definitions; mastery jumps after a restructure. | Event sourcing plus stable IDs plus alias/split semantics (§2); diff mastery before and after every graph change and alert on large jumps. |
| 7 | **Review-load explosion**: every paper adds 30 KCs, each with reviews, and the queue grows until he quits. | Due reviews per day rising week over week; skipped review sessions. | Hard budget; value-weighted retention; implicit repetition; letting finished paper-local KCs lapse. |
| 8 | **Illusion of competence from passive modes**: read/listen feels like progress. | Lots of exposure events, few graded ones. | Exposure gives no evidence; nudge toward graded items; show "evidence quality" per KC. |
| 9 | **Ordering harms motivation**: strict bottom-up prerequisite order before any paper content. | Long gap before the first paper-specific lesson. | Open with a gist or advance organiser of the paper (blurry), then the fringe, each lesson anchored to a paper passage. |

---

## 5. Evaluating with one user and no labelled data

### Day-one logs (non-negotiable)

For every graded interaction:

- timestamp, session ID, user-chosen effort level, time since the KC was last seen
- item ID, item version, full item text, item type, generator model and prompt version,
  predicted difficulty tier
- KC tags (primary/secondary) **as of that moment**, plus graph version
- **the model's predicted P(correct) before the response**, and the components it came from
  (θ, b, R)
- raw response (text or transcript), latency, number of edits
- grade, grader model and prompt version, rubric, grader rationale, diagnosed KC
- user overrides: disputes, "I know this", "bad question", self-confidence (optional 1–3 tap)

For non-graded events: exposures (what was read or heard, how long), lesson generations (with
sources cited), graph mutations (with before/after), goal changes.

Also keep: every LLM extraction output for each paper (candidate KCs, edges, provenance), so you
can re-run extraction with new prompts and diff the results.

### Measurements

1. **Predictive calibration of the learner model** (main offline metric). Log loss, Brier score,
   and a reliability curve of logged P(correct) against outcomes. Because of event sourcing, you
   can replay the log under alternative models (different K, FSRS parameters, implicit-credit
   weights, no partial credit) and compare. This is the standard EDM evaluation and it works at
   n=1 after a few hundred responses. Report it separately for first attempts on new KCs
   (acquisition) and for reviews (memory).
2. **Goal attainment: paper comprehension pre/post.** When a paper is ingested, generate and
   freeze 10–15 comprehension questions about *the paper itself* (what the method does, why a
   design choice was made, what an ablation shows, how to apply the method to a new setting).
   Never use them in teaching. Ask a few before teaching (also useful for diagnosis), and all of
   them after the guided read, then again 2–4 weeks later. Grade with a frozen rubric. This is
   the closest you'll get to ground truth on "did it teach what I needed".
3. **Time to comprehension:** learner minutes from ingestion to passing the comprehension set.
   Track it per paper; over papers it should fall as the registry fills.
4. **Diagnostic efficiency:** the fraction of taught KCs that the learner passed on first attempt
   (high means wasted teaching), and the fraction of KCs the learner *needed* that the system
   missed. You measure the second by asking, after each guided-read section, "what confused
   you?" and mapping answers to KCs. Misses are graph recall failures.
5. **Within-subject holdout (cheap causal evidence).** For a random 10–20% of fringe KCs on
   low-stakes goals, *don't teach*. Compare comprehension-question performance on passages that
   depend on taught versus held-out KCs. With a few papers this will be noisy, but it is the only
   honest estimate of whether teaching a KC helps.
6. **Retention:** delayed probes on anchor items for KCs not reviewed for a while, compared with
   the model's predicted R.

### Offline rubric checks (LLM judge plus occasional owner spot checks)

- **KC extraction:** for a sample of papers, a strong model with the full paper scores each
  candidate KC as needed / nice-to-have / not needed / mis-specified, and lists needed KCs that
  are missing. Track precision and recall across prompt versions. Seed a small "gold" set by
  having the owner annotate 2–3 papers he knows well (about an hour each, and worth it).
- **Edges:** sample `requires` edges and judge with the counterfactual question from §2.
- **Items:** rubric of keyed-answer correctness, single defensible answer, not answerable from
  surface cues, tests the tagged KC (not a neighbour), and the right difficulty tier. The
  independent-solve check gives an automated proxy.
- **Explanations:** factual accuracy against cited sources, brevity, anchored to the paper,
  contains a check-your-understanding element. ADEPT works as a checklist here, not as a
  required template.
- **Grader agreement:** periodic regrading of logged answers with a second model; track the
  agreement rate.

---

## 6. MVP scope

**Include:**

- Paper ingestion → passage-anchored KC candidates with provenance classes and explicit
  "unknown/unverified" flags; fetching of cited papers for `cited` KCs.
- KC registry with dedup-on-insert, stable IDs, and merge/alias. Typed edges (`requires`,
  `encompasses` at minimum), with the verification pass.
- Top-down adaptive diagnostic.
- Two item formats: LLM-graded short answer (including application and contrast items) and
  typed-recall flashcards. Generate → independent-solve validation. Diagnosis-producing grader.
- Elo-style acquisition plus FSRS-style memory per KC, implicit credit down `encompasses` edges,
  a review budget.
- A short lesson generator (paper-anchored, source-cited, ADEPT-ish, brief).
- Guided reading of the paper by section, with just-in-time pop-outs and frozen comprehension
  questions.
- Event log with predictions; "I know this", "bad question", and dispute buttons.
- A minimal "why am I seeing this" line per activity (which goal and passage it serves). This
  builds trust and is free debugging.

**Exclude (for now):**

- Worked homework and code-verified problems. Design the item schema to allow them; build them
  second.
- Audio/podcast generation. Text "read" mode is enough to test the idea.
- Spoken answers (they add transcription error on top of grader error).
- Fitted BKT/DKT/IRT, or any learned model. Replay-based model comparison comes once logs exist.
- Automatic graph splitting. In the MVP, propose splits and merges and apply them with a click.
- Multi-goal optimisation beyond weighted sums; language learning; graph visualisation beyond a
  simple list or tree.

---

## 7. Where I disagree with the owner's stated preferences

1. **"Order by generality, more foundational first."** For an expert this is the main way to
   waste his time. Order by *goal need × readiness*; generality is a tie-breaker. Go to
   foundations only when evidence shows a failure there. Prerequisite structure should *gate*
   (don't teach B before A), not *drive* (don't start from the roots).
2. **"Track things the user might need to know."** Agree, but tracking is not teaching. Most
   "might need" KCs should be resolved by a 30-second probe, not a lesson. Keep "candidate" and
   "taught" as distinct states.
3. **Questions should vary rather than repeat.** Mostly agree; variation reduces rote
   memorisation and tests transfer. But unconstrained variation destroys measurement: you can't
   tell whether a failure reflects the learner or a harder variant. Keep one anchor item per KC,
   generate variants within a declared difficulty tier, and validate them. Also, for
   term/notation KCs, plain repetition is fine and cheaper.
4. **No-effort reminders as a learning level.** They are useful as advance organisers and
   refreshers, but they produce no evidence and weak retention (re-reading is one of the weakest
   study strategies in the retrieval-practice literature). Don't count them toward "maintaining"
   knowledge.
5. **Flashcards as the generic low-effort mode.** Self-graded reveal cards on *concepts* produce
   recognition, not usable understanding, and self-grades are biased upward. Use typed one-line
   recall, and keep classic cards for terms and notation.
6. **"Keep that knowledge over time" (implicitly: all of it).** Maintenance should be
   value-weighted, and letting paper-local details lapse is correct. ADEPT's own point supports
   this: what survives is the analogy and gist. Make the gist the long-term retention target for
   finished papers, not the details.
7. **ADEPT and "blurry to sharp" versus prerequisite order.** They don't conflict if you separate
   *macro* order from *micro* order. Macro: gist of the whole paper first (blurry), then fringe
   KCs, then guided reading (sharp). Micro: within a lesson, analogy → example →
   technical. But beware the **expertise reversal effect**: for an expert, analogies and fully
   worked examples can be redundant and slow. Lead with a problem or the technical statement for
   KCs near his expertise, and use analogies for KCs far from it. Let the diagnostic decide
   which.
8. **Cost is no object.** Agreed for model spend, but **latency is an engagement cost**.
   Pre-generate and validate item pools and lessons for the fringe in the background, so the
   learner never waits on a generate-then-verify chain.

---

## 8. Important things the owner didn't ask about

1. **The paper is the best curriculum.** Guided reading with just-in-time support is probably a
   higher-value product than a standalone prerequisite course. Much of the confusion in
   ML papers comes from *paper-local* notation, unstated assumptions, and experimental details,
   not missing textbook prerequisites. Model paper-local KCs explicitly.
2. **Cold-start priors from the user's own work.** He writes code and papers and has read many
   papers. Seed the registry with "inferred known" KCs from a self-report checklist, a list of
   papers he has read, or his own writing, then spot-check them. This shortens the first
   diagnostic a lot.
3. **Misconceptions as first-class units.** For ML research, the expensive errors are subtle
   misconceptions (e.g. treating influence scores as causal leave-one-out effects), not gaps.
   Graders should check rubric "must-not-say" lists, and recurring misconceptions should become
   nodes with refutation items.
4. **Transparency and user override as a modelling feature.** The learner is an expert who can
   tell you when the graph is wrong. Cheap override buttons are your best source of labelled
   data. Log every override and use it in evaluation.
5. **The "use and extend" goal implies transfer tasks.** "Can you apply this method to your own
   project?" is the real test. Eventually let the user state a project goal and generate items
   in *his* setting (his models, his datasets). These are excellent items, and they double as
   project help.
6. **Language learning will stress the abstraction differently.** There, units are thousands of
   lexical and grammatical items with no deep prerequisite chains. Frequency and interest
   ordering dominate, and per-item FSRS is close to correct as-is. Keep the KC "type" field and
   make the scheduler type-aware, so you don't force paper-style graph machinery onto vocabulary.
   Speaking and listening items also need a different grader. Check now that the event and item
   schemas don't assume text-only answers.
7. **Versioning everything that generates or grades.** Models change under OpenRouter. Pin model
   IDs and prompt versions per log row, or your longitudinal data will silently mix graders.
8. **A stopping rule per goal.** Define "done with this paper" explicitly (e.g. passes the
   comprehension set, then drops to gist-retention mode). Without it, goals linger, reviews
   accumulate, and stale-goal handling has nothing to anchor to.
