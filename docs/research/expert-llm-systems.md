# Expert opinion: LLM systems design for an adaptive "learn what you need for this paper" tool

Perspective: I build and evaluate multi-step LLM pipelines in production (extraction, grading,
generation, judge models, eval sets, prompt regression testing). I read only the brief and its
ADEPT appendix. Opinions are deliberately strong; where I'm guessing I say so.

The thesis up front: **the models should make many small, local, checkable judgments with
evidence attached, and deterministic code should own all the state and every aggregate decision.**
The failure mode to design against is not "the model is dumb". It is "the model is fluent,
confident, and wrong, and nothing downstream can tell". Most of the architecture below exists so
that every model output is either checked by something independent or tied to text the owner
can click on.

---

## 1. Architecture: who decides what

### 1.1 Core data model (deterministic, owned by code)

Four kinds of things, all stored by code and never rewritten free-form by a model:

1. **Sources**: the paper (prefer the arXiv LaTeX source over the PDF, since it gives you
   `\newcommand` macros, `\begin{definition}`, section structure and a clean bibliography),
   cited papers, linked code repositories, and web pages. Each is split into addressable spans
   with stable IDs.
2. **Concepts**: a global, deduplicated store. Each concept has a canonical ID, aliases, a short
   grounded definition, **provenance** (which spans define or use it), a **knowledge-status**
   (see §3), and typed edges to other concepts (`requires`, `is-a/specializes`,
   `contrasts-with`, `used-in`). Concepts are shared across goals. That is what lets knowledge
   carry over from one paper to the next.
3. **Goals and requirements**: a goal is a paper, project or trip. A *requirement* links goal to
   concept and carries: the required **depth** (recognize / explain / apply / extend or modify),
   **centrality** to the goal (is it core to the contribution, used in the method, used only in
   experiments, or mentioned in passing), the paper spans that justify it, and a status
   (candidate, confirmed, dismissed by user, satisfied).
4. **Learner evidence**: an append-only log of observations. Examples: "self-rated *know* on
   concept C at time t", "answered item I, grader gave 2/3 key points, user disputed",
   "highlighted span S as confusing", "marked explanation E as *already knew*". **Mastery is a
   function computed by code from this log.** It is never a model's free-text opinion of the user.

The concept-plus-requirement split matters. "What the paper needs" and "what the user lacks"
are different questions, answered by different processes, and joined by code.

### 1.2 Pipeline stages and which component owns each decision

| # | Stage | Decided by | Reads | Writes |
|---|---|---|---|---|
| 0 | Ingest: fetch LaTeX or PDF, parse, split into spans, resolve bibliography to arXiv/Semantic Scholar IDs, pull cited abstracts, find code repo | **Code** (plus a model only as a fallback for messy bibliography entries) | URL | Sources, spans |
| 1 | Paper map: one-paragraph gist, main contribution, method skeleton, "what you'd need to extend this" | Model (Opus-class), grounded in spans | Paper spans | Paper map (shown to the user first; see blurry-to-sharp in §6) |
| 2 | Requirement extraction: concepts the paper *uses*, each with depth, centrality and spans | Model, **run several times across 2–3 model families**, results unioned | Paper spans, paper map | Candidate requirements |
| 3 | Concept resolution: match candidates to existing global concepts, or create new ones | Embedding retrieval (**code**) proposes matches; a model adjudicates merge/new/specializes; **code** applies the result, with an undo log | Candidates, concept store | Concepts, aliases, edges |
| 4 | Knowledge-status / novelty: is this standard, from a cited paper, introduced here, or unknown to the model? | Mix: **code** (citation dates vs. model cutoff, "defined in this paper" span detection) plus a model closed-book probe (§3) | Concepts, sources | Knowledge-status, grounding requirements |
| 5 | Prerequisite edges: does understanding A at depth d require B? | Model, local pairwise judgments only, never "draw me the whole graph" | Concept pairs proposed by code | Edges with confidence |
| 6 | Learner diagnosis | **Code** chooses what to probe. User self-ratings plus a few model-generated diagnostic items. **Code** updates beliefs, propagating along edges | Requirements, graph, evidence log | Evidence |
| 7 | What next (ordering) | **Code**: a scoring function over the graph (below) | Graph, requirements, mastery, user-chosen effort level | Queue |
| 8 | Explanation generation | Model (ADEPT-shaped template), grounded, with citations to spans | Concept, grounding spans, learner's known concepts | Explanation artifact (cached, versioned) |
| 9 | Item generation (flashcards, application questions, homework) | Model generator → **independent model checker** → **code** gate | Concept, explanation, item spec | Item bank |
| 10 | Grading | Model grader against the item's key-point rubric; **code** turns key-point credit into a score | Item, key, user answer | Evidence |
| 11 | Scheduling | **Code** (FSRS or similar) | Evidence | Due dates |
| 12 | Reading companion: the user reads the actual paper in-app and highlights confusing spans | UI and code; a model answers in context and maps the confusion back to concepts | Spans, concepts | Evidence and **missed-requirement signals** |

