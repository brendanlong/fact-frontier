# Devil's advocate: the atomic fact pool is the wrong core

Hypothesis under attack: *"The right core is a growing pool of atomic, single-claim facts
extracted from papers (prerequisites the paper assumes plus its contributions), deduplicated
across papers, linked by prerequisite edges and clustered; mastery is tracked per fact, and
teaching and review are generated from that pool."*

Evidence base: `data/pool.db` after ingesting four papers (Bae 2022 PBRF, Grosse 2023,
Soligo 2026, Der 2026): 159 facts, 162 fact-source rows, 269 edges, 7 clusters. Fact IDs
below are `facts.id`. Graph statistics were computed with networkx on a read-only copy.

---

## 1. Why this is the wrong abstraction for "teach what's needed to understand a paper, efficiently"

### 1.1 Atomicity was chosen to fix storage, not teaching
The wiki says so directly: "Atomicity is the lever for dedup quality." The unit of teaching
was shaped by what makes merging work. But understanding a paper means being able to follow
and rebuild its **argument**, and an argument lives in the connections between claims. Atomizing
moves all of that into the edges, and the edges are the weakest data in the system (§3).

Example: Bae et al.'s whole contribution is one argument. "Influence functions on non-converged,
damped, Gauss-Newton networks don't estimate leave-one-out retraining. Each of their
approximations matches a term of a different objective, the PBRF, so that is what they estimate,
and they estimate it well." In the pool this is spread over facts 23–36 and 37–47: 25 sentences
averaging 22 words, and none of them says that chain of reasoning. Fact 31 ("Linearizing the
PBRF ... gives an objective whose optimum is exactly the damped Gauss-Newton influence estimate")
comes closest, but it can only be understood as a step in an argument that no fact holds.

### 1.2 Per-fact mastery means memorizing the paper, which the profile rules out
The profile says: "understand ... well enough to use and extend their methods, not to memorize
them." Yet 112 of 162 fact-source rows (69%) are *contributions*: the paper's own results,
which per-fact mastery would schedule for months of spaced review. Examples:

- 153: "Turn-level attribution to a system-prompt paragraph rose relative to a neutral-query
  baseline ... though only slightly."
- 154: "In a 14-turn conversation, a pruned turn-averaged graph traced degenerate output back
  through an adversarial-prompt (jailbreak) detection feature ..."
- 47: "Two-stage retraining correlates better with influence estimates than warm-start
  retraining, but worse than the PBRF."

Drilling these is the "contents-recall" product the wiki set out *not* to build. The tool
would only differ from Recallity and similar apps in the 50 prerequisite rows (31%), and those
are the rows with no quality control (§2.3).

### 1.3 Importance doesn't separate anything, so the filter idea fails
The wiki's fix for drift into paper detail is to "filter on importance". But 82 of 162 rows
(51%) have importance 3 and only 6 have importance 1. Facts 153 and 157 have importance 2,
the same as the K-FAC efficiency mechanism (68). Filtering on importance ≥ 3 still leaves
82 facts for four papers.

### 1.4 Learner-time cost is probably worse than reading the paper
The brief's metric is learner time. Rough estimate (mine, not measured): 159 facts × (about 1.5
minutes to teach + about 6 reviews × 30 s in year one) ≈ 12 hours for four papers, about 3
hours per paper. That is about the time a careful read takes. The product only pays off if
those hours buy much more understanding than a read, and atomized results are the part least
likely to do that.

### 1.5 Prerequisite-order teaching conflicts with the ADEPT appendix
Teaching in topological order goes bottom-up. The longest path in the current graph is 12 steps:

`2 (strongly convex def) → 4 (IFT) → 49 → 16 → 23 → 27 → 28 → 63 → 64 → 66 (LiSSA) → 81 → 83`

