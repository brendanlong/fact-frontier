# Expert opinion: a research mentor's view

Perspective: I've supervised PhD students and research engineers, including several strong
software engineers moving into ML research. This is my view from that experience, based only
on the brief. I haven't read the implementation.

The short version: the hard part of "understanding a paper" is rarely a missing definition. It
is usually not knowing **which few things in the paper carry the weight**, **why the authors
made the choices they made**, and **what the result would look like if it were wrong**. A tool
that is very good at filling definitional gaps but doesn't train those three things will feel
productive and still fall short of the user's actual goal, which is to use and extend methods.

---

## 1. What "understanding a paper" means, and which level this user needs

These levels are cumulative, and each one demands something different:

| Level | Can do | Typical evidence |
|---|---|---|
| **Skim** | Say what problem the paper tackles, its main claim, and whether it's relevant to you | A 3-sentence summary that the authors would accept |
| **Follow the argument** | Reconstruct the chain: problem → idea → method → evidence → conclusion. Say why each step is there | Can explain Figure 1/2 and the main table to a colleague without the paper open |
| **Critique** | Say which claims the evidence supports and which it doesn't. Name confounds, missing baselines and the effect of the eval choice. Say what would falsify it | Proposes the ablation the reviewers asked for; knows the main weakness |
| **Reproduce** | Implement it, including the details the paper leaves out (normalisation, damping, LR schedules, which layer, which judge prompt) | Working code that gets numbers in the right ballpark |
| **Extend** | Know the design space: which assumptions carry weight, what the knobs are, what alternatives were rejected and why, where the method breaks | Can say "if I swap X for Y, I expect Z, because…" and be roughly right |

**This user needs "extend", but only for the paper's core.** That requires critique-level
understanding (you can't extend safely if you don't know which claims are solid) and
"reproduce in principle" (knowing the hidden implementation decisions). It does **not** require
extend-level depth everywhere.

The level is **per component, not per paper**. This is the most important design implication of
this section. Examples:

- **An EK-FAC influence-function paper** (e.g. Grosse et al. 2023 on LLM influence). Extend
  level on what the inverse-Hessian-vector product is approximating, why damping matters, the
  reinterpretation of influence as the proximal Bregman response function rather than
  leave-one-out retraining, and why that matters for evaluation. Follow level on the K-FAC
  eigendecomposition mechanics. Skim level on query batching and the infrastructure tricks.
- **A sparse autoencoder paper** (TopK vs. L1 vs. JumpReLU). Extend level on the loss, the
  sparsity mechanism, the reconstruction/sparsity tradeoff and how it's measured (L0, fraction of
  variance unexplained, downstream CE loss when spliced in), plus dead latents and feature
  splitting. Skim level on the specifics of the auto-interpretability pipeline, unless his
  project depends on it.
- **Emergent misalignment** (Betley et al. 2025 and follow-ups). Critique level matters most:
  how misalignment is measured (LLM judge, thresholds, which free-form questions), which control
  conditions rule out which explanations (e.g. the "educational framing" insecure-code control,
  the jailbroken-model comparison), and how robust the effect is across seeds and models. The
  fine-tuning setup only needs reproduce level.

So the tool has to assign a **target depth to each concept relative to the goal**, not a
single "known/unknown" bit.

---

## 2. What people are actually missing, and what a tool can teach

When a strong engineer "can't read" a paper, the gap is usually a mix of these. I've ordered
them roughly by how often I see each one as the actual blocker for SWE-to-ML people:

1. **Not knowing what the paper is for.** They read the method section without a sharp sense
   of the problem it solves, or what the obvious approach was and why it fails. Everything then
   looks like an arbitrary list of choices. *Highly teachable.* This is the "blurry whole" in
   ADEPT, and an LLM is good at it when grounded in the intro and related work.
2. **Not knowing what is important vs. boilerplate.** They spend an hour on the appendix theorem
   that exists to satisfy reviewers, and skim past the one ablation that carries the paper.
   *Teachable by demonstration* ("this is the key figure, and here's why"). The meta-skill only
   comes from repeated critique practice where they predict importance and then get feedback.