### 1.3 Where code must own the decision

- **Ordering and "what next".** Have the model supply local facts (edges, centrality, depth).
  Code computes priority. A reasonable starting score is
  `priority = centrality × P(not known at required depth) × unlock_value`, subject to the
  constraint that all `requires` prerequisites must be above the mastery threshold or included
  first. `unlock_value` is how many other unmet requirements this concept is a prerequisite for,
  which is what "generality" should mean operationally. Code is reproducible, debuggable and
  tunable. "Ask Opus what to teach next" is none of those, and it will drift between runs.
- **Mastery and memory state.** A model grades one answer. Code aggregates answers. Never let a
  model write "user understands X" into state.
- **Scheduling.** Use FSRS. Don't invent your own, and don't let a model schedule.
- **Dedup and merge application, provenance, versioning, cutoff dates, citation resolution,
  budget/timeouts, retry policy.**
- **Gates.** "Item passes checker", "explanation passes faithfulness check" and
  "requirement has ≥1 supporting span" are code-enforced predicates over structured model outputs.

### 1.4 Model-call conventions

- **Structured outputs everywhere** (JSON schema / tool calls). Every claim field is paired with
  `evidence_span_ids` and an explicit `unknown`/`abstain` option. If there is nowhere to put
  "I don't know", the model will fill the field.
- **One judgment per call where feasible.** Pairwise edge judgments, per-key-point grading and
  per-item checking are more accurate, easier to evaluate and easier to cache than mega-prompts.
  Money is no object, so spend it on decomposition and redundancy.
- **Cross-family redundancy for high-stakes judgments.** Generate with one family (e.g. Claude)
  and check/judge with another (GPT or Gemini via OpenRouter). This is the cheapest available
  defence against self-preference and shared blind spots.
- **Version everything**: prompt template hash, model ID, temperature, input hashes. Cache
  outputs keyed on these so regression runs are cheap and diffs are meaningful.

---

## 2. Rubrics for each model-made decision

General rule: **binary or small-ordinal criteria, each answerable from evidence the judge can
see.** Likert "quality 1–10" scores are noise. Every rubric item should be one an outsider
could check in under a minute with the cited spans open.

### 2.1 "What does this paper require?" (requirement extraction)

Per extracted requirement:
- **Grounded**: at least one cited span actually uses the concept (code-checkable by string or
  alias match plus a model check for paraphrase).
- **Necessary**: if a reader lacked this concept, would they misunderstand a specific claim,
  equation or method step? The answer must name which one. "Helpful background" is not
  necessary, so tag it `context` rather than `requirement`.
- **Depth correct**: recognize / explain / apply / extend, judged by how the paper uses it.
  Using a KL penalty in a loss means *apply*. Citing RLHF in related work means *recognize*.
- **Granularity**: teachable in one sitting of 5–15 minutes, and not a whole field.
  "Transformers" is too coarse and "the 1/√d scaling" is too fine, unless the paper hinges on
  it. Specify this with **anchor examples**, because granularity is the thing models are least
  consistent about.
- **Centrality**: core contribution / method / experimental setup / passing mention.

Set-level rubric (the more important one):
- **Recall against the owner's list** on the gold set (§4). Recall matters more than precision
  here, because triage filters cheaply but a missed requirement is invisible.
- **Coverage of every equation and algorithm block**: code enumerates them, and for each one
  the model must list the concepts needed to read it. This mechanical sweep catches a lot of
  misses that a "read and summarize" pass skips.

### 2.2 "What does the user lack?"