So a headline Grosse result (83, "curvature is necessary") sits behind 11 ordered steps,
starting from a convexity definition. That is the "facts in prerequisite order" style Azad
argues against. The pool also gets blurry-to-sharp backwards *within a concept*: the informal
PBRF definition (63, "keeps parameters near the final trained ones in both weight space and
function space") has an edge **from** the formal definition (28). The graph teaches the sharp
version first and the blurry one after it.

A one-sentence claim also has nowhere to hold an analogy, a diagram or a worked example. Those
belong to a *concept*, not a claim. Only one fact in the pool is analogy-shaped (136,
"Averaging acts as a low-pass filter over the token dimension"), and it is one of the best.

### 1.6 The "depth levels" problem is a symptom, not an edge case
The wiki ends on a "policy question": near-duplicates that state the *same concept at different
precision* (informal and formal PBRF; "always PSD" and "PSD when the loss is convex"). That is
not a leftover merge bug. It shows the natural unit is a **concept with several levels of
depth**, and statements are views of it. Any concept-first design gets this for free; the fact
pool has to add a "refines" edge type to rebuild it.

### 1.7 Things the paper needs you to know that aren't single claims are missing
The extractor only emits claims, so it can't capture **experimental setups and measurement
conventions**, which are what you need to *use and extend* a method. Soligo et al. mention
"judge" 23 times, "LoRA" 27 times and "rank-1" adapters 15 times. No fact explains how emergent
misalignment is measured (an LLM judge; "EM" means alignment < 30 and coherency > 50), what a
rank-1 LoRA adapter is, or why a steering vector is "comparable to" one (fact 105 uses "LoRA"
without defining it). You can't judge fact 98 ("induce emergent misalignment more strongly")
or 111 without the metric. The review prompt actively drops this kind of material as
`paper_detail`.

---

## 2. Grading the facts as teaching material for this user

Rubric: **A** = correct, needed by this user, worth retaining after the paper. **B** = useful
but flawed (compound, missing its "why", hard to read in prose, near-duplicate). **C** =
correct but not worth this learner's time (already known per the profile, trivia, or a
paper-specific result not worth reviewing). **F** = wrong or self-contradictory in the pool.

