# Expert opinion: a learning scientist's view

*Perspective: cognitive psychology / learning science (retrieval practice, spacing, worked
examples, transfer, cognitive load), with edtech advisory experience. Written from the brief
alone, without reference to the current implementation.*

---

## 1. How I would approach this problem

**Core idea.** Treat each goal (a paper) as a *performance target* first and a body of
knowledge second. Before deciding what to teach, write down what "understanding this paper well
enough to use and extend it" looks like as a short **target exam**: 10-20 questions an expert
colleague would ask after a reading group (what problem does it solve, why does the method work,
what would break it, when would you use it instead of X, how would you apply it to your own
project). Then work backwards (Wiggins and McTighe's *backward design*). Figure out which
knowledge components the exam depends on, **find out which ones this learner already has**
(the most important and most neglected step for an expert learner), teach only the gaps, as
late as possible and as close to the paper as possible, and then send the learner back into the
paper itself. Retention practice comes after that, and only for components that have future
value beyond this one paper. The system is a **diagnose → teach the gap → get them into the
paper → verify → selectively maintain** loop. It is not a curriculum generator.

**Specifics:**

1. **Target exam first, written before any teaching plan exists.** It is the definition of
   success, the sampling frame for prerequisites and the outcome measure (section 5). Generate it
   with a separate model call that cannot see the teaching plan, so the plan can't be built to
   pass the exam.
2. **Prerequisite extraction grounded in sources.** Build the candidate prerequisite set from
   the paper's text, its methods section and its cited works. Ground every component in a
   source passage, and *fetch the cited papers* for anything post-cutoff or unfamiliar. Don't
   let the model rely on its memory.
3. **Diagnose before teaching.** This user is an expert ML researcher. Most "prerequisites" (backprop, KL
   divergence, fine-tuning, attention) are already known, and teaching them is not just wasted
   time but actively harmful: the *expertise reversal effect* (Kalyuga et al., 2003) shows that
   instructional support that helps novices hurts experts. Use a short adaptive pretest of one or
   two generative probes per candidate component, starting at the frontier, and infer downward
   ("if they can explain influence functions, don't test them on Hessians"). Pretesting has a
   bonus: attempting questions before instruction improves later learning even when the
   attempts fail (the *pretesting effect*, Richland, Kornell and Kao 2009).
4. **Teach gaps just-in-time, anchored in the paper.** Explanations should use the paper's own
   notation and running example. An explanation of "Hessian-vector products" in the abstract is
   much less useful than one showing equation 4 of *this* paper.
5. **Get them reading early.** The paper itself, read with support, is the main learning
   activity. Offer *adjunct questions* while reading (Rothkopf's classic finding: questions
   embedded in text improve learning of the questioned material and, when they come after the
   passage, of the surrounding material too) and self-explanation prompts at key equations
   (Chi et al., 1989/1994).
6. **Verify with the target exam**, graded against a rubric, both immediately and after a delay.
7. **Maintain selectively.** Spaced retrieval goes to components that are general and
   reusable (a method family, a core technique), not to paper-specific details. For details,
   rely on *savings in relearning* (Ebbinghaus): a fast refresh when a new goal needs them is
   cheaper than a year of reviews.

---

## 2. Unit of knowledge and its structure

**Unit: the knowledge component (KC)**, in the sense of Koedinger, Corbett and Perfetti's
*Knowledge-Learning-Instruction (KLI) framework* (2012). A KC is an acquired unit of cognitive
function that can be inferred from performance on a set of related tasks. The definition is
operational: **a KC exists at the granularity at which you can write questions that test it
independently and where success on one question predicts success on another.** That gives
you a granularity rule, which "fact" or "concept" do not.

KCs should be **typed**, because type determines how they are taught, practiced, scheduled
and assessed:

| Type | Example (ML) | Example (language) | Best practice format |
|---|---|---|---|
| **Term / notation** (fact) | "What does $\mathcal{I}(z, z_{test})$ denote in this paper?" | vocabulary item | flashcard, short spaced retrieval |
| **Concept / mechanism** (principle) | why influence functions approximate leave-one-out retraining | why the subjunctive appears after *quiero que* | explanation, then "explain why" / "predict what happens if" questions |
| **Procedure** (skill) | derive the influence estimate; compute a TracIn score on a toy model | conjugate in context | worked example → faded example → problem |
| **Conditional / discrimination** (when to use what) | influence functions vs. TracIn vs. datamodels for a given setting | *ser* vs. *estar* | interleaved contrast cases, "which method and why" |
| **Claim / result** (paper-specific) | "they find EM generalizes from insecure-code fine-tuning" | n/a | one or two questions, usually *not* maintained long-term |

Structure it as a **graph with two edge types**:
- **prerequisite** edges (A must be understood to understand B), used for diagnosis inference and
  for gating formal material;
- **elaboration / part-of** edges (B is a sharper version or a component of A), which support
  blurry-to-sharp sequencing (section 3).

Each KC should carry: the type; a one-sentence statement of what knowing it lets you *do*; source
grounding (passages and citations); a confidence flag ("model-uncertain / post-cutoff /
grounded"); links to the goals that need it, with a criticality weight per goal; and a learner
state (section 3).

**Granularity rules of thumb:**
- Split when two parts can be known independently (a learner can know what TracIn computes
  without knowing why the checkpoint sum approximates something). Merge when you can't write a
  question that tests one without the other.
- **A concept KC should be "chunk-sized" for an expert**: something they could explain in one to
  three sentences once learned. If the explanation needs a page, it is a cluster of KCs with a
  parent.
- **Don't atomize into trivia.** Ten flashcards on a paper's notation and dataset names do not
  add up to understanding its method. Enforce a quota, e.g. no more than about 20% of a goal's
  KCs may be term/claim type.
- **Schemas emerge; don't model them directly.** What you want the expert to end up with is a
  schema ("data attribution methods trade off fidelity vs. cost along this axis"). You build
  schemas through discrimination KCs and compare-and-contrast questions across sibling KCs.
  You don't need a separate "schema" object.

KCs must be **shared across goals**. The second paper on training data attribution should find
most of its KCs already in the graph with learner state attached. This is where the system's
value compounds.

---

## 3. What to teach, in what order, and what comes next

### What to teach

Priority for a candidate KC = **(criticality to current goals) × P(learner doesn't know it) ×
(reusability, for maintenance decisions)**, with a hard filter: don't teach anything whose
P(known) is high, and don't teach anything that isn't on a path to a target exam question.
"Things the user *might* need to know" should be *tracked* but *lazily evaluated*: kept as
candidates, never pushed, only promoted when a target question or a failed probe points to them.

### Blurry-to-sharp vs. prerequisite-first

This is a false dichotomy. The research supports a specific hybrid:

- **Blurry-to-sharp at the level of the whole goal.** Start with a one-paragraph to one-page
  overview of the paper's idea: the problem, the key move, why it might work, and a picture.
  That is Ausubel's *advance organizer*, Reigeluth's *elaboration theory* ("zoom-lens"
  sequencing: epitome first, then elaborate) and 4C/ID's insistence on *whole tasks from the
  start* (van Merriënboer). It gives every later detail somewhere to attach, and for a motivated
  expert it keeps the purpose visible.
- **Prerequisite-gated at the level of each formal component.** When you sharpen a specific piece
  (the actual influence-function derivation), the formal prerequisites have to be in place first
  or cognitive load swamps the learner (Sweller's element interactivity). Within a component,
  go blurry-to-sharp *in the explanation* (analogy → example → technical statement), but don't
  present the technical statement before its formal prerequisites.
- **Depth-first along the critical path, not breadth-first by generality.** Sharpen the one
  component the paper's main contribution depends on, then the next. Breadth-first "all
  foundations first" delays the payoff and front-loads things the expert already knows.
- **For experts, consider problem-first.** Schwartz and Bransford's *A Time for Telling* (1998)
  and Kapur's *productive failure* show that brief struggle with contrasting cases *before* the
  explanation improves transfer, especially for learners with relevant prior knowledge. For
  this user, a good opening move for a new method is often: "Here is the problem this paper
  solves. How would you approach it? What would go wrong with the obvious approach?" Then
  explain. (Use this sparingly. It costs time and it fails for true novices.)

The danger in blurry-to-sharp is that **blurry stays blurry**. Analogies produce durable
misconceptions (Spiro et al.'s *cognitive flexibility theory* documents the "reductive bias" of
oversimplified models in advanced learning). Every analogy should come with **"where this
analogy breaks"**, and no KC should count as learned on the strength of analogy-level answers.

### Effort levels: chosen by learning stage and KC type, not by mood

Map activities to *stages* of learning a KC:

1. **Encoding** (first exposure to a gap): a short explanation (ADEPT-style, but brief and
   anchored in the paper), **immediately followed by a generative act**: a self-explanation
   prompt or a single question. Reading or listening alone is acceptable only as the encoding
   step and must never be logged as a review.
2. **Consolidation** (same session to a few days later): retrieval practice (the *testing
   effect*, Roediger and Karpicke 2006). Concepts get "explain why" and "predict what happens if"
   questions. Terms get flashcards. Discrimination KCs get interleaved contrast items (Rohrer and
   Taylor; Kornell and Bjork 2008 on interleaving for category learning).
3. **Skill building** (procedures; only where the goal requires *using* the method): worked
   example → faded worked example → independent problem (the *worked-example effect*, Sweller
   and Cooper; *fading*, Renkl and Atkinson). For this user the high-value "homework" is concrete:
   derive the key equation, or implement the method on a toy model in about 50 lines and
   predict the result before running it. It is expensive, so do it for at most one or two KCs per
   paper: the ones the user plans to extend.
4. **Maintenance** (weeks to months): spaced, varied retrieval on reusable KCs only. Expanding
   intervals (Cepeda et al., 2008: optimal gap is roughly 10-20% of the desired retention
   interval). Use a mix of question variants (section 7 on why variants complicate scheduling).
5. **Transfer** (any time after consolidation): "how would you use this in your project on
   X?", "which method fits this new scenario?" These are the most valuable questions for this
   user, and should be a regular part of maintenance rather than a separate tier.

The **user chooses the time budget and context** (5 minutes on a phone, 30 minutes at a desk,
commuting with audio). The **system chooses the activity** that best fits that budget given the
KC states. The audio/reading "no effort" mode is legitimate for encoding new material and for
gist-level refreshers. It is not retrieval practice and should not advance any schedule. If you
want an audio mode that does count, make it spoken retrieval: the system asks, the user
answers aloud, and the answer is transcribed and graded.

### What comes next (the session loop)

Each session: (1) any due maintenance items for high-value KCs (capped); (2) the next gap on the
critical path of the active goal; (3) a nudge back to the paper section that the newly learned
KC unlocks. After every response, update the learner state per KC. A simple per-KC model is
enough: strength/stability (FSRS-style) plus a separate "highest level demonstrated"
(recognize / recall / explain / apply / discriminate). Don't build Bayesian Knowledge Tracing
or IRT for one user. You won't have the data to fit it.

---

## 4. What is most likely to go wrong (ranked)

**1. Illusion of learning: fluent LLM explanations plus easy questions feel like understanding.**
LLM explanations are extremely fluent, and fluency gets mistaken for learning (Koriat and
Bjork; Rozenblit and Keil's *illusion of explanatory depth*). LLM-generated questions tend to be
answerable from the stem, test recognition, or accept vague paraphrases, and LLM graders are
lenient. The system can show 90%+ accuracy and a satisfied learner while producing little
durable or transferable knowledge.
*Early warning:* first-attempt accuracy above ~85% on new material; answers that paraphrase
the question; the learner can't answer the *target exam* or a delayed probe despite high
practice scores; grader "partial credit" on answers a human expert would mark wrong.
*Mitigation:* a held-out target exam written independently; an adversarial grader with an
explicit rubric and a "would a domain expert accept this?" check; a question rubric (section 5)
enforced by a critic pass; aim for practice success around 70-85%, not 95%.

**2. Teaching what the expert already knows.** This wastes their time, triggers the expertise
reversal effect and causes abandonment, which is the most common edtech failure there is.
*Early warning:* high skip rate, "I know this" clicks, near-perfect first-try accuracy on
taught KCs, the user reading the paper directly instead.
*Mitigation:* diagnosis-first; a one-click "I know this" that triggers *one* verifying probe
rather than being taken on faith; seed the learner model from the user's own papers and
research areas.

**3. Wrong or hallucinated content, especially for new papers.** The brief already worries
about this, and it is worse than it sounds: models confidently "explain" post-cutoff methods
by pattern-matching the name onto an older method. A plausible wrong explanation is worse
than none, because it is learned *and* interferes later (proactive interference).
*Early warning:* explanations that don't cite a passage; the user spotting errors; explanations
of the same KC that disagree across regenerations.
*Mitigation:* source grounding as a hard requirement (every claim tied to a passage in the paper
or a fetched citation); self-consistency checks across samples; an explicit "uncertain"
status shown in the UI; for uncertain KCs, the default activity is "read this section of the
cited paper", not a generated explanation.

**4. Review burden explosion (the Anki death spiral).** Each paper adds 20-50 KCs. After ten
papers the daily review queue is long, the user skips days, the backlog grows, and the user
quits.
*Early warning:* due count trending up week over week; sessions consisting entirely of reviews;
missed days.
*Mitigation:* maintenance only for reusable KCs; a hard daily cap; automatic retirement of
paper-specific KCs after the goal is done; "maintenance value" decays when a goal is archived.

**5. Atomization: facts instead of understanding.** It is easy to generate cards like "what
dataset did they use" and "what does λ denote". These are easy to grade and schedule, so the
system drifts toward them.
*Early warning:* the KC type distribution skews toward terms and claims; questions start with
"What is the name of..."
*Mitigation:* type quotas; a requirement that each goal has at least N mechanism and
discrimination KCs; questions tied to target exam items.

**6. Analogy-level understanding mistaken for the real thing** (the blurry-to-sharp failure
mode). The learner can tell the story but not use the method.
*Mitigation:* a KC is "learned" only at the *explain* or *apply* level, never at the analogy
level; every explanation includes where the analogy breaks.

**7. The tool replaces the paper.** The learner spends hours on prerequisite modules and never
reads the paper, or reads it much later. Learning *about* the paper replaces engaging with it.
*Early warning:* time from goal creation to "read section 3" is long; most time goes to
prerequisite modules.
*Mitigation:* the metric is time-to-competence on the target exam; push the learner into the
paper as soon as the critical path for the next section is covered.

**8. Question variation corrupts the memory model.** If every review is a different question at
a different difficulty, a failure might mean "forgot the KC" or "harder variant", and spacing
algorithms built for fixed cards (FSRS, SM-2) get noisy signals.
*Mitigation:* tag each question with KC and level; record outcome per (KC, level); keep a small
stable "anchor" question per KC for measurement; let variants mostly test the KC at a level
already demonstrated.

**9. Grading noise in free-response answers.** Short-answer LLM grading is decent but
inconsistent at the margins, which feeds noise into scheduling.
*Mitigation:* rubric-based grading with reference answers; let the user override (and log
overrides as a grader-quality metric); periodically audit a random sample by hand.

---

## 5. How to tell if it's working

### Learner outcomes (the ones that matter)

1. **Target exam score**, immediate and delayed (1 week, 1 month), graded blind against a
   rubric. This is the primary outcome.
2. **Time to competence:** learner-minutes from goal creation to a passing target exam score
   (e.g. 80% at "explain/apply" level). This is "efficiency" as the owner defined it.
3. **Transfer:** performance on novel scenarios that appear in neither the paper nor the
   practice items ("given this new setup, which attribution method and why?").
4. **Calibration:** ask for a confidence rating (1-4) with each answer and compute a Brier score
   or a calibration curve. Well-calibrated learners study efficiently, and a poorly calibrated
   one reveals illusion-of-learning problems.
5. **Real-world proxies:** did the user go on to use, implement, cite or critique the method?
   Ask after the fact ("did you use X this month?").

### Single user, no control group: use within-subject, item-level randomization

This is entirely doable and is the standard approach in memory research:
- **Withhold teaching on a random subset.** For each goal, randomly assign about 20% of the
  diagnosed-gap KCs to "not taught" (they are still pretested and post-tested, and the
  learner can still read the paper). The difference in post-test performance between taught
  and untaught KCs is your causal estimate of what the teaching adds beyond reading the paper.
  If it's near zero, you've built an expensive paper-reader.
- **Withhold maintenance on a random subset.** Randomly assign reusable KCs to "maintained"
  vs. "not maintained" and probe both at 1-3 months. This tells you whether maintenance pays for
  its time.
- **Randomize activity types within the learner.** Assign KCs to "explanation + question"
  vs. "question-first (productive failure)" or "flashcard" vs. "explain-why" and compare
  delayed outcomes. With dozens of KCs per paper, you get meaningful signal in a few months.
- **Pre-register the target exam.** Freeze it before teaching starts so it can't drift toward
  what was taught.
- **Pretest/posttest gains** per KC, normalized (Hake's normalized gain), to avoid ceiling
  artifacts with an expert.

### Rubric for taught material (score each explanation 0-2 per criterion)

- **Accurate:** every technical claim is supported by a cited passage; nothing contradicts the
  paper.
- **Targeted:** addresses the specific gap diagnosed, at the learner's level; no re-teaching of
  known material.
- **Anchored:** uses the paper's notation and/or example.
- **Generative:** ends with something the learner must *do* (predict, explain, compute).
- **Bounded:** states where the analogy or simplification breaks.
- **Brief:** shortest version that achieves the above (for this learner, most explanations
  should fit on a phone screen; longer means it should be split).

### Rubric for questions (pass/fail per criterion; fail any = regenerate)

- **Retrieval, not recognition:** the answer must be generated, not picked out of the stem.
  Multiple choice only for discrimination items, with plausible distractors drawn from real
  misconceptions.
- **No leakage:** the stem doesn't contain or strongly cue the answer.
- **Gradeable:** has a reference answer and a rubric listing the essential elements; two
  independent graders would agree.
- **Targets a named KC at a named level** (recall / explain / apply / discriminate / transfer).
- **Short answer:** answerable in one to three sentences or a short calculation.
- **Discriminating:** someone who doesn't know the KC would likely get it wrong. (Test this:
  have a model without access to the explanation attempt it. If it passes easily from general
  knowledge, the question isn't measuring what you taught... though for an expert learner,
  this is also a hint that the KC wasn't a gap.)

### Process health metrics (dashboards, weekly)

First-attempt accuracy on new items (target 70-85%); delayed-probe accuracy; daily due count
trend; skip / "I know this" rate; grader override rate; share of time spent in the paper vs.
in modules; KC type distribution.

---

## 6. MVP: include and exclude

**Include:**
1. Paper ingestion → **target exam** (independent call, frozen).
2. KC extraction grounded in sources (paper and fetched citations), with types, prerequisite
   edges and an explicit **uncertain** flag.
3. **Adaptive diagnostic pretest** (generative probes, inference along prerequisite edges) plus
   an "I know this" button with a verifying probe.
4. **Paper overview** (blurry whole-paper epitome) shown first.
5. **Just-in-time gap explanations** (brief, anchored in the paper, analogy-with-limits), each
   followed by one generative question.
6. **Short-answer retrieval questions**, LLM-graded with a rubric, user override, confidence
   rating.
7. **Simple per-KC spacing** (FSRS or plain expanding intervals at KC level), maintenance only
   for KCs flagged reusable, with a daily cap.
8. **Measurement:** the immediate and delayed target exam, plus the randomized
   withheld-teaching subset from day one. If you don't build measurement in from the start
   you'll never be able to add it credibly.

**Exclude (for now):**
- Podcasts/audio generation (an encoding-only mode with weak learning effect; nice later).
- Auto-generated, auto-graded homework. Instead offer a *suggested* exercise per paper ("implement
  X on a toy model; predict Y first") with no grading machinery.
- Language learning and SE skill paths. Keep the schema generic (goal → KCs → evidence →
  activities) but don't build lesson types for them.
- Sophisticated learner models (BKT, IRT, deep knowledge tracing).
- Diagrams, unless generated as code (Mermaid/TikZ) and checked. Bad diagrams cost more than
  no diagrams.
- Gamification, streaks, multi-user.
- Cross-goal optimization beyond KC sharing.

---

## 7. Where I disagree with the owner's stated preferences

1. **"Effort levels chosen on demand."** Partly disagree. Learners reliably pick the
   least-effective strategies: they prefer rereading over retrieval (Karpicke, Butler and
   Roediger, 2009) and judge blocked practice as better than interleaved even when it is worse
   (Kornell and Bjork, 2008). These are Bjork's *desirable difficulties*, and they *feel*
   worse. Let the user set **time and context**; let the system pick the **activity**. The "no
   effort" tier should not count as review.

2. **"Order by generality, more general and foundational first."** Disagree as a primary
   ordering rule. For an expert, the most general and foundational material is exactly what
   they already know. Order by **criticality to the target × probability of a gap**, depth-first
   along the critical path, after a whole-paper overview. Generality matters for the
   *maintenance* decision (general KCs are worth keeping), not for teaching order.

3. **"Track things the user might need to know."** Agree with tracking, disagree with any
   implication of teaching them speculatively. Candidates should be lazy: promoted only by
   evidence.

4. **"Keep that knowledge over time" (implicitly, all of it).** Disagree. Maintaining
   everything is unaffordable and unnecessary. Paper-specific details can be forgotten and
   relearned quickly when needed (Ebbinghaus savings). The paper is an external memory. Keep
   general, reusable KCs.

5. **"Varied recall."** Agree strongly on the learning side (variability of practice aids
   transfer; Schmidt, and Kornell and Bjork). But it has costs the brief doesn't mention: it
   complicates scheduling and measurement, and it raises grading difficulty. Handle it by
   scheduling at the KC level, logging outcomes per question level, and keeping a stable
   anchor item per KC.

6. **"Flag what it doesn't know rather than guess."** Agree with the goal, but don't expect
   the model to know what it doesn't know. LLM self-reported uncertainty is poorly calibrated.
   Use *structural* signals: the method's name or citation is post-cutoff; the explanation
   isn't supported by a retrievable passage; samples disagree. Then fetch the source.

7. **The ADEPT appendix.** Mostly agree as a writing guide, with three caveats. (a) The "E,
   an example the learner works through *themselves*," is the only element with a strong active
   learning ingredient. Make it mandatory; the others are presentation. (b) The claim that
   "what survives a year later is the analogy or diagram" is consistent with gist memory
   (fuzzy-trace theory, Brainerd and Reyna). But for a researcher who wants to *extend*
   methods, the gist isn't enough: the technical layer is the point, and retaining it is
   precisely what spaced retrieval is for. (c) For experts, starting with an analogy can be
   condescending and slow. Often the right order is problem → technical statement → analogy as
   a check, or skip the analogy entirely. The expertise reversal effect applies to explanation
   style too.

8. **"MVP focuses on deciding what to teach."** Agree, but I'd add that **diagnosing what the
   learner already knows** is half of "deciding what to teach" and the half most likely to be
   underbuilt. Evaluation also needs to be in the MVP, not deferred.

---

## 8. Important things the owner didn't ask about

1. **Reading the paper is the main event.** The brief frames this as "teach prerequisites,
   then (implicitly) the user reads". Most understanding will happen *during* reading.
   Supporting reading (adjunct questions at section boundaries, "explain this equation in your
   own words" prompts, on-demand "what is this?" lookups that create KCs on the fly) may be
   worth more than any prerequisite module. On-demand lookups during reading are also the best
   diagnostic signal you'll get: they reveal real gaps at the moment they matter.

2. **Connect everything to the learner's own research.** Questions like "how would this method
   apply to your emergent misalignment work?" use the *self-reference effect* and elaborative
   interrogation, and they are the most direct path to the stated goal (use and extend). Give
   the system a short, editable description of the user's active projects.

3. **Bootstrapping the learner model.** For an expert, a cold start is expensive. Seed it from
   the user's own papers, code repositories, reading history and a one-time self-assessment,
   then calibrate with probes.

4. **Interference between similar methods.** The user's fields are full of near-neighbor
   methods (influence functions, TracIn, datamodels, TRAK; various SAE variants). Similar KCs
   learned separately interfere. Teach them as **contrasting cases** with explicit
   discrimination questions. This is where the conditional KC type pays off.

5. **Metacognitive calibration as a feature.** Showing the user "you were 90% confident and
   right 55% of the time on mechanism questions" is itself a learning intervention, and it
   corrects the fluency illusion.

6. **Sustainability and motivation.** Most self-directed learning tools die from usage decay,
   not bad pedagogy. A capped, short, high-value daily session that visibly connects to the
   user's current work matters more than an optimal schedule that's ignored.

7. **Language learning is structurally different.** It is high-volume, procedural and
   automaticity-driven, with comprehensible input (Krashen) and spaced vocabulary as core
   activities, and fluency (speed) as an outcome, not just accuracy. The KC abstraction holds,
   but expect very different KC counts (thousands), activity types and scheduling. Don't let
   the ML-paper design hard-code assumptions such as "KCs are few and conceptual" or "answers
   are graded by an LLM rubric".

8. **Content quality control is the long pole, not the scheduler.** Budget for a critic
   pipeline (accuracy against sources, rubric conformance for questions, leakage checks) and for
   human spot-checks. Since compute is cheap, spend it here: generate several candidate
   explanations or questions, critique them and choose the best.