Mostly not a model rubric. It is a measurement problem (§1.3). The model-made pieces are:
- **Diagnostic items**: does the item discriminate? A user who knows the concept at the required
  depth should pass it, and one who knows only the name should fail it. Validate by having a
  model answer with *only the name and a one-line gloss* in context. If that model passes, the
  item tests recognition, not understanding.
- **Propagation edges**: a `requires` edge should satisfy "a competent explanation of A
  necessarily invokes B". Have the judge look for B in a reference explanation of A.

### 2.3 Ordering

Code owns ordering, so the rubric is on its *output*, judged pairwise by the owner (and by a
model only after calibration):
- No item appears before a hard prerequisite.
- The first five items are the ones the owner would most regret skipping before reading section 3.
- No queued item is already known (measured as the rate of "already knew this").

### 2.4 Explanations

Per explanation:
- **Faithful**: every technical claim is supported by a cited span or is standard background.
  Use claim-level entailment checking by a separate model. Unsupported claims about
  post-cutoff concepts are automatic failures.
- **Targeted**: it explains the concept *as used in this paper*, at the required depth, and it
  connects to the specific equation or step where the paper uses it.
- **Calibrated to the learner**: it doesn't re-explain concepts marked known, and it does
  define concepts the learner has not yet learned. Code supplies the known/unknown list, so
  this is checkable.
- **ADEPT elements present where they fit**: an analogy that is *labelled as an analogy* with
  its breaking point stated, a concrete worked example with numbers, the plain-English version,
  then the technical version. Diagrams are optional; ask for mermaid or LaTeX/TikZ and render
  them, don't trust generated images.
- **Brevity**: under N words for the depth level, with no throat-clearing.
- **Analogy quality**: the owner judges this pairwise. A model judge cannot reliably tell a
  memorable analogy from a misleading one, and misleading analogies are what survive a year.

### 2.5 Question and item generation

Each item is generated from an **item spec**, not an open prompt: concept, depth, item type
(definition recall / apply in a new scenario / choose between methods / predict what happens if
X changes / find the bug / derive), answer-length budget, and the misconception it targets.

Rubric for the checker:
- **Answerable**: a strong model, given *only the item and the source spans*, produces an answer
  that matches the key. If it doesn't, either the item or the key is wrong.
- **Not answerable from surface cues**: a model given only the item stem and no knowledge of
  the concept should fail. This catches answers leaked in the stem.
- **Unambiguous**: two independent solvers agree.
- **Key decomposes into 1–4 gradable key points**, each objectively checkable.
- **Matches spec**: an "apply in a new scenario" item really does use a scenario not present in
  the explanation. Check n-gram and semantic overlap in code, then confirm with a model.
- **Short answer**: the expected answer fits within the length budget.

### 2.6 Grading

- Per key point: `credit ∈ {full, partial, none}`, plus the quoted span of the user's answer
  that earns it, plus a misconception tag from a small fixed list.
- Grade **for meaning, not wording**. Include anchor examples of correct-but-terse answers that
  must get full credit. Graders over-penalise brevity, and this user's answers will be terse.
- The grader can output **"needs human"** when the answer is off-key but possibly correct. Route
  these to the owner. They are the best labels you will get.
- One-click **dispute** in the UI. Disputes go to the eval set automatically.

### 2.7 Validating the rubrics themselves

A rubric is a measuring instrument, so validate it the way you validate any instrument:
1. **Owner gold labels**: ~30–50 items per rubric (§4.2), labeled before looking at the judge.
2. **Judge vs. owner agreement**: Cohen's κ per criterion. Under ~0.6, rewrite the criterion
   (it is usually ambiguous) or split it. Look at disagreements by hand. They usually reveal a
   criterion the owner applies but never wrote down.
3. **Perturbation and sensitivity tests**: take good artifacts and inject known defects (a wrong
   claim, a leaked answer, an off-target concept, a swapped equation sign). The rubric must catch
   ≥90% of them. A rubric that passes everything is worthless, and this is the commonest failure
   I see.
4. **Invariance tests**: position swaps in pairwise judgments, reformatting, and length padding
   should not change the verdict. Length bias in particular is large and well documented.
5. **Cross-judge agreement**: two model families score the same artifacts. Persistent
   disagreement on a criterion means the criterion is underspecified.
