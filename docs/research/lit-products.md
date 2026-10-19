# Literature notes: products and practitioners

Compiled verbatim from four research sub-agents' final reports. Their shared web-search budget ran out partway, so coverage gaps are noted inside each section.

---

# Part: AI flashcards and spaced-repetition overload

I've covered the main topics, but not everything you asked for. The web search budget ran out partway through, so a few products and stats have no evidence below. Those are listed under "Gaps" at the end. A follow-up turn could fill them in.

# 1. AI-generated flashcards: what goes wrong

## The best evidence: Kirkby & Matuschak's "Memory Machines" report (2026)
- **Source:** https://memory-machines.com/report
- **Setup:** Ozzie Kirkby and Andy Matuschak built the `srs-prompts` dataset: about 1,500 memory prompts taken from 93 sources, each graded on a four-tier quality scale. They tested Claude Opus/Sonnet, GPT-4o/5, Gemini 2.5/3 Pro, Qwen3, DeepSeek and others.
- **Headline result:** the best model, GPT-5.2, still produced unusable prompts **36%** of the time. GPT-4o was at 71% and Claude 3.7 Sonnet at 56%.
- **Their four tiers:**
  - **T0, off-target:** misses what the user highlighted.
  - **T1, needs refactor:** "looks plausible—often even aligned with what you want—but won't reliably survive long-horizon review." This is the most dangerous failure, because it costs you thought during review and is still unstable.
  - **T2, needs polish:** minor problems that can be fixed.
  - **T3, ready to review.**