3. **Field conventions and tacit knowledge.** What "standard setup" means; what a reasonable
   baseline is; whether a 2-point gain is large; that "faithfulness" means something specific in
   interpretability; that LLM-judge evals have known biases; that "we use the Fisher" usually
   means the empirical Fisher, with known caveats; what is routinely left out. *Mostly
   teachable, and LLMs are unusually good at it*, often better than textbooks, because it's
   folklore spread across many papers. It's best delivered as annotations on the paper ("when
   they say X here, it means…") rather than as flashcards.
4. **Background concepts** (Hessian, Fisher/Gauss–Newton, KL, superposition, LoRA, RLHF/DPO
   basics). *The tool's sweet spot.* The catch for SWEs: they often know the **definition** but
   lack the **operational sense**. They know what a Hessian is, but not that it's indefinite for
   a non-converged network, or why you damp it. Teach the operational sense, not the definition.
5. **Mathematical maturity.** Reading notation fluently, grouping an equation into meaningful
   pieces, knowing which approximations are harmless and which change the meaning (e.g.
   first-order Taylor + convexity in influence functions, which is exactly where deep-net
   influence goes wrong). *Partially teachable, and slowly.* Translating notation helps right
   away, scaffolded derivations help over months, and there's no shortcut.
6. **The paper's place in the literature.** What it reacts to, who disagrees with it, and what
   happened next (replications, critiques). For influence functions: Koh & Liang → Basu et al.
   "fragile" → Bae et al. "If influence functions are the answer, then what is the question?" →
   TRAK / datamodels and the LDS metric → EK-FAC at scale. Without this chain you can't tell
   whether a new TDA paper is incremental or important. *Teachable, with retrieval.* Very
   high-value, and it's where a model is most likely to hallucinate for recent work.
7. **Hands-on intuition.** What actually happens when you train an SAE: dead latents, feature
   absorption, how sensitive results are to the LR and the activation normalisation. Or how noisy
   influence scores are across seeds. *The tool can't teach this directly.* It can only assign
   small experiments and debrief them. For "extend", this matters a lot.
8. **Research taste.** Whether a result is surprising, whether it will hold up, and what the next
   experiment should be. *Not teachable by recall at all.* It can be **practised** through
   prediction and critique exercises with feedback, and that's about it.

**Rule of thumb:** the tool can carry 1, 3, 4 and 6 almost entirely. It can support 2 and 5
with the right exercises. It should be honest that 7 and 8 come from doing research, and route
the user toward doing it (small experiments, prediction exercises) rather than pretend that
cards will cover them.

---

## 3. Deciding what to teach, in what order, and judging importance

### Step 1: Map the paper before mapping prerequisites

Before generating any concept list, produce a **paper map**:

- The problem, and why the obvious approach fails.
- **The 1–3 load-bearing contributions.** Test: if you removed it, would there still be a paper?
- For each contribution, the main claim and the specific evidence for it (which figure, which
  table, which ablation).
- The method, in a paragraph.
- Known or likely weaknesses, and what reviewers or follow-ups said if that can be retrieved.

Prerequisites are then derived **from the claims**: "to follow claim 2's evidence you need A, B
and C". Every concept should link back to the claim it serves. A concept that serves no claim
is peripheral by definition. This one link is what keeps the tool from teaching what is easy to
define instead of what matters.

**Importance heuristics** that hold up in practice:

- **Signals of what matters:** the title, the abstract, the contributions list in the intro, and
  Figures 1–2. Also what the ablations defend: authors ablate what they think reviewers will
  attack.
- **Signals of boilerplate:** proofs in the appendix, and long related-work sections.
- **What later papers cite it for**, if any exist. This is often different from what the authors
  emphasised.
- **The user's goal.** If he's going to *use* the method, implementation details of the core
  become important. If he's going to *critique* it or position against it, the evaluation
  methodology becomes important.

### Step 2: Diagnose; don't survey