6. **Re-validate whenever the judge model changes.** Pin judge model versions.

---

## 3. Handling unknowns: flag, don't guess

### 3.1 Don't rely on self-reported confidence

Asking the model "do you know this term?" is weakly informative. Models will happily define a
plausible-sounding expansion of an unfamiliar acronym. Use **behavioral and structural
signals** instead, and combine them in code:

1. **Structural or dated signals (code)**: the concept is introduced via a citation whose
   publication date is after the generating model's training cutoff (the model's cutoff is a
   config constant per model), or within a margin before it, since coverage near the cutoff is
   thin. Also flag: the concept is defined in this paper (`\begin{definition}`, "we propose",
   "we call this"), or the name is a new coinage, meaning a capitalised acronym that does not
   appear in a reference corpus of older arXiv abstracts.
2. **Closed-book vs. open-book probe (model)**: ask model A to define the term *closed-book*.
   Separately, extract the definition *from the paper and the cited source*. A judge checks
   whether they agree. Disagreement means the model's prior is wrong or stale, so mark the
   concept `grounding-required`. Agreement on a well-known concept means `standard`.
3. **Cross-model disagreement**: different families giving materially different closed-book
   definitions is a strong "nobody actually knows" signal.
4. **Name collisions**: the same term means different things in different subfields
   ("influence", "attribution", "probe", "steering"). The open-book definition always wins for
   this paper. Store paper-specific senses as separate concepts linked by `homonym-of`.

The resulting knowledge-status is one of: `standard` (model may explain from its knowledge,
still checked), `from-citation` (must ground in the fetched cited paper), `introduced-here` (must
ground in this paper), or `unknown` (no adequate source found). **`unknown` is a first-class UI
state**: "This paper relies on *X* from [ref 23], which I could not retrieve and which is newer
than my training data. Here is everything the paper itself says about it." That is far more
useful than a confident fabrication.

### 3.2 Grounding hierarchy

For explanation and item generation, in priority order:
1. **The paper's own text**: definitions, method section, appendix, equations. LaTeX source is
   much better than PDF extraction for equations.
2. **The paper's code repo**, if linked. For a research engineer, the training loop or the
   attribution function is often the clearest definition there is. Pull the relevant file and
   cite lines.
3. **Cited papers**: resolve them via arXiv / Semantic Scholar, fetch the full text for anything
   tagged `from-citation`, and do retrieval within it. Recurse one level for central concepts.
4. **Curated web search**, as a last resort for terminology: docs, well-known blogs, and
   survey papers. Prefer surveys dated after the concept's introduction.
5. **Model prior knowledge**: allowed only for `standard` concepts, and still subject to the
   faithfulness check.

Enforce it in the output schema: every technical sentence in an explanation carries a source
tag (span ID, or `background`). A code gate rejects `background` tags on any concept that isn't
`standard`.

### 3.3 Test that flagging actually works

- **Canary concepts**: build synthetic or lightly edited papers that introduce invented methods
  with plausible names (e.g. "Gradient Echo Attribution (GEA)") and a definition that differs
  from what the name suggests. The system must flag them as `introduced-here` and explain them
  *from the text*, not from the name. Run canaries in every regression suite. Also include real
  papers published after the generator's cutoff.
- **Track the "confident wrong" rate on post-cutoff concepts as a headline metric.** It should
  be near zero. This failure destroys trust fastest.

---

## 4. Evaluation without ground truth, with one user

### 4.1 Build the eval sets

- **Gold set A, papers the owner already understands well** (8–15 of them, in the owner's
  research areas, spanning pre- and post-cutoff). For each, the owner spends 15–20 minutes
  writing "what someone with a strong SWE + general ML background would need to know, and how
  deeply", plus "the 3 things that matter most". This is the single highest-value annotation
  activity. It gives recall and precision for extraction, and top-k quality for ordering.
- **Gold set B, canary papers** (§3.3).
- **Gold set C, live papers**: every paper the owner actually uses. Labels come from usage
  (§4.2) and accumulate over time.
- **Item bank set**: ~100 generated items, with owner labels for good / ambiguous / wrong key /
  trivial, plus ~50 of the owner's own answers with owner-assigned grades. These are used to
  validate the checker and grader.
