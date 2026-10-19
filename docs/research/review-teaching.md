# Review of PLAN.md: teaching and learning-science perspective

Reviewer stance: learning science / instructional design. I read `docs/PLAN.md`, `brief.md`,
`lit-learning-science.md`, `expert-learning-scientist.md`, `expert-research-mentor.md`,
`expert-its.md`, `devils-advocate.md`, the Math Academy / Matuschak / Nielsen part of
`lit-products.md`, and spot-checked `lit-ai-methods.md`, `expert-llm-systems.md` and
`expert-language.md` for specific claims.

Overall: the plan is a faithful and unusually disciplined synthesis on the *what to teach* and
*measurement plumbing* side. Its weak side is the *teaching* side. It specifies in detail how
items are generated, checked and graded, but says little about what the learner actually does
with his head while reading, what happens after he gets something wrong, and how the paper's
argument (not just its prerequisites) gets learned. Those are exactly where "faster than reading
with a chat assistant" will be won or lost. The north-star instrument (the target exam) and the
Phase 3 exit test also have design problems that could make the whole project report success or
failure for the wrong reasons.

Issues are ordered by priority. Severity: **blocker** (fix before building the affected phase),
**major** (fix before Phase 3 is evaluated), **minor**.

---

## 1. The target exam is the north star, but it is unvalidated, coupled to the teaching pipeline, and reused as a teaching gate

**Severity:** blocker. **Sections:** §1, §4.2 step 1 and 6, §4.4 step 6, §5, §8.

**What's wrong**
- §5 gives every model decision a rubric and a κ ≥ 0.6 validation, *except the target exam*,
  which has neither a rubric row nor an owner-validation step. No phase exit checks it. Yet
  §1 makes it the measure of understanding and Phase 3's exit test depends on it.
- §4.2 says the paper map "is what the target exam is written against", and the map also drives
  requirement extraction (claims → requirements). The exam therefore shares its main upstream
  input with the teaching plan. An error or omission in the map (a missed load-bearing claim, a
  misread control) is invisible to measurement, because both the teaching and the test inherit
  it. The learning-scientist report asked for the opposite: a call "that cannot see the
  teaching plan", serving as the *sampling frame* for prerequisites.
- §1 says the exam is "never used in teaching", but §4.4 step 6 makes "passing the target exam"
  the stopping rule that moves a goal to gist mode. Once passing it changes what the system
  does, it is part of teaching (and invites teaching toward its questions after a failed
  attempt). No pass threshold is defined.
- "Ask a few questions before teaching" is a pretest, and pretests improve learning of exactly
  the prequestioned material (Pan & Carpenter 2023, cited in lit-learning-science finding 8).
  Those items will be inflated at post-test relative to the rest of the exam unless the same
  pretest is given in the "read with Claude" arm and the analysis separates pretested from
  non-pretested items.
- The exam is model-written, so it is subject to the documented bias of generated questions
  toward easy, lower-order items (lit-ai-methods §2 takeaway 5). Nothing guarantees it contains
  the mentor's critique-level questions (which control rules out which hypothesis, what the
  main weakness is).

**Suggested change**
- Add an "Exam" row to §5: covers each load-bearing claim with at least one *why / evidence /
  weakness / predict-if-changed* question; at most 20% definitional; each question answerable
  from the paper; key points per question. Validate it on Gold A papers: the owner rates each
  question "would an expert colleague ask this after a reading group?" before Phase 1 exits.
- Generate the exam from the paper text directly (not from the map), with a different model
  family from the map writer, and have it list the claims it thinks are load-bearing. Compare
  that list with the map's as a cheap independent check on the map.
- Add the mentor's learner-generated free-write as a second, instrument-independent outcome:
  before and after each paper (both arms), 10 minutes writing a 3-sentence summary, the main
  claim and its evidence, the biggest weakness, and one extension with a predicted result.
  Grade against OpenReview reviews or a follow-up critique where they exist.
- Separate the stopping rule from the exam: stop on a separate set of post-reading items (or the
  free-write), keep the exam purely for measurement, and define pass thresholds up front.
- Pre-test the same 2–3 exam items in both arms, and report pretested and non-pretested items
  separately.

---

## 2. The Phase 3 exit test cannot distinguish a working tool from practice effects

**Severity:** blocker. **Sections:** §6 causal checks, §8 Phase 3.