| ID | Paper | Fact (abridged) | Grade | Why |
|---|---|---|---|---|
| 2 | Bae | "A function is strongly convex if its Hessian is positive definite everywhere." | **F** | Wrong. Strong convexity needs ∇²f ⪰ mI with m > 0. Counterexample: eˣ has a positive definite Hessian everywhere, but it isn't strongly convex and has no minimizer. Combined with fact 3, the pool teaches a false theorem. |
| 3 | Bae | "A strongly convex function has a unique minimizer and an invertible Hessian." | B | True, but two claims joined by "and" got past the reviewer. |
| 4 | Bae | IFT: "...derivative given by the inverse Hessian times the mixed derivative." | **F** | Missing the minus sign. Fact 49 has it (−H⁻¹∇), so the pool contradicts itself. Also a theorem squeezed into one sentence. |
| 13 | Bae | Early stopping ≈ L2 for quadratic objectives | C | True and tangential (importance 1). |
| 16 | Bae/Grosse | Influence = ε · H⁻¹ · ∇loss via Taylor expansion | B | The central concept of two papers, given as one 40-word sentence with no intuition. Has three sibling versions (17, 49, 61) with different sign conventions. |
| 24 | Bae | Three gaps are "differences between solutions to different questions, not errors" | A | The key insight of the paper. But it is only understandable inside the argument (§1.1). |
| 28 | Bae | Formal PBRF written out in words | B | The equation rendered as prose; hard to parse without the formula. |
| 34 | Bae | "Truncating LiSSA implicitly adds extra damping." | C | True and niche. Its edges are wrong (§3). |
| 43 | Bae | Damping trade-off: better conditioning and less linearization error, but a bigger proximity gap | A | Directly useful for running the method. |
| 46 | Bae | Two-stage LOO retraining procedure | C | Importance 1; a paper-specific baseline. |
| 48 | Grosse | "The Hessian ... is the matrix of second derivatives" | C | The profile says calculus is solid. Teaching this wastes time. |
| 51 | Grosse | "The Gauss-Newton Hessian is always positive semidefinite." | **F** | Only true for loss convex in outputs; contradicts fact 8, which says exactly that. Both are kept, so a quiz can grade either answer as wrong. |
| 59 | Grosse | TF-IDF/BM25 definition | C | Two definitions in one fact; a software engineer likely knows it. |
| 60 | Grosse | "A power-law tail appears as a straight line on a log-log plot of the CCDF." | C | General statistics trivia. |
| 63 | Grosse | Informal PBRF ("keeps parameters near ... in weight space and function space") | B | The *better first explanation*, but the graph orders it after the formal version (28). |
| 66 | Grosse | LiSSA, "needing thousands of iterations ... rerun for every query" | C | Duplicates fact 15 and wasn't merged. Has a wrong prerequisite edge from 64. |
| 73 | Grosse | Influence covers only MLP parameters | C | Implementation choice. Its edge from 72 (weight sharing) gives a reason the paper doesn't. |
| 87 | Grosse | Small models' top sequences share tokens; 52B models' are thematically abstract | A | A headline finding that transfers. |
| 93 | Grosse | Proposed explanation for order sensitivity (prefix in lower layers, predictions in upper) | B | Good mechanism fact, correctly hedged; depends on 92. |
| 96 | Grosse | Influence functions as top-down interpretability | A | A framing fact that connects to the user's research areas. |
| 97 | Soligo | Definition of emergent misalignment | A | Essential. |
| 102 | Soligo | EM is mediated by a linear misalignment direction | A | Essential prior result. |
| 109 | Soligo | KL divergence formula | C | Already known per the profile (losses, probability). |
| 110 | Soligo | KL regularization on out-of-domain data produces narrow misalignment | A | The method. |
| 113 | Soligo | "Efficiency" = low training loss at small parameter norm | B | The paper's own operational definition, presented as a general term. |
| 115 | Soligo | "Flatness depends on parametrisation" | C | Importance 1, tangential. Teaching it means teaching sharpness-reparametrization subtleties the paper doesn't need. |
| 116 | Soligo | General solutions get lower loss at the same norm | A | The core result. |
| 120 | Soligo | Preference "may reflect pre-training" | B | Speculation that will be drilled as if it were a fact. |
| 122 | Der | SAE definition | A/C | Correct. May already be known to someone interested in interpretability; the profile doesn't say. |
| 127 | Der | Attribution graph: nodes, edges, linearized backward pass | B | Three ideas in one statement; essential. |
| 132 | Der | Turn-averaged SAE = ordinary SAE on the turn's mean activation | A | The method, in one line. Excellent. |
| 136 | Der | Averaging as a low-pass filter over tokens | A | The best fact in the pool: an analogy that supports predictions. |
| 140 | Der | Decoupled SAE is causally disconnected for attribution | B | 50+ words; a derivation compressed into a sentence. |
| 146 | Der | Pooling per-token features (sum or max) for comparison | C | Evaluation-protocol detail. |
| 153 | Der | Attribution to system prompt "rose ... though only slightly" | C | A weak, paper-specific result. Reviewing it for months has negative value. |
| 154 | Der | 14-turn jailbreak case study | C | An anecdote. |
| 157 | Der | Edge-weight correlation falls with conversation length (higher-order effects) | B | Useful caveat, tied to this setup. |

**Tally across 37 graded facts:** A 12, B 11, C 11, F 3. Roughly a third of the sample is
not worth this learner's time, and about 1 in 12 is wrong.

### 2.1 Over-teaching relative to the profile
Facts 48 (Hessian), 58 (linear-layer gradient is an outer product), 109 (KL) and 2/3
(convexity) cover material the profile marks as solid. Telling the extractor to "stop at facts
the learner profile says they already know" isn't enough. Without a pre-test, the tool can't
know where the edge of the learner's knowledge actually is.