- **Adversarial grading set**: deliberately wrong-but-fluent answers, correct-but-terse answers,
  answers using different terminology, and partially correct answers. Have models write them,
  then the owner labels them.

### 4.2 Using the owner as annotator efficiently

The owner's time is the scarcest resource. Make labels a **side effect of using the app**, with
a separate annotation session only for gold set A.
- **Triage screen**: after extraction, show the candidate concepts as a dense list with
  three-way buttons: *know it* / *heard of it* / *don't know*, plus *irrelevant*. Fifty concepts
  take about two minutes. These are both learner evidence and extraction-precision labels.
- **Inline micro-feedback** on every explanation and item: *already knew* / *not needed for
  this paper* / *wrong* / *confusing* / *great*. One click, optional comment.
- **Grade disputes**: one click, and they become gold grading labels.
- **Reading companion highlights**: "I got stuck here" on a paper span is the best ground-truth
  signal in the whole system. Each one either maps to a concept that was taught (did teaching
  fail?), a concept that was extracted but skipped (was ordering or triage wrong?), or nothing
  (an **extraction miss**).
- **Pairwise preferences, not absolute scores**, when comparing prompt versions: "which
  explanation would you rather read?" Ten pairwise judgments beat fifty Likert ratings.
- **Active selection**: send the owner only the items where judges disagree or confidence is
  lowest. Don't ask about cases the judges already agree on.

### 4.3 Judge reliability checks

- Calibrate every judge against owner labels before trusting it (κ per criterion, §2.7). Re-run
  on judge model change.
- **Self-preference**: the judge is never the same model family as the generator for anything
  that gates. Spot-check by swapping families and comparing pass rates. A big asymmetry means
  bias.
- **Position and length bias**: randomise order in pairwise judgments and judge both orders.
  Count it as a tie if the verdict flips.
- **Leniency drift**: track the grader's mean score over time against owner-dispute rates. If
  scores rise while disputes don't fall, suspect leniency rather than learning.
- **Sentinel items**: seed known-good and known-bad artifacts into every judge batch, and alarm
  if the judge misclassifies them.

### 4.4 Regression testing of prompt changes

- Freeze the inputs: gold papers, the concept-store snapshot, the learner-evidence snapshot.
- On every prompt or model change, re-run the affected stages on the frozen inputs and compute:
  extraction recall and precision vs. gold A; canary flag rate; item checker pass rate on
  standard specs; grader accuracy vs. labeled answers; ordering top-k overlap with the owner's
  "3 things that matter most".
- For generative outputs, run a **pairwise old-vs-new judge** (cross-family, both orders) on a
  fixed sample, and ask the owner to adjudicate only the flips.
- **Re-run each eval 3× at production temperature** and report variance. Many "improvements"
  are within run-to-run noise.
- Keep prompts as versioned files with a changelog. Each stage carries its own eval in CI, which
  can be manual-trigger because of cost and latency.

### 4.5 Logs to keep, all of them, forever (it's a single user, so storage is trivial)

- Every model call: stage, prompt version, model ID, params, full input, full output,
  latency, cost, parse errors, retries.
- Every decision with its inputs. For example, the priority score's components for each queued
  concept at the time it was queued, so "why did it show me this?" can be answered after the
  fact.
- Every learner interaction: item shown, answer text, time to answer, grade, dispute, feedback
  clicks, highlights, session boundaries.
- Concept-store mutations (merge, split, rename, edge add or remove) with the reason and an
  undo path.
- Source snapshots (paper version, fetched cited papers), since arXiv versions change.

---

## 5. What will most likely go wrong (ranked)

1. **Over-teaching: the system teaches things he already knows or doesn't need.** An
   experienced ML researcher reading an interpretability paper needs perhaps 3–8 genuinely new
   things, but naive extraction produces 40–80 "prerequisites". This one problem decides whether
   the tool saves time or wastes it.
   *Warning signs*: high *already knew* / *not needed* click rate; the user skipping the queue
   and reading the paper directly.
   *Mitigations*: triage screen first; aggressive centrality filtering; propagate "known" down
   the prerequisite graph; cap the default queue at the top ~5 by priority, with the rest
   available but hidden; a teach-on-demand path from the reading companion.