- **What models can and can't judge:** they reliably spot T0 cards but struggle to tell T1 from T2. In the authors' words, "taste in construction" doesn't come through prompting, rubrics, or fine-tuning.
- **What helped:** "grounding," meaning showing the model graded examples from the same passage. This raised precision from 56% to 78%.
- A secondary summary of the report (https://evakeiffenheim.substack.com/p/when-ai-flashcards-pollute-your-anki) says the failures are mostly structural: ambiguous questions, wordiness, and cards that only make sense with the source in front of you. Outright hallucinations are less common. It also quotes the line "LLMs lack the 'taste' required to project whether a flashcard will be timeless enough to go into your deck." I took that from the secondary summary and did not check it against the report itself.
- **Takeaway for us:** it's realistic to build an LLM filter that removes off-target cards. Judging durable quality is much harder. Showing the model good and bad examples for the same passage helps a lot.

## Matuschak's earlier notes on LLM-written prompts
- Giving GPT-4 a set of prompt-writing principles "seems to do a better job," but "it's not clear how strong or reliable these effects are… sometimes seem to matter a lot and sometimes not." https://notes.andymatuschak.org/zPXE9jtKyU7AQRBmAUQrbWQ
- **Shallow pattern matching:** learners memorize surface cues instead of the knowledge. His example: "whenever they see a 'who'-type question about quantum computing, the answer is John Preskill." Orphan prompts with little connection to other cards are the most vulnerable. Fixes he suggests: several phrasings of the same question with the same answer, encoding a fact from multiple angles, and asking the learner to apply it in a new context. https://notes.andymatuschak.org/z6S3cEUXNktEEZEzRqUXh5ivRNMWjJ2nq72Ys
- He found that GPT-3.5 and GPT-4 can generate shallow rewordings of a question, which works against pattern matching. https://notes.andymatuschak.org/zEhne31FD53eNQw3bpcuomfxMYL3s1qkhbF
- **Takeaway for us:** LLM-generated rewordings are one of the clearest wins for a tool like ours.

## Hallucinated cards: a first-hand account
- A biologist generated 100 cards with Claude and initially found only two errors. A third error surfaced later and nearly broke an experimental design. https://denovo.substack.com/p/ai-generated-anki-cards-are-not-to
  - The errors: yeast gene names used for human meiosis, a complex (TTM) the model didn't know about, and a card that named the right signaling molecule but "got the direction of the gradient backwards."
  - The author's conclusion: "learning incorrect things is really bad." They withdrew their earlier view that AI cards are "worth the risk."
- **Takeaway for us:** subtle errors are the dangerous kind, and researchers will be using these cards to make decisions.

## Other studies
- **Crk & Gultepe (Frontiers in Education, 2026):** compared 14 LLM-written and 21 human-written multiple-choice questions in an undergraduate Operating Systems course with 42 students. They found no significant difference in difficulty, discrimination, or reliability (α 0.695 human vs 0.734 LLM). Important caveat: the LLM questions were checked by experts before use. https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2026.1837523/full
- **SmartFlash (Li et al., arXiv 2602.14431):** a design study with only 6 students. They valued automation but "require transparent, editable AI outputs to maintain cognitive ownership," and saw AI as "a collaborative partner demanding verifiable reasoning rather than an autonomous agent." https://arxiv.org/abs/2602.14431
- **Bachiri et al.:** AI and human flashcards were of comparable quality in a MOOC setting. **Agnes & Srinivasan:** AI-generated mnemonic keywords improved vocabulary retention. I only saw both through search summaries (related-work citations, e.g. Memdora https://arxiv.org/pdf/2607.25096) and did not read the original papers.
- **Hobbyist blind comparison (r-bloggers, 2024):** tested GPT-4 Turbo, GPT-3.5 and local Llama-family models on cards about Fleiss' kappa. https://www.r-bloggers.com/2024/01/comparing-gpt-4-3-5-and-some-offline-local-llms-at-the-task-of-generating-flashcards-for-spaced-repetition-e-g-anki/
  - GPT models won.
  - "Would I use this card" ratings did not correlate with the other quality ratings.
  - On curating the input by hand: "if I need to manually curate the input text, I could just as well create the flashcards without the help from AI."
- **Memdora (arXiv 2607.25096):** criticizes the standard card format as "a single binary gesture: flip and self-rate." https://arxiv.org/abs/2607.25096

## Generation effect: what you lose by not writing your own cards
These figures come from the secondary summary above (https://evakeiffenheim.substack.com/p/when-ai-flashcards-pollute-your-anki); I did not read the originals.
- **Bertsch et al. (2007):** meta-analysis of 86 studies, generation effect d = 0.40.
- **Pan et al. (2022):** six experiments; cards learners made themselves beat premade cards, d = 0.45 for memory and d = 0.29 for application.
- **Barcaui (2025):** students who used ChatGPT freely scored 57.5% on a test 45 days later, versus 68.5% for the control group.
- **An et al. (2025):** AI-written practice questions that instructors reviewed first gave 89% accuracy, versus 73% without review.
- **RemNote itself admits the effect:** "information you produce yourself, by hand, is remembered better than information you read." https://www.remnote.com/blog/traditional-vs-ai-flashcards

## What users say
- **HN thread on the Anki-LLM bulk card generator:** https://hn.svelte.dev/item/45790443
  - treetalker: making the cards "contributes substantially to the learning."
  - ATMLOTTOBEER: aim for "as few cards as possible," because thousands of cards mean "a half hour or more per day doing reviews."
  - thomascountz: he "never find[s] the cards to be useful by default."
- **LessWrong (Jacob G-W):** "There are a lot of those services, but they usually generate bad cards." https://www.greaterwrong.com/posts/aPzhXZw7Zbm7PqXkZ/open-and-welcome-thread-may-2023/comment/5ZNQLjiff4ttHrjwJ
- **RemNote feedback board:** users say explanations on AI multiple-choice cards are "bare-bones" and ask for "Why True" and "Broader Context" buttons. https://feedback.remnote.com/p/improved-ai-flashcard-insights-for-multiple-choice-cards
- **Quizlet Magic Notes:** reviews say to "check for accuracy" (https://nibble-app.com/blog/quizlet-review). App-store reviews complain that AI grading marks correct answers wrong (https://kimola.com/reports/unlock-insights-quizlet-ai-flashcards-customer-feedback-report-app-store-us-148155).
- **Anki forum proposal for a "card health report":** it would flag cards from behavior, e.g. many lapses, too much text, slow answers, or always "Easy." Commenters objected that it would be too prescriptive and that beginners wouldn't know what thresholds to set. https://forums.ankiweb.net/t/an-intelligent-card-quality-assistant-to-help-users-avoid-common-pitfalls/63138
- **Takeaway for us:** these behavioral signals could flag bad LLM-generated cards automatically, without the user having to tune anything.

# 2. Spaced repetition overload, burnout, and quitting

## Ease hell and what FSRS changed
- **The Anki manual:** under SM-2, "repeatedly failing a card after it has graduated… could reduce its ease a lot." FSRS: "This is not a problem that FSRS suffers from." https://docs.ankiweb.net/deck-options.html
- **FSRS FAQ (quoted in the Anki forum):** "solved by mean reversion of difficulty." Pressing Good repeatedly pulls difficulty back toward a default value. https://forums.ankiweb.net/t/does-fsrs-solve-ease-hell/38275/2
- **It still happens in edge cases.** A user with a 10-year-old deck got optimized parameters (difficulty reversion 0.0701) where "the convergence of pressing Good is so slow and insignficant, that it is by all means hell." The fixes were default parameters or ignoring old review history. https://forums.ankiweb.net/t/ease-hellish-in-fsrs/44622
- **Users don't trust long intervals.** One user fought FSRS's long intervals until concluding "FSRS was right and I was wrong." They were also frustrated that a single "Again" button can't tell total forgetting from partial recall. https://forums.ankiweb.net/t/struggles-adjusting-to-fsrs/69849?page=2

## Desired retention vs. workload
- **Manual:** the default 90% "offers a good balance"; "above 97% the workload can be overwhelming." https://docs.ankiweb.net/deck-options.html
- **FSRS wiki:** workload as a function of desired retention is U-shaped. Higher retention means more reviews; lower retention means more relearning. https://github.com/open-spaced-repetition/fsrs4anki/wiki/The-optimal-retention
  - The "Compute Minimum Recommended Retention" tool finds the retention that minimizes study minutes per unit of knowledge, using simulation (Brent's method).
  - Since Anki 24.04 it optimizes workload divided by knowledge, rather than knowledge alone.
- Anki 24.11 added an FSRS simulator so users can see how daily workload changes with desired retention. https://forums.ankiweb.net/t/relationship-between-desired-retention-rate-and-dailyworkload/53702

## Anki 24.11: load balancer, Easy Days, and backlog sort order
Release notes: https://newreleases.io/project/github/ankitects/anki/release/24.11
- **Load balancer:** "within your fuzz range, Anki will now try to pick days that have fewer reviews waiting."
- **Easy Days:** "tell Anki to try avoid certain days of the week."
- **Backlog sort order:** the notes say "Decks can now be sorted by descending retrievability. Simulations have shown this is a better choice when you have a backlog, and this sort order is likely to become the default."
- **The manual seems to contradict this.** It calls "Relative overdueness" (ascending retrievability under FSRS) "generally recommended if you have a large backlog." https://docs.ankiweb.net/deck-options.html
- The two orders differ: descending reviews the cards you probably still remember first, while ascending reviews the most-forgotten cards first. It's worth checking the current Anki default before we pick one.

## SuperMemo: treat overload as normal and prioritize
- **Priority queue documentation:** https://www-v1.supermemo.com/archives1990-2015/help/priority
  - Auto-postpone: on the first start of each day, SuperMemo "will first postpone repetitions that you failed to execute on previous days… After postponing the backlog of repetitions, SuperMemo will sort today's repetitions."
  - The cost is stated openly: "In a heavily overloaded learning process, **the retention of low-priority material will drop substantially**."
  - Some randomness is allowed so that "precious articles that were displaced in priority by a massive inflow of new material" can come back up.
- **What's new in SuperMemo 2006:** "auto-postpone ensures you never need to worry about the overload of material for review"; "only your available time is now a limit." https://www-v1.supermemo.com/archives1990-2015/help/new2006
- **History of Mercy, from a search summary of supermemo.guru** (the site returned 403, so not checked directly):
  - Mercy was proposed in 1992 and spreads overdue reviews out into the future.
  - SuperMemo 2006 "dealt an ultimate death-blow to Mercy… A substantial overload becomes a norm, and the user is supposed to only do his or her best to pass as much of the top-priority material as possible." https://supermemo.guru/wiki/Mercy
  - Wozniak describes overload as natural, "an exuberant learning drive." https://supermemo.guru/wiki/Overload
- **Older SuperMemo help** (https://www-v1.supermemo.com/archives1990-2015/help/pam):
  - Postpone: "Increase intervals of elements that meet the postpone criteria."
  - Mercy: "Redistribute elements equally in a short period."
  - A warning that "massed review of related items may produce false positives."

## Burnout and quitting
- **There are no public numbers on how many Anki users quit.** On the Anki forum: "I don't think there are usage statistics like that available." https://forums.ankiweb.net/t/how-many-users-use-anki-for-long-term-retention/54053
- **The closest data is from medical students** (Baylor poster): https://cdn.bcm.edu/sites/default/files/2023-09/51-merlinsky-e.pdf
  - Students with a deck tailored to their course: 83% used Anki consistently, 10% inconsistently, 7% never.
  - Students with only generic decks: 52% consistent, 9% started and stopped, 39% never.
  - This suggests relevant, ready-made content drives adoption. I only saw these figures through a search summary.
- **The "review debt" death spiral:** miss a day, the next day doubles, you fall further behind, then face thousands of overdue cards. One forum user did 1,671 reviews in a day. Example: "missing a single day would quickly escalate into an overwhelming backlog that made me feel like I was suffocating." These come from a commercial blog post that aggregates Reddit (https://www.neonlingo.com/blog/anki-burnout) and a search summary, so treat them as anecdotal.
- RemNote users have asked for a way to "miss a day… or three." https://forum.remnote.io/t/ability-to-miss-a-day-or-three/5815

# 3. Why Quizlet shut down Q-Chat
- **What happened:** Q-Chat was an AI tutor built on the ChatGPT API, launched in 2023. It became unavailable after **June 30, 2025**. https://artificial-intelligence-wiki.com/industry-ai/ai-in-education/quizlet-q-chat-guide/ and https://quizgecko.com/blog/best-q-chat-alternative
- **Quizlet gave no detailed reason.** Both sources say the public notice has no technical or business explanation. "Operational costs, usage patterns, and strategic priorities" is outside speculation.
  - One search snippet credited Quizlet with "After careful evaluation and customer feedback, we've decided to retire the Q-Chat study mode." An exact-phrase search instead matched a Zendesk notice. **Treat that quote as unverified.** quizlet.com and its help center returned 403, so I couldn't confirm it.
- **Known weaknesses listed by third parties:** hallucinations, trouble with complex multi-step problems, and being limited to the contents of Quizlet study sets.

# Gaps
- **No evidence collected** for Brainscape AI, Knowt, Wisdolia, StudyFetch, Gizmo, Glutanimate's add-ons, AnkiGPT, Mochi, or Duolingo/Quizlet retention numbers.
- **Several pages were blocked (403):** supermemo.guru, quizlet.com and its help center.

**The lessons that matter most for the design:**
1. Expect about a third of LLM cards to be unusable even with the best model, and filter for durable quality, not just accuracy.
2. Add an evidence-grounded verification step, because subtle errors are the dangerous ones.
3. Keep cards small, editable, and few, so the learner keeps some of the benefit of writing their own.
4. Copy SuperMemo: auto-postpone by priority instead of letting a backlog build up.
5. Expose the retention-vs-workload tradeoff to the learner.
6. Use rewordings of each question to defeat shallow pattern matching.

---

# Part: Paper tools, study modes and AI curricula

I covered topics 1 and 3 well, but topic 2 is thin. The shared web-search budget (200 searches per turn across all agents) ran out partway through. After that I could only fetch primary URLs I already knew. I found nothing on Khanmigo efficacy, Brilliant's AI, Fermat/Rocket, Speechify, Sizzle, Coursera Coach outcomes, Elicit/Consensus internals, or the Reddit/HN user discussions. You can send a follow-up to continue those searches, or raise `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`.

---

## Topic 1: Paper-reading tools, LLM study modes, and evidence on learning

### Paper-reading tools

**SciSpace Copilot**
- You highlight confusing text, math or tables and get "a simple explanation"; you can clip unfamiliar equations to ask what they mean. https://www.futuretools.io/tools/scispace-by-typeset , https://chrome.google.com/webstore/detail/scispace-do-hours-of-rese/cipccbpjpemcnijhjcdjmkjhmhniiick
- Answers cite the paper, and it finds related papers from a corpus of about 280M. (same sources)
- Prerequisites are handled one passage at a time, only when the user asks. It has no model of what the user knows.

**Explainpaper**
- "Highlight confusing text and get instant, simple explanations." https://www.explainpaper.com/
- Claims "Adjustable complexity - From beginner to expert level," answers "grounded in the document itself," and auto-generated insights that "map conceptual relationships." (same)
- It is the same per-passage pull model as SciSpace, with no persistent user model.

**alphaXiv**
- Began as a site for comments on arXiv papers. It then added AI paper blogs, chat on papers, and communities, "now used by millions." https://x.com/StanfordAILab/status/1952898111732629998
- In chat you can highlight a section and "@" other papers to pull them in as context. An "Explore" mode answers general research questions and has hot and recommended topics. Blog generation is one click; it also makes a podcast. https://rehoyt.medium.com/taming-the-research-fire-hose-how-alphaxiv-is-changing-the-way-we-read-arxiv-papers-6baeae3fd1cb
- One user's account: "I can understand a paper in 5-10 minutes instead of 30-45 minutes," and "most of the time, you don't need to read every detail of a paper." https://markptorres.com/ai_workflows/2025-10-16-using-alphaxiv-to-read-papers
- This is the speed-over-mastery framing our tool is reacting against.

**Emergent Mind**
- It "tracks new preprints, highlights trending papers, extracts open problems, and answers questions grounded in the literature." https://www.emergentmind.com/about
- "Open Problems" (2025): "36K unsolved research questions drawn from arXiv papers, each with its background and the papers that raise it." It also has an API (2025-09-04) and agent skills (2026). https://www.emergentmind.com/
- The background it gives is per problem, not per user.

**NotebookLM (Sept 2025 student update)**
- Generates flashcards and quizzes from your sources, and "you can customize the topic, set the difficulty and share your study sets." Each has an "explain" feature with citations. https://blog.google/innovation-and-ai/models-and-research/google-labs/notebooklm-student-features/ , https://9to5google.com/2025/09/08/notebooklm-flashcards-quizzes/
- Learning Guide is a chat style that "helps you break down problems step-by-step and adapts explanations to your needs" using "probing, open-ended questions." (same sources)
- I found no mention of mastery tracking or spaced repetition. Decks are one-off artifacts. (Google blog, above)
- Audio Overviews are two AI hosts in podcast form. https://en.wikipedia.org/wiki/NotebookLM

### LLM study modes

**ChatGPT Study Mode (July 29, 2025)**
- Uses Socratic questions, step-by-step hints, "scaffolded explanations, and frequent checks for understanding." https://futurefive.com.au/story/chatgpt-launches-study-mode-to-boost-learning-through-guidance , https://datanorth.ai/news/openai-launches-study-mode
- Personalizes "based on prior chat memory and user self-assessment," with quizzes and open-ended feedback. https://ukranews.com/en/news/1096804-chatgpt-introduces-study-mode-ai-will-give-step-by-step-hints-instead-of-ready-made-answers
- OpenAI's own page blocked my fetch (403): https://openai.com/index/chatgpt-study-mode/
- Its only prerequisite signal is memory plus the user's self-report. There is no structured knowledge model.

**Gemini Guided Learning (Aug 6, 2025)**
- Built on LearnLM. It "breaks down problems step-by-step and adapts explanations to your needs," using "images, diagrams, videos and interactive quizzes." https://blog.google/outreach-initiatives/education/guided-learning/ , https://techcrunch.com/2025/08/06/google-takes-on-chatgpts-study-mode-with-new-guided-learning-tool-in-gemini/
- The blog does not say it assesses prior knowledge.

**Claude learning modes**
- Claude for Education got Learning mode in April 2025; all users got it on Aug 14, 2025. https://alternativeto.net/news/2025/8/claude-s-learning-mode-is-now-available-to-all-users-with-new-coding-styles
- The Learning style is Socratic. Claude Code gained "Explanatory" and "Learning" output styles; Learning inserts `#TODO`s for the user to fill in. https://www.tomsguide.com/ai/claudes-new-learning-modes-take-on-chatgpts-study-mode-heres-what-they-do , https://engadget.com/ai/claudes-new-learning-mode-will-prompt-students-to-answer-questions-on-their-own-172057828.html

**Common pattern:** all three study modes are prompt-level behavior changes. None of them keeps a persistent per-user model of concepts or prerequisites, or schedules review.

### Evidence: does AI help learning or just summarizing?

**Bastani et al., PNAS 2025** ("Generative AI without guardrails can harm learning")
- Nearly 1,000 Turkish high-school math students. https://papers.ssrn.com/abstract=4895486 , https://ideas.repec.org/a/nas/journl/v122y2025pe2422633122.html
- During practice, GPT Base gave +48% and GPT Tutor +127%. https://knowledge.wharton.upenn.edu/article/without-guardrails-generative-ai-can-harm-education
- On the exam without AI, GPT Base was 17% worse than control; GPT Tutor was roughly equal to control. (same)
- GPT Tutor's safeguards included teacher-written hints rather than direct answers. Students "overestimated" their learning. (Wharton, above)
- Bastani: "If we use it sort of lazily and completely trust the machine learning model, then that's when we could be in trouble." (Wharton)
- Takeaway: guardrails removed the harm but produced no gain over control.

**Kestin & Miller, Scientific Reports 2025** (Harvard PS2 AI tutor RCT)
- 194 students in a crossover design: AI tutor at home vs. an in-class active-learning lesson. https://pmc.ncbi.nlm.nih.gov/articles/PMC12179260/
- Median post-test 4.5 vs 3.5, from a 2.75 baseline. Effect size was 0.63 SD by linear regression and 0.73–1.3 SD by quantile regression. Median time 49 min vs 60. (same)
- Design points relevant to us:
  - It used GPT-4, with prompts "enriched … with comprehensive, step-by-step answers" written by experts to avoid hallucination.
  - It guided students "sequentially through each part of each problem."
  - It gave one step at a time.
  - (same source)
- Authors' caveat: it may not hold for "complex synthesis of multiple concepts and higher-order critical thinking." (same)
- Critics add: one topic, two weeks, Harvard students, no retention or transfer measure, and the tutor was built by the same people who designed the class it beat. https://etcjournal.com/2025/11/10/review-of-kestin-et-al-s-june-2025-harvard-study-on-ai-tutoring/

**Kosmyna et al., MIT Media Lab 2025** ("Your Brain on ChatGPT", arXiv 2506.08872, not peer reviewed)
- 54 participants in LLM, search-engine and brain-only groups. Only 18 did session 4, where the groups swapped. https://arxiv.org/abs/2506.08872
- "LLM users displayed the weakest connectivity." LLM users "struggled to accurately quote their own work," reported the lowest ownership, and showed "reduced alpha and beta connectivity" after switching to no tools ("cognitive debt"). (same; https://www.hpcwire.com/2025/07/19/ai-is-making-us-dumber-mit-researchers-find/)

**Melumad & Yun, PNAS Nexus 2025** (LLM summaries vs. web search)
- Seven experiments, n = 10,462. https://scale.stanford.edu/ai/repository/experimental-evidence-effects-large-language-models-versus-web-search-depth-learning
- LLM-summary learners developed "shallower knowledge," even when real-time web links were added. They spent less time and wrote advice that was sparser and less original.
- Mechanism: summaries "lessen the need to discover and synthesize information from original sources—steps essential for deep learning." https://www.psypost.org/learning-from-ai-summaries-leads-to-shallower-knowledge-than-web-search/
- Caveat: hypothetical, low-stakes tasks. (PsyPost)

**Kreijkes et al. (Microsoft Research) 2025**
- Pre-registered RCT with 405 students aged 14–15, tested 3 days later. https://www.microsoft.com/en-us/research/publication/effects-of-llm-use-and-note-taking-on-reading-comprehension-and-memory-a-randomised-experiment-in-secondary-schools/
- Note-taking alone, or note-taking plus LLM, beat LLM alone on retention and comprehension.
- Most students preferred the LLM and thought it more helpful. This is the clearest "illusion of understanding" data point.

**Clin Deffarges, Kosmyna & Maes, arXiv 2609.00584 (Sept 2026)**
- 50 participants: an unrestricted chatbot beat Socratic and EEG-adaptive tutors on an immediate post-test (p < .03, d > 0.80). https://www.alphaxiv.org/abs/2609.00584
- Socratic-mode users "initially attempted to reason through the hints before progressively disengaging." The authors say the chatbot's advantage "is not an evidence of deeper learning, but rather a result of the immediate post-test evaluation." (same)
- Design lesson: pure Socratic friction causes dropout, and immediate tests overstate gains. Measure delayed retention.

**AI summaries / podcasts study (UC eScholarship)**
- Undergraduate business course comparing AI text summaries, AI audio summaries and human summaries. It found "no significant differences in immediate comprehension." https://escholarship.org/uc/item/31p5p8t4
- I could not retrieve the full results, so the delayed-retention findings are unknown.

**Audio Overview retention claim (unverified)**
- An SEO site claims a Feb 2026 Stanford GSE working paper found +11% short-term recall that faded after two weeks.
- I could not verify it and it has no primary source. Treat it as unverified.

---

## Topic 2: LLM-generated adaptive curricula (partial)

**Google "Learn Your Way" (Google Research, Sept 2025)**
- Personalization signals are only the student's self-reported grade level and interests. Text is "re-leveled to the learner's reported grade level, while maintaining the scope of its content," and examples are swapped for interest-aligned ones. https://research.google/blog/learn-your-way-reimagining-textbooks-with-generative-ai/
- It produces five formats: immersive text with embedded questions, section quizzes, narrated slides, audio teacher-student dialogues, and mind maps. Built on LearnLM / Gemini 2.5 Pro. (same; https://blog.google/outreach-initiatives/education/learn-your-way/)
- Efficacy study:
  - 60 Chicago students aged 15–18, up to 40 minutes, versus a PDF reader.
  - Scores were 9% higher immediately, and 78% vs 67% on retention after 3–5 days.
  - 93% vs 67% would use it again.
  - (Google Research blog)
- Quality check: three pedagogy experts gave "an average expert rating of 0.85 or higher across all pedagogical criteria." (same)
- Limits: it starts from a fixed textbook source, so hallucination risk is bounded. There is no tracking of knowledge over time.

**Oboe (oboe.fyi, now redirects to oboe.com)**
- Current tagline: "Chat that actually teaches you. Structured, cited, personalized, and interactive." https://oboe.com/
- The site also says: "We're building something new, so Oboe chats will be going away soon. Once they're gone, your past chats and artifacts won't be accessible." So it is mid-pivot. (same)
- Its marketing page makes no claim about tracking prerequisites or knowledge.

**Synthesis Tutor**
- For ages 5–11, 35,000+ families. "Micro-assessments" in every lesson; students advance only after showing mastery. https://www.synthesis.com/tutor
- They say explicitly they do not hand teaching to an LLM: "We do not simply outsource your child's education teaching to an LLM… it is not Chat-GPT." Experts vet the content. (same)
- This is a hand-built curriculum with mastery gating, not generated per topic.

**Alpha School / 2 Hour Learning**
- "adaptive AI for personalized 1:1 learning, mastery-based methods." Claims "2.6x Growth" on MAP tests and "99th Percentile." https://alpha.school/the-program/
- Self-reported marketing. The page gives no method for detecting gaps.

**Khanmigo**
- "guides learners to find the answer themselves" over Khan Academy's existing content library. Common Sense Media gave it 4 stars. https://www.khanmigo.ai/
- Its per-user knowledge model comes from Khan's existing mastery system, not from the LLM. I couldn't search for efficacy studies or the reports of math errors.

**AI course generators (Coursebox, Mindsmith)**
- Coursebox takes a prompt, PDF, Word or PPT and produces "the full course draft, structure and content, in minutes," plus an AI tutor "trained on your course content, so its answers stay accurate." https://www.coursebox.ai/
- Its accuracy control is human editing: "everything the AI generates is fully editable." It auto-marks assessments. (same)
- Mindsmith is enterprise eLearning authoring (Generate → Author → Share → Analyze) with 30+ interactive elements, SCORM/xAPI support and 16,000+ designers. https://www.mindsmith.ai/
- Both are authoring tools for instructors, not tools that keep per-learner prerequisite models.

**Coursera Coach**
- The only thing I could confirm is "interactive, personalized instruction" for educators (Sept 2024). https://blog.coursera.org/tag/coursera-coach/
- No outcome data found.

**Pattern across topic 2:** no product I could verify builds a per-user prerequisite graph that persists over time. Personalization is self-reported (grade, interests, chat memory) or uses a pre-built curriculum's mastery tracking (Khan, Synthesis, Alpha). Hallucination control is either grounding in a fixed source (Learn Your Way, Kestin's expert solutions) or human review (Coursebox, Synthesis).

---

## Topic 3: Prerequisite and definition tools for papers

**ScholarPhi (Head, Lo, Kang, Fok, Skjonsberg, Weld, Hearst; CHI 2021)** — the most relevant prior work. https://arxiv.org/abs/2009.14237

What it is:
- It targets "nonce words": terms and symbols coined within one paper.
- Four features:
  - position-sensitive definition tooltips
  - a "declutter" filter showing every use of a term
  - automatic equation diagrams
  - an auto-generated glossary
- It analyzes TeX source rather than the PDF.
- Symbol detection had 96% precision and 88% recall. Its definition detection is the state of the art at 73% precision and 74% recall, and the authors say recall is the main problem.

Formative study (9 readers):
- Readers either inferred meaning, deferred the lookup hoping the paper would explain later, or searched elsewhere.
- One reader (R1) described the failure mode: a reader "may reach a point in the text where they lack an understanding of so many important terms that they can no longer understand the text without stopping and searching."
- Looking things up was an unwanted "context switch" out of the "headspace" (R4). One reader hand-built glossaries of symbols in the margins.

Usability study (27 researchers):
- With ScholarPhi, readers answered questions significantly faster and viewed significantly less of the paper. One comparison showed 45.4 fewer seconds per task than the basic reader.
- Limitation: a single paper.

Key gap for our design:
- "readers in the formative study, pilot studies, and usability study all asked for the ability to look for definitions of terms that resided outside of a paper." That is, they wanted external prerequisites, which ScholarPhi left to future work.
- It has no user model at all.
- Source for all of the above: arXiv PDF 2009.14237, sections 3, 5 and 6.

**Paper Plain (August, Wang, Bragg et al.; arXiv 2203.00130, TOCHI)**
- Aimed at non-expert readers of medical papers. Four features: definitions of unfamiliar terms, plain-language section summaries ("gists"), a Key Question Index, and answer gists. https://arxiv.org/abs/2203.00130
- Readers had "an easier time reading and understanding research papers without a loss in paper comprehension."
- 18 of 20 readers who had the Key Question Index picked it as the most helpful feature. https://deepai.org/publication/paper-plain-making-medical-research-papers-approachable-to-healthcare-consumers-with-natural-language-processing
- Lesson: guided questions beat definitions.

**CiteSee (Chang et al., CHI 2023 Best Paper)**
- The closest thing to a per-user knowledge model in the Semantic Reader work. It uses the user's publishing, reading and saving history to mark citations as known (already cited or opened) or as relevant but unknown. https://arxiv.org/abs/2302.07302
- Beat three baselines on paper discovery in a lab study; in a field study it improved "situational awareness." https://news.cs.washington.edu/?p=36290
- Analogy: inferring what a user knows from their own papers and reading history could seed our prerequisite gap model.

**Threddy (Kang et al.)**
- Personalized threads: users pull research threads out of related-work sections as they read, and it recommends papers based on those threads. https://www.deepai.org/publication/threddy-an-interactive-system-for-personalized-thread-based-exploration-and-organization-of-scientific-literature

**Semantic Reader Project (Lo et al., CACM 67(10), 2024)**
- An umbrella over ScholarPhi, Paper Plain, CiteSee, Scim, Threddy, Relatedly, CiteRead, Papeos and Synergi. https://arxiv.org/abs/2303.14334
- Only CiteSee and Scim are marked "In-Production." https://openreader.semanticscholar.org/
- Open tooling: PaperMage (PDF parsing) and PaperCraft (React reading UI components). (same)
- So in-situ definitions were researched but, as far as the platform page shows, not shipped.

**Commercial "explain" tools** (Explainpaper, SciSpace, alphaXiv)
- Explanations are pulled on demand, one passage at a time, with no persistent per-user model and no ranking of which prerequisites matter.

**Did not find:** any shipping product that builds a prerequisite graph for a paper and diagnoses gaps against a user model. I couldn't search for niche "paper prerequisites" tools, so this is incomplete. Of the verified sources, ScholarPhi and CiteSee come closest.

---

## Design implications from the evidence

- **Grounding:** ground generated teaching in verified source material (Kestin's expert solutions, Learn Your Way's textbook source) rather than open generation.
- **Measurement:** measure delayed retention. Immediate tests favor answer-giving (Clin Deffarges et al.), and users prefer the LLM even when it teaches worse (Kreijkes et al.; Bastani's overestimation).
- **Friction:** some is good (note-taking, effortful synthesis per Melumad & Yun), but pure Socratic withholding causes disengagement. Step-at-a-time scaffolding (Kestin) is the best-supported middle ground.
- **Where the gap is:** in-situ definitions inside the paper are researched (ScholarPhi). What users asked for and didn't get is external prerequisite knowledge plus a persistent per-user model. Our tool would sit in that gap.

---

# Part: Language learning apps

I've written the notes below. Duolingo, the vocabulary-coverage research and AnkiMorphs/WaniKani/Clozemaster are well covered from primary sources. Topic 3 (LLM-native tools) is thin, because the shared web-search limit (200 per turn) ran out partway through. After that I could only fetch URLs I already knew. These went unresearched: Kanji Koohii, Refold's sentence-mining page (404), Speak's OpenAI case study (403), Migaku's official docs, LingQ's AI assistant "Lynx" (403), and any academic papers on LLM-generated graded readers. You can raise `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION` or send a follow-up to fill those gaps. I wrote no files; a temporary PDF extraction in /tmp was deleted.

# Notes: how language apps decide what to teach next, and what fails

## 1. Duolingo

### Half-life regression (Settles & Meeder, ACL 2016): *when* to review a word
- HLR estimates "the 'half-life' of a word or concept in a student's long-term memory." It used 13M Duolingo learning traces and cut prediction error by more than 45% compared with baselines. In a live study it raised daily engagement by 12%. Code: github.com/duolingo/halflife-regression. https://preview.aclanthology.org/landing_page/P16-1174
- The model is h = 2^(Θ·x), and predicted recall is p = 2^(−Δ/h). The features are how often a word was seen, the counts of correct and incorrect answers, and **the word itself (lexeme tags)**. Easy words tend to be cognates or regular forms. Hard words are "rare words, 'irregular' forms, or use complex grammar like past/present participles." The predictions feed the strength meters and "pick your weakest words for practice." A/B results: "9.5% increase in retention for practice sessions, 1.7% for lessons, 12% for overall activity." https://blog.duolingo.com/how-we-learn-how-you-learn
- Error was "nearly half" that of the earlier Leitner system (same source).

### Birdbrain: *what* to show next
- "If HLR answers when to show you a word, Birdbrain answers what to show you next." (Search-result summary attributed to Duolingo's Birdbrain post: https://blog.duolingo.com/learning-how-to-help-you-learn-introducing-birdbrain)
- V1 is logistic regression in the style of item response theory (IRT), with a learner ability score and an exercise difficulty score. A wrong answer lowers the ability estimate and raises the difficulty estimate. Surprising outcomes move the estimates more, similar to Elo. Scale: about 1B exercises a day. https://spectrum.ieee.org/duolingo
- The "Session Generator" builds lessons "from a wide pool of prospective exercises." Birdbrain adds a predicted-success filter so lessons fit each learner. A/B tests showed learners "learn more" and were "more likely to return again day after day." https://blog.duolingo.com/learning-how-to-help-you-learn-introducing-birdbrain
- V2 (May 2022) is an LSTM that compresses a learner's whole history into a **40-dimensional vector**. That lets it represent, say, weak future tense alongside strong past tense. It raised both engagement and learning metrics further. The goal is to keep learners "squarely in the zone where they remain engaged but are still learning at the edge of their abilities." https://spectrum.ieee.org/duolingo
- On being open about difficulty: when lessons were labelled as harder, "learners spent more time studying… more likely to return." A learner quote: "If I make a mistake, I don't feel as bad, because you warned me that it was hard." https://blog.duolingo.com/duolingo-difficult-exercises

### LLM content pipeline and Duolingo Max
- Duolingo writes exercises with "Mad Lib" prompts. Fixed rules (number of answer options, length limits) are combined with variable slots (CEFR level, theme, grammar focus such as "THE PRETERITE TENSE"). The model generates about 10 candidates, and learning designers choose and edit them for "naturalness, learning value, and appropriate vocabulary." "Our Spanish teaching experts always have the final say." https://blog.duolingo.com/large-language-model-duolingo-lessons/
- Max (GPT-4) adds three features. **Explain My Answer** is a chat explaining why an answer was right or wrong. **Roleplay** is scenario chat (for example, ordering coffee). **Video Call** is a conversation with the character Lily. https://blog.duolingo.com/duolingo-max ; https://www.techradar.com/news/duolingos-new-gpt-4-ai-will-happily-explain-why-your-spanish-is-wrong
- How Video Call is built (https://blog.duolingo.com/ai-and-video-call):
  - A System prompt sets the learner's CEFR level, and greetings and first questions are vetted for that level.
  - **Learner memory:** after each call an LLM pulls facts about the learner into a "List of Facts" that goes into future prompts ("two dogs… studying architecture… favorite food is tacos").
  - Problem: too many instructions produced "sentences that are overly complex or missing the vocabulary." The fix was a separate "Conversation Prep" step that generates the first question.
  - Problem: "learners didn't want to talk about the subject that Lily was instructed to focus on." The fix was checks during the call so the learner can change topic.
- Duolingo's own Video Call studies report speaking-test gains and higher confidence compared with lesson-only users. The post gives no sample sizes or significance tests. https://blog.duolingo.com/video-call-research-report

### The 2025 "AI-first" shift
- On April 28, 2025, CEO Luis von Ahn's memo said Duolingo would stop using contractors for work "that AI can handle." Users publicly abandoned streaks ("That owl is dead to me"). TikTok reportedly lost more than 400K followers. Von Ahn said he "did not expect the amount of blowback." https://www.latintimes.com/duolingo-flooded-pledges-quit-app-following-decision-replace-contractors-ai-that-owl-dead-582106 ; https://knowyourmeme.com/memes/events/duolingos-ai-first-controversy
- On April 30, 2025, Duolingo launched 148 courses in under a year using GenAI plus a "shared content" approach: build "a high-quality base course and quickly customize it for dozens of different languages." This brought the 7 most popular languages to all 28 interface languages. "Developing our first 100 courses took about 12 years." https://investors.duolingo.com/news-releases/news-release-details/duolingo-launches-148-new-language-courses
- Quality complaints:
  - A long-time user found the AI stories incoherent ("I'm not sure I understand what they're talking about?"). He called the new voices "inconsistent and downright wrong," the stories "usually pointless now," and saw "no quality control of the AI-generated questions at all." https://lars.ingebrigtsen.no/2025/08/02/friends-dont-make-friends-read-ai-generated-texts-a-duolingo-odyssey/
  - Users said "now complete rubbish — I have let go of my nearly 900 day streak." https://www.the74million.org/article/as-duolingo-turns-to-ai-some-users-say-language-app-has-joined-the-dark-side/
  - A Neowin headline says an AI-built course left out key words; a search summary said the missing words were French "and"/"or". I could not fetch the article (403), so treat the detail as unverified. https://www.neowin.net/news/duolingos-ai-content-push-backfires-an-entire-course-loses-key-words/
- Gamification complaints, via a search summary of Reddit posts (not checked against the originals): "1526 day streak in 4 languages but not… fluent," and pre-2021 Duolingo "could actually teach you, but now you're just playing a game."

### Evidence on learning outcomes
- In a study published in Foreign Language Annals (2022, company-affiliated), Duolingo-only learners who finished 5 units of Spanish or French scored like students after 4 university semesters in reading and listening. That level is ACTFL Intermediate Low for reading and Novice High for listening. Speaking was not tested. https://investors.duolingo.com/news-releases/news-release-details/leading-language-research-journal-publishes-study-showing ; https://experts.nau.edu/en/publications/evaluating-the-reading-and-listening-outcomes-of-beginning-level-/

## 2. Content-driven and interest-driven tools

### The research behind "what to teach next"
- **Krashen's i+1.** "A necessary (but not sufficient) condition to move from stage i to stage i + 1 is that the acquirer understand input that contains i + 1." Krashen explicitly argues against aiming at i+1 deliberately: "the best input should not even attempt to deliberately aim at i + 1… if communication is successful, i + 1 is provided," and "deliberate aim at i + 1 might miss!" Roughly tuned input covers several learners' i+1 at once. (Krashen, *Principles and Practice*, pp. ~21-22) https://www.sdkrashen.com/content/books/principles_and_practice.pdf
- **Coverage thresholds.**
  - Hu & Nation (2000) put adequate reading comprehension at 98% known words. The result rests on a regression with only 66 New Zealand university students. https://aila2021.dryfta.com/program/abstract-archive/abstract/public/416/unknown-vocabulary-density-reading-comprehension-and-the-98-coverage-figure-replicating-hu-nation-2000
  - Nation (2006): reading authentic text takes 8,000–9,000 word families, not about 3,000 (same source).
  - Schmitt, Jiang & Grabe (2011), with 661 participants, found a "relatively linear relationship" between coverage and comprehension, with "no indication of a vocabulary 'threshold'." They suggest 98% is the more reasonable target for academic texts. **So coverage is a dial, not a cliff.** https://experts.nau.edu/en/publications/the-percentage-of-words-known-in-a-text-and-reading-comprehension/
  - Webb & Rodgers (2009): 3,000 word families plus proper nouns gives about 95% coverage of TV. Children's shows need about 2,000. Reaching 98% takes about 4,000 families for unscripted shows and 6,000 for scripted ones. This is directly relevant to a "learn from a TV show" feature. https://revistas.um.es/ijes/article/view/137131

### Tool by tool
- **LingQ.**
  - Words you haven't marked appear blue. Words you save to study ("LingQs") are yellow and go through statuses 1–4, with 4 = "Learned." "Both Learned Words and Known Words count towards your Known Word total."
  - **By default, turning the page marks every remaining blue word as Known.** This is the main way the count gets inflated. https://lingq-support.groovehq.com/help/how-do-i-increase-my-known-words
  - Refold's review says the count "isn't perfect, and can inflate or deflate your true known word count depending on the language." LingQ is weaker for Chinese, Japanese and Korean, where word segmentation is hard. Crowdsourced definitions "may be totally wrong" for less common languages. Pluses: "gamified well," and a full immersion suite. https://refold.la/blog/lingq-review
- **Migaku.** Words are red (unknown), yellow (learning) or green (known), plus "Track" and "Ignore." In Migaku's flashcards a word moves to Known automatically after it passes several times over a period. It can schedule i+1 cards first and bulk-export the "1T" sentences from a whole episode (1T = exactly one unknown word). Sources are community pages, not official docs: https://migaku.com/community/m/1261791545024188436 ; https://magenta-dirigible-0d8.notion.site/Migaku-Basics-8db656fa80f44a5993000eeb77176357
- **AnkiMorphs** (successor to MorphMan).
  - It splits cards into morphs (roughly, words) and treats morphs from already-learned cards as known. "Low scores are good."
  - Score = min(10⁶ × number of unknown morphs + min(weighted priority + length deviation, 10⁶ − 1), max). Frequency priority and sentence length only break ties, so "all 1T cards should appear before any MT cards." MT means more than one unknown.
  - The length penalty is piecewise, for sentences too long or too short.
  - https://mortii.github.io/anki-morphs/user_guide/usage/recalc.html ; https://mortii.github.io/anki-morphs/
- **Clozemaster.** Sentences come from Tatoeba under CC-BY. The blank is "the least common word in the sentence within the 10,000… most common words." Frequency lists come mostly from Wiktionary; Japanese uses JLPT lists. Mastery is 25%, 50%, 75% and 100% at 1, 10, 30 and 180-day intervals, and a wrong answer "goes back to 0% mastered." https://www.clozemaster.com/faq
- **WaniKani.** Radicals unlock kanji, and kanji unlock vocabulary, once the prerequisite reaches "Guru" (stage 5 of 9). Intervals run 4h, 8h, 1d, 2d, 1w, 2w, 1mo, 4mo, then "Burned." A wrong answer drops an item 2 stages at Guru and above, 1 stage below that. This is an explicit prerequisite graph with a mastery gate. https://knowledge.wanikani.com/wanikani/srs-stages/
- **Lingvist.** Prioritizes the most frequent words (marketing claims they cover "80% of everyday scenarios") and repeats the words you get wrong. "Course Wizard" builds a course from a user's topic (music, career and so on) by stitching together example sentences, and detects which words the learner already knows. https://www.languagemagazine.com/2019/09/13/customizable-ai-based-language-learning-platform/ ; https://thepienews.com/news/lingvist-launches-ai-language-learning-platform/
- **Language Reactor.** Dual subtitles and a pop-up dictionary on Netflix and YouTube. Saved words are highlighted wherever they reappear. You can set a vocabulary level so that probably-unknown words are highlighted, and import a known-words list to hide highlighting. https://jalt-publications.org/articles/28605-enhancing-functionality-youtube-and-netflix-language-reactor
- **Readlang.** Click to translate on any webpage or upload; every lookup becomes an SRS flashcard. Adds AI "context explanations." https://readlang.com/
- **Glossika.** Sentence-level SRS: it "prepares a personalized list of sentences… you're particularly at risk of forgetting." It does not explain how it picks content by interest. https://ai.glossika.com/
- **Refold.** Seven phases, from Foundations through Comprehension, Listening, Speaking and Accuracy to Fluency. Its sentence-mining page returned 404. https://refold.la/roadmap/
- **Sentence-mining burnout** (user discussion). Making detailed cards is laborious. One user dropped Anki for tracking word status during immersion "eliminating burnout." Others say cards mined from engaging media stick ("These are the words that I remember most!"). https://community.bunpro.jp/t/whats-your-experience-with-sentence-mining/49802

## 3. LLM-native tools (2024–2026)

- **Speak (OpenAI-backed).**
  - Uses a Learn → Practice → Apply sequence, built on phrase patterns. Curriculum comes from usage research and stuck-point analysis, written by human designers with "Speak's internal curriculum design AI." A course of 4 units is 50+ lessons. https://www.speak.com/blog/how-speak-reinvents-language-learning
  - The winter 2025 release added adaptive paths and a "Speak Level" measure of "what you've mastered, what's next." https://www.speak.com/blog/winter-2025
  - Live Tutor Lessons on GPT-Live-1 (Sep 2026): the authored script plus a conversational model. It delivered 476 of 477 authored lesson lines. About 85% of its corrections were warranted, and it caught about 80% of targeted errors. Framing the model as a tutor cut interruptions during thinking pauses from 27.6% to 13.6%. https://www.speak.com/blog/live-tutor-lessons-powered-by-openais-gpt-live-1
  - Live Roleplays use the OpenAI Realtime API (Oct 2024). https://www.speak.com/blog/live-roleplays
- **Langua.** AI voice characters with regional dialects and instant corrections. Saved words are "woven into flashcards, stories and conversations." Human tutors are available too. https://languatalk.com/
- **Duolingo Video Call memory and Lingvist Course Wizard** (above) are the clearest documented cases of personalizing to interests or the learner's life.
- **Gap:** I found no independent outcome studies of LLM-generated, interest-based content. All the evidence above is published by the vendors themselves.

## Design implications for a general system

1. **Keep "when to review" separate from "what to present next."** Duolingo uses HLR for the first and Birdbrain for the second. Model both per concept, not just per item. Include item features such as word identity, irregularity and frequency, so difficulty carries over to new items.
2. **Aim for a predicted-success band rather than a single "i+1" point.** Krashen warns that aiming exactly at i+1 "might miss," and coverage research shows a linear trend. Use coverage as a dial: about 95–98% known words for comfortable input, lower for study mode. For TV, 3k–6k word families sets realistic expectations.
3. **Don't trust self-reports or implicit "known" signals.** LingQ marking every word Known on page turn is the cautionary example. Treat known-ness as a probability that rises with evidence: graded recall, as in Migaku and WaniKani, and decay, as in HLR. Show uncertainty and let the learner correct it.
4. **Use prerequisite graphs with mastery gates where structure exists** (WaniKani: radical, then kanji, then vocabulary). The same idea works for ML papers: concept, then the prerequisites it depends on.
5. **Rank strictly on comprehensibility first, value second** (AnkiMorphs: unknowns dominate the score, then frequency and goal relevance, then length). For interest-driven learning, "value" should weight words that appear in the learner's target content, such as the show's script or the trip's phrases, not only general frequency.
6. **LLM-generated content needs controls and review.**
   - Constrain prompts by level, target items and theme.
   - Split generation into stages, since overloaded prompts produced text that was too complex or missed the target vocabulary.
   - Check generated text automatically: coverage against the learner model, and whether the target items are present (the reported missing "and"/"or" case).
   - Duolingo's backlash shows unreviewed AI output erodes trust quickly.
7. **Let the learner steer topics.** Duolingo had to add mid-conversation topic changes. Keep a fact memory of the learner's interests and life for continuity.
8. **Don't use streaks or XP as a proxy for learning.** Measure outcomes with periodic held-out comprehension or skill checks. Make difficulty visible; Duolingo found that labelling exercises as hard raised effort.
9. **Keep card-making and review load low** to avoid sentence-mining burnout. Mine automatically from content the learner is already consuming, cap daily new items, and favour immersion-time tracking over heavy card creation.

---

# Part: Math Academy, Matuschak and Nielsen

# Research notes: Math Academy, Matuschak/Nielsen, and practitioner views on LLM-generated flashcards

Main source abbreviation: **MAW** is Justin Skycak's *The Math Academy Way* (working draft PDF), https://www.justinmath.com/files/the-math-academy-way.pdf. I downloaded it and read the relevant chapters in full. Page numbers below are the book's own.

Gaps up front: the web-search budget ran out partway through. I found no primary source on why Orbit was paused or shelved, didn't reach HN/Reddit threads directly, and couldn't get the Quantum Country RCT page (it returned 404).

---

## 1. Math Academy

### Knowledge graph: how it's built and how big it is
- **It's built entirely by hand.** "All content is handcrafted in-house," including the topics, the links between them, the questions, solutions and metadata. Topic granularity is a matter of feel: "You just kind of get a 'feeling' for what the right chunk size is." https://justinmath.com/how-math-academy-creates-its-knowledge-graph/
- **Size:** about 2,500 topics, each with 3–4 *knowledge points*. Each knowledge point links to one or more prerequisites. (same URL)
- **Encompassing weights took about 250 hours of one person's time:** 1,500 topics × 5 prerequisites × 2 minutes each, at "8 hours per day for 30 days." Skycak: "just because something's tedious doesn't mean it's low ROI." (same URL)
- **Structure of a topic** (MAW p.74–75): each topic is a lesson split into knowledge points. Each knowledge point is a worked example followed by similar questions. The first knowledge point covers the most basic case, and later ones "gently introduce more advanced cases." A course is "simply a section of our knowledge graph", and "the knowledge graph is the ultimate source of truth."
- **Three kinds of edge:**
  - **Prerequisites:** a DAG that defines learning paths.
  - **Key prerequisites** (MAW p.75–76): each *knowledge point* (not each topic) links to "the prerequisite knowledge that is most directly being used." Their example is that "Evaluating an Exponential Expression" links to "Multiplying Negative Numbers", even though that topic is several steps back in the graph. This is what targeted remediation uses.
  - **Encompassings** (MAW p.77–78): "Encompassed topics are usually prerequisites, but prerequisites are often not fully encompassed." Weights are fractional, and you can "loosely interpret each weight as representing the probability that a random problem from the advanced topic encompasses a random problem from the simpler topic" (MAW p.366).
- **Sparse weight-setting** (MAW p.367–368): a full pairwise matrix would have tens of millions of entries, so they only set weights that are (1) nontrivial, (2) can't be inferred by transitive "repetition flow", and (3) between topics that are close in the graph. In practice this means weights only along direct and key-prerequisite edges, so the count scales linearly with the number of topics. Direct prerequisite edges can have weight **zero** when "a topic requires some amount of conceptual familiarity with the prerequisite, but does not require the student to actually have mastered" it. In FIRe, credit flows down "like lightning bolts" and penalties flow up "like growing trees" (p.365).
- **Core vs supplemental topics** (MAW p.391–392): an algorithm labels topics as "core" under two rules: if a topic is core, all its ancestors are core, and each course must have a balance of core and supplemental topics. Core topics are taught first so they collect more review. They found that "roughly a third of 4th grade through AP Calculus BC topics … were not actually prerequisites for university math", and cut those out to make the adult "Mathematical Foundations" sequence. This is the closest thing in the material to an explicit position of "don't teach what isn't on the path".

### Task types
- The task types are lesson, review, multistep and quiz, plus the diagnostic. https://mathacademy.com/how-it-works
- **Lessons:** "If the student gets two practice problems correct in a row, then they move on to the next example, otherwise, they're given additional problems." (same URL)
- **Quizzes:** one "every 150 XP" covering "a variety of recent topics". "Any topics missed during the quizzes are then immediately assigned as review topics", followed by an optional retake. (same URL) Quiz topics aren't announced in advance, so the result is an honest signal "without priming" (MAW p.463).
- **Reviews:** questions are drawn "from the same exact pool of questions" as the lesson, but never a question the student has already seen (MAW p.464). "Why are there multiple questions in reviews?" has its own FAQ entry (p.413).

### Diagnostic / placement (MAW ch.30, p.375–381)
- **Question count:** a naive diagnostic would need 500+ questions. Theirs uses "20-40 questions for lower-grade courses … and 40-60 for higher-grade."
- **How inference works:** credit propagates positively to prerequisites and negatively to post-requisites. Positive credit also spreads between sibling "leaf topics" in a module. The graph is compressed beforehand: a topic counts as "covered" if it has an ancestor and a descendant in the diagnostic graph, each within 3 edges.
- **Plus-minus balance per topic:** the sign is the prediction (knows / doesn't know) and the magnitude is the confidence. A correct but slow answer gets reduced weight (an "accuracy-time conflict"). Topics with a positive balance are credited with that many repetitions.
- **Conditional completion:** topics that are "just barely" placed out are assumed known, but "if the student struggles, then the system will immediately begin 'falling backwards'."
- **Conservative vs aggressive edge of mastery:** placement measures the conservative edge, and lessons operate on the aggressive edge. That explains why students who finished a course sometimes place lower when they retake its diagnostic.
- **Choosing a diagnostic question:** pick "the simplest question that (1) would convince an expert tutor … and (2) exercises all of the topic's prerequisites." The most difficult question in a topic is avoided because of silly-mistake risk.
- **Placement errs low:** the system "intentionally places students at the bottom of their lowest knowledge holes" (p.448). Students can't edit their own knowledge profile because "Learners have a tendency to massively overestimate self-reported knowledge, and then fault the resulting instruction" (p.463).
- **Supplemental diagnostics** are small follow-up diagnostics, sent when the graph changes and a student's profile goes stale (p.380).

### XP and gaming the system (MAW ch.22, p.309–313)
- 1 XP is calibrated to "1 minute of fully-focused, fully-productive work for an average serious (but imperfect) student."
- **Graded awards:** bonus XP for perfect work, "a little XP for nearly passable performance, zero XP for poor performance, and a negative XP penalty for blowing off a task."
- **Why penalties exist:** without them, "adversarial students will complete tasks that they feel are easy and then submit random guesses to intentionally fail out of tasks that require more effort." They call these students "XP hackers." After penalties were added, "many adversarial students' rates of passing learning tasks jumped from under 50% to over 90%." Penalties are calibrated to "how frustrated a teacher, tutor, or guardian sitting next to the student would become."
- **No "I don't know" button** (p.464–465), for two reasons:
  - Kids abused it on purpose. When the system was deployed in schools, it "was getting attacked left and right by adversarial students."
  - Underconfident students give up even when their "guess" would have been right.
- **Remediation is slow on purpose:** knowledge isn't peeled back quickly after failures because that "would create an exploit" where students fail tasks deliberately to get easy work (p.417).

### Failure handling and explanations
- **Pass rates:** "95% of lessons are passed on the first try and 99% within two tries."
- **After a first failure:** the lesson is paused, and coming back later gives an "80% chance of passing the lesson the second time around without any additional intervention."
- **After a second failure** at the same knowledge point, reviews on that knowledge point's key prerequisites are assigned. (MAW p.416–417)
- **No re-explaining:** "If a student gets a question incorrect, shouldn't the system try to explain things differently?" Their answer is no. Needing many explanations means either the original explanation was bad, or the explanation that "clicked" skipped the prerequisite, which "means the curriculum is watered down." (p.418)

### Review load
- Reviews are front-loaded with new material at first, then ramp up. In the long run it's "a couple reviews per lesson on average."
- If a student slows their pace, a "review tsunami" builds up (their credit-card analogy). They "force a lesson every ~3 reviews on average, even when there's a big backlog." (p.405–406)
- Review volume varies with how many encompassings exist in that part of the graph (p.405).
- Reviews are meant to "feel as mentally taxing as initial lessons" ("Spaced repetition = 'wait'lifting") (p.407).
- The system is "not trying to keep a student's knowledge 100% fresh". A separate test-prep mode exists for exams. They admit "there is room for us to more precisely calibrate our spaced repetition system" (p.409).
- When a newer topic that isn't yet due encompasses an older due topic, they serve the newer topic and give it a discounted early repetition (p.410).

### Non-interference (MAW ch.17, p.247–249)
- Related topics are spaced out in time, and dissimilar topics are taught side by side. The motivating figure: "well over half, and potentially as high as 90%, of multiplication mistakes are caused by interference."
- The variety also fights boredom: it works "just like a personal trainer packs a wide variety of exercises."

### LLMs
- **Explicit rejection of conversational AI** (MAW p.465–466): "Many people who have (unsuccessfully) attempted to apply AI to education have focused too much on the 'explanation' part and not enough on scaffolding, navigating, and managing the entire learning process… You solve just enough of the problem to produce a cool demo." Their alternative: "We simply hardcode explanations into bite-size pieces… And we close the feedback loop by having students solve problems."
- They also say that when a student struggles, the system "should not lower the bar for success … (e.g., by giving away hints)."
- **Content is human-made:** "All of our content and exercises are created in-house… by a team of math experts" (p.462).

### Skycak's critiques of other approaches
- **Projects:** "Projects are valuable for pulling skills together, but students need to acquire the component skills first… Most students can't learn component skills on the fly in the context of a bigger project." https://justinmath.com/can-you-teach-a-math-class-on-the-basis-of-projects-only/
- **Flashcard-style SRS:**
  - Existing spacing models are "limited to the setting of independent flashcard-like tasks", whereas STEM subjects are "highly connected" (MAW p.~258).
  - "A common criticism of spaced repetition is that it requires an overwhelming number of reviews. While this can be true if spaced repetition is used to learn unrelated flashcards…" — encompassings are how they avoid that (MAW ch.18).
- **Agency:** "Why can't I choose my own tasks?" Because of efficiency. The future feature they're considering is "tell us what your specific goal is and we'll put you on the most efficient path to that goal" (p.462). That is essentially the paper-targeted design you're building.

### What users say goes wrong
- **Andy Matuschak's review** https://notes.andymatuschak.org/Math_Academy
  - The lesson queue is a "black box", creating "emotional disconnect and a feeling of passivity."
  - "Theorems are often presented as things-to-be-learned, rather than things-to-be-understood."
  - There are few transfer tasks. On proof templates: "at no point do I need to decide what proof strategy to use—which is the skill I really need!"
  - His forgetting outpaced the review schedule, so he added his own SRS on top.
  - He praised the interleaving of reading with tasks, worked examples, the XP pacing, and the hierarchical SRS.
- **Oz Nova** https://newsletter.ozwrites.com/p/a-balanced-review-of-math-academy
  - Good for procedural fluency, weak on understanding.
  - "One slip up here cursed me with a long sequence of middle school trigonometry."
  - Timed diagnostic questions penalize conceptual reasoning.
  - He recommends using it alongside textbooks.
- **atvbt** https://www.atvbt.com/math-academy-a-mixed-review/
  - When they wanted linear algebra, the trig and calculus prerequisites were "unskippable". The reviewer quit entirely rather than "learning slightly sub-optimally."
  - The reviewer argues MA could "grey out any areas … that require a given unit" but chooses not to.
- **Complaints MA itself acknowledges in its FAQ** (MAW p.396–467): too many reviews, reviews feeling hard, lower-grade lessons that feel irrelevant, too many diagnostic questions, "I know those topics, I swear!", silly mistakes and tedium, wanting to choose topics, losing a quiz when interrupted.

---

## 2. Matuschak, Nielsen, Quantum Country, Orbit

### Quantum Country results
- From *How can we develop transformative tools for thought?* https://numinous.productions/ttft/
  - After the first review, readers have "just over 2 days of demonstrated retention, per card."
  - After 6 repetitions, about 54 days per question across 112 questions. Reaching that takes "about 95 minutes of total review time."
  - "A less than 50% overhead in time commitment can provide many months or years of retention."
  - "Six months after release … 195 users had demonstrated one full month of retention on at least 80% of cards."
  - Self-critique: learning "is about much more than memory", and readers may "parrot the answer without engaging deeply."
- From Matuschak's notes https://notes.andymatuschak.org/zRxhtQqHvLpatPLB4BvzMRB
  - Late-2019 cohort: after five repetitions, most readers had "at least 1 month of demonstrated retention for at least 95% of questions."
  - Caveat: the data only covers readers who answered 80% or more of questions before their first review, so selection bias is acknowledged.
- **Long-term stats.** These come from search-result snippets of Matuschak's notes; the pages returned 404 when I tried to fetch them.
  - The median user is at 95% accuracy after demonstrating 5-day retention. https://notes.andymatuschak.org/z2Rv4RAjXUrwa3fMYn9Q1iR
  - "95% of Quantum Country questions produce no lapses for most readers' first half year." https://notes.andymatuschak.org/zUReaqSDR9zonWKta1UxmRU
  - For 53 readers who reviewed for a full year: median 463 reviews, and for most, under 2% of repetitions are lapses.
  - A related note title warns that high accuracy "may mask forgetting because of cuing."
- **Causal evidence:** RCTs exist. Linked findings include "a retry intervention produces substantial increases in early accuracy." https://notes.andymatuschak.org/zuCfBJSkm5BnqC1qw1bLH2

### Mnemonic medium: problems and lessons
- **Known weaknesses** https://notes.andymatuschak.org/Mnemonic_medium
  - The habit is onerous and the benefits aren't immediately visible.
  - It needs a critical mass of content.
  - The design is rigid.
  - "Transfer learning: Current design doesn't strongly support application beyond recall."
  - Open questions include personalization across reader backgrounds.
  - One strength: "Expert authorship removes the burden of prompt-writing."
- **Cost and premature scaling:** mnemonic essays cost "35-50% reading time overhead". He judged scaling premature because "we don't know what the medium wants to be." https://notes.andymatuschak.org/zjrts41M36NpjJkj14tTdToSr8gtsWnwQ5A6
- **Non-technical texts:** readers found it "like homework", e.g. "answering prompts is a very cold, grey thing to do" and "a reflection of my own intellectual inadequacy." Others said it "made me slow down." His conclusion: **the medium should give readers control over which prompts they collect.** https://notes.andymatuschak.org/zG29usta2L9LLjkVbnvCzcV
- **Current status:** his homepage lists Orbit as "A platform for memory system experiments" and lists essays titled "Revamping the mnemonic medium for reader control", "Architectures for a more flexible mnemonic medium", "Highlight-driven practice", and "Self-explanation support". He is now working on Pico, "a conservatory for human attention." https://andymatuschak.org/ I found no explicit post-mortem on Orbit.

### How to write good prompts
Source: https://andymatuschak.org/prompts/
- Good prompts are **focused, precise, consistent, tractable and effortful**.
  - Tractable: "you can almost always answer correctly."
  - Effortful: "You shouldn't be able to trivially infer the answer."
- **Lenses for conceptual knowledge:** attributes and tendencies, similarities and differences, parts and wholes, causes and effects, significance and implications.
- **For procedures:** focus on the key verbs and the conditions for moving between steps.
- He says prompt-writing is "surprisingly difficult."

### LLM-generated prompts (Matuschak's GPT-4 experiments, 2023)
- **Top-level finding:** "GPT-4 can often generate usable spaced repetition prompts for declarative knowledge from explanatory text with guidance." What helps:
  1. Treat **choosing reinforcement targets** and **writing prompts for them** as separate problems.
  2. Give the model prompt-writing principles.
  3. Give hints about the angle to reinforce.
  4. Give ample context.

  https://notes.andymatuschak.org/zJRDpsHzhrx87XxabV5jqXg , https://notes.andymatuschak.org/Using_machine_learning_to_generate_good_spaced_repetition_prompts_from_explanatory_text
- **Main failure mode:** "LLMs lack prompt-writing patterns for complex conceptual material." His example is "echelon form". The model gives term→definition and definition→term cards, when it should ask for classification of examples, generation of positive and negative examples, connections to other concepts, and purpose. "these questions reinforce information, not understanding." A simple hint isn't enough; he has to say "Generate an example linear system and ask whether it's in echelon form." He suggests a "pattern language of prompt-writing" as the fix. https://notes.andymatuschak.org/zmrbnm683nVZi9ut63vsr8BwYKEtATA6e4B3
- **Angle hints:** "There are often so many things one could reinforce… I get much better results if I give the model a word or two hinting at what aspect… I want to reinforce." Also: "How could it know that my issue was that the notation was surprising to me?" https://notes.andymatuschak.org/zomoPzCNzSi5GqtfTeVWgm7RjmiArjS8vvM5
- **Effect of principles:** giving principles helps, but "It's not clear how strong or reliable these effects are." He recommends building a dataset of expert-written prompts for evaluation. https://notes.andymatuschak.org/zPXE9jtKyU7AQRBmAUQrbWQ
- **Easier tasks that work:**
  - Shallow rephrasings of a question so it's worded differently each time, which also counters pattern-matching. GPT-4 did slightly better than 3.5 in a 2023-06-14 test. https://notes.andymatuschak.org/zBcEii9Hf2Rv7vsUSB7pBoP
  - Converting cloze cards to Q&A, judging whether two cards are functionally equivalent, and checking whether one prompt gives away another. https://notes.andymatuschak.org/z3r1Lqmf4W9KPU2scVDSdbafthRBisJgv3G6a

### "How might we learn?" (2024): the closest match to your design
Source: https://andymatuschak.org/hmwl
- His running example is a person, "Sam", learning prerequisites in order to understand papers for a brain-computer-interface (BCI) project.
- **Practice should be synthesized and varied:** "These synthesized prompts can vary each time they're asked… practice accessing the same idea from different angles." It should get deeper over time, stay "grounded in the details of Sam's BCI project", and the learner "can steer them with feedback."
- **Risks he names:**
  - Parroting: "I may recognize the text of the question without really thinking about it."
  - Transfer: "I won't always recognize what knowledge I should use… I need to acquire schemas."
  - Generic cards: memory-system questions "feel like generic textbook questions."
- **On chatbot tutors:** they live "in a windowless box" and are "transactional, amnesic." He argues explicit study should be "utterly in service to your actual aims."

### Michael Nielsen, "Augmenting Long-term Memory"
Source: http://augmentingcognition.com/ltm.html
- **Reading the AlphaGo paper:** he made several skimming passes and wrote elementary questions first, then deeper ones over 5–6 passes.
- **Card design:** atomic cards (he split a Unix soft-link card into two), multiple cards per idea, and avoiding "orphan" questions.
- **Cost:** about 4–7 minutes of total review time per card. If something seems worth more than 10 minutes of future time, it's worth a card.
- **Limits:** cards don't give procedural fluency, and shared decks are weak because "making Anki cards is an act of understanding in itself."

---

## 3. Other practitioners on card quality for conceptual material
- **Wozniak, "20 rules"** https://www.supermemo.com/en/blog/twenty-rules-of-formulating-knowledge
  - Rule 1 "Do not learn if you do not understand", rule 2 "Learn before you memorize", rule 3 "Build upon the basics", rule 4 minimum information principle.
  - Avoid sets and enumerations, and combat interference ("Interference is probably the single greatest cause of forgetting").
  - Redundancy doesn't contradict minimum information, and personalized examples help.
- **Gwern** https://gwern.net/spaced-repetition
  - He quotes research that spacing benefits "may be muted for many mathematics tasks" and decline as "conceptual difficulty … increased."
  - On adoption, he relays a developer's report: "Less than 20 people out of 4000 did more than one session."
  - He favors custom-made cards over pre-made decks.
- **Nicky Case** https://ncase.me/remember/
  - "Each flashcard should have one & only one idea."
  - Start at 5 new cards a day and build up to about 30.
  - Connect cards to something "MEANINGFUL", and make your own.

---

## What this means for the design
These are my synthesis, not claims from the sources.
- **Keep two edge types, as MA does:** prerequisites for gating, and fractional encompassings for implicit credit. Give each fact or knowledge point its own key-prerequisite links so remediation can be targeted. Zero-weight prerequisites ("familiarity only") are a legitimate edge type.
- **LLM generation should be split into two steps,** choosing what to reinforce and then writing the question. Give the model explicit conceptual "patterns": classify an example, generate a counterexample, compare with a neighboring concept, ask why it matters. Use the target paper as the context and the "angle hint".
- **Expect a tension between MA's rigidity and Matuschak's emphasis on agency.** Users quit over unskippable paths and opaque queues. Showing the learner the path to the paper, and letting them skip or claim a node and then verifying the claim cheaply (as MA's conditional completion does), would address both.
- **Plan for gaming and underconfidence** (guessing, an "I don't know" button that gets abused), and **for review debt** (cap the review-to-new ratio).