### 2.2 Under-teaching where it matters
Missing: how EM is measured (LLM judge, thresholds); LoRA and rank-1 adapters; the linear
representation hypothesis, which connects facts 99–103 (EM directions) to 122 (SAE features)
and is the common foundation of two of the four papers; what a "measurement" or query function
is in Grosse's framing; and why a counterfactual "response function" is the right way to frame
attribution at all. These are *concept* gaps, not missing claims.

### 2.3 Prerequisites, the "most valuable part", get no verification
Every **F** is a prerequisite written from the model's memory (2, 4, 51). The reviewer
deliberately doesn't see the paper and is told "do not add claims of your own", so it can check
form but not truth. The brief's requirement to "flag what it doesn't know" has no
representation in the schema: no confidence field, no "not in the model's knowledge" marker,
no source for prerequisite facts. Facts 2 and 51 sound fluent and are wrong, which is exactly
the failure that requirement was written to prevent.

---

## 3. What the prerequisite graph and clusters get wrong

### 3.1 Many edges are artifacts of the pipeline
`review.apply` gives every split piece **all** of the original's prerequisites. As a result,
13 groups of sibling facts share identical prerequisite sets:

- 40, 41, 42 ← {27, 31, 32}. "Width reduces linearization error" (40) has nothing to do with
  the non-convergence gap (27). "Longer training reduces the non-convergence gap" (41) has
  nothing to do with linearization (31, 32). "Larger weight decay reduces all gaps" (42) should
  depend on 23 (the decomposition).
- 33, 34 ← {21, 22, 31, 32}. "Truncating LiSSA adds damping" (34) doesn't require "linearization
  error grows with removal size" (32).
- 43, 44 ← {26, 31, 32, 33, 34}; 102, 103 ← {97, 99, 100, 101}; 104, 105 ← {100, 101}.

The graph also isn't direct-only, despite the prompt's instruction: a transitive reduction
removes 38 of 269 edges (14%).

### 3.2 Wrong direction or wrong relation
- 21 ("IHVP is infeasible at O(d³)") ← 14 (CG), 15 (LiSSA). Backwards: the infeasibility is
  *why* CG and LiSSA exist.
- 63 (informal PBRF) ← 28 (formal PBRF). One definition "requiring" another definition of the
  same thing; blurry-to-sharp inverted.
- 66 (LiSSA) ← 64 ("damped GN is PD, so PBRF influence is well-defined"). A solver doesn't
  depend on a claim about PBRF.