2. **Confident errors about novel or post-cutoff concepts.** The model explains a 2026 method
   as if it were a similarly named 2023 one. The user learns something wrong, and it may never
   surface.
   *Warning signs*: explanations of `introduced-here` or `from-citation` concepts with few span
   citations; closed-book vs. open-book disagreement being ignored; canary failures.
   *Mitigations*: §3 in full; hard code gates on grounding; show the sources inline.

3. **Bad items and bad grading that erode trust.** Ambiguous questions, wrong keys, answers
   leaked in the stem, a terse correct answer graded wrong. Two or three of these and the user
   stops trusting the quizzes, at which point all learner evidence is junk.
   *Warning signs*: dispute rate above ~5%; the checker passing nearly everything (it has gone
   lenient); grades correlating with answer length.
   *Mitigations*: generator → solver → leak-check → ambiguity-check pipeline; "needs human"
   routing; terse-answer anchors; dispute → eval set.

4. **Compounding errors across stages.** A missed extraction never gets taught. A bad merge
   ("attention" merged with "attention sink") corrupts mastery for both. A wrong edge blocks
   the queue. Each stage at 90% gives about 60% end to end.
   *Warning signs*: reading-companion highlights that map to no concept (extraction miss);
   mastery on a concept that suddenly jumps or drops after a merge.
   *Mitigations*: per-stage evals; redundancy at the highest-leverage stage, which is multi-run
   cross-family extraction unioned; reversible merges; end-to-end metrics from the reading
   companion.

5. **Concept-store drift as data accumulates.** After 30 papers you have near-duplicates,
   inconsistent granularity, homonyms and orphan concepts. Retrieval for resolution gets worse,
   and mastery is split across duplicates.
   *Warning signs*: growth in concept count per paper that doesn't slow over time (it should
   slow as the store saturates in the owner's areas); many concepts with one requirement and
   no evidence.
   *Mitigations*: canonical IDs and aliases; a periodic offline consolidation job that
   *proposes* merges and splits for owner approval; granularity anchors; homonym handling.

6. **LLM "students" that already know everything.** Simulating a learner with an LLM to test
   whether explanations teach or whether ordering helps is mostly invalid. The model can't
   un-know things, and it will "learn" from bad explanations. It even answers questions about
   post-cutoff concepts by pattern-matching names.
   *Use simulated students only for narrow mechanical checks*: "Is this item answerable from
   these spans alone?", "Is the answer leaked in the stem?", "Does the explanation contain the
   information needed for the item?" Never use them as evidence of pedagogical effectiveness.
   Only the owner's behavior is that.

7. **Judge bias: self-preference, length, leniency.** Same-family judges rate their own outputs
   higher. Longer explanations win pairwise comparisons. Graders drift lenient.
   *Mitigations*: §4.3. This is ranked here because the countermeasures are well known and
   cheap if you do them from day one.

8. **Silent regressions from model upgrades.** OpenRouter routes and provider model updates
   change behavior without changing the code.
   *Mitigations*: pin model IDs; log the actual model served; run the regression suite before
   any upgrade.

9. **Stale goals.** A concept learned for a paper the owner abandoned stays in review forever,
   and review load grows without bound.
   *Mitigations*: tie review priority to active goals; let goals expire or archive; drop
   concepts with no active goal to a low-frequency maintenance schedule, or retire them.

10. **Varied questions breaking the memory model.** FSRS models repeated retrieval of *the same*
    item. Varied items for one concept mean you are scheduling a concept, not a card, and the
    difficulty parameters get noisy.
    *Mitigation*: accept it, and schedule at the concept-and-depth level. Treat item difficulty
    as a separate per-item parameter, estimated over time, IRT-style if you want to be fancy.
    Keep a stable "anchor" card per concept for the pure memory component, and use varied
    items for the application component.

---

## 6. MVP recommendation, disagreements, and things not asked about

### 6.1 MVP

Build the smallest thing that closes the loop *paper → gaps → teach → reads paper → was it
enough?*

1. Ingest an arXiv paper (LaTeX source preferred) and resolve its citations.
2. Paper map: a gist and method skeleton, shown first.
3. Multi-run, cross-family requirement extraction with spans, depth, centrality and
   knowledge-status (including the post-cutoff and introduced-here flags).
