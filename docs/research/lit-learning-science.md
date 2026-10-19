# Literature review: learning science and intelligent tutoring for "what to teach, in what order, and how to practice it"

Scope: learning-science and ITS research that bears on the brief (`docs/research/brief.md`):
choosing knowledge components (KCs), ordering them, tracing what the learner knows, choosing
practice formats and effort levels, and keeping knowledge over time. It also covers the
ADEPT / "blurry-to-sharp" question added to the brief: overview-first vs prerequisite-first.

Method note: this was compiled from web searches and fetches in October 2026. The search budget
ran out before every number could be re-checked against a primary PDF. Claims marked
**(unverified)** come from my prior knowledge of the paper; the link points to the paper or a
summary of it, but the exact figure was not re-confirmed in this session.

Evidence-strength labels used below:
- **Strong**: several meta-analyses or many replications, including classroom or delayed tests.
- **Moderate**: a meta-analysis with large heterogeneity, or a few solid experiments.
- **Weak**: single studies, practitioner reports, or vendor claims.

---

## 1. Ten decision-relevant findings

1. **Retrieval, not re-exposure, should be the default way knowledge is maintained.** Practice
   tests beat restudy and other comparison conditions with g = 0.61 over 272 effect sizes
   ([Adesope et al. 2017](https://journals.sagepub.com/doi/10.3102/0034654316689306)). Once an
   item could be recalled, more studying had no effect on delayed recall while more testing had
   a large one ([Karpicke & Roediger 2008](https://www.brucehayes.org/Teaching/papers/2008_Roediger_Karpicke_Science.pdf)).
   Rereading a chapter gave essentially no gain over reading it once
   ([Callender & McDaniel 2009](https://profiles.wustl.edu/en/publications/the-limited-benefits-of-rereading-educational-texts/)).
   **So the system should** treat "no effort" items (reading, podcasts) as first exposure or
   priming, never as the thing that marks a KC as maintained. Maintenance credit should come
   only from a retrieval event.

2. **Practice at the level you want to use the knowledge.** Fact quizzes improved later fact
   tests but *not* higher-order tests, while higher-order or mixed quizzes improved higher-order
   tests, with no need to build the fact base first
   ([Agarwal 2019](https://retrievalpractice.org/blooms)). Testing does transfer to new
   inferential questions: about twice the restudy group's score on factual items and about 50%
   higher on conceptual ones ([Butler 2010](https://profiles.wustl.edu/en/publications/repeated-testing-produces-superior-transfer-of-learning-relative-/)).
   But transfer is weaker for application and inference than for rephrased questions
   ([Pan & Rickard 2018](https://escholarship.org/content/qt45x0w7t8/qt45x0w7t8.pdf)).
   **So the system should** make application and discrimination questions ("which method fits
   this situation?", "what happens if…?") the main practice for conceptual KCs. Atomic
   definition cards are supporting material, not the main event. For a user who wants to *use
   and extend* methods, flashcards alone will not get them there.

3. **Separate the scheduled unit (the KC) from the question shown.** Prompt-writing advice wants
   each prompt focused, precise and *consistent*, because inconsistent answers risk
   retrieval-induced forgetting ([Matuschak, "How to write good prompts"](https://andymatuschak.org/prompts/);
   [Wozniak, 20 rules](https://supermemo.guru/wiki/20_rules)). Transfer research wants varied
   questions (finding 2). These fit together if memory state is tracked per KC and each review
   draws a different but tightly targeted variant. Each variant still has one short, checkable
   answer. **So the system should** schedule KCs and generate a fresh variant at each review
   from a per-KC pattern (apply, contrast, predict, diagnose). Every variant should test the
   same KC, so the memory model's evidence stays about one thing.

4. **Space reviews on an expanding schedule driven by a per-learner memory model, and err
   long rather than short.** The best gap grows with the retention interval: about 20–40% of a
   1-week horizon, falling to 5–10% of a 1-year horizon. Too short a gap hurts more than too
   long ([Cepeda et al. 2008](https://pubmed.ncbi.nlm.nih.gov/19076480/)). Personalized
   model-driven review beat massed study by 16.5% and generic spacing by 10% in a semester-long
   class ([Lindsey et al. 2014](https://home.cs.colorado.edu/~mozer/Research/Selected%20Publications/reprints/LindseyShroyerPashlerMozer2014.pdf)).
   **So the system should** use an off-the-shelf memory model (FSRS-style; see §5) per KC,
   rather than invent one, and spend design effort on what counts as a review.

5. **Use prerequisite structure plus mastery gating, but expect the gains to come from
   feedback, correction and good content, not from clever sequencing.** Mastery learning
   averages +0.52 SD ([Kulik et al. 1990](https://www.academia.edu/81783373/Effectiveness_of_Mastery_Learning_Programs_A_Meta_Analysis);
   see also the [Slavin 1987 critique](https://Www.Gwern.net/doc/psychology/1987-slavin.pdf)). Re-analysis of
   Bloom's "2 sigma" attributes about 1.1 SD of it to feedback and retesting, and sets a
   realistic tutoring effect near 0.33 SD
   ([von Hippel 2024](https://www.educationnext.org/two-sigma-tutoring-separating-science-fiction-from-science-fact/)).
   ALEKS, the flagship knowledge-space system, came out "as good as, but not better than"
   classroom teaching ([Fang et al. 2019](https://digitalcommons.memphis.edu/facpubs/7254)).
   RL-optimized sequencing has a mixed record against reasonable baselines
   ([Doroudi, Aleven & Brunskill 2019](https://dx.doi.org/10.1007/s40593-019-00187-x)).
   **So the system should** spend its model budget on correct KCs, correct prerequisite edges
   and high-quality explanations and questions with corrective feedback. A simple frontier
   rule is enough for sequencing: teach the most important unmastered KC whose prerequisites
   are mastered.

6. **KC granularity is an empirical question that data can settle; start with LLM-proposed
   KCs and refine them from learning curves.** In KLI, KCs are the unit that explains
   transfer between tasks ([Koedinger, Corbett & Perfetti 2012](https://kilthub.cmu.edu/articles/journal_contribution/The_knowledge-learning-instruction_framework_bridging_the_science-practice_chasm_to_enhance_robust_student_learning_/6470522)).
   Learning Factors Analysis and the Additive Factors Model split or merge KCs until error
   rates fall smoothly with practice
   ([Cen, Koedinger & Junker 2006](https://learnlab.org/wp-content/uploads/2025/07/CenKoedinger-Junker-05pdf.pdf);
   [closing-the-loop study](https://jedm.educationaldatamining.org/index.php/JEDM/article/download/212/pdf_29)).
   GPT-4-generated KCs were often preferred to human ones by domain experts
   ([Moore et al. 2024](https://arxiv.org/abs/2405.20526v1); see also
   [KCGen-KT](https://arxiv.org/html/2502.18632v2)). **So the system should** log each question
   with the KCs the grader blames for a miss (an on-the-fly Q-matrix). With enough data, it
   should flag KCs whose curves are flat or jagged (granularity is wrong) and offer to split or
   merge them.

7. **Match the format to the learner's current expertise on that KC; don't leave it entirely
   to the learner.** Worked examples help novices (g = 0.48 in math,
   [Barbieri et al. 2023](https://oaks.kent.edu/hcri/meta-analysis-worked-examples-effect-mathematics-performance)),
   but the advantage reverses as expertise grows (the expertise reversal effect,
   [Kalyuga 2007](https://www.uky.edu/~gmswan3/EDC608/Kalyuga2007_Article_ExpertiseReversalEffectAndItsI.pdf)).
   Learners systematically prefer the easier, less effective option: they rated massed study
   as better even after doing worse with it ([Kornell & Bjork 2008](https://bjorklab.psych.ucla.edu/wp-content/uploads/sites/13/2016/07/Kornell_Bjork_2008_PsychScience.pdf)),
   and students in active classes learned more but felt they learned less
   ([Deslauriers et al. 2019](https://uateachingacademy.ua.edu/research/research-roundup-active-learning-vs-full-lectures-what-really-enhances-learning/)).
   **So the system should** recommend an activity per KC from its state: new means
   explanation plus worked example; shaky means faded example or easy retrieval; solid means
   varied application problems. The user picks how much *time* to spend, not which kind of
   practice the KC gets.

8. **Ask before you teach.** Pretests and prequestions improve learning of the material they
   target even when the answers are wrong, provided feedback follows
   ([Pan & Carpenter 2023 review](https://link.springer.com/10.1007/s10648-023-09805-6)).
   Short "first-step" diagnostics can assess task expertise in seconds and drive adaptive
   tutorials ([Kalyuga, rapid assessment](https://igi-global.com/chapter/adaptive-procedures-efficient-learning/25741)).
   Trying a problem before instruction helps conceptual understanding
   ([Sinha & Kapur 2021](https://www.weforum.org/stories/2021/09/students-who-productively-fail-learn-more/)).
   **So the system should** open each candidate prerequisite with one or two diagnostic
   questions. That both decides whether the KC needs teaching (saving an expert user's time)
   and primes learning when it does.

9. **Overview first, then prerequisites just in time, then sharpen. This combines
   "blurry-to-sharp" with a prerequisite graph rather than choosing one.** Pre-training on the
   names and behaviour of the main components gives a median d = 0.75
   ([Mayer, pretraining principle](https://cambridge.org/core/books/cambridge-handbook-of-multimedia-learning/principles-for-managing-essential-processing-in-multimedia-learning-segmenting-pretraining-and-modality-principles/DD24C2F48B9B1277CE59F78276110258)).
   Presenting elements in isolation first, then together, helps novices with high
   element-interactivity material ([Pollock, Chandler & Sweller 2002](https://ro.uow.edu.au/edupapers/145)).
   Whole-task, simple-to-complex 4C/ID programs show d = 0.79
   ([Costa et al. 2022](https://ciencia.iscte-iul.pt/publications/the-four-component-instructional-design-model-4cid-a-meta-analysis-on-use-and-effect/81383?lang=en)).
   Comparing cases gives d = 0.50 ([Alfieri et al. 2013](https://www.lrdc.pitt.edu/Schunn/papers/ContrastingCasesMeta-AlfieriEtAl2013.pdf)).
   But a single analogy can plant misconceptions that later block understanding
   ([Spiro et al. 1989](https://www.cambridge.org/core/books/similarity-and-analogical-reasoning/multiple-analogies-for-complex-concepts-antidotes-for-analogy-induced-misconception-in-advanced-knowledge-acquisition/FF07DBE3F194DB258119713D3000E730)).
   **So the system should** start each goal with a short whole-picture orienting explanation
   of what the paper does and why, using analogy and diagram. That orientation is *not* a
   mastery claim. Next come gated prerequisite KCs, then the paper's own KCs. Analogies should
   be plural and should state where they break. See §8.

10. **LLM tutoring helps only with guardrails that force the learner to generate.** Unguarded
    GPT-4 access raised practice scores but cut later unassisted performance by 17%. A tutor
    prompted to give hints rather than answers removed most of that harm
    ([Bastani et al. 2025, PNAS](https://papers.ssrn.com/abstract=4895486)). A
    pedagogically scaffolded AI tutor produced more than double the learning gains of an
    active-learning class, in less time ([Kestin et al. 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12179260/)).
    Self-explanation prompts give g = 0.55 ([Bisra et al. 2018](https://www.Gwern.net/doc/psychology/spaced-repetition/2018-bisra.pdf)),
    and generating beats reading by d = 0.40 ([Bertsch et al. 2007](https://pubmed.ncbi.nlm.nih.gov/17645161/)).
    **So the system should** require an attempt (answer, prediction or self-explanation)
    before it reveals explanations in quizzes and homework, and should give the explaining and
    grading agents explicit rubrics for this.

---

## 2. Knowledge components, KLI, Q-matrices and granularity

**Findings**

- **KLI framework.** Koedinger, Corbett & Perfetti (2012) separate observable events
  (instructional and assessment events) from unobservable learning events and **knowledge
  components**. A KC is "an acquired unit of cognitive function or structure that can be
  inferred from performance on a set of related tasks." KLI classifies KCs by
  application-condition and response type (constant/variable) and argues that different kinds
  of KC need different instruction: memory and fluency processes need spacing and retrieval,
  induction needs varied examples and comparison, and understanding needs explanation and
  self-explanation
  ([paper, KiltHub](https://kilthub.cmu.edu/articles/journal_contribution/The_knowledge-learning-instruction_framework_bridging_the_science-practice_chasm_to_enhance_robust_student_learning_/6470522);
  [preprint PDF](https://home.cs.colorado.edu/~mozer/Teaching/syllabi/TopicsInCognitiveScienceFall2011/KLI-paper-v5.00.pdf)).
  *Relevance:* a paper's concepts mix constant facts ("Gauss-Newton is PSD"), variable-condition
  skills ("given this loss, which approximation applies?") and principles. The KC type should
  pick the practice type. **Evidence: framework (theory), widely used in ITS.**
- **Q-matrix.** A Q-matrix maps each item to the KCs it requires. Additive Factors Model
  (AFM) and Performance Factors Analysis fit success probability as a function of KC easiness
  and practice counts ([Cen, Koedinger & Junker 2006](https://learnlab.org/wp-content/uploads/2025/07/CenKoedinger-Junker-05pdf.pdf);
  [Knowledge Tracing Machines, which generalizes AFM/PFA](https://arxiv.org/pdf/1811.03388)).
- **Granularity is chosen by fit.** Learning Factors Analysis searches over splits and merges
  of KCs, guided by human-proposed factors, and keeps the model that best predicts performance
  (BIC/cross-validation). A "good" KC model produces smooth, declining learning curves
  ([LFA](https://learnlab.org/wp-content/uploads/2025/07/CenKoedinger-Junker-05pdf.pdf)).
  A refined KC model, used to redesign a tutor, led to faster learning in a follow-up classroom
  study ([Liu & Koedinger, "Closing the loop", JEDM](https://jedm.educationaldatamining.org/index.php/JEDM/article/download/212/pdf_29)).
  DataShop is the public infrastructure for this ([DataShop accomplishments](https://learnlab.org/?p=33)).
  **Evidence: moderate (several datasets; closing-the-loop studies are few).**
- **KC modelling is hard in non-math domains.** Expert-blind-spot and ill-structured domains
  make KC identification hard
  ([Challenges of KC modeling: software-engineering case study](https://www.academia.edu/84593925/Challenges_of_Knowledge_Component_Modeling_A_Software_Engineering_Case_Study)).
- **LLM-generated KCs.** GPT-4 KCs for chemistry and e-learning MCQs were judged against human
  KCs by domain experts, who often preferred the LLM's. An unsupervised clustering grouped
  questions by KC ([Moore, Schmucker, Mitchell & Stamper 2024](https://arxiv.org/pdf/2405.20526)).
  KCGen-KT generates KCs for programming problems and uses them in an interpretable KT model,
  matching or beating human KCs ([arXiv 2502.18632](https://arxiv.org/html/2502.18632v2)).
  **Evidence: moderate, but all on fixed question banks. None on a growing, goal-driven pool.**

**Implications**

- Treat KC boundaries as hypotheses. Store item→KC attributions from the LLM grader and
  revisit granularity when curves look wrong. The "compound fact" problem seen in the
  prototype's first ingestion run (owner's notes in `~/wiki/pages/fact-pool-learning-tool-design.md`)
  is exactly the problem LFA formalizes.
- With one user, learning-curve refinement will be data-starved for a long time. Cross-KC
  pooling (KCs of the same *type* likely have similar curves) and LLM priors will have to
  carry most of the weight.

---

## 3. Prerequisite structure: knowledge spaces, mastery learning, Math Academy

**Findings**

- **Knowledge space theory (KST) / ALEKS.** A knowledge state is the set of items a learner
  can do. The feasible states form a "knowledge space" determined by prerequisite relations.
  The "outer fringe" of the state is what the learner is ready to learn next. Adaptive
  assessment finds the state in a small number of questions
  ([ALEKS / KST overview](https://www.mheducation.com/content/dam/mhe/research/prek-12/essa-tier-4/aleks-practical-perspective-knowledge-space-theory.pdf)).
  Outcome evidence: a meta-analysis of 15 studies (24 samples) found ALEKS **as good as, not
  better than** traditional instruction, with larger effects for shorter use
  ([Fang, Ren, Hu & Graesser 2019](https://digitalcommons.memphis.edu/facpubs/7254)).
  **Evidence: strong for "KST assessment works", weak-to-null for "KST-sequenced instruction
  beats teachers".**
- **Mastery learning.** 108 controlled evaluations gave an average +0.52 SD on exam
  performance, with stronger effects for weaker students but more time on task
  ([Kulik, Kulik & Bangert-Drowns 1990](https://www.academia.edu/81783373/Effectiveness_of_Mastery_Learning_Programs_A_Meta_Analysis)).
  Slavin argued effects shrink on standardized measures and longer studies
  ([Slavin 1987](https://Www.Gwern.net/doc/psychology/1987-slavin.pdf)). Bloom's "2 sigma"
  came from two small, three-week dissertations that combined tutoring with mastery feedback.
  Von Hippel estimates a realistic tutoring effect near 0.33 SD and attributes about 1.1 SD of
  Bloom's figure to feedback and retesting alone
  ([von Hippel 2024](https://www.educationnext.org/two-sigma-tutoring-separating-science-fiction-from-science-fact/);
  [Bloom 1984](https://web.mit.edu/5.95/readings/bloom-two-sigma.pdf)).
  **Evidence: moderate-strong for mastery + corrective feedback.**
- **Math Academy.** It uses a hand-built prerequisite graph, an adaptive diagnostic to find
  the "knowledge frontier", mastery-gated progression with "layering", spaced repetition,
  interleaved review, and quizzes calibrated to about 80% expected score
  ([How our AI works](https://mathacademy.com/how-our-ai-works);
  [The Math Academy Way (draft book)](https://justinmath.com/files/the-math-academy-way.pdf)).
  **FIRe** (Fractional Implicit Repetition) adds a second graph of *encompassings* with
  fractional weights. Success on an advanced topic sends partial review credit down to the
  topics it implicitly practices, failure sends penalties up to dependent topics, and reviews
  are chosen to "knock out" other due reviews
  ([Skycak, FIRe](https://www.justinmath.com/individualized-spaced-repetition-in-hierarchical-knowledge-structures/)).
  Skycak acknowledges "we don't have any official academic studies out at the moment" and that
  building encompassing weights is laborious expert work (same source).
  **Evidence: weak (vendor outcomes, no controlled studies), though each ingredient is
  individually well supported.**
- **RL / model-based sequencing.** Doroudi, Aleven & Brunskill's review of decades of
  RL-for-instructional-sequencing studies found that RL policies beat baselines in only some
  studies. Successes clustered where a well-grounded psychological model existed (e.g.
  paired-associate memory and spacing) and against weak baselines. Results were weaker for
  concept learning **(details unverified; [paper](https://dx.doi.org/10.1007/s40593-019-00187-x))**.

**Implications**

- A prerequisite graph is useful mainly for three things: (a) not teaching something whose
  pieces are missing, (b) diagnosing efficiently (KST-style inference: if they know X they
  probably know its prerequisites), and (c) implicit-review credit (FIRe). Do not expect
  sequencing optimization itself to be the source of large gains.
- For conceptual ML material, "encompassing" is fuzzier than in math. A scenario question
  about influence functions only partially exercises "Hessian definition". LLM grader
  attribution per miss (finding 6) is a plausible substitute for hand-set FIRe weights, but
  it is untested.

---

## 4. Knowledge tracing and next-item selection

**Findings**

- **BKT** (Corbett & Anderson 1995) models each KC as a two-state hidden Markov model with
  learn, guess and slip parameters. **AFM/PFA** are logistic models over KC difficulty and
  success/failure counts ([KTM overview](https://arxiv.org/pdf/1811.03388)). **DKT** (Piech et
  al. 2015, [arXiv](https://arxiv.org/abs/1506.05908)) uses an RNN over interaction sequences.
- **Depth buys little.** BKT extended with forgetting, skill discovery and individual ability
  matched DKT ([Khajah, Lindsey & Mozer 2016, "How deep is knowledge tracing?"](https://arxiv.org/pdf/1604.02416)).
  The pyKT benchmark found most deep KT models improve only minimally on the original DKT, and
  that bad evaluation setups leak labels and inflate results
  ([Liu et al. 2022, NeurIPS](https://proceedings.neurips.cc/paper_files/paper/2022/hash/75ca2b23d9794f02a92449af65a57556-Abstract.html)).
  **Evidence: strong (multiple benchmarks).**
- **LLM-era KT.** Next-Token Knowledge Tracing feeds question text and history to a pretrained
  LLM. It reports gains over neural KT and better cold-start generalization to new questions
  and users ([NTKT, arXiv 2511.02599](https://arxiv.org/abs/2511.02599v1)). Other work uses LLMs
  to build explainable learner profiles ([CIKT, arXiv 2505.17705](https://arxiv.org/abs/2505.17705v1)).
  **Evidence: weak-moderate (new, benchmark-only, school datasets).**
- **Memory models for spacing.** Half-life regression at Duolingo
  ([Settles & Meeder 2016](https://aclanthology.org/P16-1174/)) and FSRS
  ([srs-benchmark](https://github.com/open-spaced-repetition/srs-benchmark)) predict recall
  probability per item. A secondary summary of the open benchmark reports FSRS-5 log-loss of
  0.291 against 0.354 for SM-2, with about 25% fewer reviews at equal retention
  ([summary](https://www.mindomax.com/fsrs-vs-sm2-spaced-repetition-algorithm); numbers not
  checked against the repo). Model-driven personalized review gave +16.5% retention in a
  classroom ([Lindsey et al. 2014](https://home.cs.colorado.edu/~mozer/Research/Selected%20Publications/reprints/LindseyShroyerPashlerMozer2014.pdf)).
- **Evaluation.** KT models are almost always evaluated by next-response AUC on logged data.
  That is not the same as learning gains when the model drives selection (Doroudi et al.,
  above). Mastery thresholds (e.g. BKT P(known) > 0.95) are conventions, not optima.

**Implications**

- For one user and sparse data, use a simple, interpretable per-KC state: memory stability and
  difficulty (FSRS-like) plus a mastery/understanding estimate. Let an LLM supply priors from
  the item text and the learner's history (the NTKT idea) rather than training anything.
- Evaluate the system the way learning scientists do: delayed, unassisted performance on
  *novel* questions per KC, not in-session accuracy (see Bastani, finding 10).

---

## 5. Retrieval practice, spacing, interleaving, generation, desirable difficulties

**Findings**

| Effect | Size | Key caveat | Source |
|---|---|---|---|
| Practice testing vs restudy and other conditions | g = 0.61 | Larger with feedback and matching formats | [Adesope 2017](https://journals.sagepub.com/doi/10.3102/0034654316689306) |
| Testing → transfer to new questions | d ≈ 0.40 overall **(unverified figure)** | Weak for application/inference without elaborative feedback or broad initial tests | [Pan & Rickard 2018](https://escholarship.org/content/qt45x0w7t8/qt45x0w7t8.pdf) |
| Repeated testing → inferential transfer | ~2× restudy on facts, ~+50% on concepts | Prose passages, 1-week delay | [Butler 2010](https://profiles.wustl.edu/en/publications/repeated-testing-produces-superior-transfer-of-learning-relative-/) |
| Higher-order quizzes → higher-order tests | fact quizzes did **not** transfer up | Middle school and college | [Agarwal 2019](https://retrievalpractice.org/blooms) |
| Spacing: optimal gap vs retention interval | 20–40% of 1 wk → 5–10% of 1 yr | Too short hurts more than too long | [Cepeda 2008](https://www.evullab.org/pdf/CepedaVulRohrerWixtedPashler-PS-2008.pdf) |
| Interleaving vs blocking | g = 0.42 overall; math 0.34; words −0.39 | Helps when categories are similar to each other and variable within | [Brunmair & Richter 2019](https://www.psychologie.uni-wuerzburg.de/fileadmin/06020400/2019/Brunmair_Richter_in_press__2019_META-ANALYSIS_OF_INTERLEAVED_LEARNING.pdf) |
| Generation vs reading | d = 0.40 | Large moderator variance | [Bertsch 2007](https://pubmed.ncbi.nlm.nih.gov/17645161/) |
| Self-explanation | g = 0.55 | Held when time on task controlled | [Bisra 2018](https://www.Gwern.net/doc/psychology/spaced-repetition/2018-bisra.pdf) |
| Prequestions / pretesting | benefits prequestioned info; weaker spillover | Needs feedback | [Pan & Carpenter 2023](https://link.springer.com/10.1007/s10648-023-09805-6) |

- Dunlosky et al.'s review rated **practice testing** and **distributed practice** "high
  utility", and rereading, highlighting and summarization "low utility"
  ([APS summary of Dunlosky et al. 2013](https://www.psychologicalscience.org/news/releases/which-study-strategies-make-the-grade.html)).
  **Evidence: strong.**
- Spacing also helps *inductive* concept learning, against the old claim that spacing is "the
  enemy of induction". Yet learners judged massing more effective
  ([Kornell & Bjork 2008](https://bjorklab.psych.ucla.edu/wp-content/uploads/sites/13/2016/07/Kornell_Bjork_2008_PsychScience.pdf)).
- Interleaving is a *discrimination* tool: it helps most when items are easily confused. The
  brief's "choose between methods for a given situation" question is an interleaved
  discrimination item, and is well supported for confusable method families (e.g. influence
  functions vs TracIn vs datamodels).

**Implications**

- Each review should be a retrieval with feedback. Explanatory feedback is needed for the
  transfer benefits (Pan & Rickard).
- Build "contrast sets" of confusable KCs and generate discrimination questions across them.
- Expect the user to *feel* that easy formats work better. Show delayed-test evidence in the
  UI rather than in-session fluency.

---

## 6. Worked examples, fading, expertise reversal, cognitive load: matching effort to state

**Findings**

- **Worked examples:** g = 0.48 on math performance (55 studies). Correct examples alone beat
  incorrect or mixed ones, and, surprisingly, added self-explanation prompts *reduced* the
  effect in that sample ([Barbieri et al. 2023](https://oaks.kent.edu/hcri/meta-analysis-worked-examples-effect-mathematics-performance)).
- **Fading:** progressively removing worked steps (backward fading) improves near transfer in
  math and physics ([LearnLab wiki: Fading](https://learnlab.org/research/wiki/index.php/Fading);
  [Renkl and colleagues](https://faculty.engineering.asu.edu/mre/wp-content/uploads/sites/31/2020/02/MoRO09.pdf)).
- **Expertise reversal:** methods that help novices (worked examples, integrated text and
  diagrams, explanatory text) become redundant or harmful for more expert learners. Instruction
  must track expertise *per task class* ([Kalyuga 2007](https://www.uky.edu/~gmswan3/EDC608/Kalyuga2007_Article_ExpertiseReversalEffectAndItsI.pdf)).
  **Rapid assessment:** "first-step" and "rapid verification" tests diagnose expertise in
  seconds and drove adaptive tutorials in algebra and kinematics
  ([Kalyuga, adaptive procedures](https://igi-global.com/chapter/adaptive-procedures-efficient-learning/25741);
  [Chartered College summary](https://my.chartered.college/?p=5912)). **Evidence: moderate-strong.**
- **Productive failure:** problem solving *before* instruction beat instruction-first for
  conceptual knowledge across 53 studies. The effect was larger when designs followed PF
  principles faithfully ([Sinha & Kapur 2021, summary](https://www.weforum.org/stories/2021/09/students-who-productively-fail-learn-more/);
  reported g ≈ 0.36, **unverified**). This sits in tension with worked-example results: PF
  helps conceptual understanding, worked examples help procedural skill for novices.
- **ICAP:** engagement modes rank Interactive > Constructive > Active > Passive for learning
  ([Chi & Wylie 2014](https://csi.asu.edu/wp-content/uploads/2018/01/ChiWylie2014ICAP.pdf)).
- **Tutoring granularity:** step-based ITS reached d = 0.76 against human tutoring's 0.79 vs no
  tutoring. Answer-only systems reached 0.31 and sub-step systems 0.40
  ([VanLehn 2011, summary](https://marginalrevolution.com/marginalrevolution/2013/10/how-good-are-computers-as-tutors.html)).
  Feedback on intermediate steps is what matters, which supports "worked homework" with
  per-step checking over answer-only grading.

**Mapping the brief's effort levels to evidence**

| Brief level | ICAP mode | Best use per evidence | Counts as maintenance? |
|---|---|---|---|
| Reminder (read / podcast) | Passive | First exposure, orientation, priming before a quiz; for experts, a quick refresher of context | No, unless followed by a retrieval |
| Flashcards | Active (retrieval) | Constant KCs: terms, notation, definitions, "what is X for" | Yes, for that KC's memory strength |
| Quiz (written/spoken) | Constructive | Application, discrimination, prediction, self-explanation | Yes; strongest evidence for transfer |
| Worked homework | Constructive/Interactive | Novices: study worked or faded example first. Experts: solve with step feedback | Yes; multi-KC credit (FIRe-like) |

The system, not the learner, should pick the *format* for a KC from its state (expertise
reversal). The learner picks the *time budget* ("I have 5 minutes, hands busy" → spoken quiz,
not podcast).

---

## 7. Flashcard and prompt writing for conceptual material

**Findings**

- **Matuschak, "How to write good prompts".** Good prompts are focused, precise, consistent,
  tractable (about 90% answerable) and effortful (not trivially inferable). For concepts,
  write *many* small prompts through several lenses: attributes and tendencies, similarities
  and differences, parts and wholes, causes and effects, significance. Watch for answers
  memorized by question shape (pattern matching), especially with yes/no cards
  ([andymatuschak.org/prompts](https://andymatuschak.org/prompts/)).
  He argues spaced repetition *can* build conceptual understanding when prompts are written
  this way ([note](https://notes.andymatuschak.org/z9Vi7YVx7NzxU2wawNgsJbk)).
- **LLMs and prompts.** By default, LLMs write prompts that "reinforce the surface—what is
  said, rather than what it means or why it matters" (definition↔term cards). They do much
  better with explicit patterns ("generate a system and ask whether it is in echelon form")
  ([note](https://notes.andymatuschak.org/zGkLPdiEs7Qohkesq7TNiBe)). **Choosing what to
  reinforce is the harder problem**, because the model cannot know the reader's goals or prior
  knowledge. Matuschak suggests reader highlights as cheap target selection
  ([note](https://notes.andymatuschak.org/z62s1nNLEfhGbDmpb8Z7dZiYyi3kaSziuLVXd)).
- **Mnemonic medium (Quantum Country).** Once readers had demonstrated 5-day retention, median
  accuracy stayed at about 95% or higher. Readers who reviewed for a year had a median of 463
  reviews and 10 lapses ([note](https://notes.andymatuschak.org/z2Rv4RAjXUrwa3fMYn9Q1iR)).
  The causal effect of the reviews on retention is an open question in his own notes
  ([note](https://notes.andymatuschak.org/zuCfBJSkm5BnqC1qw1bLH2)). **Evidence: observational,
  for embedded-question recall, not transfer.**
- **Nielsen, "Augmenting long-term memory".** He used Anki to understand papers (the AlphaGo
  paper): many small cards per paper, read in several passes, "syntopic" reading across
  papers, and deleting cards that no longer matter. He argues memory underpins understanding
  rather than opposing it ([essay](http://augmentingcognition.com/ltm.html);
  [summary](https://stafforini.com/works/nielsen-2018-augmenting-longterm-memory/)).
- **Wozniak's 20 rules.** Rule 1 is "do not learn if you do not understand" and Rule 2 is
  "learn before you memorize": build the overall picture first, then cards. Rule 4 is the
  minimum information principle ([20 rules](https://supermemo.guru/wiki/20_rules)).
  Note that Rules 1–2 *are* a blurry-to-sharp ordering: understanding first, atomization second.
- **Gwern.** Spaced repetition is very efficient for what it targets, but says nothing about
  *what* to memorize. It suits large bodies of discrete material best
  ([Gwern, spaced repetition](https://gwern.net/spaced-repetition)).

**Implications**

- Give the prompt-writing agent a pattern language: a lens list, a contrast list, and
  "apply to a fresh example", plus the rules (focused, consistent, not inferable). Check
  prompts with a reviewer agent, as the prototype already does for facts.
- Atomic prompts serve *retention* of constant KCs. Understanding needs explanation +
  self-explanation + application questions. Do not rely on the card deck alone.

---

## 8. Overview-first vs prerequisite-first: ADEPT / blurry-to-sharp

**Findings**

- **Advance organizers (Ausubel).** Meta-analyses from the 1970s–80s report small positive
  average effects on learning and retention, larger for retention and for unfamiliar material
  ([Luiten, Ames & Ackerson 1980, citation](https://journals.sagepub.com/doi/ref/10.2190/PQXY-M6NT-UT6B-R618);
  [updated meta-analysis "Thirty years after Ausubel"](https://www.ideals.illinois.edu/items/20405);
  exact effect sizes **unverified**). **Evidence: weak-moderate, old, heterogeneous.**
- **Pre-training principle (Mayer).** Learning the names and characteristics of key components
  *before* a complex explanation: 13 of 16 tests positive, median d = 0.75
  ([Mayer, Cambridge Handbook chapter](https://cambridge.org/core/books/cambridge-handbook-of-multimedia-learning/principles-for-managing-essential-processing-in-multimedia-learning-segmenting-pretraining-and-modality-principles/DD24C2F48B9B1277CE59F78276110258)).
  Segmenting (learner-paced chunks): 10 of 10 positive, median d = 0.79 (same source).
  This is *part-first* evidence, but the "parts" are lightweight names and behaviours, not full
  mastery.
- **Isolated-then-interacting elements.** For high element-interactivity material, novices
  learned better when elements were first presented in isolation (deliberately incomplete
  understanding) and then together. Experts did not benefit
  ([Pollock, Chandler & Sweller 2002](https://ro.uow.edu.au/edupapers/145)). This is a
  "sharp parts first, then whole" result for novices.
- **Whole-task sequencing (4C/ID).** Learners work on simple-to-complex versions of the
  *whole* task from the start, with supportive information and just-in-time part-task
  practice. Meta-analytic d = 0.79, more suitable for higher education
  ([Costa, Miranda & Melo 2022](https://ciencia.iscte-iul.pt/publications/the-four-component-instructional-design-model-4cid-a-meta-analysis-on-use-and-effect/81383?lang=en);
  [4C/ID overview](https://edutechwiki.unige.ch/en/4C-ID)). Reigeluth's elaboration theory
  similarly starts with an "epitome" of the whole and elaborates it
  ([Elaboration theory](https://edutechwiki.unige.ch/en/Elaboration_theory)); its direct
  experimental support is thin. **Evidence: moderate for 4C/ID as a package; the ordering
  component is not isolated.**
- **Analogies.** Relational reasoning underlies higher-order thinking, and analogies in
  instruction work when supported: visible source, explicit mapping, gestures and diagrams
  ([Richland & Simms 2015](https://learninglab.uchicago.edu/Publications_files/Richland%26Simms_WIREs.pdf)).
  *Comparing two cases* beats studying them separately, and transfer rises with comparison
  support ([Gentner, Loewenstein & Thompson 2003](https://dedregentner.owlstown.net/publications/38525-learning-and-transfer-a-general-role-for-analogical-encoding)).
  A meta-analysis gives d = 0.50 for case comparison. Stating the principle *after* the
  comparison beats stating it before ([Alfieri et al. 2013](https://www.lrdc.pitt.edu/Schunn/papers/ContrastingCasesMeta-AlfieriEtAl2013.pdf)).
  Risk: a single simple analogy can create misconceptions that later block fuller
  understanding, and multiple analogies are the antidote
  ([Spiro et al. 1989](https://www.cambridge.org/core/books/similarity-and-analogical-reasoning/multiple-analogies-for-complex-concepts-antidotes-for-analogy-induced-misconception-in-advanced-knowledge-acquisition/FF07DBE3F194DB258119713D3000E730)).
- **Concreteness fading.** Start concrete and fade explicitly to abstract representations.
  This beats either concrete-only or abstract-only for transfer in math and science
  ([Fyfe, McNeil, Son & Goldstone 2014](https://www.doi.org/10.1007/S10648-014-9249-3);
  [Learning Scientists summary](https://learningscientists.org/blog/2018/2/1-1)). This is the
  closest experimental analogue of ADEPT's Example → Plain English → Technical progression.
  **Evidence: moderate (systematic review, mostly children and math).**
- **Dual coding / diagrams.** Mayer's multimedia principles (words + pictures beats words alone,
  plus segmenting, pre-training and coherence) have many replications
  ([Mayer handbook](https://cambridge.org/core/books/cambridge-handbook-of-multimedia-learning/principles-for-managing-essential-processing-in-multimedia-learning-segmenting-pretraining-and-modality-principles/DD24C2F48B9B1277CE59F78276110258)).
  Expertise reversal applies: diagrams with redundant text can hurt experts
  ([Kalyuga 2007](https://www.uky.edu/~gmswan3/EDC608/Kalyuga2007_Article_ExpertiseReversalEffectAndItsI.pdf)).
- **Try-first.** Pretesting and productive failure both put an attempt *before* the sharp
  explanation ([Pan & Carpenter 2023](https://link.springer.com/10.1007/s10648-023-09805-6);
  [Sinha & Kapur 2021](https://www.weforum.org/stories/2021/09/students-who-productively-fail-learn-more/)).
- **Adults and conceptual material specifically:** I found no study that directly compares
  "overview-first" with "prerequisite-first" ordering for adult experts learning
  research-level concepts. The evidence above comes from adjacent settings.

**What this implies for the tension (Math Academy vs blurry-to-sharp)**

The two are answers to different questions, and the evidence supports a hybrid:

1. **Mastery gating is about *practice*, not exposure.** Math Academy gates *lessons with
   problems* on mastered prerequisites, which is supported by mastery-learning and
   cognitive-load evidence. Nothing in that evidence forbids a short, unassessed orienting
   overview of the whole target first. Advance organizers, epitomes, 4C/ID whole tasks,
   pretraining and Wozniak's "learn before you memorize" all point toward a whole-picture
   orientation that is *not* counted as mastery.
2. **Sharpening needs prerequisites.** For high element-interactivity content (most ML
   method sections), novices need the interacting elements learned first, or separately
   (Pollock et al.; pretraining). So after the overview, the system should teach gated
   prerequisites before it tries the "technical" layer of the target KC.
3. **"Blurry" should be multiple analogies plus contrasting cases, each with explicit limits.**
   That keeps the memorable gist ADEPT values while avoiding analogy-induced misconceptions.
4. **Expertise reversal moderates all of this.** For this user (an experienced engineer and ML
   researcher), many prerequisites will already be known. Diagnostic-first (finding 8) skips
   them. The overview can be terse, and analogies may be redundant for KCs in the user's
   strong areas.
5. **Ordering by "generality".** Generality and prerequisite depth are correlated but not the
   same. The evidence supports *foundational-first for practice* (prerequisites) and
   *whole-first for orientation*, rather than "most general first" for everything.

Concrete per-goal flow suggested by the evidence: orient with a whole-paper sketch (analogy,
diagram, why it matters), then probe diagnostic questions on candidate prerequisites, then
teach and practice the missing prerequisites in graph order, then build up the paper's KCs from
concrete example to plain-language to technical, then run varied retrieval and application
under spacing.

---

## 9. Passive formats (reading, podcasts) and retention

- Rereading has low utility and adds little over a single reading
  ([Callender & McDaniel 2009](https://profiles.wustl.edu/en/publications/the-limited-benefits-of-rereading-educational-texts/);
  [Dunlosky summary](https://www.psychologicalscience.org/news/releases/which-study-strategies-make-the-grade.html)).
- Once an item is learned, restudying it does not improve delayed recall but retrieving it
  does ([Karpicke & Roediger 2008](https://www.brucehayes.org/Teaching/papers/2008_Roediger_Karpicke_Science.pdf)).
- **Listening ≈ reading** for comprehension, and reading-while-listening helps only when
  pacing is externally fixed ([Clinton-Lisell 2023 meta-analysis](https://files.eric.ed.gov/fulltext/EJ1403866.pdf)).
  So audio is a valid *delivery channel*, but it is still passive.
- ICAP puts passive reception at the bottom
  ([Chi & Wylie 2014](https://csi.asu.edu/wp-content/uploads/2018/01/ChiWylie2014ICAP.pdf)).
- **When passive helps:** first exposure before retrieval (testing effects presuppose initial
  study); orientation and advance organizers; and Matuschak's "salience prompts", which keep
  ideas in mind for noticing in daily life ([prompts essay](https://andymatuschak.org/prompts/)).
  A podcast that *asks questions and pauses for answers* turns a passive format into a
  retrieval format. That is a cheap upgrade for the "no effort" tier.

---

## 10. Teaching people to read research papers

- **Keshav's three-pass method:** pass 1 (5–10 min) covers title, abstract, headings and
  conclusions; pass 2 (about 1 h) covers figures and the main argument, skipping proofs;
  pass 3 (1–5 h) virtually re-implements the paper and challenges assumptions
  ([Keshav, "How to read a paper"](https://www.cs.princeton.edu/courses/archive/fall10/cos597B/papers/howtoread-keshav.pdf)).
  This is itself blurry-to-sharp. **Evidence: practitioner advice, no controlled tests.**
- **ScholarPhi** gives position-sensitive definitions of terms and symbols, a declutter
  filter, equation diagrams and an auto-glossary. In usability studies, readers found
  definitions faster and preferred it to a baseline reader
  ([Head et al. CHI 2021](https://arxiv.org/abs/2009.14237v2)).
- **Paper Plain** offers term definitions, plain-language section summaries, and "key
  questions" that guide readers to answering passages, for non-expert readers of medical
  papers ([August et al.](https://arxiv.org/pdf/2203.00130)). Plain-language summaries tailored
  to a *specific* audience help more than generic ones, with some pitfalls
  ([Know Your Audience](https://arxiv.org/pdf/2403.04979)).
- **Gap:** I found no learning-science study of *building the background* needed for a
  particular paper (prerequisite identification plus pre-teaching) and measuring paper
  comprehension. The closest are pretraining (Mayer) and the reading-support tools above,
  which help *during* reading rather than building durable knowledge beforehand.

**Implication:** a good evaluation target for the MVP is "after N minutes of the tool, can the
user answer pass-2 and pass-3 questions about the paper?" Pass-3-style questions (re-derive,
critique an assumption, predict an ablation) are the right "homework" level.

---

## 11. Where the evidence contradicts common assumptions or the brief

| Brief / common assumption | What the evidence says | Source |
|---|---|---|
| "No effort" reminders (read/podcast) as a maintenance tier | Re-exposure barely helps retention once something is learned; only retrieval maintains. Keep the tier for orientation and first exposure, or make audio interactive | [Karpicke & Roediger 2008](https://www.brucehayes.org/Teaching/papers/2008_Roediger_Karpicke_Science.pdf); [Callender & McDaniel 2009](https://profiles.wustl.edu/en/publications/the-limited-benefits-of-rereading-educational-texts/) |
| Effort level "chosen on demand" by the user | Learners prefer and overrate easier, less effective formats; format should follow learner state (expertise reversal). Let the user choose time and modality, and the system choose the format | [Kornell & Bjork 2008](https://bjorklab.psych.ucla.edu/wp-content/uploads/sites/13/2016/07/Kornell_Bjork_2008_PsychScience.pdf); [Deslauriers 2019](https://uateachingacademy.ua.edu/research/research-roundup-active-learning-vs-full-lectures-what-really-enhances-learning/); [Kalyuga 2007](https://www.uky.edu/~gmswan3/EDC608/Kalyuga2007_Article_ExpertiseReversalEffectAndItsI.pdf) |
| Flashcards as a sufficient low-effort path to understanding | Fact retrieval does not transfer to higher-order performance; you need practice at the target level | [Agarwal 2019](https://retrievalpractice.org/blooms) |
| "Facts first, then application" (Bloom's taxonomy as a sequence) | Higher-order retrieval works without building fact knowledge first; mixed practice is best | [Agarwal 2019](https://retrievalpractice.org/blooms) |
| Varied recall vs repeating the same card | Both are right for different things: consistency for memory of a constant KC, variation for transfer. Track per KC and vary the surface | [Matuschak](https://andymatuschak.org/prompts/); [Butler 2010](https://profiles.wustl.edu/en/publications/repeated-testing-produces-superior-transfer-of-learning-relative-/) |
| Strict prerequisite order (Math Academy) vs blurry-to-sharp | Complementary: orient whole-first (unassessed), practice prerequisite-first (gated) | §8 |
| Order by "generality" | Generality ≠ prerequisite depth; whole-first helps orientation, foundations-first helps practice | §8 |
| A smarter sequencing/KT model is the key risk | Simple KT models match deep ones; KST-sequenced instruction ≈ teachers; gains come from content, feedback and mastery | [Khajah 2016](https://arxiv.org/pdf/1604.02416); [Fang 2019](https://digitalcommons.memphis.edu/facpubs/7254); [von Hippel 2024](https://www.educationnext.org/two-sigma-tutoring-separating-science-fiction-from-science-fact/) |
| The owner's belief that *what to teach* is the main risk | Partly confirmed: Matuschak finds target selection is the harder problem for LLM-made prompts | [Matuschak note](https://notes.andymatuschak.org/z62s1nNLEfhGbDmpb8Z7dZiYyi3kaSziuLVXd) |
| An LLM tutor is inherently helpful | Without guardrails, learning dropped 17% once access was removed | [Bastani et al.](https://papers.ssrn.com/abstract=4895486) |
| ADEPT: "what survives is the analogy" | Plausible (gist outlasts detail), but a single analogy can mislead; use several, with their limits stated | [Spiro et al. 1989](https://www.cambridge.org/core/books/similarity-and-analogical-reasoning/multiple-analogies-for-complex-concepts-antidotes-for-analogy-induced-misconception-in-advanced-knowledge-acquisition/FF07DBE3F194DB258119713D3000E730) |

---

## 12. Open questions the literature does not answer

1. **KC granularity for research concepts.** LFA needs many learners and many items per KC.
   With n = 1 and a growing pool, how do you decide whether "Gauss-Newton ≈ Fisher" is one KC
   or two? There is no validated single-learner method.
2. **Memory models for varied items.** FSRS/HLR assume a repeated identical item. How should a
   KC's memory state update when each review is a new application question of varying
   difficulty? IRT-style difficulty per variant plus FSRS per KC is a guess, not established.
3. **Implicit-review credit for conceptual graphs.** FIRe weights are hand-set for math and
   unevaluated. Can LLM attribution of which KCs a scenario exercised replace them, and how
   much credit should a successful scenario give each component?
4. **Mastery criteria for conceptual knowledge** graded by an LLM from short free-text answers.
   What threshold, how many varied successes, and how reliable is LLM grading per KC?
   (Grading reliability was not covered here; the search budget ran out.)
5. **Overview-first vs prerequisite-first for expert adults** learning research-level material:
   no direct comparison found.
6. **How much background is "enough" to read a paper.** Nothing measures the trade-off between
   pre-teaching depth and paper comprehension or time.
7. **LLM-identified prerequisites for post-cutoff papers.** I found no evaluation of LLM
   prerequisite-edge accuracy or of "I don't know this term" calibration. The KC-generation
   papers above use fixed, older domains.
8. **Goal change and forgetting priorities.** When goals shift, which KCs should keep being
   maintained? Spaced-repetition work assumes a fixed deck. Value-of-retention modelling tied
   to goals is open.
9. **Evaluation with a single user.** RCT evidence won't exist. Within-subject designs (as in
   Kestin et al., one topic per condition) and delayed novel-question probes per KC are the
   most transferable methods.
10. **Language learning and skills later.** KLI and 4C/ID cover these domains, but the
    practice types (comprehensible input, speaking) differ. Keep KC "type" in the schema so
    format selection can differ by domain.