- 4 (IFT) ← 2, 3 (strong convexity). The IFT needs an invertible Hessian, not strong convexity.
- 9 (GN = Fisher for common losses) ← 8, 51 (PSD claims). Irrelevant to the equality.
- 72 (shared MLP weights break K-FAC's independence assumption) ← 69 (EK-FAC). Should be 67
  (K-FAC).

### 3.3 Missing edges, including the cross-paper ones the pool exists for
- 105 ("a single trained steering vector induces misalignment comparable to LoRA") lacks 104
  ("a steering vector can be trained by gradient descent"), its literal prerequisite.
- 103 (the direction transfers across finetunes) lacks 102 (the direction exists).
- **There are zero edges between papers 3 and 4, or between them and papers 1–2.** All 36
  cross-source edges are between the two influence-function papers. The wiki says the
  misalignment and SAE papers were "linked where they genuinely share ideas (steering vectors
  and LLM judges)". The current database has no such links and no LLM-judge fact at all.
  Missed links include: 10 (gradient descent's implicit bias toward the initialization) ↔ 112
  (implicit regularisation); 99 (mean-diff direction) ↔ 159 (contrastive ranking of persona
  features); 100 (steering) ↔ 155 (adding a decoder direction as an intervention); 102 ↔ 122
  (both rely on linear representations, which have no fact).

The merge step only shows the judge about 9 nearest neighbours per candidate, and merge plus
link happens once, at ingest. Cross-paper structure is exactly what that kind of local
retrieval misses.

### 3.4 "Prerequisite" is several relations mixed together
Of 269 edges, 21 start from a *result*. Examples: 83 ← 81, 82; 88 ← 87; 90, 91 ← 89; 150 ← 149;
47 ← 27. These mean "follows from", "is evidence for", "contrasts with" or "same experiment",
not "you must understand A to understand B". The graph mixes at least five relations: uses a
term defined in; motivates; is evidence for; refines; same topic. Only "uses a term defined in"
is safe for ordering, and it can be checked mechanically (does B mention a term whose
definition is A?). The other relations matter for *explanations*, and treating them as hard
ordering constraints produces the 12-step chain in §1.5.

### 3.5 Clusters mostly reproduce paper membership
Cluster 10 is all 38 Der facts. Cluster 8 is 21 of Soligo's facts, and Cluster 7 is 16 Grosse
facts. The one cross-paper merge is a mislabel: Cluster 4, "Influence functions vs
leave-one-out retraining gaps", contains Soligo's implicit-regularisation and efficiency facts
(112–115), placed there by embedding similarity but under a name that doesn't describe them.
Cluster 6, "Curvature approximations" (38 facts), mixes linear-algebra prerequisites (54, 55)
with Grosse's empirical results (81–83) and Bae's damping trade-off (43). At this scale the
clusters add little beyond `fact_sources.source_id`, and the "map of what they know" would show
four papers with fuzzy borders.

---

## 4. Alternative cores

### A. Concept nodes with depth levels; claims are assessment items, not nodes
The unit is a named concept ("Gauss-Newton Hessian", "PBRF", "emergent misalignment",
"turn-averaged SAE"), at the grain of a short lesson, like a Math Academy topic or an ALEKS
item type. Each concept holds content at several levels (analogy, plain description,
technical definition, worked example) plus a bank of claims and question templates. Mastery is
tracked per concept, using evidence from the items.
- **Why it might win:** Dedup becomes mostly name and alias matching, which is far easier than
  matching one-sentence claims. Depth levels are built in, so the "refines" problem goes away.
  Fits ADEPT naturally. Prerequisite edges between ~30 concepts per paper are easier to get
  right than between ~40 claims, and a human can inspect them. KCGen-KT and Moon et al.,
  cited in the wiki, are evidence for LLM-generated *knowledge components*, which are closer
  to this than to sentences.
- **How it might fail:** Concept granularity becomes the hard question again ("is EK-FAC its own
  concept?"). Naming can drift across papers. Concept-level mastery is coarse.

### B. Paper-first "argument map plus just-in-time prerequisites" (a reading guide)
For each paper, produce the argument as 5–10 steps (claim → why → evidence), with a prerequisite
explainer attached where each step first needs it. A short diagnostic before starting skips
what the user already knows. Only the *prerequisite concepts* go into a long-lived store; the
paper's results stay in the guide.
- **Why it might win:** It targets the stated goal (understand this paper) directly. Keeps
  the argument whole (§1.1), applies blurry-to-sharp at the paper level, and avoids long-term
  review of paper results (§1.2). Cheap to build and to evaluate.
- **How it might fail:** On its own it doesn't build up across papers. Without a concept store
  underneath it, prerequisites get re-taught for every paper. Retention of the paper's own ideas
  is left to the user.

### C. Capability/task-centric (skills, not knowledge)
The unit is something the user can *do*. "Given an attribution question, choose between LOO,
influence functions and the PBRF and say what each measures." "Explain why turn-averaging
destroys token-level features." "Predict whether KL regularization will keep misalignment
narrow if the KL data is in-domain." Practice is the varied scenario questions the brief asks
for, and concepts are tagged on as a Q-matrix.
- **Why it might win:** Matches "use and extend methods". The varied-recall requirement is the
  core of the design, not an add-on. Hard to fill with trivia: no one writes a task for fact 153.
- **How it might fail:** Good tasks are hard to generate and to grade. Fewer units and less
  coverage. Credit assignment needs the concept layer anyway, which makes it A + C.

### D. Tutor-first with a lightweight learner model
No pool. An agentic tutor works through the paper with the user: it probes, explains and keeps
free-text notes of what the user knows and has misunderstood, and generates review from those
notes later.
- **Why it might win:** Adapts to the actual learner instead of a profile paragraph. Finds stuck
  points empirically rather than guessing them. Almost no schema risk. Fastest to try.
- **How it might fail:** No durable structure, so scheduling and dedup across months are fuzzy.
  Quality depends on each session. Hard to show what was learned.

**My bet:** A as the store, B as the experience for each paper, C as the practice format, and
a tutor (D) used for diagnosis. The atomic claim survives as a *question-generation seed*
attached to a concept, not as the unit of tracking.

---

## 5. What's worth keeping regardless

- **Profile-conditioned prerequisite extraction from the full paper.** Asking "what does this
  paper assume?" is the right question, and Sonnet-class models do it reasonably well (facts
  97, 102, 122, 127 are what a reader needs).
- **The "read it without the paper" review test.** A strong rubric for standalone
  explanations. Extend it with a *truth* check against a source.
- **Provenance:** fact_sources with role, evidence and importance *per source*, plus merge_log
  with reasons. Keep this for whatever the unit becomes.
- **Separating tracked units from derived groupings**, so reclustering never touches history.
  Correct, whatever the unit.
- **Embedding + FTS candidate retrieval followed by a model's decision** for dedup. Correct
  mechanics, and easier at concept level.
- **FIRe-style credit propagation and LLM-attributed Q-matrices.** These work better with fewer,
  cleaner, typed edges.
- **Cost logging and side-by-side model comparison** (`compare_review.py`). That's how the
  Haiku "worth knowing" failure was found.
- **Some individual facts are excellent** (132, 136, 24, 43, 116, 87) and show what good output
  looks like: one mechanism or decision rule that supports predictions.

---

## 6. The fastest experiment to show whether this is viable

**A stuck-point coverage audit on one new paper (about 1–2 hours of the user's time, no UI).**

1. Choose a recent paper in the user's area that the user hasn't read and that isn't in the
   pool. Ingest it, but **don't look at the facts**.
2. The user reads the paper cold, with a timer, and marks every place they got stuck or
   skimmed without understanding, plus the 3–5 ideas they would need to *use or extend* the
   method. This is ground truth for "what this user needs."
3. Score the extracted facts against those marks:
   - **Recall:** the fraction of stuck points that some fact (or a pair of linked facts) would
     have resolved. The user judges this by reading only the matched facts.
   - **Precision:** the fraction of facts that address a stuck point or a needed idea, versus
     already-known, unneeded or wrong.
   - **Order:** whether the graph puts the facts that resolve a stuck point before the stuck
     point's own facts.
4. **Comparison arm, same cost:** one Opus call producing a reading guide (alternative B: an
   argument map with prerequisite explainers inserted where needed) for the same paper, scored
   on the same stuck points.

**Decision rule:** if the fact pool's recall is below about 60%, or its precision below about
50%, *or* the one-shot reading guide matches it on recall, then the pool isn't paying for its
complexity, and the core should move to concepts plus a reading guide. If the pool clearly
wins on recall *and* the user says the matched facts actually unblocked them, the atomic core
earns its place, and the effort should go into edge typing and truth-checking prerequisites.

This tests the one claim everything else depends on: that extracted atomic facts are what this
user needs to understand a paper. It needs no teaching UI, scheduler or mastery model. A
retention study can come later.