Don't present a 50-concept checklist. Ask 5–8 **discriminating** questions on the central
prerequisites, and infer down the graph: if he can explain why EK-FAC beats K-FAC, he knows
what the Fisher is. Self-reports are useful but miscalibrated in predictable ways. SWEs
over-claim math definitions ("yes, I know what a Hessian is") and under-claim concepts they've
used in code without naming them. Use quick checks on the items that matter, and accept
self-report for the periphery.

**The user's own questions while reading are the best diagnostic signal you will get.** Build
in "ask about this paragraph" and log every question as evidence of a gap.

### Step 3: Order top-down and just-in-time, not general-first

**This is my biggest disagreement with the brief.** "General and foundational first" is textbook
order. For an experienced adult reading a specific paper, it destroys motivation and wastes time
on prerequisites they don't need at the depth the textbook goes to. What works with my students:

1. **Blurry whole first.** What problem, what idea, what result, in a few minutes, with an
   analogy and the key figure.
2. **Read the paper as the spine.** At each section, teach just enough of the prerequisites that
   section needs, at the target depth, then return to the paper.
3. **Go depth-first only where the core needs it.** Stop recursing as soon as you hit something
   the learner already knows or something peripheral.
4. **Sharpen on a second pass.** Revisit the core with the technical detail, derivations and
   implementation choices.

This is exactly Azad's blurry-to-sharp, and I think it applies to **ordering and structure**,
not just to how individual explanations are written. **Generality matters for retention, not for
first exposure.** General concepts (Fisher information, superposition, LLM-judge pitfalls) get
reused across papers, so they deserve the spaced-repetition investment. Paper-specific details
mostly don't.

Prerequisite structure still matters, but within a section, as a local order. Don't try to
build a precise global graph. LLM-generated prerequisite graphs are noisy, and precise edges buy
little. "Needed for claim X at depth Y" is worth more than an exact DAG.

### Step 4: Very new papers and unknown prerequisites

The common failure here isn't the model saying "I don't know". It's **name collision**: a new
term that looks familiar and gets confidently explained with an older meaning. "Emergent
misalignment" read by a model that predates it becomes generic "emergent capabilities +
misalignment". A new SAE variant gets explained as if it were the 2023 L1 recipe. Mitigations:

- **Ground every explanation of a paper-specific term in a quotation** from the paper, or from a
  fetched cited reference. If it can't be grounded, mark it as such.
- **Classify each concept by source:** (a) defined in the paper; (b) standard, and the model knows
  it well; (c) from a cited reference, so fetch it; (d) undefined and unreferenced, so flag it.
  Only (b) may be explained from model knowledge alone.
- **Run a cheap collision check:** have the model define the term without the paper, then with it.
  If the two differ materially, treat it as a new term, explain it from the paper's definition,
  and show the user that it differs from the older meaning. That difference is itself worth
  teaching.
- **Recognise when the right lesson is "read paper P first".** Sometimes the best prerequisite is
  the predecessor paper or a good blog post (e.g. Anthropic's *Towards Monosemanticity* before a
  2026 SAE-variant paper). The tool should recommend external sources, not only generate.
- **Don't treat the paper's claims as ground truth.** The tool teaches what the paper *claims*,
  and should keep that separate from what is established.

---

## 4. Practice that builds research-level understanding

Recall is necessary but not sufficient. Research-level understanding shows up as the ability to
**predict, explain why, choose, diagnose, derive, implement and critique**. The
learning-science results that transfer well here are retrieval practice, spacing, interleaving
(mixing related methods so the learner has to *choose*), self-explanation, the generation effect
(predict before the reveal), and worked examples that fade into independent problems. For
conceptual material, what should be spaced is **varied problems about a concept**, not the same
card. The brief's instinct on varied recall is right.

The effort levels aren't interchangeable. They produce different kinds of understanding.
Flashcards cannot get anyone to extend level, however many there are. The tool should
**recommend** a level per item rather than treat the levels as a pure menu.

### No effort (read or listen)

Good for exposure (the blurry stage), re-encountering a topic, and literature context. It does
little for retention unless it's paired with a single thing to think about.