**What's wrong**
- The exit is "beats the read-with-Claude papers at equal or lower time, **or** time per paper
  drops clearly from paper 1 to paper 3 in the same area." The second branch will almost
  certainly pass with *any* method: the third paper in an area is faster to read because the
  learner has read two papers in it. The branch has no comparison condition, so it can't fail
  for the right reason.
- With 3–4 papers alternating between arms, there are 1–2 papers per arm. Variation in paper
  difficulty will swamp any tool effect. "Clearly" and "beat" have no numbers.
- The exit uses only immediate exam scores. The plan's own risk #3 (illusion of learning) is
  detected by *delayed* performance, and §1 schedules a 2–4 week retest, but the exit test
  ignores it. A tool that front-loads fluent explanations will look best at exactly the point
  where it is measured.
- Withholding teaching for ~20% of diagnosed gaps (§6) gives roughly one concept per paper if
  the plan's own estimate holds that 3–8 concepts matter (§7 risk 1). Worse, the withheld
  concepts are still explained on demand by "ask about this paragraph", so the holdout is
  contaminated. The comparison actually being run is "pre-taught vs. explained on request".

**Suggested change**
- Drop the "or time drops" branch as a pass condition. Test compounding against a control:
  the chat-arm papers in the same area should get faster too, so the claim is that tool-arm time
  drops *more*. Alternatively compare to the owner's logged time on matched papers before the
  tool existed.
- Use matched pairs within a sub-area, ordered ABBA, with at least 6 papers. Pre-register the
  thresholds (for example: tool arm ≥ 10 exam points higher at equal time, or ≥ 25% less time at
  equal score), and include the delayed exam in the exit test.
- Rename the holdout honestly as "pre-teach vs. on-demand only". That is a useful question in
  its own right, since it tells you whether diagnosis and pre-teaching beat a good reading
  companion. Pool it across papers, and don't expect significance before roughly 30 concepts.
