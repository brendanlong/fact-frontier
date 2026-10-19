# Plan: deciding what to teach, and getting it right

Status: v2, 2026-10-19, revised after three reviews: [teaching](research/review-teaching.md),
[AI systems](research/review-ai-systems.md) and [pragmatist](research/review-pragmatist.md).
Inputs: the [problem brief](research/brief.md) and the research reports in
[`research/`](research/): five independent expert opinions, a devil's-advocate audit of the
prototype, and literature on learning science, AI methods and existing products.

## 0. Summary

1. **Track typed concepts with operational objectives, not atomic facts.**
   - The prototype's single-claim facts made dedup easier but taught badly. Of 37 facts the
     devil's advocate graded, 11 weren't worth this learner's time and 3 were wrong.
   - Most extracted facts were paper results that would be drilled as trivia. Each paper's
     argument was scattered across sentences that are never read together.
   - Claims now become *assertions* that seed questions, not units of mastery.
2. **The paper is the spine.**
   - Order: pose the problem → a map of the whole paper (blurry) → just-in-time teaching of
     the gaps that block each section → guided reading of the paper itself (sharp) →
     reconstructing and critiquing its argument.
   - This resolves blurry-to-sharp vs. prerequisite-first: blurry at the macro level,
     prerequisite-gated at the micro level.
3. **Diagnose before teaching.** Over-teaching an expert is a top-ranked risk in every expert
   report: first for two, closely related to the first for the others.
   Probe a few central concepts, infer conservatively and expand deeper only where he fails.
4. **Models judge, code decides.**
   - Models make small, local, evidence-backed judgments. Code owns learner state, ordering,
     scheduling and every quality gate.
   - All of it sits on an append-only evidence log where corrections are new events, never
     edits. A model never writes "user knows X".
5. **Unknowns are detected from behaviour, not self-report.**
   - Signals: where a concept comes from, whether it collides with an older meaning, and
     whether each claim is grounded.
   - Missing grounding blocks generation; it is not papered over. This applies to "standard"
     background too: the prototype's wrong facts were all standard maths.
6. **Item quality, feedback and grading are as risky as choosing what to teach.** Even the best
   model writes unusable memory prompts about a third of the time (Memory Machines). Grading
   drifts lenient. Feedback after an error is the active ingredient, not the score.
7. **Measure honestly from day one, but don't wait to be useful.**
   - Measurement: a sealed exam per paper, written from the paper alone; a semantic matcher
     for requirement recall; canaries; owner labels collected as a by-product of use.
   - The owner uses the first version on a real paper within about a week.
   - Gates are decision points with fallbacks decided in advance, not walls.

The owner was right that the app shell is easy, with one correction from every reviewer. The
reading companion and the feedback buttons are not shell: they are where the labels come from,
and without them no part of the AI can be evaluated.

## 1. Goal and how success is measured

**Goal:** minimise the learner's time to understand a target (first: a paper) at the depth he
needs, and keep the reusable parts.

**Outcome measures:**

- **Sealed exam per paper.**
  - Written *from the paper text alone*: no teaching map, no practice items, and a different model
    family from the one that writes the map and explanations.
  - About 10–15 questions an expert colleague would ask after a reading group: what problem,
    why the method works, what would break it, when to use it instead of X, how to apply it to
    your project.
  - Keys, rubric and pass rule are frozen with it, along with the test conditions (closed
    book, or source open, and that condition is logged).
  - Validated by the owner on papers he already knows before it is trusted.
  - Pretesting is itself an intervention, so the pre-test uses a separate small subset. The
    delayed test (2–4 weeks) uses *unseen, matched transfer* questions. Exposed questions are
    reported separately.