- **Good:** "2-minute note: why SAEs are overcomplete. Superposition says the model represents
  more features than it has dimensions, so the dictionary needs more atoms than d_model. Think
  about on your walk: what would you expect to happen to feature interpretability as you scale
  the dictionary from 4× to 64×?"
- **Good:** "Follow-up to the paper you read: Bae et al. argue that influence functions in deep
  nets approximate something other than leave-one-out retraining. Read §1–3 (15 min)."
- **Bad:** "Listen to this hour-long interpretability podcast." It isn't tied to a gap, a claim
  or a question.

### Low effort (flashcards)

Good for vocabulary, notation, key distinctions and the "one-line claim" of each paper.
Fluency here speeds up reading every later paper. Cards should be atomic and discriminating.

- **Good:** "K-FAC → EK-FAC: what does the eigenvalue correction fix?" → "It refits the
  diagonal scaling in the Kronecker-factored eigenbasis, so the approximate curvature matches
  the true one better than the Kronecker product of factors does."
- **Good:** "TopK SAE: what replaces the L1 penalty, and what problem with L1 does that avoid?" →
  "It keeps the k largest pre-activations and avoids L1's shrinkage of active latents."
- **Good:** "Emergent misalignment, one line: what was trained, and what was observed?"
- **Bad:** "What is an influence function?" It's too broad, gets answered vaguely, and gets marked
  correct anyway.
- **Bad:** "What year/venue was Koh & Liang?" This is trivia.
- **Bad:** "List the five steps of the method." List cards are notoriously poor.
- **Bad:** A card answerable by pattern-matching its own wording. Rephrasing variants help here,
  but the variants must test the **same knowledge component**. Track mastery at the component
  level, not the card level.

### Higher effort (quiz; short written or spoken answers)

This is where application, choice, prediction and diagnosis live. Answers should be 1–4
sentences and gradable against a rubric.

- **Good (diagnose):** "You train an SAE on layer-12 residual activations and 30% of latents are
  dead after 10k steps. Give two likely causes and one fix for each."
- **Good (choose):** "You want to find which fine-tuning examples drive a model's generalisation
  from insecure code to broadly misaligned answers. TRAK, EK-FAC influence, or retraining-based
  evaluation with LDS: what does each give you, at what cost, and which would you start with?"
- **Good (predict / interpret a control):** "In the emergent-misalignment paper, the same insecure
  code with a benign stated reason ('for a security class') produced little broad misalignment.
  Which hypotheses about the mechanism does that control weaken?"
- **Good (explain why):** "Why do influence-function papers add damping λI before inverting? What
  goes wrong at λ→0 for a non-converged network?"
- **Bad:** "Explain sparse autoencoders." It's unbounded and ungradable, and it rewards fluent
  vagueness.
- **Bad:** Multiple choice with throwaway distractors. If used at all, distractors should be
  real misconceptions.

### Very high effort (homework)

These are derivations, small implementations, mini-experiments and critique/design problems.
They're rare and expensive, and they're the only route to extend level.

- **Good (derivation):** "Starting from the first-order optimality condition, derive the influence
  of up-weighting training point z on test loss. Mark exactly where you used strict convexity,
  and say what the expression computes when that assumption fails."
- **Good (implementation):** "Here are cached GPT-2-small layer-6 activations. Implement a TopK SAE
  in about 60 lines. Train for 10 minutes and report L0 and FVU. Then train an L1 SAE tuned to
  the same L0 and compare. Which has more dead latents?"
- **Good (design/critique):** "Design one experiment that distinguishes 'fine-tuning induces a
  misaligned persona' from 'fine-tuning on bad code generically degrades safety training'. What
  result would support each?"
- **Bad:** "Reproduce Table 2." It's too big, needs too much compute, and gives no feedback until
  it's done.
- **Bad:** Problems whose answers the grader can't check. Every homework item needs a reference
  solution and a rubric with the key insight, the required steps and common wrong turns.

