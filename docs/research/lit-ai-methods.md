# Literature notes: AI and NLP methods

Compiled verbatim from four research sub-agents' final reports. Their shared web-search budget ran out partway, so coverage gaps are noted inside each section.

---

# Part: LLM tutoring and assessment

I ran out of web searches before the feedback-generation part of topic 3. That section is thin: there are no numbers on feedback quality, and the Steiss et al. 2024 human-vs-ChatGPT writing-feedback study was not retrieved. Everything else below was found and checked against the abstract, the paper's HTML or reputable secondary sources.

## 1. LLM tutors: learning-gain evidence

**Studies where it helped**
- **Kestin et al., Harvard physics (Scientific Reports, June 2025).** Crossover RCT with N=194, comparing a GPT-4 tutor used at home against an expert in-class active-learning session.
  - Effect size was 0.73–1.3 SD (quantile regression). Median post-test was 4.5 vs 3.5 out of 5, and median time was 49 minutes vs about 60. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12179260/)
  - The tutor revealed only one step at a time, asked students to try first, kept answers short, and was given correct solutions in advance to prevent hallucination. [iatrox summary](https://www.iatrox.com/blog/harvard-ai-tutor-trial-what-it-showed-question-banks)
  - Caveats: one course, and the system prompt took months to develop. [Panickssery](https://arjunpanickssery.substack.com/p/five-recent-ai-tutoring-studies)
- **De Simone et al., World Bank Nigeria (2025 working paper).** Six-week after-school program using GPT-4 through Copilot for English.
  - +0.31 SD on the overall assessment and +0.23 SD on English. The authors equate this to 1.5–2 years of normal schooling, among the most cost-effective programs measured.
  - Larger effects for girls and for students who started higher. [VoxDev](https://www.voxdev.org/topic/education/how-ai-tutors-improved-learning-nigeria), [World Bank](https://openknowledge.worldbank.org/entities/publication/15e1ff08-15ae-4f7a-b2a8-d146e6c113ee/full)
- **Tutor CoPilot (Wang et al., 2024).** The AI assisted human tutors rather than students. RCT with 900 tutors and 1,800 K-12 students.
  - Topic mastery rose 4 percentage points overall (p<0.01) and 9 points for students of lower-rated tutors. Cost was $20 per tutor per year.
  - Tutors with access asked more guiding questions and gave away answers less often. [arXiv](https://arxiv.org/abs/2410.03017)
  - Caveat: 66% vs 62% on exit tickets, and tutors used the tool in only 29% of sessions. [Panickssery](https://arjunpanickssery.substack.com/p/five-recent-ai-tutoring-studies)
- **Ghana (Rori, a WhatsApp math tutor).** N=637. Gains of 5.13 vs 2.12 points on a 35-question test. [Panickssery](https://arjunpanickssery.substack.com/p/five-recent-ai-tutoring-studies)

**Studies where it hurt or did nothing**
- **Bastani et al. (PNAS 2025).** About 1,000 high-school math students in Turkey. [PNAS/IDEAS](https://ideas.repec.org/a/nas/journl/v122y2025pe2422633122.html), [Wharton](https://knowledge.wharton.upenn.edu/article/without-guardrails-generative-ai-can-harm-education)
  - Plain ChatGPT ("GPT Base") raised practice scores 48% but lowered later unassisted exam scores 17% compared with no AI.
  - "GPT Tutor" (teacher-written hints, no direct answers) raised practice scores 127% with exam scores about equal to control.
  - Students overestimated how much they had learned, including high achievers.
- **Course-integrated GenAI tutor RCT (Liu, Sweet et al., EdWorkingPaper, October 2026).** N=2,379 undergraduates and 30 instructors.
  - Access *reduced* final grades by 0.37 SD and LMS participation by 0.90 SD. Losses were larger for first-generation students.
  - Mechanism: the tutor replaced engagement with existing course activities. [EdWorkingPapers](https://edworkingpapers.com/ai26-1598)
- **Khanmigo, Tennessee (Oreopoulos & Low, NBER w35620).** Two-year cluster RCT in 18 schools.
  - +1.3 national percentile ranks per term (about 0.06–0.08 SD a year), similar to Khan Academy without AI.
  - 96% of students tried it, but the median student messaged it on only a third of practice days and in only 17% of sessions where they made a mistake. [NBER](https://www.nber.org/papers/w35620)
- **Khanmigo, undergraduate physics.** No significant difference from Google search. [EKU](https://encompass.eku.edu/fs_research/782)
- **Italy, ESL homework.** N=76, small and non-significant effects. [Panickssery](https://arjunpanickssery.substack.com/p/five-recent-ai-tutoring-studies)

**Meta-analyses (treat with caution)**
- Wang & Fan (2025) pooled 51 studies: g=0.867 for performance and g=0.457 for higher-order thinking. [HumanProgress](https://humanprogress.org/chatgpts-great-effect-on-students-learning-performance/)
- It has been criticized for its methods. [critique](https://shadowrunners.substack.com/p/a-criticism-of-the-recent-chatgpt), [WINS](https://www.winssolutions.org/wang-fan-chatgpt-study-flawed-methods/)
- An IRRODL meta-analysis of 22 studies found g=0.573, with g=0.538 for undergraduates. [IRRODL](https://www.irrodl.org/index.php/irrodl/article/view/8775)
- These pooled numbers are much larger than what the big recent RCTs found.

**Tutoring-behavior benchmarks**
- **MathDial (Macina et al., 2023).** About 3,000 dialogues. When asked to tutor, ChatGPT revealed the solution 66% of the time and gave incorrect feedback 59% of the time. [arXiv](https://arxiv.org/abs/2305.14536v2)
- **MRBench (Maurya et al., NAACL 2025).** 192 dialogues and 1,596 responses, annotated on eight dimensions with human agreement κ=0.71. [arXiv](https://arxiv.org/html/2412.09416)
  - GPT-4 spotted the student's mistake 94% of the time but held back the answer only 53% of the time.
  - Claude 3.5 Sonnet held back the answer 94.8% of the time, and expert humans 90.6%.
  - Prometheus2 and Llama-3.1-8B, used as automatic judges, correlated near zero or negatively with humans on most dimensions. Small LLMs cannot be trusted to judge teaching quality.
- **LearnLM (Google, December 2024).** Pedagogy experts preferred it over GPT-4o by 31%, Claude 3.5 Sonnet by 11% and Gemini 1.5 Pro by 13%. [arXiv 2412.16429](https://arxiv.org/pdf/2412.16429)
- **"Arena for learning" (2025).** 189 educators role-played learning sessions and 206 experts judged them. Gemini 2.5 Pro won 73.2% of non-tied matchups against Claude 3.7 Sonnet, GPT-4o and o3. [arXiv 2505.24477](https://arxiv.org/abs/2505.24477)
- **Pedagogy Benchmark (multiple-choice test of teaching knowledge).** 97 models scored 28–89%: Gemini 2.5 Pro 88.8%, o3 87.9%, Claude Opus 4 Thinking 87.4%. [arXiv 2506.18710](https://arxiv.org/abs/2506.18710)
- **TutorEval.** 834 questions about textbook chapters. Fine-tuning on the TutorChat dataset gained 8.5 points over UltraChat (48.4 vs 39.9). [arXiv](https://arxiv.org/abs/2402.11111v2)

**What helped vs what hurt**
- Helped: withholding answers, step-by-step hints, asking the learner to attempt first, short replies, giving the model reference solutions, and building the pedagogy into the system.
- Hurt or did nothing: unrestricted chat (used as a crutch), optional access with low use, and tools that displace existing study activity.

## 2. Generating questions and distractors

- **Doughty et al. (ACE 2024), GPT-4 Python multiple-choice questions.** 651 generated vs 449 human-written, across 246 learning objectives. [arXiv](https://arxiv.org/html/2312.03173v1)
  - Single correct answer: 95.1% vs 98.9%.
  - No obviously wrong options: 96.0% vs 99.1%.
  - Aligned with the learning objective: 88.0% vs 79.5% (GPT-4 better).
  - 81.7% of generated questions passed every criterion.
  - Generated questions were easier (80.1% vs 76.3% answered correctly).
  - Rater agreement: Fleiss κ=0.22, but Gwet's AC1 was 0.62–0.96.
- **Hong Kong emergency-medicine licensing exam, GPT-4o questions.** [PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11806894/)
  - AI questions were easier (difficulty index 0.78 vs 0.69, p<0.01). Discrimination was similar (0.22 vs 0.26).
  - More flaws: factual errors 6% vs 4%, irrelevant 6% vs 0%, wrong difficulty 14% vs 1%.
  - Mostly tested lower-order thinking (χ²=14.27, p=0.003).
  - A meta-analysis found human questions discriminate better between strong and weak students (SMD −0.70).
- **Control over Bloom level is unreliable.** GPT-4o questions were rated high quality but often did not match the requested Bloom level. [Edinburgh MSc](https://project-archive.inf.ed.ac.uk/msc/20247200/msc_proj.pdf)
- **Distractors (Feng et al., NAACL Findings 2024).** 1,400 Eedi math questions. [arXiv](https://arxiv.org/html/2404.02124v3)
  - The best method used three similar example questions in the prompt (kNN in-context). It matched at least one human distractor 73.9% of the time, matched 38.5% of distractors overall, and all three only 11.0% of the time.
  - Experts rated mathematical validity 3.28 vs 3.99 out of 5, and plausibility 2.68 vs 3.72 (p<0.05).
  - LLMs do not anticipate real student misconceptions well.
  - Survey of the area: [Alhazmi et al., EMNLP 2024](https://arxiv.org/abs/2402.01512v2)
- **Checking item difficulty with simulated students.**
  - LLMs role-playing classrooms, then fitted with item response theory: correlations of 0.75/0.76/0.82 with real difficulty for grades 4/8/12. Surprisingly, weaker models such as Gemma did better. [arXiv 2601.09953](https://arxiv.org/abs/2601.09953v1)
  - SMART (simulated students trained with DPO to match IRT) beat earlier difficulty-prediction methods on 49 reading items and 50 Java items. [arXiv 2507.05129](https://arxiv.org/abs/2507.05129)
  - A fine-tuned response simulator produced generated tests whose scores correlated r=0.93 with expert-written forms. [Stanford HAI](https://hai.stanford.edu/sites/default/files/2024-02/Item%20Response%20Simulator_Zelikman%26Ma.pdf.pdf)

## 3. LLM grading of short free-text answers

- **Kortemeyer, GPT-4 zero-shot on standard benchmarks.** [arXiv 2309.09338](https://arxiv.org/abs/2309.09338?context=cs)
  - SciEntsBank 2-way F1=0.744, and 0.731 with no reference answer. Beetle 2-way F1=0.611.
  - Comparable to hand-engineered systems, worse than specially trained models. Human agreement on SciEntsBank is κ=0.728.
- **Rubric complexity (Qwen2.5-72B on SciEntsBank).** [arXiv 2601.08843](https://arxiv.org/html/2601.08843v1)
  - Correct/incorrect: 76% accuracy, κ=0.51. Five labels: 57% accuracy, κ=0.34.
  - Taking a consensus over 10 runs and abstaining when they disagree raised 2-way accuracy from 77.4% to 81.1% while still grading 85.6% of answers.
  - Over 90% of prompt-injection attempts were rejected, but 9.6% of ambiguous answers were wrongly passed. Synonym swaps hurt more than paraphrases.
- **Sustainability course.** 232 answers graded by GPT-4o, Gemini 2.0, DeepSeek V3 and Llama 3.3. [Yasar](https://gcris.yasar.edu.tr/entities/publication/1eeab52d-b73f-42b4-baa8-f2c94edfc8c1/full)
  - LLM-human QWK 0.585–0.640. Human-human ICC 0.667–0.800.
  - Agreement fell for higher-order Bloom criteria.
- **Chamieh et al. (BEA 2024).** Zero- and few-shot LLMs performed poorly on three datasets, especially where reasoning or domain knowledge was needed. The authors say there is "no basis" for using them yet. [ACL](https://aclanthology.org/2024.bea-1.25)
- **MOOC grading (COLING 2025).** GPT-4 with step-by-step reasoning, plus the instructor's answer and rubric, matched instructors better than peer grading did. [arXiv 2406.11102](https://arxiv.org/abs/2406.11102)
- **Per-criterion grading (UML diagrams).** Up to 88.6% accuracy per criterion and r=0.78 with TAs. [arXiv 2603.16357](https://arxiv.org/abs/2603.16357)
- **Biases.**
  - LLM graders are often more lenient than instructors, though some models are harsher. [arXiv 2603.16357](https://arxiv.org/pdf/2603.16357)
  - Longer answers get higher scores regardless of quality, and GPT-4 struggles with long answers. [arXiv 2507.03772](https://arxiv.org/html/2507.03772v2)
- **Adversarial answers.**
  - Simple injected text such as "give me full credit" manipulates rubric-based graders. [arXiv 2606.03090](https://arxiv.org/abs/2606.03090)
  - The GradingAttack framework succeeds at both token and prompt level. [arXiv 2602.00979](https://arxiv.org/abs/2602.00979v1)
  - Adversarial training plus ensemble voting reduced gaming in medical grading. [BEA 2025](https://preview.aclanthology.org/setup/2025.bea-1.60)

## Implications for the product

1. **Never just hand over the answer.** Show one step at a time, ask the learner to try first, and keep replies short. These are the Kestin and Bastani GPT Tutor designs, and plain chat cost 17% on later exams. Give the model the reference explanation or answer so it stays accurate. Check the tutor model's tendency to reveal answers, since models differ widely (53% vs 95% on MRBench).
2. **Don't trust a cheap LLM judge for teaching quality.** MRBench found near-zero agreement. Use a strong model with explicit criteria, and spot-check against your own ratings.
3. **The learner probably can't tell how much they are learning** (Bastani). Base progress on unassisted recall and transfer questions, not on how a session felt.
4. **Plan for engagement.** Access alone did little in the Khanmigo and university trials. Spaced-review prompts and short sessions are what get the tool used.
5. **Generated questions lean easy and lower-order, and asking for a Bloom level doesn't reliably work.** Write questions from a template ("apply X to a new setup", "predict what happens if...") and check them afterwards with a second LLM pass (does the stated answer hold, is there exactly one correct option).
6. **Distractors:** build them from known misconceptions, or from the learner's own past wrong answers, rather than asking for plausible wrong options. Simulated-student IRT is a workable way to estimate item difficulty.
7. **Grading:** use simple per-criterion rubrics, mostly pass/fail checklists with a reference answer included, since agreement drops from κ≈0.5 to 0.34 with more levels. Grade several times and flag disagreements as uncertain rather than guessing. Expect κ/QWK around 0.5–0.65, below human-human agreement.
8. **Guard against known grader failures.** Correct for length (or cap answer length), treat the answer as data rather than instructions, and lean toward strictness to offset leniency. Let the learner dispute a grade. Prompt-injection risk is low for a single motivated learner, but answers that over-explain will be over-rewarded.
9. **Use grading as feedback, not final judgment.** Higher-order answers are where LLM grading is least reliable, so show the rubric criteria that were missed and let the learner self-assess before their spaced-review schedule is updated.

---

# Part: Prerequisites and knowledge components

# Literature notes: concept prerequisites, LLM-generated knowledge components, and LLM knowledge tracing

The session's web-search limit (shared across agents) ran out near the end. Two things are therefore not covered: a separate check for other 2025–26 LLM-prerequisite papers (e.g. "Dong et al. 2025", which LECDPR cites as an LLM baseline), and the Open-ended KT paper (Liu et al. 2022). Ask me to continue if you need them. I fetched and read every number below from the linked source unless I say otherwise.

## 1. Learning prerequisite relations between concepts

**How well people agree on labels.** Agreement is moderate. Since F1 against these labels is capped by how much the annotators themselves disagree, treat that ceiling as the main constraint.
- **Talukdar & Cohen 2012** (Wikipedia, Mechanical Turk) https://aclanthology.org/W12-2037.pdf
  - 5 domains (meiosis, public-key crypto, parallel postulate, Newton's laws, global warming), 200–400 pairs each.
  - Pairwise κ between frequent workers was 0.47–0.63, mean **0.54** ("moderate").
  - A MaxEnt classifier trained on the other four domains and tested on the held-out one beat random by only **+8.6 points accuracy** on balanced classes.
- **Gordon et al. 2016** (ACL Anthology topics, 8 judges, 6–8 hours each) https://aclanthology.org/P16-1082.pdf
  - Agreement on "would understanding topic 1 help with topic 2" was Pearson r = **0.357** overall (0.395 among NLP researchers, 0.329 among non-experts).
  - Judges often marked pairs as mutually helpful, i.e. prerequisites are often graded and two-way rather than strict.
- **Pan et al. 2017** (Coursera MOOCs: ML, data structures & algorithms, calculus) https://aclanthology.org/P17-1133.pdf
  - Three annotators with domain background, three labels; κ = **0.59–0.65**.
  - 1,411–5,676 labeled pairs per dataset.
- **LectureBank (Li et al. 2019)** https://arxiv.org/pdf/1811.12181
  - 1,352 lecture files, 208 topics, 921 positive pairs vs 41,829 negative (about 2% positive).
  - Two NLP PhD students labeling binary yes/no: κ = **0.7**.
  - The earlier three-way labeling of the same pairs (Fabbri et al.) got κ ≈ **0.3**.
  - Lesson: a binary question plus a reference curriculum roughly doubles agreement.
- **LectureBankCD (Li et al. 2021, ACL)** https://ar5iv.labs.arxiv.org/html/2105.03505
  - Domains: NLP (322 concepts, 1,551 positive pairs), computer vision (201 / 871), bioinformatics (100 / 234).
  - κ = 0.64 for CV and 0.80 for BIO.

**Methods before LLMs.**
- **RefD (Liang et al. 2015)** https://aclanthology.org/D15-1193.pdf
  - An unsupervised score of how asymmetrically two Wikipedia articles link to each other, compared against a supervised MaxEnt classifier.
  - Matches or beats MaxEnt on accuracy. Recovered F1 values include **71.9** (marked significant). MaxEnt overfits: high precision, low recall.
  - Used on the CrowdComp dataset and on a Course dataset (CS 678 pairs, MATH 658 pairs).
  - Performance varies a lot by domain, depending on how well Wikipedia covers it.
- **AL-CPL datasets (Liang et al. 2018, active learning)** https://ojs.aaai.org/index.php/AAAI/article/view/11396 ; stats from https://backiee.wasmer.app/https_github_com/Damon03/AL-CPL-dataset
  - Data mining 120 concepts / 826 pairs; geometry 89 / 1,681; physics 153 / 1,962; precalculus 224 / 2,060. 29–35% of pairs are positive.
  - Query-by-committee was the best active-learning strategy, reducing the labels needed. I did not get its F1.
- **Pan 2017** reached F1 of about **72.6** on ML (+10.5 over the T-SRI baseline, which scored 62.1–65.2). A hyponym-pattern baseline had high precision and terrible recall (ML F1 29.0).
- **LectureBank** baselines: best F1 about **0.72–0.75** (SVM on Doc2Vec with oversampling). The graph autoencoders (GAE and VGAE) had high recall but low precision. The authors explicitly prefer high recall: it's better to surface too many prerequisites than to miss one.
- **Cross-domain transfer (CD-VGAE)**: NLP→CV F1 0.675 and NLP→BIO 0.651, against in-domain supervised scores of 0.817 / 0.806. Transfer without target-domain labels keeps roughly 80% of supervised performance.

**LLM-era results.**
- **Yang et al. 2024**, "Leveraging LLMs for Concept Graph Recovery…" https://arxiv.org/html/2402.14293
  - GPT-4 zero-shot on LectureBankCD: F1 **0.795 NLP / 0.763 CV / 0.774 BIO, average 0.777**.
  - Best supervised baseline (Node2Vec): average 0.747 (0.618 / 0.817 / 0.806).
  - So GPT-4 wins clearly on NLP but loses to supervised methods on CV and BIO.
  - Limitation: the number of pairs grows quadratically, so they evaluated sampled edges rather than all pairs.
  - The same paper's TutorQA benchmark has 500 expert-checked QA pairs; adding the recovered graph improved some tasks by up to 26% F1.
- **LECDPR (IJCAI 2026)** https://www.ijcai.org/proceedings/2026/0567.pdf
  - Benchmarks are balanced 50/50 (LectureBank 246 concepts, 601 positive + 601 negative; a MOOC set with 406 concepts; UCD with 407).
  - Plain LLM baselines: Qwen2-7B F1 0.79 and GPT-4o-mini F1 0.81 on LectureBank, and about 0.77–0.80 on MOOC and UCD.
  - The best graph neural network (GKROM) is close (F1 0.81–0.84).
  - LECDPR itself uses an LLM to write concept descriptions, then a GNN with contrastive alignment: F1 **0.86 / 0.89 / 0.85**, AUC 0.92–0.95.
  - Caveat: balanced test sets inflate F1 compared with the real ~2% positive rate.
- **Le & Abel 2025** https://arxiv.org/html/2507.18479
  - 13 LLMs generate prerequisite skills for 3,196 ESCO skills.
  - Best BERTScore F1 0.835 (LLaMA4-Maverick); Claude-3.7-Sonnet 0.817.
  - BERTScore is a text-similarity metric, not edge-level F1. The authors note that high BERTScore can coexist with low semantic similarity, which suggests surface matching.
- **Yang et al. 2025** https://arxiv.org/abs/2504.08856 found GPT can produce usable course concepts and relations. The abstract I read had no numbers.

**Takeaway.** Zero-shot frontier LLMs are already at or above supervised methods (~0.75–0.80 F1 on balanced or sampled pairs). Human agreement is only κ 0.5–0.7, so the remaining headroom is small and partly label noise. Benchmarks are tiny (100–400 concepts) and mostly about NLP, ML or school maths. None of them is conditioned on what a particular learner already knows.

## 2. LLM-generated knowledge components (KCs) and Q-matrices

A knowledge component is a skill or concept tagged to a question; a Q-matrix records which KCs each question requires.

- **KCGen-KT (Duan et al.)** https://arxiv.org/html/2502.18632v3
  - Method: GPT-4o reads representative student code submissions, proposes KCs per problem, then clusters and summarizes them. CodeWorkout went from 103 to 50 KCs; FalconCode from 161 to 60.
  - Data: CodeWorkout has 246 students, 50 problems, 10,834 submissions. FalconCode has 3,267 students, 157 problems, 28,617 submissions.
  - Predicting future student responses (AUC), generated KCs beat human-written KCs and the baselines:

    | Dataset | Generated KCs | Human KCs | TIKTOC | Code-DKT |
    |---|---|---|---|---|
    | CodeWorkout | **0.816** | 0.797 | 0.788 | 0.766 |
    | FalconCode | **0.771** | 0.752 | 0.728 | — |

  - Learning-curve fit (performance factor analysis, PFA): R² 0.21 for generated KCs vs 0.18 for human ones.
  - Two instructors judged 98.6% of KCs clear and 93.2% of problem–KC mappings correct. Coverage matched or exceeded the human set in 96% of cases. Instructor agreement κ was 0.594.
  - Failure: because KCs are generated per problem, the pipeline misses KCs that several problems share.
- **Moon, Davis, Neshaei & Dillenbourg (EDM 2025)** https://arxiv.org/html/2409.20167v2
  - GPT-4o extracts KCs from multimedia questions, followed by embedding clustering. Tested on 5 courses from the OLI platform's data in CMU DataShop, from 17K to 3.3M transactions.
  - KT with PFA, LLM KCs vs human KCs: French AUC 0.787 vs 0.752, Computing 0.723 vs 0.699, Statics 0.751 vs 0.693.
  - With DAS3H, DKT and SAKT the two were roughly tied.
  - Fit of the additive factors model (AFM, the standard learning-curve model; RMSE): roughly a tie (Statics 0.395 vs 0.394; French 0.363 vs 0.345, human better; Computing 0.397 vs 0.416, LLM better).
  - Failures:
    - More than 50% of the data was lost in preprocessing (Flash and audio content).
    - The item-blocked AFM got worse as KCs got finer (sparsity).
    - The models that concatenate skills could not use multi-KC tags.
- **Wang, Lin & Koedinger (CMU)** https://arxiv.org/html/2511.09935v1
  - 646 multiple-choice questions. The LLM produced **569 KCs vs 101 from experts**.
  - Item-blocked AFM RMSE: plain LLM 0.4285; after merging KCs at cosine similarity 0.8, 0.4259; expert model **0.4206**.
  - The LLM KCs never beat the expert model. The failure mode is too many redundant, near-duplicate KCs, and merging helps.

**Takeaway.** LLM KCs match or beat human KCs as features for prediction (AUC), and roughly match them on learning-curve fit. The main problem is granularity and deduplication. Validating KCs needs response data (AFM or PFA fit); judging labels by eye is not enough.

## 3. LLM-based knowledge tracing (KT)

KT means predicting whether a student will answer the next item correctly from their history.

- **Neshaei et al. (EDM 2024)** https://arxiv.org/html/2403.14661v1
  - Datasets: Statics (282 users, 189K responses), ASSISTments09 (278K responses), ASSISTments17 (935K responses).
  - Zero-shot GPT-3.5 was at chance: AUC **0.49–0.50**.
  - Fine-tuned GPT-3 (babbage-002): AUC 0.68–0.71. That roughly equals BKT (0.63–0.71) and is below DKT (0.75–0.83).
  - GPT-2 produced invalid tokens; BERT collapsed to always predicting the majority class.
- **Bhattacharyya et al. (EDM 2026)**, "Specialised KT Models Outperform LLMs" https://arxiv.org/html/2603.02830
  - Data: 512K responses from 12.8K students, 66% correct.
  - Accuracy and F1:

    | Model | Accuracy | F1 |
    |---|---|---|
    | SAKT | 72.7% | 0.669 |
    | DKT | 71.8% | 0.650 |
    | Llama-1B, LoRA fine-tuned | 71.0% | 0.592 |
    | Gemini-2.5-flash-lite | 66.5% | 0.527 |
    | GPT-4o-mini | 58.6% | 0.579 |
    | Llama-1B, zero-shot | 33.5% | 0.251 |

  - Cost: KT models are 600–12,400 times cheaper. Serving 100K students cost under $2 a year vs $2,322 for GPT-4o-mini.
- **LKT (Lee et al. 2024)** https://arxiv.org/html/2406.02893v2
  - Encoder models (BERT-style) given the question and concept text instead of IDs.
  - On the large XES3G5M (5.5M interactions): AUC **0.851** (DeBERTa) vs 0.821 for AKT.
  - On the small DBE-KT22 (167K interactions) it **lost**: 0.764 vs 0.798.
  - Zero-shot transfer to a new dataset beat DKT, which sits at 0.5 there.
- **NTKT (Norris, Gal & Bulathwela 2025/26)** https://arxiv.org/pdf/2511.02599v2
  - Fine-tuned Llama-3.2-3B on the Eedi dataset (1.9M interactions, 39.9K students): AUC **0.903** vs about 0.73 for DKT, AKT and DTransformer.
  - Their DKT baseline looks weak, and their zero-shot Llama gets 0.756, which beats it.
  - Inputs matter: concept tags only gave AUC 0.846, IDs only 0.771.
  - Unseen questions: baselines dropped from 0.777 to 0.732 while NTKT held at 0.843. It also did much better for new users from their very first interaction.
- **CLST (Jung et al., JEDM)** https://arxiv.org/html/2406.10296v1
  - Fine-tuned Mistral-7B. Trained on only 8 students, it reached AUC 0.635 vs 0.540 for DKT on NIPS34, and 0.689 vs 0.553 on ASSISTments09.
  - Gains over baselines held across 5 datasets. Cross-domain transfer within maths worked.
- **DDKT** https://arxiv.org/abs/2502.19915 was **withdrawn** for data-recording errors. Don't cite it.

**Takeaway.** Prompted LLMs zero-shot are at chance or worse at predicting correctness. Fine-tuned LLMs that see the question text help mainly with cold-start (new users or new items). Once there's enough data, small specialized KT models are about as accurate and orders of magnitude cheaper.

## What this means for the product

1. **Use Claude to propose prerequisites, not to decide them.** Zero-shot edge F1 of about 0.78 is near human agreement, but that still means many wrong or missing edges. Bias toward recall, as LectureBank argues, and let the learner prune with "I know this" (cheap feedback).
2. **Ask binary, curriculum-anchored questions** ("Must you understand A to follow B, per a standard grad ML syllabus?"). Moving from three labels to binary took κ from 0.3 to 0.7. Expect graded and mutual dependencies (Gordon).
3. **Prerequisites are relative to the learner and the paper.** No benchmark conditions on what the learner already knows. Score "needed for *this* paper given *this* learner" directly. The quadratic number of pairs also argues against enumerating every pair: generate candidates per paper, then verify.
4. **Plan for KC sprawl.** LLMs over-generate KCs (569 vs 101). Deduplicate by embedding (cosine ≈0.8), keep a canonical concept store, and reuse KCs across papers. Per-problem generation misses shared KCs (KCGen-KT).
5. **Don't ask Claude "will the learner get this right?"** Zero-shot it is at chance (AUC ~0.5). Track mastery with a simple model (BKT, PFA or a spaced-repetition scheduler) over KC-tagged quiz items. LLMs belong in item generation, KC tagging and grading, plus a text-based prior for brand-new concepts (the cold-start benefit).
6. **Validate with learning curves**, not just ratings. If error rates fall smoothly on a KC across practice, it's a real skill (AFM or PFA fit). This needs logged responses from day one.
7. **One user means permanent cold-start.** Population KT gains won't apply. Rely on semantic priors (the LLM's judgment of concept difficulty and relatedness) and propagate evidence along prerequisite edges.

---

# Part: Paper reading aids

## Literature notes: background-concept support for paper reading

Coverage caveat: I hit the session's web-search limit partway through. I did not verify DEFT, Synergi, the math-symbol-definition work, Threddy's own N, PaperQA, Elicit or alphaXiv, so none of them appear below. I also couldn't reach the full text of the CHI 2026 "Supporting or Hindering?" study ([ACM](https://doi.org/10.1145/3772363.3798788) returned 403); its search snippet says N=13 student HCI researchers read papers with and without LLM help and wrote critical reviews. Send a follow-up if you want the gaps filled. No files were written.

### 1. AI2 Semantic Reader and its components

**Umbrella paper** ([Lo et al., arXiv 2303.14334](https://arxiv.org/abs/2303.14334))
- Reports usability studies with "300+ participants" across all its prototypes.
- Lesson stated in the paper ([PDF](https://arxiv.org/pdf/2303.14334)): "even slight errors in these models can have detrimental effects on the readers."
- LLMs let the team "quickly test different granularities and complexity-levels" of summaries without retraining models.
- Ethics warning: efficiency tools "may encourage readers to take shortcuts that lead to incorrect understanding." They recommend supporting triage plus provenance and verification instead of raw throughput.

**ScholarPhi** ([Head et al., CHI 2021](https://arxiv.org/pdf/2009.14237)): position-sensitive definitions of terms and symbols.
- Formative study (N=9 readers thinking aloud for 40 min): 8 of 9 got confused by terms. Confusing items included out-of-field terms, paper-invented terms ("symbolic validator"), shorthand, and vague back-references. Readers avoid outside lookups because it pulls them away from the text. One reader hand-wrote symbol glossaries in the margins.
- Usability study: N=27 (18 PhD students; 13 in ML), within-subjects comparison of Basic PDF vs. Declutter vs. ScholarPhi.
  - ScholarPhi was about 45 s faster per question than Basic. Readers viewed less of the paper and rated it higher on Ease and Confidence.
  - There was no significant gain in correctness. The reason is the most important failure in this set: on a question about the symbol T, which the paper uses inconsistently, readers "almost always answered incorrectly" with ScholarPhi. They assumed the definitions list was complete. The authors' conclusion: the tool "can mislead if it implies incorrect information."
- Usage during 15 min of free reading:
  - 96% used at least one feature.
  - Definition tooltips were the most used (median 10 symbol tooltips and 5 term tooltips) and "unanimously appreciated."
  - Equation diagrams: 21 of 27 opened at least one.
  - The up-front "priming glossary" was used least; only 6 of 27 spent 10 s or more on it. Some readers went to it as a fallback when a tooltip lacked depth.
  - Declutter split opinion; some readers preferred Ctrl-F.
- The production version's definition detector is HEDDEx ([Kang et al. 2020](https://arxiv.org/pdf/2010.05129)). It beats the prior system by 12.7 F1 at sentence level and 14.4 F1 at document level, but the high-recall document-level task "is much lower" in performance. ScholarPhi cites about 73% precision and 74% recall for definition recognition ([PDF](https://arxiv.org/pdf/2009.14237)).

**Paper Plain** ([August et al., TOCHI 2023](https://arxiv.org/pdf/2203.00130)): helps non-experts read medical papers.
- Formative study (N=12): nearly all participants struggled with jargon. Dense text and not knowing what to read were as big a barrier as individual terms.
- Main study: N=24, comparing four interface variants.
  - Paper Plain vs. plain PDF: reading difficulty about 1.98 points lower on a 5-point scale (p<.0001); understanding +1.18 (p=.002); relevance +1.17 (p=.003).
  - Comprehension was non-inferior (3.67 vs. 3.50 out of 7).
- Key finding: when all features were available, readers chose the Key Question index plus "answer gists" (13 to 14 clicks each). Only 8 of 12 touched section gists or term definitions, averaging 4 definition clicks. 18 of 20 readers named the Key Questions the most helpful feature.
- The Semantic Reader authors read this as: passage-level summaries let readers "bypass definitions of individual terms" ([Lo et al.](https://arxiv.org/pdf/2303.14334)).
- During iteration, readers double-checked generated gists against the original text because the gists were vague.

**CiteSee** ([Chang et al., CHI 2023, Best Paper](https://arxiv.org/pdf/2302.07302)): personalizes citations from the reader's history.
- Lab study N=10, field deployment N=6.
- 57% of discoveries in the field came from inline citations.
- Citations the reader had seen before were only 8.2% of all citations but 37% of the paper cards readers opened, about 4.5 times over-represented. Connecting new material to what the reader already knows draws attention strongly.

**Scim** ([Fok et al., IUI 2023](https://ar5iv.arxiv.org/html/2205.04561)): faceted highlights to support skimming.
- Lab study N=19: 94 s vs. 118 s per answer (p<.05), with no accuracy difference. The speed-up disappeared when the answer was outside the highlights.
- Diary study N=12: 70% of entries said highlights helped.
- Problems: missing context, errors on dense math, facet mislabels that hurt trust, mismatches with the author's own emphasis, and a risk of over-reliance.

**Relatedly and Threddy** ([Lo et al.](https://arxiv.org/pdf/2303.14334))
- Relatedly: after 20 min of literature review, participants wrote summaries rated significantly more coherent, insightful and detailed than with a baseline.
- Threddy: a lab study showed lower clipping cost without breaking reading flow.

**PaperWeaver** ([Lee et al., CHI 2024](https://arxiv.org/html/2403.02939v1)): LLM-written descriptions of a recommended paper, contextualized against papers the user has collected.
- N=15 CS graduate students.
- Understanding relevance: 6.07 vs. 3.80 (p=.001). Understanding connections to the user's papers: 5.80 vs. 3.00. No difference in workload.
- Error rates: 8% of aspect summaries and 20% of paper-to-paper comparisons contained errors. Users treated the descriptions as "supplementary bridges" and verified them.

**Qlarify** ([Fok et al., UIST 2024](https://arxiv.org/html/2310.07581v2)): abstracts that expand on demand.
- Interview study N=9, deployment N=275, comparison study N=12.
- Readers wanted four kinds of expansion: definition, instantiation (a concrete example), clarification, and motivation.
- 77.5% of expansions started from AI-suggested entities rather than manual highlighting. 58% of expansions were threaded follow-ups.
- Accuracy: 87.5% fully accurate and 5.8% inaccurate, yet interview participants didn't notice the errors. Satisfaction was 6.2 vs. 4.8 (p=.02).

**Personalized jargon identification** ([Guo et al., NAACL 2024](https://ar5iv.labs.arxiv.org/html/2311.09481))
- 10,571 familiarity ratings from 11 CS researchers on terms from 100 abstracts.
- Only 19% of terms got the same rating from everyone, even within one subfield.
- Readers' information needs were definition, background or example.
- GPT-4 prompted with the reader's own publications predicted familiarity best. The target domain was the strongest feature, and subdomain beat broad domain.

**ReadingQuizMaker** ([Lu et al., CHI 2023](https://web.eecs.umich.edu/~xwanghci/papers/CHI23-ReadingQizMaker.pdf)): instructors strongly preferred human-in-the-loop question generation ([summary](https://e-hail.umich.edu/stories/researchers-recognized-at-chi-for-work-on-human-nlp-system-to-create-reading-quiz-questions)). ReaderQuizzer ([arXiv 2308.07988](https://arxiv.org/abs/2308.07988)) generates in-paper questions with ChatGPT but has no user evaluation.

### 2. Generating definitions with controlled complexity

**August et al., ACL 2022** ([PDF](https://aclanthology.org/2022.acl-long.569.pdf))
- Dataset of 8,263 terms from MedQuAD plus Wikipedia, with each definition paired to its source abstract.
- Human evaluation with 233 MTurk raters. GeDi produced the opposite complexity to the one requested. DExperts separated levels best but was the least factual.
- Factuality: 60% of all generated definitions were flagged incorrect by at least one annotator. The SVM-reranker method was flagged 38% by one annotator and 16% by both, vs. DExperts at 86% and 67% (d=1.24).
- Takeaway: making text simpler and keeping it true pull against each other. These are pre-LLM models, so absolute error rates are outdated, but the tension remains.

### 3. Adapting complexity to the reader with LLMs

**"Know Your Audience"** ([August et al., CHI 2024](https://arxiv.org/html/2403.04979)): three studies (N=199, 191, 203), each comparing low, medium and high complexity summaries.
- Low-familiarity readers found the simple versions much easier (d≈1.5–1.6).
- High-familiarity readers rated all levels equally easy. With the simple versions they skipped nearly an extra section (d=0.90); limitations sections were the most skipped (25% of skips), yet they still rated the simple versions as engaging.
- Simplified summaries also lost information.
- When a plain-language version kept all the information, it became much longer and only helped the least-familiar readers.

**TranSlider** ([Kim et al., arXiv 2411.09969](https://arxiv.org/html/2411.09969)): a slider controlling how much the text is personalized, N=15.
- Preferences ranged widely: mean 53/100, SD 33. People reading for intrinsic reasons chose more personalization (63) than extrinsic readers (41).
- Some analogies came out "unnatural." Participants worried about inconsistency and over-reliance, and split between wanting manual control and wanting it automated.

**"Explain Like I'm 5 or Whatever I Choose"** ([Panigrahi & August, arXiv 2606.06788](https://arxiv.org/pdf/2606.06788))
- 13 of 16 participants valued a direct-manipulation complexity control over re-prompting.
- Across 5 LLMs (GPT-5.1, Claude Sonnet 4.5 among them) and 557 queries, models moved complexity measures in the requested direction at most 33.67% of the time.

**LLM concept maps** ([Han & Choi, BEA 2025](https://aclanthology.org/2025.bea-1.58.pdf)), N=14 undergraduates:
- 31.5% lower perceived load (5.0 vs. 7.3, p<.001) and 14% faster on the assessment.
- Accuracy roughly equal (98% vs. 97%), but readers spent 22.6% more time with the map than reading linearly.

### 4. Commercial and 2024–26 tools

- Explainpaper and SciSpace Copilot ([AAAI 2024](https://ojs.aaai.org/index.php/AAAI/article/view/30578); [overview](https://devtoollab.com/ai-tools/explainpaper)) explain whatever passage you highlight, with citations. They're reactive and keep no learner model or prerequisite tracking.
- PaperFlow ([arXiv 2606.07454](https://arxiv.org/pdf/2606.07454)) maintains an inspectable user profile that tracks interest drift, but for recommending papers, not teaching background. Its real-user pilot had only 5 people.
- I found no peer-reviewed tool that infers a specific reader's prerequisite gaps for a specific paper and then teaches and maintains them. Guo et al. (familiarity prediction) and PaperWeaver/CiteSee (anchoring to the reader's history) are the closest building blocks.

### Implications for the product

1. **Estimate gaps per person, not per field.** Familiarity varies a lot even between researchers in the same subfield (only 19% agreement). Seed the learner model from the user's own papers and code, and get feedback from the user. LLM prompting with the user's publications beat feature-based models ([Guo](https://ar5iv.labs.arxiv.org/html/2311.09481)).
2. **Default to just-in-time, in-context help.** Tooltips were the most used and most liked; an up-front glossary was mostly ignored ([ScholarPhi](https://arxiv.org/pdf/2009.14237)). Keep a pre-reading primer optional and short. Some readers did study a glossary for 2–5 minutes, so keep it available.
3. **Make the paper's own structure the entry point.** Question- and gist-based navigation beat term definitions when both were present ([Paper Plain](https://arxiv.org/pdf/2203.00130)). Present background concepts as answers to "what do I need to follow section X?", not as a vocabulary list.
4. **Offer four kinds of help, not just definitions:** definition, concrete example, clarification, and motivation/background ([Qlarify](https://arxiv.org/html/2310.07581v2); [Guo](https://ar5iv.labs.arxiv.org/html/2311.09481)).
5. **Don't over-simplify for an expert user.** Experienced readers skip more and lose limitations content when text is simplified ([Know Your Audience](https://arxiv.org/html/2403.04979)). For an ML research engineer, link concepts to things they already know (CiteSee's 4.5× attention effect; PaperWeaver's comparisons to the user's own papers) instead of writing plain-language versions.
6. **Give the user an explicit depth control, and validate the output.** Preferences vary widely, and LLMs follow complexity requests inconsistently (at most 34%). Check generated levels against each other automatically ([ELI5](https://arxiv.org/pdf/2606.06788); [TranSlider](https://arxiv.org/html/2411.09969)).
7. **Build verification in and show what's missing.** Measured error rates were 6–20% (Qlarify, PaperWeaver), and users often fail to spot errors. Incompleteness misleads too (ScholarPhi's "T" symbol). Attribute every explanation to a source passage, and say when coverage is partial.
8. **Measure comprehension, not only ease.** Every study improved ease, speed or confidence, but comprehension gains were mostly null (ScholarPhi, Paper Plain, Scim, concept maps). Over-reliance and shortcut reading came up repeatedly. Fitting for a tool that maintains knowledge: add retrieval checks such as in-paper questions in the style of ReaderQuizzer and ReadingQuizMaker, and spaced review.

---

# Part: Calibration, fact decomposition, dedup and evaluation

Search budget note: the shared web-search limit (200 per turn) ran out partway through topic 4. Simulated-student pitfalls, TaxoInstruct, concept-map generation and the "simulated learners overestimate competence" line therefore have only partial or no coverage. Every number below comes from a page I fetched, except one item marked UNVERIFIED.

## 1. Calibration, abstention, and knowing what they don't know

- **Kadavath et al. 2022 (Anthropic).** Large models are well calibrated on multiple-choice and true/false questions when the question is formatted correctly. Self-evaluation "P(True)" (the model proposes an answer, then rates whether it is correct) calibrates and scales well. "P(IK)" (predicting "I know" before answering) works within a task, but its calibration degrades on new tasks. P(IK) rises when relevant source material is put in context. https://arxiv.org/abs/2207.05221v1
- **Tian et al. 2023 ("Just Ask for Calibration").** For RLHF models (ChatGPT, GPT-4, Claude), confidence stated in words is better calibrated than token probabilities. It often cuts ECE by about 50% relative on TriviaQA, SciQ and TruthfulQA. https://arxiv.org/pdf/2305.14975v1
- **Xiong et al. ICLR 2024.**
  - Verbalized confidence is overconfident: values cluster at 80–100% and come in multiples of 5.
  - Average ECE across 8 datasets: GPT-4 0.18, GPT-3.5 0.377.
  - Failure-prediction AUROC for GPT-4 is only 62.7%.
  - What worked: sampling several answers and measuring agreement. AUROC averaged 73.0% this way vs 56.4% from a single answer, and GSM8K went from 54.8% to 92.7% with 5 samples.
  - https://arxiv.org/html/2306.13063
- **Semantic entropy (Farquhar et al., Nature 2024).** Take 10 samples, cluster them by bidirectional entailment, then compute entropy over the meaning clusters.
  - Mean AUROC 0.790 vs naive entropy 0.691, P(True) 0.698 and embedding regression 0.687. It held at 0.78–0.81 across LLaMA, Falcon and Mistral from 7B to 70B.
  - Failure mode: it only catches arbitrary confabulations. It misses errors the model makes consistently, which is exactly the "confidently wrong about a post-cutoff term" case.
  - https://pmc.ncbi.nlm.nih.gov/articles/PMC11186750
- **SelfCheckGPT (Manakul et al., EMNLP 2023).** Sample several times and flag sentences the samples contradict, with no external resource. It beat grey-box methods on sentence-level AUC-PR (WikiBio, GPT-3). https://aclanthology.org/2023.emnlp-main.557
- **Abstention survey (Wen et al., TACL 2025).** Frames abstention from three angles: the query, the model, and human values. https://arxiv.org/abs/2407.18418v2
- **Post-cutoff knowledge and new terms**
  - **NewTerm (NeurIPS 2024).** New terms reduce performance by more than 20%. Moving the cutoff later covers some terms but does not generalize to terms further in the future. LLM-automated benchmark construction was over 80% accurate after human filtering. https://arxiv.org/abs/2410.20814
  - **Dated Data (COLM 2024).** A model's effective cutoff often differs sharply from its reported cutoff and varies by sub-resource. Causes: old data inside new CommonCrawl dumps, and deduplication problems. So "after the cutoff date" is not a safe proxy for "unknown to the model." https://arxiv.org/abs/2403.12958
  - **FreshQA (Vu et al., ACL Findings 2024).** All model sizes struggle with fast-changing facts and false premises. FreshPrompt (search results in the prompt) beat Self-Ask and Perplexity. The number and order of retrieved evidence matter. https://arxiv.org/abs/2310.03214v2
- **Made-up terms**
  - **PhantomBench (Jung & Gonen, 2026).** Over 60K nonexistent terms, checked against Dolma, tested on 21 models.
    - Average hallucination rates reach 86.7%, and meaning hallucination is 87.3% for Gemma 3-12B.
    - Asking "does X exist?" directly does much better (14.3% for Llama 3.1-8B).
    - Hallucination is worst when the prompt presupposes the term exists.
    - 35.9% of abstentions still contained fabricated content.
    - Reasoning models (DeepSeek-R1, GPT-OSS-20B) hallucinated more than instruction-tuned models.
    - https://www.emergentmind.com/papers/2606.11105
  - **HypoTermQA.** 784 hypothetical terms, 19,508 questions. https://avesis.metu.edu.tr/yayin/b759b484-da69-44dd-b330-f34277678065/hypotermqa-hypothetical-terms-dataset-for-benchmarking-hallucination-tendency-of-llms
- **"Why language models hallucinate" (Kalai et al., OpenAI 2025)**
  - After pretraining, the hallucination rate is at least the fraction of facts seen only once in training (the "singleton rate").
  - Accuracy-only grading rewards guessing.
  - Proposed fix: state a confidence threshold t in the prompt and penalize wrong answers by t/(1−t). That is a 1-point penalty at t=0.5, 2 at 0.75 and 9 at 0.9.
  - https://arxiv.org/html/2509.04664
  - UNVERIFIED (the blog returned 403): the blog's SimpleQA table, as I recall it, shows gpt-5-thinking-mini at about 52% abstain / 26% error vs o4-mini at about 1% / 75%. A secondary paper reports a roughly 2:1 abstain-to-hallucinate ratio for gpt-5-thinking-mini. https://arxiv.org/pdf/2609.17686
- **Citation grounding**
  - **ALCE.** About 50% of ChatGPT and GPT-4 generations on ELI5 were not fully supported by the passages they cited. Its citation recall and precision metrics correlate with human judgment. https://arxiv.org/pdf/2305.14627
  - **Self-RAG.** Retrieval on demand plus reflection tokens improved factuality and citation accuracy over ChatGPT. https://arxiv.org/abs/2310.11511
  - **Fabricated references.** 55% of GPT-3.5 references and 18% of GPT-4 references were fabricated. Across 13 LLMs, citation hallucination ranged from 14% to 95%. https://arxiv.org/pdf/2603.03299

## 2. Atomic fact decomposition

- **FActScore (Min et al. 2023).** InstructGPT scored 42.5% and ChatGPT 58.3%. The automated estimator has less than 2% error. https://arxiv.org/pdf/2305.14251
- **SAFE/LongFact (Wei et al. 2024).** Agreed with crowd annotators on 72% of about 16k facts. On 100 disagreements, SAFE was right 76% of the time. It is more than 20x cheaper than humans. https://nips.cc/virtual/2024/poster/96675
- **VeriScore (Song et al. 2024).** Extracts only verifiable claims, so hypotheticals and examples are not penalized. Humans preferred its claims 93% of the time. https://arxiv.org/html/2406.19276v1
- **Wanner et al., *SEM 2024.** Decomposition is not neutral.
  - The same text scored FActScore 24.1% to 35.3% depending on how it was decomposed.
  - DecompScore (decomposition quality) was 42.3 for the Russellian/neo-Davidsonian method vs 31.7 for FActScore's own decomposer.
  - https://arxiv.org/html/2403.11903v1
- **DnDScore (Wanner et al., Dec 2024).** Decomposition and decontextualization interact, and the chosen strategy changes the scores. https://arxiv.org/abs/2412.13175
- **Molecular facts (Gunjal & Durrett 2024).** Fully atomic facts become ambiguous.
  - Verification accuracy on ambiguous entities: atomic 68.7%, molecular 74.7%, SAFE-style 73.4%.
  - Claims grew from 7.61 to 14.96 words.
  - Human-rated minimality: molecular 52% minimal, simple decontextualization 16%.
  - https://arxiv.org/html/2406.20079
- **Claimify (Metropolitansky & Larson, ACL 2025).**
  - Extracts claims only when it is confident of the interpretation.
  - Entailment 99.0%, about the same as VeriScore's 99.2%; DnD 89.1%, SAFE 96.6%.
  - Element coverage accuracy 87.9% vs DnD 76.9%, SAFE 74.6%, VeriScore 64.7%.
  - Decontextualization judged desirable about 80.6% of the time.
  - Human inter-annotator α went from 0.44 to 0.72 after practice rounds.
  - https://arxiv.org/html/2502.10855
- **Core (Jiang et al., ACL Findings 2025).** FActScore-style metrics can be gamed by adding trivial or repeated subclaims. Core filters subclaims for uniqueness and informativeness, which makes the metrics robust. https://arxiv.org/abs/2407.03572v2

## 3. Dedup, entity resolution and organization

- **Peeters et al. (entity matching).**
  - GPT-4 zero-shot averaged F1 86.80. It matched or beat fine-tuned Ditto on 3 of 6 datasets.
  - On unseen entities, fine-tuned PLMs fell 22–61% F1, and GPT-4 beat the best transferred PLM by 34%.
  - SOLAR (open model) scored 80.08.
  - Caveat: no single prompt is best; it must be tuned per dataset.
  - https://arxiv.org/html/2310.11244v3
- **Few-shot clustering (Viswanathan et al., TACL).** Find the closest distinct pairs in embedding space and use the LLM as a must-link / cannot-link oracle. This was state of the art on entity canonicalization, so the useful pattern is embeddings to find candidates and an LLM to decide. https://arxiv.org/pdf/2307.00524
- **TopicGPT (NAACL 2024).** Harmonic purity 0.74 / 0.57 vs LDA 0.64 / 0.52 and BERTopic 0.58 / 0.39. LDA remains a strong baseline. https://arxiv.org/pdf/2311.01449
- **Chain-of-Layer (CIKM 2024).** Builds the taxonomy top-down, layer by layer, with an ensemble ranking filter to cut hallucinated nodes. It was state of the art on 4 benchmarks but was later beaten by TaxoAdapt, which found poor path granularity. https://arxiv.org/pdf/2402.07386, https://arxiv.org/pdf/2506.10737
- **LLMs4OL (ISWC 2023).** Zero-shot tests of 9 model families on term typing, taxonomy discovery and relation extraction. Fine-tuned smaller models often beat larger zero-shot ones. https://arxiv.org/pdf/2307.16648

## 4. Evaluation without ground truth

- **MT-Bench (Zheng et al. 2023).** GPT-4 agreed with experts on 85% of non-tied pairs, vs 81% between humans. Known biases: position, verbosity and self-enhancement. https://papers.pytorch.kr/papers/2306.05685
- **Self-preference (Panickssery et al., NeurIPS 2024).** Judges can recognize their own outputs and favor them, and stronger self-recognition goes with stronger self-preference. A Claude judge grading Claude extractions is the risk case. https://arxiv.org/abs/2404.13076v1
- **Judging the Judges (Thakur et al.).** 13 judges tested. Even the best differed from human scores by up to 5 points. Judges were lenient and could be fooled by dummy answers. Percent agreement hides the gaps (use kappa). Rankings are more robust than absolute scores. https://arxiv.org/abs/2406.12624v5
- **Norman et al. 2026.** 21 judges, about 541K judgments.
  - Kappa ran 33–41 points below exact-match agreement.
  - A judge's rank shifted by up to 14 positions depending on the benchmark.
  - Two judges had test-retest reliability above 0.95 yet position bias above 0.10, so consistency does not imply validity.
  - Verbosity bias was minimal.
  - https://arxiv.org/abs/2606.19544
- **Rubric-based judging**
  - **Prometheus.** Pearson 0.897 with humans when given rubrics, vs 0.392 for ChatGPT. https://arxiv.org/abs/2310.08491
  - **HealthBench.** 48,562 conversation-specific criteria written by 262 physicians. https://arxiv.org/abs/2505.08775
- **Simulated students**
  - **Generative Students (Lu & Wang, L@S 2024).** 45 GPT-4 personas defined by which concepts they know. Their hard items overlapped considerably with real students' hard items. https://arxiv.org/abs/2405.11591
  - **MalAlgoPy (Sonkar et al.).** Training a model to imitate misconceptions costs it correct-solving ability. Mixing correct examples back in, at ratios as low as 0.25, fixes this. Prompting alone is a weak way to make a capable model "not know." https://arxiv.org/abs/2410.12294
  - **Liu et al.** Personality-aware simulation produces diverse responses, but evidence of validity is qualitative. https://arxiv.org/abs/2404.06762

## Implications for the product

1. **Don't trust the cutoff date or the model's self-report to flag unknown concepts.** Effective cutoffs drift, verbalized confidence clusters at 80–100%, and over 86% of nonexistent terms get defined anyway. Use several signals together:
   - ask "does X exist / do you know X?" separately, before asking for a definition (the presupposition effect);
   - check agreement across samples (semantic-entropy style);
   - check whether the term is grounded in the paper or retrieved text.
   Treat abstentions as possibly still containing fabrication (35.9%).
2. **Self-consistency won't catch consistent misconceptions.** For terms that appear in the paper, use the paper as the authority: the definition must be entailed by the source text, ALCE/Claimify style. Ungrounded definitions of new terms should be flagged, not taught.
3. **Extract at "molecular" granularity, and allow refusal on ambiguous text.** Use Claimify-style "extract only when confident" and VeriScore-style "verifiable only" filters. Apply Core-style uniqueness and informativeness filters so trivial facts don't pad the pool.
4. **Dedup = embedding candidate pairs + LLM match/no-match decision.** This is the Viswanathan / Peeters pattern. Tune prompts on a small labeled set of your own concept pairs.
5. **Without ground truth:**
   - build checklist rubrics specific to each concept (HealthBench / Prometheus style);
   - use a judge from a different model family to avoid self-preference;
   - randomize presentation order;
   - report kappa and test-retest, not percent agreement;
   - spot-check a small human-labeled audit set (on the order of 100 items);
   - plant fake terms (PhantomBench style) and terms published after the model's training as canaries to measure the flagging rate directly.
6. **Simulated learners are useful for item difficulty, but don't trust them to model genuine ignorance.** Ablate the concept's text from context, or use a weaker model, rather than prompting "pretend you don't know X."

Not verified or not covered, because of the search limit: TaxoInstruct, LLM concept-map generation, and direct studies showing LLM-simulated novices overestimate their competence. A follow-up turn can fill these in.