- **Before/after free-write** (the research mentor's test, ~10 min): a 3-sentence summary, the
  main claim and its evidence, the biggest weakness, and one extension with a predicted
  outcome. Compare with a reference: OpenReview reviews, a later critique, or a strong model
  given paper plus reviews.
- **Time to competence**, counting all of the learner's minutes, including triage, tests and
  disputes.
- **Compounding:** later papers in an area need fewer lessons per unit of exam score.

**The bar to beat:** reading the paper with a Claude chat open. Phase 1–3 runs are usability and
feasibility pilots, not proof of superiority. Comparative claims need the block design in §6.

## 2. Where best practice overrides the brief

| Brief said | Change | Why |
|---|---|---|
| Order by generality, foundations first | Order by **goal need × P(gap) × unlock value**. Generality decides what to *retain*, not what to teach first | For an expert, foundations are what he knows (expertise reversal; teaching at the "fringe" in ITS) |
| Effort level chosen on demand | User picks **time budget and context**. System recommends the activity and says why. User can override | Learners reliably pick the least effective strategy (Karpicke 2009; Kornell & Bjork 2008) |
| No-effort tier (read/listen) | Keep it as **exposure, never as evidence or review** | Retrieval practice beats restudy for retention (g≈0.6) |
| Keep knowledge over time | **Value-weighted retention.** Maintain reusable concepts and each paper's one-line claim and key figure. Let paper-local detail decay | Review debt is a widely reported reason SRS users quit (anecdotal; no public quit statistics), and relearning is cheap |
| Varied recall | Keep, with controls: vary *within* an objective, keep one stable anchor item per objective for scheduling | Unconstrained variation breaks the memory model and grading |
| Flag what the model doesn't know | Keep, but detect it **structurally** (§4.6), and require grounding for central claims even when "standard" | Self-reported confidence is poorly calibrated. The prototype's errors were in standard maths |
| ADEPT for explanations | Use as a checklist. The **example the learner works through** is mandatory. Analogies state where they break. Near his expertise, lead with the problem or the technical statement | Only the worked example is an active ingredient. Analogies can slow experts |

## 3. What happens to the prototype

**Keep:** the OpenRouter client and cost logging; paper loading; profile-conditioned extraction
from the full paper; the "read it without the paper" test (plus grounding); embedding + keyword
retrieval followed by a model decision for dedup; per-source provenance and merge logs;
side-by-side model comparison.

**Retire:** atomic facts as the tracked unit; untyped "prerequisite" edges; per-fact mastery;
clusters as the knowledge map.

**The current pool:** read-only legacy input. Useful facts can be imported as *unverified
assertions* with legacy IDs. Old edges and background claims must not be promoted to trusted
status.

**Known prototype issues to fix:**
- Missing model judgments default to "keep" or "new"; they must fail closed.
- Logging commits on the same connection as graph mutations.
- The merge step doesn't dedupe within a new batch.
- Split facts inherited all parent edges.
- There are no cross-paper links between the misalignment and SAE papers. The wiki was
  corrected.

## 4. Design

### 4.1 Core model (shared across domains)

The reviewers found that "concept", "depth", "facet" and "item" were conflated. They are
separated as follows:

| Entity | What it is |
|---|---|
| **Concept** (with revisions) | A stable meaning and scope ("the PBRF", "LoRA", "emergent misalignment as Betley et al. define it"). Has a type, aliases and a definition grounded in assertions. Stable ID; never deleted, only merged, split or deprecated through explicit events |
| **Objective** | A concept × an operational capability (recognize / explain / apply / choose-between / critique / extend), plus an optional domain facet and conditions, each with a success criterion. Levels are *not* assumed to form a universal ladder; any implication between levels is explicit and conservative |
| **Requirement** | A goal's need for an objective. Records the spans and claims it serves, necessity, centrality, review status and the extraction candidates it came from. Kept separate: learner gap, current delivery mode (teach / gloss / ignore, chosen after diagnosis) and retention policy |
| **Assertion** | A claim with a kind: `paper_claim`, `reported_observation`, `derivation`, `external_background` or `hypothesis`. Carries assumptions and evidence links of a stated relation: quoted, paraphrased, derived, illustrative, analogy. The prototype's "facts" survive here, as seeds |
| **Item version** | An immutable assessment: stem, allowed resources, response modality, answer budget, a versioned rubric of 1–4 key points each tagged to objectives, misconception rules, the assertions it is grounded in, and validation artifacts |
| **Event** | Append-only. Attempts, grades, disputes, triage clicks, stuck points, exposures, graph changes. Corrections and re-attributions are *new* events that supersede old ones |

**Concept types:** term, mechanism, procedure, contrast (choosing between methods, a first-class
type), claim, misconception, and **argument**. An argument is a paper's chain of problem →
idea → method → evidence → conclusion, practised as a whole.

**Learner state (derived; never written by a model):**
- Kept per objective, with acquisition evidence and memory evidence held separately.
- Starts simple and conservative: fixed difficulty tiers, explicit known / uncertain / gap
  states, and FSRS only on stable anchor items, fed only by unassisted, resource-appropriate
  attempts.
- Application performance is stored separately.
- Implicit "encompasses" credit (Math Academy's FIRe) runs **in shadow only**, as logged
  predictions compared with a no-propagation baseline, until it proves it helps.
- Replay comes in two views, both pinned to versions: *as-observed* and
  *current-attribution*.
  - After a split, old evidence goes to children only through reviewed mappings.
  - Ambiguous evidence stays on the retired parent, or is marked low-confidence.

**Credit and blame:** a failure is charged only to the objective a constrained diagnosis names.
Allowed outcomes:
- one of the tagged objectives or their direct prerequisites,
- `slip`,
- `item_defect`,
- `alternative_valid`,
- `undetermined`.

Uncertain diagnoses trigger a follow-up probe, not a penalty. Unresolved or disputed grades
create no strong state updates.

The core is domain-agnostic. Ingestion, item types and rubrics are per-domain plugins. The
language requirements are in §4.8, as a design checklist only.

### 4.2 Paper pipeline: what does this paper require?

The pipeline is a small DAG of persisted stages. Each stage records immutable inputs and hashes,
bounded retries, explicit failed/partial states and idempotent application. Models never mutate
the store directly.

0. **Source contract** (code):
   - Each document revision gets explicit version and content-hash identity.
   - The text is split into addressable spans with a reversible location map.
   - Inventories of equations, algorithm blocks, tables, figures and captions.
   - Citations, with resolution confidence and `unresolved` / `ambiguous` outcomes.
   - Parse-coverage warnings are visible.

   PDF is acceptable at first with honest warnings. Bounded LaTeX support comes next. Extracted
   archives get no shell escape and no code execution. Paper, repository and citation text is
   **untrusted data**, delimited in prompts.
1. **Map** (Opus-class, grounded): the problem and why the obvious approach fails; the **1–3
   load-bearing claims**, each with its evidence (figure, table, ablation); the method in a
   paragraph; weaknesses. The paper's place in its literature comes only from a bounded,
   dated retrieval task, and says when it found nothing.
2. **Requirement extraction**, as complementary passes, each namespaced `(run, pass, local_id)`,
   with all raw outputs kept:
   - **Reader pass:** done *directly from the paper*, not the map, so map errors don't
     propagate.
   - **Claim/evidence pass:** what a reader needs to follow each load-bearing claim's
     evidence.
   - **Mechanical sweep:** code enumerates every equation, algorithm, table and *measurement
     or protocol*, and the model names what each needs. This catches what the prototype
     missed: the LLM judge and its thresholds, LoRA and rank-1 adapters.

   Each candidate carries sense, required capability, served spans, quotes, necessity,
   centrality, origin hints and an explicit `uncertain`. Known-but-required concepts are kept;
   the profile prunes *teaching* later, not requirements. Before committing to an ensemble,
   ablate it: is a strong single call as good as several passes across model families?
3. **Reconciliation** within the new batch, then **resolution** against the registry. A model
   proposes; code validates and applies approved decisions with undo.
   - Directional relations: same, broader, narrower, overlaps, homonym, related, new,
     uncertain.
   - Retrieval recall is measured separately from adjudication accuracy.
   - Borderline merges need owner approval. False merges are worse than duplicates.
4. **Provenance**, recorded as separate dimensions (§4.6).
5. **Ordering hints:** soft ordering by default. A **hard** prerequisite is recorded only with a
   concrete blocked task ("you can't follow eq. 4 without knowing X at explain level"), over
   objectives rather than concepts, allows alternative routes, and the user can override it.
   "Results support claims" never becomes an ordering edge.
6. **Delivery** (code, after diagnosis): teach / gloss inline / ignore. Ignored requirements stay
   listed in an "ignored" report. The queue shown to the user is capped (top ~5), not the stored
   extraction.
7. **Sealed exam** (separate, from the paper only, §1).

### 4.3 What does this learner lack?

Diagnosis is short and has its own budget: about 10 minutes per paper by default. That is
roughly 10–15 one-tap triage clicks plus 5–8 probes.

- **Priors:** the profile (with an editable **active projects** section); the owner's own papers
  and code; concepts already in the store.
- **Triage** of only the ~10–15 most central candidates: *know it / heard of it / don't know /
  irrelevant*. This is not the full list; the research mentor warns against 50-item checklists.
  Peripheral candidates go to self-report silently, or to on-demand glosses.
- **5–8 discriminating probes** on the central objectives. Self-reported "know it" on a central
  objective earns **one** verifying probe. Software engineers over-claim maths definitions and
  under-claim things they've used in code; Math Academy finds learners overestimate their
  knowledge.
- **Conservative inference:** a passed probe gives weak "known" evidence only for objectives
  the item's key points *necessarily* exercise. No transitive-closure mastery. The metric is
  spot-checked false-known rate, not the fraction of candidates removed.
- Pretests help later learning only **with feedback**, so every probe gets brief feedback.

### 4.4 The session

1. **Problem first:** "Here's the problem this paper solves. How would you approach it? What
   goes wrong with the obvious approach?" One or two minutes, skippable. This draws on
   Schwartz & Bransford and productive failure, and also counters the false sense of
   understanding a fluent map creates.
2. **The map:** gist, the load-bearing claims and the key figure. Audio optional.
3. **For the next section:** teach the 1–3 gaps blocking it.
   - A short grounded explanation, then one question that requires using it, with feedback.
   - Teach a new concept **by contrast with its known neighbour** (EK-FAC vs. K-FAC; TopK vs.
     L1 SAEs), since many papers' contribution *is* a contrast. Comparing cases has d≈0.5.
   - At most 2–3 new concepts per session. Don't introduce two *new* confusable concepts in one
     session.
4. **Guided reading of that section:**
   - **Glosses** for paper-local notation, answered directly.
   - **"Ask about this paragraph"**: direct answers for definitions and notation. On *core*
     concepts it gives a hint first and asks him to try, with a visible "just tell me" button.
     This follows Bastani et al.: unguarded help cut later unaided performance by 17%, and a
     hint-first tutor avoided that.
   - **Self-explanation prompts** at each core equation ("in your own words, what is this
     term doing?").
   - **"I got stuck here"** and **"already knew"** buttons. Every question and stuck point is
     logged as gap evidence and as a recall label for extraction.
5. **After each section:** one or two adjunct questions on the paper.
6. **After the paper:**
   - Reconstruct the argument: he states the chain, and it is compared with the map.
   - Critique: "what's the weakest link? what control would you add?"
   - Choose / predict / diagnose items on core objectives.
   - One **project-grounded** question about his active projects.
   - An optional homework item.
7. **A follow-up session 1–3 days later:** retrieval on the core plus one transfer question.
   This is the second, sharpening pass.
8. **Stopping rule:** separate from the exam. The goal moves to gist-retention mode after the
   follow-up session, when the owner marks the paper done or after a period of inactivity.

**Feedback ladder after a wrong answer:**
1. Explain the key point he missed, citing the source.
2. Retry later with a new variant.
3. If it fails again, probe the diagnosed prerequisite.
4. If that still doesn't resolve it, flag the item or concept for the owner.

**Format follows the objective's state:**

| State | Format |
|---|---|
| New gap | Explanation plus one question |
| Consolidating | Explain-why / apply items |
| Discrimination | Choose-between items |
| Procedure he wants to extend | Worked example, then homework |

At most ~20% of a paper's items are definitional.

**Effort:** he sets time and context. The planner recommends the activity, with a "why am I
seeing this?" line showing the goal, the passage and the score components. **Agency:** pin, drop,
or skip with a quick check; reorder the queue; edit the active projects. Matuschak's main lesson
from the mnemonic medium was that readers need control.

### 4.5 Teaching artifacts

**Explanations.**
- Validated claim by claim. Each claim states its relation to the evidence: quoted or
  paraphrased (with a span), derived (with its premises, plus an executable check for signs
  and equations where possible), an illustrative assumption, or a bounded analogy.
- Central background claims must be grounded in an authoritative fetched source too, not just
  model memory.
- Each section keeps a local notation map.
- Content rules: the worked example is mandatory, and code or a tiny numeric example is often
  the best "diagram" for this user. Analogies are labelled and say where they break. Brevity
  budget is a phone screen. Each ends with something to do.

**Items.**
- Pipeline:
  1. A spec: objective, allowed resources, assumptions, difficulty tier and answer budget.
  2. Generate the item together with its versioned rubric.
  3. Independently check each key point: is it correct, necessary, and what equivalent answers
     are allowed.
  4. Blind solvers, who see neither the key nor each other's work, check that the key is
     correct.
  5. An adversarial search for alternative valid answers.
  6. A direct **surface-leakage** check (does the stem state or paraphrase the key points?)
     and counterfactual variants (change the setup so the answer changes).
  7. Code gate.
- The rejected version of this pipeline asked a model to "pretend not to know", which doesn't
  work because models can't forget.
- Choose / apply / extend items get an acceptable-answer *space*, not a single string.
- Ground generation in owner-labelled examples of good and bad items. In Memory Machines,
  graded examples from the same passage raised precision from 56% to 78%.
- Log every rejected candidate. Owner audits a sample of *accepted* items.

**Grading.** Four separate steps:
1. Evaluate each key point semantically. Quotes are validated as exact offsets, but a valid
   quote doesn't prove correctness.
2. A global check for contradictions and misconceptions in context. Quoting a misconception in
   order to refute it is fine.
3. An optional constrained diagnosis.
4. A deterministic evidence update.

Other rules:
- Anchors: terse but correct answers get full credit.
- The grader comes from a different family from the generator, and role assignments are
  tested empirically.
- Aggregation and abstention rules are explicit. "Needs human" stays queued until reviewed.
- One-click dispute appends a superseding event.

### 4.6 Unknowns and very new papers

Provenance is several dimensions, not one badge:

- **Origin**, per occurrence: introduced in this paper, from a citation, external background.
- **Sense-collision status:**
  - A closed-book definition is compared with one grounded in the paper and citation.
  - A mismatch *escalates* to the owner or to grounding. A match never certifies the
    definition, because shared errors exist.
  - Ask "does X exist?" before asking for a definition, because presupposing it exists
    increases fabrication (PhantomBench).
- **Grounding status**, per assertion or artifact: supported, contradicted, not enough
  evidence, not applicable.
- **Model familiarity**, per model and probe. This is a weak signal. A missing cutoff date
  means `unknown`, never a guess.

Generation rule: no explanation or item about a central objective passes unless its claims are
grounded. "Standard" earns no exemption for central claims. Unsupported items show what the
paper says and suggest "read [ref 23] first".

**Canaries:** invented methods with familiar-sounding names, altered signs or conditions,
missing definitions, unresolved citations, and unchanged standard controls, with fresh
variants each run. Report counts with confidence bounds. Zero errors in 30 independent cases
still allows roughly a 10% error rate at 95% confidence, so a small suite is a smoke test, not
a guarantee.

### 4.7 Maintenance (later)

- FSRS runs on anchor items, with target retention set by goal value:

  | Concept | Target retention |
  |---|---|
  | Active goal needs it soon | ~0.9 |
  | Reusable, still in use | ~0.8 |
  | Paper-local, goal finished | Recognition, or stop |

- A hard daily budget; when it overflows, auto-postpone by value (SuperMemo).
- Goal weight decays without engagement unless pinned. Ask once: keep / archive / keep only the
  general ideas.

### 4.8 Keeping language learning possible (design checklist, not built now)

- Planning must work with **no** prerequisite edges, using frequency and coverage, with no LLM
  call per item, at 10⁴–10⁵ items.
- Objectives carry facets (read / listen / speak / write), and latency is recorded on every
  attempt.
- Evidence comes in kinds: exposure, self-report, test.
- Probability-known generalizes to untested items through a learner-level ability over item
  features.
- Coverage goals with deadlines (e.g. "98% of this show's words").
- Teach / gloss / ignore is a planner output. Vocabulary is a concept type.
- One prompt can test a target and give weak credit to context items.
- `confusable_with` affects when new items are introduced.
- Evidence can point to a source location, such as an episode timestamp.
- The profile has a domain-specific section (L1, target variety).

## 5. Agents and rubrics

Rubrics use binary or small-ordinal criteria, each checkable with the cited evidence. They are
**diagnostic instruments, not proof**. Report for each:
- confusion matrices, κ with class counts and uncertainty;
- defect sensitivity *and* clean-control pass rate (a judge that rejects everything catches
  every defect);
- consequential errors: false full credit, false-known inference, false merge, false approval
  of wrong content.

Validate only rubrics that **gate a decision or touch the learner**. Labels for the rest come
from use. Blind judges to which system produced the output. Pin model and prompt versions.

| Decision | Made by | Rubric essentials |
|---|---|---|
| Map | Opus-class | Names 1–3 load-bearing claims, each with its specific evidence. Problem and why the obvious approach fails. Every statement span-linked. Fair to the authors (hypotheses marked as such) |
| Requirement | Complementary passes | Grounded in a span. **Necessary**: names the step that would be misunderstood without it. Capability and depth match the paper's use. Granularity matches anchors. Centrality |
| Requirement set | Matcher + owner | Semantic coverage of gold and stuck points (Appendix B of the AI-systems review): fully covered only if all required elements are covered at the right depth and sense; several narrow predictions can jointly cover one; broad names get no blanket credit. Macro per paper; core misses listed |
| Resolution | Model proposes, code applies | Directional relation, with abstention. Merge only if scope and objectives are compatible with the whole destination concept |
| Hard prerequisite | Proposer + reviewer | A concrete blocked task, over objectives, with alternatives allowed |
| Explanation | Generator + grounding judge | Each claim supported under its stated relation. Targeted at the gap. Doesn't re-explain known things. Uses the paper's notation. Worked example. Bounded analogy. Brief. Analogy quality judged by the owner, pairwise |
| Item | Pipeline (§4.5) | Key correct and complete. Acceptable-answer space defined. No surface leakage. Targets its objective. Fits the answer budget |
| Grade | Four-step grader | Each key point evaluated in context. Contradiction check. Terse-correct anchors. Abstains when unsure |
| Feedback | Generator + judge | Names the missed key point, cites the source, gives no new unsupported claims, ends with a retry or next step |
| Companion on core concepts | Policy + test set | Hint first unless he asks to be told; tested on a fixed set of ~10 "just give me the answer" prompts (MRBench-style) |
| Exam | Separate pipeline | Covers core claims, assumptions, evaluation and one new application. Keys validated. Owner-checked on familiar papers |

## 6. Evaluation

**Owner labels, cheapest first:**
- **Triage clicks on the four papers already ingested** (Phase 1a). About 45 minutes on the
  combined candidate list from the new extractor and the reading-guide baseline, shown blind
  and in random order. This reuses the devil's advocate's 37 graded facts as seed labels.
- **Stuck points from his natural reading** in the companion.
- **2 familiar papers** annotated as capability-level gold entries (Phase 0, ~20 min each),
  using the format in the AI-systems review's Appendix B. To save his time, a model drafts the
  entries and he corrects them. This is the small, locked acceptance set.
- **Disputes and "bad question" clicks.** These are biased toward visible errors, so they are
  supplemented by a recurring random audit of *accepted* outputs, which catches confident
  errors that every judge agreed on.

**Owner time budget:**

| Phase | Owner time |
|---|---|
| Phase 0 | ~1 h: gold for 2 familiar papers (~40 min), exam validation (~20 min) |
| Phase 1a | ~45 min triage of the four ingested papers, plus the first live paper |
| Each live paper, early phases | ~30–45 min beyond reading: pre-test, two short free-writes, post-test, diagnosis. Shrinks once measurement stabilizes |
| Audits | ~15 min a week |

Every label request is counted against these budgets.

**Datasets:** split by paper before any tuning.
- **Dev:** the four ingested papers.
- **Locked acceptance:** the 2 gold familiar papers, plus 2 canary papers.
- **Prospective:** every live paper. Source,
parser, registry and learner snapshots are frozen for comparisons, so a warm concept store
doesn't advantage only the new system.

**Metrics:**
- Pipeline:
  - requirement coverage (macro, core misses), precision on adjudicated predictions;
  - stuck-point coverage, tracked separately (stuck points are observed needs, not a complete
    list);
  - canary results with denominators;
  - retrieval recall@k and adjudication accuracy, separately;
  - false-merge count;
  - accepted-item defect rate;
  - grader false-full-credit rate.
- Learner and outcome: the sealed exam and free-write, time to competence, calibration of
  confidence (logged with each answer) and process alarms.
- **Alarms, not gates:**

  | Alarm | Threshold |
  |---|---|
  | "Already knew" rate | > 30% |
  | First-try accuracy on new material | outside 70–85% |
  | Disputes | > 5% |
  | Daily review minutes | rising week over week |
  | Paper time vs. module time | too little time in the paper |

**Causal checks (n=1):**
- **Pre-teach vs. on-demand:** for randomly chosen gap bundles, skip pre-teaching and rely on
  glosses and the "ask" box. Record incidental exposure and analyze by assignment. This answers
  a useful product question, and is honest about the fact that withheld concepts still leak in
  through other channels.
- **Tool vs. chat**, later, in matched paper blocks with randomized (ABBA) order and
  differences decided in advance. Tool papers must improve faster than chat papers; a faster
  third paper alone proves nothing.
- Pre-answer predictions are logged so learner models can be compared chronologically by log
  loss.

**Logs:**
- Every model call as an artifact: inputs, outputs, prompt and schema hashes, requested and
  served model, retries, cost. Logged outside graph-mutation transactions.
- Every planner decision with its score components; every event; every graph change with its
  undo.
- Logs stay local. Be explicit about what private material goes to which provider.

## 7. Top risks

| # | Risk | Early warning | Main mitigation |
|---|---|---|---|
| 1 | Over-teaching an expert | "Already knew" > 30%; first-try > 85%; he reads the paper directly | Short diagnosis; top-5 queue; paper as spine; glosses instead of lessons |
| 2 | Confident errors, including in "standard" maths | Ungrounded claims; definitions differ across runs; canary failures; owner corrections | Grounding required for central claims; collision escalation; executable sign checks; random audits |
| 3 | Illusion of learning | Practice > 90% while the exam or free-write lags | Sealed independent exam; strict grader; hint-first companion on core concepts; aim for 70–85% first-try |
| 4 | Bad items or grades destroy trust | Disputes; clean-control failures; grades correlate with length | Item pipeline; feedback ladder; disputes; accepted-output audits |
| 5 | Teaching what's easy to define, not what matters | > 50% definitional items; no argument or critique practice | Requirements tied to claims; argument as a concept type; item-type quotas |
| 6 | False measurement (matcher, exam, holdouts) | Scores move without content changing | Validated matcher; exam from paper only; locked acceptance set; honest estimands |
| 7 | False merges or wrong attribution corrupt state | Mastery jumps after a graph change | Conservative resolution; owner-approved merges; reviewed split mappings; two replay views |
| 8 | Errors compound across stages | Stuck points that map to nothing | Per-stage loss accounting; complementary passes; companion signal |
| 9 | Review debt | Due count rising | Value-weighted retention; budget; decay |
| 10 | The tool replaces reading the paper | PDF never opened | Guided reading is the main activity; activities point into the paper |
| 11 | Untrusted source text steers the pipeline | Injected-document fixtures fail | Data delimiting; no mutation rights in model calls; no code execution |

## 8. Phases

Each phase ends at a **decision point with a fallback decided in advance**. Thresholds are
provisional smoke tests, reported with uncertainty.

**Phase 0: foundations and measurement (days 1–3; owner ~1 h)**
- Build:
  - the new database and artifact records (Appendix);
  - the source/span contract (PDF with coverage warnings);
  - the semantic matcher, validated on a small synonym / sense / decomposition challenge set;
  - 2 canary papers;
  - the one-shot reading-guide baseline, plus a normalizer that turns the guide into
    requirement records so both systems are scored the same way;
  - the exam generator.
- Owner: correct model-drafted gold for 2 familiar papers, and validate their sealed exams.
- Decision: the gold, the guide baseline and the canaries can be scored from saved artifacts,
  and every match is inspectable.
- **Fallback:** if the matcher can't be validated, score by owner review of the match tables
  for the acceptance papers only.

**Phase 1a: requirements + reading companion on a real paper (end of week 1)**
- Build:
  - map, complementary extraction passes, reconciliation, grounding states;
  - delivery dispositions with a top-5 queue;
  - companion v0: section text, glosses, the "ask" box (hint-first on core concepts),
    self-explanation prompts at core equations, stuck / already-knew / bad buttons, event log;
  - a minimal web UI with no learner model yet: FastAPI + SQLite, like the owner's
    chess-pretraining-for-humans repo, but with a component-based frontend.
- Owner: the next paper he wants to read anyway. Sealed pre-test and free-write first, then
  read with the companion, then the post-test.
- Decision:
  - On the acceptance papers and stuck points, does the requirements engine beat the one-shot
    reading guide by more than run-to-run variance?
  - Provisional smoke checks: macro recall ≥ 0.8, adjudicated precision ≥ 0.5, no accepted
    ungrounded central assertions on canaries.
  - **Fallback:** if it doesn't beat the guide, the guide becomes the per-paper core and the
    concept store is kept only for cross-paper reuse.

**Phase 1b: safe cross-paper reuse**
- Build: conservative resolution across 2–3 related papers (including the next real paper),
  many-to-many provenance, undo, and ordering-sensitivity tests.
- Decision: owner-reviewed merges with no unexplained evidence loss. False merges and duplicates
  are reported.
- **Fallback:** if resolution is unreliable, keep per-paper requirement sets and link concepts
  only by owner approval.

**Phase 2: diagnosis, explanations, items, feedback (weeks 2–3)**
- Build:
  - triage of the central candidates plus 5–8 probes;
  - just-in-time explanations with one item each;
  - the item pipeline and the four-step grader;
  - the feedback ladder, disputes;
  - the pre-teach vs. on-demand assignment;
  - the post-paper argument / critique / project questions;
  - the 1–3 day follow-up.
- Decision:
  - accepted-item defect rate < 10% on an owner-audited sample;
  - grader κ ≥ 0.6 with false-full-credit reported;
  - false-known audit of diagnosis;
  - alarms quiet.
- **Fallback:** if items or grading fail, fall back to owner-approved items and self-grading with
  key points shown, and keep improving the pipeline offline.

**Phase 3: live use over 3–5 papers, hardening**
- Harden the components that disputes and audits show are weakest. Start the first matched
  tool-vs-chat block.
- Decision: a usability and feasibility read on overhead, errors, and whether exam scores reach
  a floor of ≥ 70% on core questions after reading. No superiority claim yet.
- **Fallback:** if overhead swamps the benefit (the owner would rather read with chat), cut to
  map + companion + glosses only, and re-test.

**Phase 4: retention and multiple goals**
- Anchor-based FSRS, budgets, goal decay. Implicit credit stays in shadow mode.
- Operational exit: bounded queue, tested archival, reproducible replay.
- **Fallback:** if delayed retention doesn't beat no-review on the holdout, keep only the
  per-paper one-line claims and reusable concepts in review.
- Evidence checkpoint: delayed performance and calibration against a no-implicit-credit
  baseline.

**Later:** audio exposure, spoken answers, code-verified homework, a language pilot, learned
models fitted on the log.

**Deferred on purpose:** global hard-prerequisite graphs, automatic concept splits,
`encompasses` memory credit, learned item difficulty, graph visualisation, and the
domain-plugin framework.

## 9. Decisions for the owner

1. **Next paper:** which paper does he want to read next? It becomes the first live test in
   Phase 1a.
2. **Two or three familiar papers** for the locked acceptance set and exam validation.
3. **Cross-family roles:** use GPT and Gemini via OpenRouter as judges and graders for Claude
   output, and vice versa. Recommended.
4. **Privacy:** may unpublished drafts or private code be sent to these providers when he adds
   his own work to the profile?
5. **Rework in place:** keep the repo and infrastructure, and treat the old pool as read-only
   legacy. Recommended.

## Appendix: the Phase 0/1a build contract

- **Storage:**
  - A new SQLite file, `data/frontier.db`, with explicit schema migrations.
  - Tables follow the AI-systems review's Appendix A: Source, DocumentRevision, Span,
    Assertion, Concept and ConceptRevision, Objective, Requirement, ResolutionDecision,
    PrerequisiteRule, Artifact.
  - ItemVersion and Event tables are added before the first probe.
  - The old `data/pool.db` stays read-only.
  - `cluster.py`, `review.py` and the fact logic in `merge.py` stay in the repo for comparison,
    but new code doesn't depend on them.
- **Artifacts:** every model call writes `data/artifacts/<stage>/<artifact_id>.json` (the
  Artifact fields) before any database change.
- **Model roles (pinned; changing them triggers a re-run of the acceptance set):**

  | Role | Model |
  |---|---|
  | Map, reader pass, explanations | `anthropic/claude-opus-5.5` |
  | Claim/evidence pass, mechanical sweep, reconciliation | `anthropic/claude-sonnet-5.5` |
  | Second-family extraction pass, exam generation, judges, graders | `openai/gpt-6.1-sol` |
  | Third-family tie-breaks | `google/gemini-3.8-flash`, or a Gemini Pro-class model if one is available |
  | Embeddings | `voyageai/voyage-4` |

  Training cutoffs are recorded per model from provider documentation, or `unknown`.
- **Canaries:** 2 short model-written papers, owner-checked. Each has 3 invented methods with
  familiar-sounding names, one altered sign or condition in a standard result, one undefined
  term and one unresolvable citation, plus standard controls. Add one real post-cutoff paper
  when one is available.
- **Granularity anchors:** seeded from the devil's-advocate grades (its A-grade and F-grade
  examples) and the research mentor's good/bad item examples. Refined from triage labels.
- **CLI:**
  - `frontier ingest <pdf|arxiv-id>`
  - `frontier map <paper>`
  - `frontier extract <paper>`
  - `frontier guide <paper>` (baseline)
  - `frontier exam <paper>`
  - `frontier score <paper>`: requirement coverage vs. gold, stuck points and guide
  - `frontier canary`
  - `frontier serve`: a FastAPI app on the owner's machine, reachable over Tailscale, serving
    the triage page in Phase 0/1a, then the companion.
- **Reports:** a per-paper HTML report (map, requirements with spans and provenance, match
  tables against gold and the guide) written to `reports/`.