**Grading is a first-class risk.** Open-ended answers graded by an LLM drift lenient
(sycophancy), or penalise correct answers that use unexpected wording. Rubrics should list the
must-mention points and named misconceptions, and the user must be able to dispute a grade,
with disputes logged.

---

## 5. What is most likely to go wrong (ranked)

1. **Prerequisite explosion.** Recursive expansion produces 60–100 concepts, and the user never
   gets back to the paper.
   - *Early warning:* more than 15 items queued before the first section of the paper is read;
     more than an hour before the first "I get what this paper is doing".
   - *Mitigation:* make the paper the spine; enforce a per-session budget; stop recursion at known
     or peripheral concepts; tie every item to a claim.
2. **Teaching what's easy to define instead of what matters.** Most items end up being "What is
   X?" The user aces them and still can't explain Figure 2 or name the paper's main weakness.
   - *Early warning:* more than half of the items are definitional; there are no items about
     evidence, controls or design choices.
   - *Mitigation:* make paper-level items (claims, evidence, weaknesses) the top of the hierarchy,
     and require a quota of choose/predict/diagnose items.
3. **Confident errors on new material** (name collision, stale meaning, hallucinated literature
   context).
   - *Early warning:* explanations with no quotation from the paper; a term explained differently
     across runs; cited "follow-up papers" that don't exist.
   - *Mitigation:* ground in quotations and fetched references; run the collision check; verify
     citations; flag what can't be grounded.
4. **Miscalibrated grading**, which produces false mastery and then bad scheduling.
   - *Early warning:* quiz pass rates above about 90%; the user often thinks "that wasn't really
     right".
   - *Mitigation:* rubrics; checkable predictions where possible; a small hand-graded calibration
     set; a dispute button.
5. **The review pile grows until the user abandons it.** Cards from ten papers, half of them for
   abandoned directions.
   - *Early warning:* daily review over about 15 minutes; skipped days; "I already know this"
     dismissals.
   - *Mitigation:* set an explicit retention target per item. Let paper-specific detail decay on
     purpose. Retire items when a goal is dropped. Keep general concepts, plus each paper's one
     line and key figure.
6. **The tool replaces reading the paper.** The user consumes the tool's summaries, which flatten
   nuance and import errors.
   - *Early warning:* the PDF is never opened; the user can't locate claims in the paper.
   - *Mitigation:* have activities point into the paper ("read §3.2, then answer").
7. **Generic textbook-voice explanations** that are too long, with analogies that mislead. For
   example, "SAE features are like words in a dictionary" encourages overclaiming
   monosemanticity.
   - *Mitigation:* use brevity budgets; always say where the analogy breaks; for this user, prefer
     code and tiny numeric examples as the "diagram" and "example".
8. **Premature generality for language learning.** The schema bends to fit both domains, and both
   end up served badly.
   - *Mitigation:* keep the shared core minimal (goals, knowledge components, items, evidence of
     mastery, schedule). Let lesson types be domain-specific plugins.

---

## 6. How the owner can tell whether it's working

Use concrete, checkable tests rather than feelings of progress:

- **Before/after paper test.** Before using the tool on a paper, spend 10 minutes writing (a) a
  3-sentence summary, (b) the main claim and its evidence, (c) the biggest weakness, and (d) one
  extension with a predicted outcome. Repeat after using the tool. Compare against a reference:
  OpenReview reviews, a follow-up critique, or a strong model given the paper plus the reviews.
- **Held-out delayed questions.** A month later, answer transfer questions generated by a
  separate process that **never saw the practice items**. If you only test on what was practised,
  you're measuring card memory.
- **Beat the real baseline.** The competitor isn't "no tool". It's **reading the paper while
  chatting with Claude**. Alternate papers of similar difficulty between that and the tool, and
  compare time-to-understanding and the before/after scores. If the tool doesn't clearly win,
  its value has to come from persistence and compounding, so test that directly (next bullet).
- **Compounding.** The second and third papers in the same sub-area (e.g. a second TDA paper)
  should need noticeably fewer items and less time. If every paper costs the same, the learner
  model or concept reuse isn't working.
