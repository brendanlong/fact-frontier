# Plan: deciding what to teach, and getting it right

Status: draft for review, 2026-10-19. Inputs: the problem brief and the twelve research reports in
[`research/`](research/). Five independent expert opinions, a devil's advocate on the current
prototype, and literature on learning science, AI methods and existing products.

## 0. Summary

The research agrees on a lot, and it changes the design substantially:

1. **The unit is a typed concept with depth levels, not an atomic fact.** The prototype's
   single-claim facts made dedup easier but taught badly. In the current pool, roughly a third of
   graded facts were not worth this learner's time and 3 of 37 were wrong. Most are paper results that would be
   drilled as trivia, and the argument of each paper is scattered across sentences no one
   reads together. Claims become *question seeds attached to concepts*, not units of mastery.
   (devil's advocate; KLI framework; Math Academy topics; KCGen-KT)
2. **The paper is the spine.** First a map of the whole paper (blurry), then just-in-time
   teaching of the gaps that block each section, then guided reading of the paper itself
   (sharp). Every expert independently put a reading companion at the center, not a
   standalone prerequisite course. This settles blurry-to-sharp vs. prerequisite-first:
   blurry at the macro level, prerequisite-gated at the micro level.
3. **Diagnose before teaching.** For an expert learner, the biggest waste and the most likely
   reason he quits is teaching what he already knows. Probe top-down from the concepts nearest
   the paper and infer downward. Expand deeper only where he fails. Every expert ranked this
   first or second.
4. **Models judge, code decides.** Models make small, local, evidence-backed judgments. Code
   owns the learner state, the ordering, the scheduling and every quality gate, all built on an
   append-only evidence log. A model never writes "user knows X".
5. **Unknowns are detected from behaviour, not self-report.** Use provenance classes
   (standard / introduced here / from a citation / unknown), cutoff-date signals, and a
   closed-book vs. paper-grounded definition comparison. LLMs define over 86% of made-up terms
   when asked (PhantomBench), so asking them whether they know a term doesn't work.
6. **Item quality and grading are as risky as choosing what to teach.** Even the best model
   writes unusable flashcards about a third of the time (Memory Machines). Grading drifts
   lenient. Use spec-based generation, independent solving, leak checks, key-point rubrics
   and cross-family judges, and log every dispute.
7. **Measure from day one.** Frozen comprehension questions per paper, an owner-annotated gold
   set, canary papers with invented methods, and within-subject holdouts. The honest
   baseline is "read the paper while chatting with Claude", not "no tool".

The owner was right that the app shell is easy. The experts add one correction: the reading
companion and the feedback buttons are not shell. They are how we find out whether any of the
AI works.

## 1. Goal and how success is measured

**Goal:** minimise learner time to understand a target (first: a paper) at the depth the
learner needs, and keep the reusable parts.

**North-star metric:** understanding per learner-minute. Understanding is measured by a
**frozen target exam** per paper: 10–15 questions an expert colleague would ask after a reading
group (what problem, why the method works, what would break it, when to use it instead of X,
how to apply it to your project). It is written by a separate model call that never sees the
teaching plan, and it is never used in teaching. Ask a few questions before teaching, all of
them after, and again 2–4 weeks later.

**The bar to beat:** reading the paper with a Claude chat open. If the tool doesn't clearly
beat that on time or exam score, its value has to come from compounding across papers. Test
that directly: the second and third papers in an area should get cheaper.

## 2. Where best practice overrides the brief

| Brief said | Change | Why |
|---|---|---|
| Order by generality, foundations first | Order by **goal need × P(gap) × unlock value**. Generality decides what to *retain*, not what to teach first | For an expert, foundations are exactly what he knows. Every expert and the literature agree (expertise reversal; ITS fringe teaching) |
| Effort level chosen on demand | User picks **time budget and context**. System picks the activity, and explains its pick. User can override | Learners reliably choose the least effective strategies (Karpicke 2009; Kornell & Bjork 2008) |
| No-effort tier (read/listen) as a learning level | Keep it, but it is **exposure, never evidence or review** | Restudy doesn't maintain memory. Retrieval does (g≈0.6) |
| Keep knowledge over time | **Value-weighted retention.** Maintain reusable concepts; let paper-local detail decay; keep each paper's one-line claim and key figure | Review debt is the main reason people quit spaced repetition, and relearning a detail later is cheap |
| Varied recall | Keep, with controls: vary *within* a declared depth level, keep one stable anchor item per concept, schedule per concept | Unconstrained variation breaks the memory model and grading |
| Flag what the model doesn't know | Keep, but detect it **structurally** (§4.6) | Self-reported confidence is poorly calibrated, and consistent misconceptions survive self-consistency checks |
| ADEPT for explanations | Use as a checklist, not a template. The **example the learner works through** is mandatory. Analogies must state where they break. For concepts near his expertise, lead with the problem or the technical statement | Only the worked example is an active ingredient. Analogies for experts can be redundant (expertise reversal) |

## 3. What we keep from the prototype

Keep: the OpenRouter client with per-call cost logging; paper loading; profile-conditioned
extraction from the full paper; the "read it without the paper" review test (adding a truth
check); embedding + keyword candidate retrieval then a model decision for dedup; provenance
per source with merge logs; derived clusters that never touch history; side-by-side model
comparison scripts.

Replace: atomic facts as the tracked unit; untyped "prerequisite" edges, which currently mix
about five relations; per-fact mastery; clusters as the map of knowledge.

Known bugs the devil's advocate found, which go away with the redesign:
- Split facts inherit all of the parent's prerequisites, giving 13 sibling groups the same
  wrong edges.
- 14% of edges are transitive.
- Some edges are reversed.
- The pool states some things in contradictory ways.
- There are no cross-paper links between the misalignment and SAE papers. The wiki wrongly
  said there were; that is being corrected.

## 4. Design

### 4.1 The core model (shared across domains)

```
Goal ──needs──▶ Requirement ──on──▶ Concept ◀──tests── Item ──▶ Evidence (append-only)
 (paper,          (depth, centrality,  (typed, global or     (spec-based,    (response, grade,
  project, show)   claim/passage it     paper-local, depth    many per         rationale, latency,
                   serves, status)      levels, provenance)   concept)         predictions)
                                          │
                                          └─ typed edges: requires · encompasses(w) · contrasts ·
                                             refines · confusable_with · homonym_of
```

- **Concept**, called a knowledge component (KC) in the learning-science literature. Its
  operational definition: you can write ≥3 distinct questions that test it independently, and
  for this learner it takes one 5–15 minute lesson to teach. Types: `term`, `concept/mechanism`,
  `procedure`, `contrast` (choose between methods, a first-class unit), `claim/result`
  (usually paper-local), `misconception`. It has **depth levels**: recognize → explain → apply →
  extend. Each concept carries a grounded definition at each level, aliases, a provenance class
  and source spans. The prototype's "informal vs. formal PBRF" near-duplicate becomes two depth
  levels of one concept.
- **Requirement** links a goal to a concept: the depth needed, centrality (core contribution /
  method / experimental setup / passing mention), the claims or passages it serves, and a
  disposition. Dispositions are *teach* (needed and reusable), *gloss* (explain inline while
  reading, don't maintain) or *ignore* (peripheral). This three-way split comes from the
  language-learning expert and fits papers well.
- **Item** is generated from a spec: concept, depth, type (recall / explain why / apply to a
  new scenario / choose between / predict what happens if / diagnose / derive / implement),
  answer-length budget, and the misconception it targets. It has 1–4 gradable key points. Items
  are separate from concepts, so one concept has many items, and one item can touch a primary
  concept plus at most two secondary ones.
- **Evidence** is an append-only log. Each row records: item and version; concept tags at that
  time; graph version; the model's predicted P(correct) logged before the answer; the raw
  answer; latency; grade per key point; grader model and prompt version; rationale; diagnosed
  concept; and any user override.
  - Learner state is derived from the log by replaying it against the current graph, so
    restructuring re-attributes old evidence instead of corrupting it.
  - Concepts have stable IDs and are never deleted, only merged (alias), split (re-tag) or
    deprecated.
- **Learner state per (concept, facet)**: *acquisition*, an Elo-style ability (has he ever
  understood it?), and *memory*, FSRS stability and retrievability (can he recall it now?).
  Facets are declared per domain: explain / apply / choose for ML; read / listen / speak / write
  for language. Evidence weights depend on the activity:

  | Activity | Evidence weight |
  |---|---|
  | Read or listen | Exposure only, zero weight |
  | Self-graded card | Low |
  | Graded short answer | Normal |
  | Application, contrast or reading-comprehension item | High |
  | Code-verified homework | Highest |

- **Credit and blame** (Math Academy's implicit-repetition scheme, FIRe): success flows down
  `encompasses` edges as fractional reviews. A failure is charged only to the concept the
  grader's diagnosis names; the concepts that depend on it get "doubt", which makes them
  eligible for a re-probe, but no penalty.

The *core* (goals, requirements, concepts, items, evidence, planner, scheduler) is
domain-agnostic. Ingestion, item generation and grading rubrics are per-domain plugins (§4.8).

### 4.2 Paper pipeline: what does this paper require?

Steps 0, 3, 5 and 6 are run by code; steps 1, 2 and 4 are model calls.

0. **Ingest** (code): prefer the arXiv LaTeX source over the PDF, to get macros, definitions,
   equations and a clean bibliography. Split into addressable spans. Resolve citations to
   arXiv/Semantic Scholar IDs with dates. Fetch abstracts, and the full text for anything
   central. Find the linked code repo.
1. **Paper map** (Opus-class model, grounded): the problem and why the obvious approach fails;
   the **1–3 load-bearing claims**, each with its evidence (which figure, table or ablation);
   the method in a paragraph; known or likely weaknesses; the paper's place in its literature,
   retrieved rather than recalled. This is shown first, and it is what the target exam is
   written against.
2. **Requirement extraction** (multiple runs, ≥2 model families, results unioned for recall):
   - For each claim and each method passage: which concepts must a reader know, to what depth,
     with spans?
   - A **mechanical sweep**: code lists every equation and algorithm block, and the model
     names the concepts needed to read each one.
   - It also extracts the things the prototype missed: experimental setup and measurement
     conventions. In the misalignment paper, these were the LLM judge and its thresholds, LoRA
     and rank-1 adapters.
3. **Concept resolution** (code proposes, a model adjudicates, code applies with undo):
   - Code proposes candidates by embedding and keyword search over names, aliases and
     definitions.
   - A model decides same / specializes / homonym / new. Matching on a name with a definition
     is much easier than matching one-sentence claims.
   - Most of a new paper's requirements should resolve to existing concepts, and the fraction
     that do is a metric.
4. **Provenance and novelty** (§4.6), then **edges**:
   - Only `requires` gates the order of teaching. It is proposed by one call and verified by a
     second, which sees only the concept definitions and is asked: "could a competent learner
     understand B while genuinely not knowing A?" Edges both calls agree on are kept;
     disagreements are downgraded to `helps`.
   - `encompasses` weights are proposed for credit flow.
   - `contrasts` edges seed "choose between" items.
   - A "results support claims" relation does **not** become an ordering edge.
5. **Disposition** (code, from centrality, reuse across goals and depth): teach / gloss /
   ignore. Cap: 30–60 candidates per paper before diagnosis. If extraction proposes 200, the
   granularity prompt is wrong.
6. **Target exam** (separate call, frozen).

### 4.3 What does this learner lack?

Diagnosis takes a few minutes per paper, before any teaching:

- **Seed priors** from the profile, the user's own papers and code, and papers already in the
  store. The second paper inherits what the first established.
- **Triage screen**: the candidate list with *know it / heard of it / don't know / irrelevant*.
  Fifty concepts take about two minutes. The answers are evidence, and they are also labels on
  extraction precision.
- **Verify the claims that matter.** Self-report is trusted for peripheral concepts. Central
  concepts marked "know it" get **one** discriminating probe. Software engineers over-claim
  maths definitions and under-claim things they've used in code without naming them.
- **Probe top-down**: start at the concepts closest to the paper. A pass marks the concepts
  it requires as *inferred known* (a distinct, spot-checkable state). Drill down only below a
  failure. Choose the next probe as the one whose answer settles the most uncertainty.
- Pretesting is itself a learning aid: attempting a question before instruction improves later
  learning, even when the attempt fails.

### 4.4 What comes next

Code scores candidates: `value = goal_weight × need × readiness × (1 + small generality bonus)`.
`need` = P(gap) for new concepts, or expected forgetting loss for acquired ones. `readiness` = all
verified `requires` parents are known, which is the "fringe" in tutoring-system terms.

**Session shape for a paper goal:**

1. The paper map: a gist plus the key figure, and optionally audio.
2. For the next section of the paper: teach the 1–3 gaps blocking it. Each gets a short
   grounded explanation followed by one question that needs it. Problem-first for concepts
   near his expertise.
3. Guided reading of that section, with inline glosses for *gloss* concepts, "ask about this
   paragraph" and "I got stuck here". Each question he asks or place he gets stuck is logged as
   evidence of a gap and as a label for extraction recall.
4. After each section: one or two adjunct questions on the paper itself.
5. After the paper: target-exam questions, choose/predict/diagnose items on the core concepts,
   and one optional homework item (derive, or implement on a toy model), plus a "how does this
   apply to *your* project?" question.
6. A **stopping rule**: passing the target exam drops the goal into gist-retention mode.

**Rules:**
- At most 2–3 new concepts per session.
- Don't introduce two confusable concepts in the same session.
- Contrasts come after both sides are acquired.
- Mix reviews in, preferring a downstream item that encompasses the due concept.

**Effort:** the user sets time and context ("10 minutes, phone"). The planner picks the
highest-value activity that fits. If he keeps choosing low effort, the planner says which
concepts have only weak evidence. Every activity shows a "why am I seeing this?" line: which
goal and passage it serves, and the score components.

### 4.5 Teaching artifacts

- **Explanations** (grounded, cached, versioned):
  - Each sentence carries a source tag: a span, or `background`. `background` is allowed only
    for `standard` concepts.
  - They use the paper's notation and running example.
  - The "example the learner works through" is mandatory. For this user, code or a tiny
    numeric example is often the best diagram.
  - Each analogy is labelled as one and says where it breaks.
  - There is a brevity budget (phone screen).
  - Each ends with something to do.
- **Items** follow a pipeline: spec → generate several candidates → an independent solver
  must reach the key using only the item and the source spans → a leak check (a solver given
  only the stem and the concept's name must fail) → an ambiguity check (two solvers agree) →
  code gate. Ground generation in graded examples of good and bad items from the same kind of
  passage; that raised precision from 56% to 78% in Memory Machines. Keep a small
  owner-labelled item bank for this.
- **Grading**:
  - A key-point rubric: full / partial / none per point, quoting the span of his answer that
    earns it.
  - A "must not say" misconception list.
  - Anchors showing that terse but correct answers get full credit.
  - The grader runs on a different model family from the generator.
  - "Needs human" routing goes to the owner.
  - One-click dispute, which voids the evidence retroactively.
  - Grade several times and treat disagreement as uncertain.

### 4.6 Unknowns and very new papers

Each concept gets a provenance class: `standard` | `introduced-here` | `from-citation` |
`unknown`. Signals, combined in code:

- **Dates:** a defining citation that is newer than, or close to, the model's cutoff. The
  *effective* cutoff varies by topic, so treat dates as a signal, not a rule.
- **Definitions:** the term is defined in this paper (`\begin{definition}`, "we propose", "we
  call").
- **Collision check:** the model defines the term closed-book. Separately, a definition is
  extracted from the paper and its cited source. A judge compares the two. If they differ, the
  concept is `grounding-required`, and the difference is worth teaching (name collision, e.g.
  "emergent misalignment" read as generic emergence).
- **Existence check:** ask "does X exist?" *before* asking for a definition. Presupposing the
  term exists increases fabrication.
- **Disagreement:** different model families give materially different definitions.

`unknown` is a first-class UI state. It shows what the paper itself says, and suggests "read
[ref 23] first" rather than generating an explanation. Only `standard` concepts may be
explained from model knowledge, and those are still faithfulness-checked. Every regression run
includes **canary papers** with invented, plausibly named methods whose definitions differ from
what the names suggest. The headline metric is the rate of confident errors on post-cutoff and
canary concepts, and it must be near zero.

### 4.7 Maintenance

- Concept-level FSRS, with a per-concept target retention set by goal value. Roughly:

  | Concept status | Target retention |
  |---|---|
  | Needed soon by an active goal | ~0.9 |
  | Reusable, still in use | ~0.8 |
  | Paper-local, goal finished | Let it lapse to recognition, or stop reviewing |

- Long-term review only for concepts reused across goals, plus each paper's one-line claim.
- A hard daily review budget. When it overflows, auto-postpone by value (the SuperMemo
  approach) instead of letting a backlog form.
- Goal weight decays without engagement (half-life of a few weeks) unless pinned. When it gets
  low, ask once: keep / archive / keep just the general ideas.

### 4.8 Keeping language learning possible

Requirements for the core now; building it comes later:

- The planner must work with **no** prerequisite edges, using frequency and coverage.
- No LLM call in the per-item planning loop. Scale to about 10⁴–10⁵ items.
- Mastery is per (item, facet). Record latency on every test from day one.
- Evidence kinds include exposure, self-report and test, at different strengths.
- Probability-known generalizes to untested items, via a learner-level ability over item
  features.
- Goals can be coverage targets ("98% of this show's words") with deadlines.
- Teach / gloss / ignore is a planner output.
- Items are separate from prompts. One prompt can test a target and give weak credit to
  context items.
- `confusable_with` affects when new items are introduced.
- Evidence can point to a location in a source: a paper span or an episode timestamp.
- The learner profile has a domain-specific section (L1, target variety).

## 5. Agents and their rubrics

Every model-made decision has an explicit rubric. Rubrics are **binary or small-ordinal
criteria, each checkable in under a minute with the cited spans open**. A rubric is validated
before it is trusted:
- Cohen's κ ≥ 0.6 against ~30–50 owner labels per criterion.
- It catches ≥ 90% of defects injected into good outputs: wrong sign, leaked answer,
  off-target concept, unsupported claim.
- It is stable when position, format and length change.

Judges come from a different model family than the generator (all available via OpenRouter),
and model and prompt versions are pinned in every log row.

| Decision | Made by | Rubric (abridged) |
|---|---|---|
| Paper map | Opus-class, grounded | Names the 1–3 load-bearing claims, each with the specific figure, table or ablation that supports it. Problem and why the obvious approach fails. Every statement span-cited. An expert would accept it as a fair summary |
| Requirement (per item) | Multi-run, cross-family | **Grounded**: a span uses it. **Necessary**: names the claim, equation or step that would be misunderstood without it ("helpful background" is tagged context instead). **Depth** matches how the paper uses it. **Granularity** matches the anchor examples. **Centrality** tagged |
| Requirement set | Code + judge | Recall against the owner's gold list (priority over precision). Every equation and algorithm block covered. Includes setup and measurement conventions |
| Concept match | Model, code applies | Same / specializes / homonym / new. Merge only if knowing one means knowing the other at the same depth. Checked against a labelled set of concept pairs |
| `requires` edge | Proposer + blind verifier | "Could a competent learner understand B while not knowing A?" Both must say no. Never from a result to a claim |
| Provenance | Code + collision probe | Class assigned from signals (§4.6). Canaries flagged |
| Diagnostic probe | Generator + checks | Discriminates: a model given only the concept's name and a one-line gloss fails, and one with the definition at the target depth passes |
| Explanation | Generator + faithfulness judge | Faithful (claim-level entailment against spans, or standard background). Targeted at the gap and depth. Doesn't re-explain known concepts. Anchored in the paper's notation. Has the worked example. Bounded analogy. Within the brevity budget. Analogy quality is judged by the owner pairwise, not by a model |
| Item | Generator → solver → leak and ambiguity checks | Retrieval, not recognition. No leak. Exactly one defensible answer. 1–4 objective key points. Targets the tagged concept at the tagged depth. Novel scenario for "apply" items. Short |
| Grade | Cross-family grader | Per key point with a quoted evidence span. Meaning, not wording. Terse-correct anchors. Misconception tags. "Needs human" when unsure |

Owner effort is spent where it pays most: a gold set, pairwise preferences rather than Likert
scores, and only the cases where judges disagree (active selection).

## 6. Evaluation

**Gold sets:**
- **A. Papers the owner already understands well** (8–15 in his areas, pre- and post-cutoff).
  For each, about 15–20 minutes writing "what a strong software engineer + general ML person
  would need, how deeply, and the 3 things that matter most". This is the highest-value
  annotation.
- **B. Canary papers** with invented methods, plus real papers published after the model's
  cutoff.
- **C. Live papers**: labels from use (triage clicks, stuck points, disputes, "already knew").
- **D. Item and grading sets**: about 100 owner-labelled items, about 50 of his answers graded
  by him, and adversarial answers (fluent but wrong, terse but correct, different
  terminology).

**Stage metrics, re-run on every prompt or model change:**
- Extraction recall and precision against gold A.
- Canary flag rate and confident-error rate.
- Item defect rate.
- Grader κ against owner grades.
- Fraction of a new paper's requirements resolved to existing concepts.
- Top-5 overlap with the owner's "3 things that matter most".

Re-run each 3× at production temperature and report the variance.

**Outcome metrics:**
- Target exam score: before, after, and 2–4 weeks later.
- Time to competence.
- Transfer questions.
- Calibration of his confidence against his correctness.
- Process health:
  - "Already knew" or skip rate: above 30% sustained means diagnosis is broken; near 0% is
    suspicious.
  - First-attempt accuracy on new material: target 70–85%.
  - Dispute rate: under 5%.
  - Daily review minutes.
  - Time spent in the paper vs. in modules.

**Causal checks at n=1:**
- Randomly withhold teaching on about 20% of diagnosed gaps, and maintenance on some reusable
  concepts. Compare the target-exam questions that depend on them.
- Alternate papers between "tool" and "read with Claude chat".
- Log the learner model's predicted P(correct) before every answer, so alternative models can
  be compared by replaying the log.

**Logs (keep all of it):** every model call (stage, prompt version, model, full input and
output, cost); every planner decision with its score components; every interaction; every graph
mutation with reason and undo; source snapshots.

## 7. Top risks

| # | Risk | Early warning | Main mitigation |
|---|---|---|---|
| 1 | Over-teaching an expert (40–80 "prerequisites" when 3–8 matter) | "Already knew" > 30%; first-try success > 85%; user reads the paper directly instead | Diagnosis first; triage; top-5 queue; paper as spine |
| 2 | Confident errors on new material (name collision, stale meanings, fabricated literature) | Explanations without span citations; definitions differ across runs; canary failures | Provenance classes; collision check; grounding gates; `unknown` state |
| 3 | Illusion of learning (fluent explanations, easy items, lenient grading) | Practice scores > 90% while target-exam scores lag | Frozen independent exam; strict cross-family grader; aim for 70–85% first-try success |
| 4 | Bad items or grades destroy trust | Disputes > 5%; checker passes everything; grades correlate with answer length | Item pipeline; defect-injection tests; dispute → eval set |
| 5 | Teaching what's easy to define, not what matters | > 50% definitional items; no items on evidence, controls or design choices | Requirements tied to claims; quotas of choose/predict/diagnose items |
| 6 | Errors compound across stages (90% per stage ≈ 60% end to end) | Stuck points that map to no concept; mastery jumps after a merge | Per-stage evals; multi-run extraction; reversible merges; reading-companion signal |
| 7 | Concept store drifts as papers accumulate | Concepts per paper not falling; near-duplicates | Canonical IDs and aliases; periodic consolidation proposals for owner approval |
| 8 | Review debt → abandonment | Due count rising week over week; skipped days | Value-weighted retention; hard budget; let paper-local items decay |
| 9 | The tool replaces reading the paper | PDF never opened; can't locate claims in the paper | Activities point into the paper; guided reading is the main activity |
| 10 | LLM "students" used as evidence of teaching | — | Use simulated students only for mechanical checks (answerability, leaks) |

## 8. Phases, each with an exit test

Rule: no phase starts until the previous phase's exit test passes. The app grows only as fast
as measurement allows.

**Phase 0: evaluation harness and gold data**
- Owner: pick 8–10 papers he knows well and annotate them (about 3 hours total). Also do a
  stuck-point read of one *new* paper (about 1–2 hours). That is the devil's advocate's fastest
  viability test.
- Build: canary papers; a scoring script for requirement sets against gold A and the stuck
  points; a one-shot baseline (an Opus "reading guide" for the same papers: argument map plus
  inline prerequisite explainers).
- Exit: the scoring runs end to end and the owner trusts the gold labels.

**Phase 1: requirements engine (no learner model yet)**
- LaTeX ingest and citation resolution, paper map, multi-run cross-family requirement
  extraction with the equation sweep, provenance classes, concept store with resolution and
  typed edges, dispositions, target exam.
- Output: an HTML report per paper (map, requirements with spans and provenance badges,
  concept graph) plus a triage page the owner can click through.
- Exit:
  - Recall ≥ 0.8 against gold A and the stuck points.
  - Precision ≥ 0.5 before triage.
  - Canary confident-error rate ≈ 0.
  - Beats the one-shot reading guide on recall at equal or better precision. If it doesn't, the
    reading guide becomes the per-paper core, and the concept store is kept only for
    cross-paper reuse.

**Phase 2: diagnosis, items and grading**
- Triage, top-down probes with inference, the item pipeline, the cross-family grader with key
  points, disputes. A minimal web UI: FastAPI + SQLite, following the chess-pretraining setup,
  with a component-based frontend.
- Exit:
  - Item defect rate under 10% on owner review.
  - Grader κ ≥ 0.6 against his grades.
  - Diagnosis removes ≥ 60% of candidates in under 10 minutes, and spot-checks show the
    removed ones really were known.

**Phase 3: the teaching loop and reading companion**
- The paper map view, just-in-time explanations, guided reading with glosses / ask / "stuck
  here", post-reading items, the target exam, the event log with predictions.
- Exit, over 3–4 real papers:
  - Target-exam scores beat the "read with Claude chat" papers at equal or lower time, **or**
    the time per paper drops clearly from paper 1 to paper 3 in the same area.
  - "Already knew" stays under 30%.

**Phase 4: maintenance and multiple goals**
- Concept-level FSRS with implicit credit, budgets, goal decay, stopping rules, the
  withheld-maintenance holdout.

**Later:** more effort modes (generated audio for exposure, spoken answers, code-verified
homework); a language-learning pilot using the §4.8 requirements; learned models fitted on the
replayable log.

## 9. Decisions needed from the owner

1. **Gold-set time.** About 3 hours to annotate 8–10 papers he knows, plus 1–2 hours for one
   stuck-point read. This is the most valuable input to the whole plan. Which papers?
2. **Cross-family judges.** Use GPT and Gemini via OpenRouter for checking and grading Claude
   outputs, and the reverse? Recommended.
3. **LaTeX source.** Prefer arXiv LaTeX, falling back to PDF? Recommended.
4. **Prototype code.** Rework the existing repo in place (keeping its infrastructure) rather
   than starting over? Recommended.