- If 6+ papers is too much owner time for one phase, call Phase 3 a pilot with a qualitative
  go/no-go (time in paper vs. modules, stuck points resolved, owner's judgment) and move the
  quantitative test to a later phase. Don't present a 3-paper result as evidence.

---

## 3. The reading companion is the "chat with Claude" baseline with logging, and has no generative act

**Severity:** major. **Sections:** §0 item 2, §4.4 step 3, §4.5.

**What's wrong**
- The plan's main activity is guided reading with "ask about this paragraph" and "I got stuck
  here". It doesn't say how the companion answers. If it answers like a chat assistant, the
  plan's main activity *is* the baseline it has to beat, plus glosses.
- The research it synthesizes says unguarded LLM help is the harmful condition: unguarded
  GPT-4 raised practice scores and cut later unassisted performance by 17%, and a hint-first
  tutor removed most of that harm (Bastani 2025; lit-learning-science finding 10;
  lit-ai-methods §1, which lists withholding answers, try-first, short replies and reference
  solutions as what helped). The plan does not carry this over at all.
- Self-explanation prompts at key equations (Chi; Bisra g = 0.55) were a specific
  recommendation of the learning scientist (§1 point 5, §8 point 1) and of
  lit-learning-science finding 10 ("require an attempt ... before it reveals explanations").
  They are absent. The only generative acts during reading are 1–2 adjunct questions *after*
  each section.

**Suggested change**
- Specify a companion policy by disposition. For *gloss* concepts and notation, answer directly
  and briefly (an expert's time matters, and that is where chat is already good). For *teach*
  concepts and core-claim passages, ask first ("what do you think the second term of eq. 4 is
  doing?"), with one-tap "just tell me". Log whether he attempted, and what he got right, as
  evidence.
- Add a self-explanation prompt at each equation or algorithm block that the requirement step
  marks as core (the mechanical sweep already finds them): "in one line, what does this term
  do / why is it here?" Grade it lightly or not at all; its value is the generation.
- Give the companion the reference explanation and spans so it stays grounded, and test its
  answer-withholding on a small MRBench-style set before Phase 3 (models vary from 53% to 95%).

---

## 4. Corrective feedback and remediation after an error are unspecified

**Severity:** major. **Sections:** §4.1 credit and blame, §4.3, §4.4, §4.5 grading.

**What's wrong**
- The research is clear that feedback and retesting are the active ingredient. Von Hippel
  attributes about 1.1 SD of Bloom's effect to feedback and retesting; mastery learning works
  through corrective feedback; testing transfers to application only with explanatory feedback
  (Pan & Rickard; lit-learning-science §5 implications). The plan specifies grading in detail
  as *measurement* (key points, cross-family graders, κ), but never says what the learner sees
  after an answer, or what happens next.
- After a failure, §4.1 charges the diagnosed concept and adds "doubt" to dependents. There is no
  remediation policy: re-explain differently? Retry later with a new variant (Math Academy
  pauses and retries, with 80% second-try success, then reviews key prerequisites after a second
  failure)? Drill down a level?
- §4.3 says pretesting helps "even when the attempt fails". The source says *provided feedback
  follows*. The triage and probe flow doesn't say whether he is shown the right answer.

**Suggested change**
- Add a "Feedback" rubric row to §5: after every graded answer, show the missed key points, *why*
  they matter (one or two sentences, tied to a span), and the specific misconception if one was
  tagged. Terse by default, expandable.
- Define a remediation ladder in §4.4: (1) explanatory feedback now; (2) a new variant at the
  same depth later in the session or the next one; (3) after a second miss, probe the requires-
  parent the grader named; (4) after a third, flag the concept or explanation for owner review
  (it may be the explanation that is wrong, or the item).
- Make every diagnostic probe end with brief feedback, so the pretest effect the plan relies on
  actually occurs.

---

## 5. The paper's argument and critique level are presented, not practised

**Severity:** major. **Sections:** §0 item 1, §4.1 concept and depth levels, §4.4 session shape.

**What's wrong**
- The mentor's central claim is that what blocks understanding is rarely a definition. It is
  knowing which few things carry the weight, why the authors made their choices, and what the
  result would look like if wrong. The devil's advocate's first criticism (§1.1) was that the
  atomic pool scattered the *argument*. The plan fixes the store (concepts) but the argument
  now lives only in the paper map, which the learner *reads* first. Claims become "question
  seeds attached to concepts". Nobody is asked to reconstruct the chain problem → idea → method
  → evidence → conclusion.
- Depth levels are recognize → explain → apply → extend. The mentor's levels are skim → follow
  the argument → critique → reproduce → extend, with critique called out as the key level for
  emergent misalignment. "Critique" (which control rules out which hypothesis, what's the main
  weakness) is a property of claims and evidence, not concepts, and has no place in the model.
- Showing a fluent, expert-quality map first is the setup for an illusion of explanatory depth.
  He will feel he understands the paper before reading it. The plan also drops the mentor's
  step 4 "sharpen on a second pass" (and Keshav's pass 3), and the learning scientist's
  consolidation step (retrieval "same session to a few days later").
- Nothing is spaced. The paper is read, examined and moved to gist mode in one burst.

**Suggested change**
- Make "the argument of paper P" a first-class paper-local unit with critique depth, and track
  evidence against it. Its items: reconstruct the chain, explain Figure N without the paper,
  name the control that rules out H, predict the ablation result, state the main weakness.
- Turn the map into a generative activity: show the problem first and ask "how would you
  approach this, and what goes wrong with the obvious approach?" (the problem-first move the
  plan already endorses for concepts), then reveal the map. After reading, ask him to
  reconstruct the argument in 3–5 lines *before* showing the map again for comparison.
- Add a short consolidation session 1–3 days after reading: 5 minutes of retrieval on the
  argument and the core concepts. This is also when the second-pass "sharpening" items (derive,
  what breaks if, design an extension) belong.
- Add a quota to §5's requirement-set rubric: at least N items per paper at critique level.

---

## 6. Diagnosis contradicts its own sources on self-report, and assessment overhead will bore an expert

**Severity:** major. **Sections:** §4.3, §6 process health, §8 Phase 2 exit.

**What's wrong**
- §4.3's triage screen shows the full candidate list (50 concepts, "about two minutes"). The
  research mentor said explicitly: "Don't present a 50-concept checklist. Ask 5–8
  discriminating questions on the central prerequisites, and infer down the graph." Math
  Academy forbids self-edited profiles because "learners have a tendency to massively
  overestimate self-reported knowledge". The two-minute figure has no source.
- The Phase 2 exit "diagnosis removes ≥ 60% of candidates in under 10 minutes" is ill-posed. The
  removal rate depends mostly on how over-inclusive extraction was, and Phase 1 is trying to
  push precision up. A good extractor *should* make the removal rate fall. The ITS expert's
  "60–80% in 10–15 minutes" was experience-based, and the plan tightens it to 10 minutes
  without evidence.
- Add up the per-paper assessment load: a few pre-exam questions, a 50-item triage, verifying
  probes, top-down probes, one question per taught gap, 1–2 adjunct questions per section, post-
  reading items, 10–15 exam questions, homework, a project question, and later a delayed exam.
  That is roughly 40–60 responses per paper, *on top of* reading. Matuschak measured 35–50%
  reading-time overhead for embedded prompts and readers called it "like homework" and "a
  reflection of my own intellectual inadequacy". The mentor warns researchers drop tools that
  feel like school. The plan has a review budget, but no assessment budget.

**Suggested change**
- Replace the full triage list with (a) priors from his profile and earlier papers, (b) 5–8
  discriminating probes on central concepts, chosen by expected information gain, and (c) a
  *collapsed* list of the remaining peripheral candidates he may scan or ignore. Self-report
  only moves peripheral concepts.
- Change the Phase 2 exit to accuracy: of the concepts diagnosis marks known, ≥ 90% pass a later
  spot-check; of those marked gaps, ≤ 30% are "already knew" when taught; total diagnosis time
  ≤ 10 minutes.
- Add an assessment budget per paper (e.g. ≤ 20% of reading time, measured) and let one response
  serve several purposes: the exam pre-questions double as diagnosis, adjunct questions double
  as evidence for the concepts the passage depends on (the ITS expert already proposed this).
  Track "assessment minutes / reading minutes" as a process-health metric.

---

## 7. The interference rule contradicts the contrasting-cases evidence, and contrast is this user's subject matter

**Severity:** major. **Sections:** §4.4 rules, §4.1 edge types.

**What's wrong**
- §4.4 says "don't introduce two confusable concepts in the same session" and "contrasts come
  after both sides are acquired". This follows Math Academy's non-interference rule (for
  multiplication facts) and the ITS expert.
- The learning scientist (§8 point 4) recommends the opposite for this user: near-neighbour
  methods (influence functions, TracIn, datamodels, TRAK; SAE variants) should be *taught as
  contrasting cases* with discrimination questions. Case comparison gives d = 0.50 (Alfieri
  2013), comparison during encoding improves transfer (Gentner 2003), and interleaving helps
  most for confusable categories (Brunmair & Richter). The plan silently picks one side of a
  real disagreement in its sources.
- For this user it matters a lot: many papers' contribution *is* a contrast with a known method
  (EK-FAC vs. K-FAC, TopK vs. L1, PBRF vs. leave-one-out). Delaying the contrast until the new
  concept is "acquired" in isolation means teaching it out of the frame in which it makes sense.

**Suggested change**
- Rewrite the rule: introduce a new concept *by comparison* with its known neighbour whenever
  one exists (only one side is new, so the interference risk is small). Don't introduce two
  *new* confusable concepts in one session unless the comparison is the paper's point, in which
  case teach them together as a contrast with a discrimination item, stating the principle after
  the comparison (Alfieri).
- Record in §2 or §4.4 that this is a deliberate departure from Math Academy, and why
  (interference evidence is strongest for low-level paired associates; comparison evidence is
  strongest for conceptual transfer).

---

## 8. Learner agency and his own research are underweighted

**Severity:** major. **Sections:** §2 (effort), §4.4, §4.7, profile (not specified).

**What's wrong**
- The plan sides firmly with "system picks the activity" (correctly, on Kornell & Bjork), but
  drops the countervailing findings: Matuschak's main conclusion from the mnemonic medium is
  that "the medium should give readers control over which prompts they collect", and his recent
  work is on reader control and highlight-driven practice. His review of Math Academy found the
  black-box queue produced "emotional disconnect and a feeling of passivity"; another reviewer
  quit over unskippable prerequisites. lit-products' synthesis explicitly flags this tension.
  The plan's only agency features are "why am I seeing this?" and override.
- Both the learning scientist and the mentor named the link to his own research as the
  strongest lever for "use and extend" (self-reference effect; "it's what students remember").
  Matuschak's "How might we learn?" scenario, the closest match to this product, has practice
  "grounded in the details of Sam's BCI project", deepening over time, and steerable. The plan
  has one "how does this apply to your project?" question at the end of a paper, and the profile
  has no editable description of his active projects.

**Suggested change**
- Add an editable "active projects" section to the learner profile, and make project-grounded
  items a standing item type at apply/extend depth for reusable concepts, including in
  maintenance (the learning scientist's "transfer" stage).
- Let him collect and pin: highlighting a passage or tapping "keep this" promotes a concept or
  claim to *teach*/maintained regardless of the computed disposition, and "drop this" demotes it.
  Both are logged as labels. Let him skip or claim any node, verified by one cheap probe
  (Math Academy's conditional completion), and show the path from where he is to the paper.

---

## 9. "Use and extend" depends on procedure and hands-on work that the plan defers

**Severity:** major. **Sections:** §4.4 step 5, §4.5, §8 Later.

**What's wrong**
- The mentor says homework (derivations, small implementations, design/critique problems) is
  "the only route to extend level", and the learning scientist recommends it for the 1–2 concepts
  per paper he plans to extend. The plan has one *optional* homework item per paper, and
  code-verified homework is in "Later".
- The procedure type exists, but the research's state-dependent format mapping (new → explanation
  plus worked example; shaky → faded example; solid → varied application; lit-learning-science
  finding 7, §6) is not in the planner. "System picks the activity" has no table saying how.

**Suggested change**
- In Phase 3, for each paper's 1–2 core method concepts, make an ungraded "predict, then run"
  exercise the default (opt-out, not opt-in): a ~50-line toy implementation or a derivation with
  a reference solution he checks himself. This needs no grading machinery (the learning
  scientist's MVP suggestion).
- Add a format-by-state table to §4.4 for each concept type (term, mechanism, procedure,
  contrast, claim/argument), including worked → faded → independent for procedures and
  "skip the example for concepts adjacent to his expertise" (expertise reversal).

---

## 10. Depth levels, facets and contrast are three overlapping axes; the learner state is underspecified

**Severity:** major (blocks implementation of §4.1 and §4.4). **Sections:** §4.1, §4.4.

**What's wrong**
- Concepts have depth levels (recognize / explain / apply / extend). Learner state is per
  (concept, *facet*) with facets explain / apply / choose. Requirements carry a "depth needed".
  "Explain" and "apply" appear on both axes. "Contrast" is simultaneously a concept type, an
  edge type (`contrasts`), and a facet ("choose"). It is not specified whether acquisition at
  "apply" implies "explain", how an item at depth d updates the state at other depths, or what
  "known" means for the readiness gate (known at which depth?).
- §4.1 attributes "failure charged only to the diagnosed concept; dependents get doubt" to
  Math Academy's FIRe. FIRe sends penalties *up* to dependent topics; the "doubt, no penalty"
  rule is the ITS expert's modification. LLM-set `encompasses` weights are also unvalidated
  (lit-learning-science open question 3; Math Academy's took about 250 hours of expert time).

**Suggested change**
- Pick one axis for ML: depth levels per concept, with "choose" handled by contrast concepts
  (a contrast is its own unit, as the ITS expert recommended). Facets stay a language-domain
  plug-in. State that the depth levels are cumulative, that an item at depth d gives full credit
  at d and partial below, and that readiness requires the parent at the *depth the requirement
  needs*.
- Attribute the blame rule correctly, and mark encompass weights as an untested hypothesis to be
  checked by replaying the log (predicted vs. actual retention for implicitly credited concepts).

---

## 11. Other exit-criteria problems

**Severity:** major (Phase 0/1), minor (Phase 4). **Section:** §8.

- **Phase 0** "the owner trusts the gold labels" is not a test. Gold A is retrospective: an
  expert annotating papers he already understands can't reliably recall what he didn't know
  (expert blind spot, flagged in lit-learning-science §2). Only one stuck-point read is
  planned, yet Phase 1's recall target uses stuck points. Suggest: 2–3 stuck-point reads, with
  stuck-point recall reported separately from Gold A recall and treated as primary; exit when
  two annotation passes on one paper a week apart agree on the "3 things that matter most".
- **Phase 1** exits without checking the paper map or the target exam (issue 1), even though
  both are built in this phase and Phase 3 depends on them. Add map and exam validation on
  Gold A.
- **Phase 2** "item defect rate under 10% on owner review": Memory Machines found models can't
  separate "needs refactor" from "needs polish", and the T1 defect ("won't survive
  long-horizon review") only shows up over time. Creation-time review will understate it. State
  the sample size (≥ 50 items across ≥ 3 papers), and re-audit after a month of use.
- **Phase 4** has no exit test, which breaks the rule at the top of §8. The withheld-maintenance
  test needs 1–3 months to read out; say so and make the exit "delayed probe accuracy on
  maintained concepts exceeds withheld ones, at ≤ N review minutes/day".
- **Calibration** is an outcome metric (§6), but the evidence row (§4.1) logs only the *model's*
  predicted P(correct), not the learner's confidence. Add an optional 1–3 confidence tap. Also
  consider showing calibration to him, which the learning scientist calls an intervention in its
  own right.

---

## 12. Fidelity: claims in the plan that the research doesn't support or overstates

**Severity:** minor (each one), but worth fixing because the plan is used as the source of truth.

| Plan says | Research says | Fix |
|---|---|---|
| §0.2 "Every expert independently put a reading companion at the center" | True of the learning scientist, ITS expert and mentor; the LLM-systems expert lists it as stage 12 and calls it necessary for evaluation; the language expert doesn't address papers | "Every expert who addressed papers..." |
| §0.3 "Every expert ranked [diagnosis] first or second" | ITS expert: #1 risk. Learning scientist: #2. LLM-systems: #1 (over-teaching). The mentor ranks prerequisite explosion #1 and puts diagnosis in the MVP, but doesn't rank it | Soften to "the three tutoring-oriented experts ranked over-teaching first or second" |
| §0.5 "LLMs define over 86% of made-up terms (PhantomBench)" | "Average hallucination rates *reach* 86.7%", from a secondary summary (emergentmind), across 21 models with wide variation | "up to ~87% in one benchmark (secondary source)" |
| §4.5 grounding with graded examples "from the same kind of passage" raised precision 56% → 78% | The Memory Machines result was for graded examples *from the same passage* | Say "same passage"; treat "same kind of passage" as an untested extension |
| §4.3 "Pretesting ... improves later learning, even when the attempt fails" | "provided feedback follows" (Pan & Carpenter) | Add the condition (see issue 4) |
| §4.1 blame rule attributed to Math Academy FIRe | FIRe propagates penalties upward; the doubt rule is the ITS expert's | See issue 10 |
| §4.3 "Fifty concepts take about two minutes" | No source; the mentor advises against a 50-item checklist | See issue 6 |
| §8 Phase 2 "≥ 60% in under 10 minutes" | ITS expert: "typically ... 60–80% in 10–15 minutes", experience-based | See issue 6 |

Things the plan represents well and should keep: retrieval-only maintenance credit, value-weighted
retention with paper-local decay, user picks time and system picks activity, "why am I seeing
this", target practice success of 70–85%, structural (not self-reported) detection of unknowns,
the reading-guide comparison arm in Phase 1, and the decision rule that demotes the concept store
if the one-shot guide matches it.

---

## 13. Smaller underspecified items

**Severity:** minor.

- **Sessions vs. sections.** "At most 2–3 new concepts per session" and "teach the 1–3 gaps
  blocking each section" together imply a paper with 6–8 gaps spans several sessions. Say
  whether that's intended, and add the mentor's warning signal (> 1 hour before the first
  "I get what this paper is doing").
- **Phone vs. paper.** The effort example "10 minutes, phone" doesn't fit guided reading of a
  LaTeX paper. List which activities are phone-able (reviews, argument retrieval, contrast items)
  and which are desk-only.
- **What counts as learner time** in "understanding per learner-minute": say explicitly that
  diagnosis, exams and companion chats are all counted, in both arms.
- **Analogies.** §4.5 asks for each analogy to say where it breaks, which is good, but the
  research also recommends *several* analogies for complex concepts (Spiro) and leading with the
  problem or the technical statement for concepts near his expertise. The second is in §2; the
  first is missing.
- **Cross-paper field maps** (mentor) and **literature context / critiques** are only covered by
  one line in the paper map. They are high-value for this user and cheap once the concept store
  exists; add them to "Later" at least.