- **Research behaviours.** Did he use the method in his own work? Did he implement it with fewer
  false starts? Did he spot a flaw or a missing control before reading the critique? Could he
  hold a technical conversation with an author or colleague about it?
- **Process health.** Track the fraction of items he marks "useless" or "already knew"
  (sustained >30% means diagnosis is broken; near 0% is suspicious), daily review minutes, how
  often he disputes a grade, and how many sessions end with the paper actually read.

---

## 7. MVP recommendation, disagreements, and things not asked about

### MVP

1. **Input:** an arXiv ID or PDF. **Output:** the paper map (problem, 1–3 load-bearing claims with
   their evidence, method paragraph, weaknesses), plus a concept list where each concept is
   tagged with the claim it serves, a target depth for this user's goal, and a source class
   (defined in paper / standard / cited reference / **flagged unknown**).
2. **Short diagnostic** (5–8 discriminating questions), producing a personal gap list.
3. **A guided reading plan with the paper as the spine:** a blurry overview, then section by
   section with just-in-time ADEPT-style explanations of the gaps and 1–2 check questions per
   section. Include an "ask about this paragraph" box whose questions are logged as gap evidence.
4. **After reading:** 5–10 medium-effort items about claims, evidence and the core prerequisites,
   plus one optional homework item.
5. **Persistence:** a cross-paper concept store with mastery tracked per component, and spaced
   review of varied items for general concepts only.
6. **Validation:** run the MVP on two papers in the same area, and check the compounding and
   before/after tests in section 6.

Defer podcasts, spoken quizzes, precise prerequisite graphs, language learning, and
sophisticated scheduling (a standard FSRS-style scheduler is fine).

### Where I disagree with the brief

- **"Order by generality":** use top-down, just-in-time ordering for first exposure. Use
  generality to decide **what to retain**, not what to teach first. ADEPT's blurry-to-sharp
  applies to structure, not only to prose.
- **"Importance is unclear at first":** less unclear than the brief assumes. Paper structure plus
  the user's goal gives a good prior from the first minute. Track candidates, but rank them from
  day one.
- **Effort levels as a free menu:** let the user pick, but the tool should recommend a level, and
  be explicit that only quizzes and homework reach critique and extend levels.
- **"Keep the knowledge over time":** not all of it. Deliberately let most paper-specific detail
  decay. Keep the general concepts, each paper's one-line claim, its key figure or analogy
  (Azad is right that this is what survives), and a pointer back to the details.
- **"Answers short enough to be practical":** right for the default, but the most valuable
  practice (derivations, experiment design, small implementations) isn't short. Keep it rare, not
  absent.
- **The owner's risk assessment:** I agree the shell is easy. Alongside "what to teach", I'd put
  **item quality and grading** as an equal risk. A perfect curriculum with lenient grading and
  definitional cards still fails.

### Things the owner didn't ask about

- **The motivating link to his own work is the strongest lever.** For each paper, generate one
  question of the form "what does this mean for *your* TDA / emergent-misalignment project?".
  This is where use-and-extend actually happens, and it's what students remember.
- **Literature context and critiques are under-supplied by every other tool.** Surfacing "who
  disagreed, what failed to replicate, what the reviewers said" is high-value and rare. It
  directly trains critique and taste, but needs retrieval and verification.
- **Field maps across papers.** His reading is a sequence within a few directions. A light
  per-direction map ("the TDA landscape: LOO-approximators vs. retraining-based vs.
  gradient-similarity; evaluation via LDS") makes each new paper slot into place, and that is
  most of what experts have that novices don't.
- **For a software engineer, code is often the best diagram.** Ten lines of PyTorch for a TopK
  SAE forward pass, or a tiny numeric influence example on a 2-parameter linear model, often beats
  a picture. Use the "E" in ADEPT that way.
- **Make it feel like a research collaborator, not school.** Adults who are already researchers
  drop tools that feel like homework they didn't choose. Keep effort opt-in, short by default,
  and visibly tied to the paper he cares about this week.