4. A two-minute triage screen.
5. A queue of the top ~5 gaps, ordered by code. For each: a grounded ADEPT-style explanation
   and 2–3 validated application items, graded with key-point rubrics and dispute.
6. **A reading companion**: read the paper in-app, highlight "stuck here", and get an
   in-context answer that is logged as a missed or failed requirement.
7. Concept-level FSRS review for confirmed concepts, using simple flashcards plus varied items.
8. Logging, gold set A for 8–10 papers, canaries, and a regression script from day one.

Defer: homework problems, spoken questions, podcasts and reminders, cross-goal planning,
language learning, and fancy knowledge tracing.

### 6.2 Where I disagree with the brief

- **"Order by generality, more general first" is the wrong default for this user.** For an
  expert reading a paper, general-first turns into a textbook course. That is how you end up
  teaching "what is a gradient" before the influence-function approximation that is actually
  the gap. Order by **goal-relevance × gap × unlock value**, and apply prerequisite constraints
  only where they bind. Generality should be a tiebreaker and the meaning of `unlock_value`,
  not the primary key.
- **ADEPT's blurry-to-sharp does bear on ordering, not just on how explanations are written.**
  Concretely, the first artifact should be a *map of the whole paper* (the blurry picture),
  followed by just-in-time sharpening of the gaps that block it. This is also "advance
  organizer" practice from the education literature. Within each concept, apply it too:
  analogy, then example, then technical. I would not take "the details don't survive a year" as
  license to skip technical detail. This user wants to *extend* methods, which means equations
  and code. Analogies get you oriented. Retained understanding at the required depth is the
  actual goal.
- **Flashcards are low-value for this user's main goal.** For "understand and use a method",
  spaced *application* questions ("you have setting X; would you use method A or B, and why?",
  "what breaks if you remove term T from this loss?") are far more useful than definition cards.
  Keep flashcards for vocabulary-like items: names, acronyms, which paper did what. They matter
  much more for the later language-learning use case.
- **The "maintain it over time" requirement is weaker for papers than it seems.** Most papers
  are read once. Knowledge worth maintaining is the *reusable* stuff that appears across
  several of his goals. Let reuse (a concept required by ≥2 goals) drive what enters long-term
  review, rather than reviewing everything taught.
- **"The app shell is easy and all the risk is in deciding what to teach" is only half right.**
  The other half of the risk is **measurement**: knowing whether those decisions were good. The
  reading companion and the feedback clicks are UI work, and without them you cannot tell
  whether any of the AI is working. Budget for them as core, not as shell.

### 6.3 Things the owner didn't ask about

- **The paper itself is the best teaching material.** Explanations should point into it ("this
  is what equation 4 is doing"). After learning concept X, send the user back to the specific
  paragraph that needed it. That is the payoff moment and a good comprehension check.
- **Use the linked code.** For this user, a 20-line excerpt of the actual implementation, with
  annotations, is often the best "worked example" in ADEPT terms.
- **Measure the outcome directly, sometimes.** Occasionally hold out 3–5 comprehension
  questions about the paper itself, generated from the paper and never used in teaching, and
  ask them after reading. Combined with time spent, this is your north-star metric
  ("understanding per learner-minute"). It will be noisy at n=1, so look at trends across
  papers, not individual numbers.
- **Generalising to language learning**: the abstraction *goal → requirements → learner
  evidence → activities* carries over, but the requirement generator is completely different.
  For a language it is frequency-weighted vocabulary and grammar from the show's subtitles or
  the trip's scenarios, not a prerequisite graph, and the activity types are mostly
  production and recall. Keep the concept store, evidence log and scheduler generic, and make
  extraction and item generation pluggable per domain. Don't design the graph schema around
  ML papers alone, and don't over-engineer for languages now either.
- **Latency still matters for interactive steps** even though money doesn't. Grading must feel
  instant, and multi-judge item validation is slow. Pre-generate and pre-validate items in the
  background as soon as a paper is ingested, and keep only the grading call on the
  interactive path.
- **Make the AI's reasoning inspectable in the UI.** Show why a concept is queued (the score
  components), the source spans, the knowledge-status badge (*introduced in this paper* /
  *from [23], newer than model cutoff*) and the per-key-point grade breakdown. Inspectability
  turns the owner from a passive user into an efficient debugger, which at n=1 is the whole
  evaluation strategy.
