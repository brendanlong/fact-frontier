# Expert opinion: designing the core so language learning fits later

Perspective: applied linguist (second language acquisition, adult self-directed learners), with
consulting experience on language-learning apps. This is an independent opinion written from the
problem brief only. Citations are from memory of the SLA literature and are meant as pointers,
not a systematic review.

## Bottom line

Building a language learner on a research-paper engine fails in two ways, and both are
decided by the core data model, not by lesson types:

1. **Scale and shape.** A paper needs roughly 20 to 150 concepts with deep prerequisite chains.
   A language needs 3,000 to 9,000 word families, thousands of multiword chunks, and a few
   hundred grammatical constructions. Prerequisite structure is shallow and the order is driven
   by frequency. If the core assumes each item is precious, LLM-curated and DAG-ordered, it will
   not scale to that.
2. **What "knowing" means.** For a paper, knowing means you can explain or apply an idea. In a
   language, knowing an item has several separate parts. You can recognize a word in print and
   still miss it in fast speech, or be unable to say it in conversation. Speed and automaticity
   are part of the competence itself. If the core stores one mastery number per item, it will
   overstate what the learner can do in every skill except the one that was tested.

If those two points are handled now, the rest (lesson types, audio, speech grading) can be added
later.

---

## 1. How language learning differs, and what a unit of knowledge looks like

### 1.1 Kinds of knowledge

| Kind | Examples | How it is learned | What "known" means |
|---|---|---|---|
| **Lexis (single words)** | *ventana*, *aunque* | Explicit form-meaning mapping (flashcards work well), then consolidation through many encounters in input | Recognize the form and get the meaning (receptive). Retrieve and produce the form (productive). Do either at speed, in print and in audio |
| **Formulaic sequences / chunks** | *¿me pone un café?*, *no pasa nada*, *de hecho* | Memorized as a whole, much like words. They give a large share of early fluency (Wray 2002; Boers & Lindstromberg 2012) | Understand and produce the whole unit with no assembly |
| **Grammar (constructions, morphology)** | Past-tense contrasts, subjunctive after *quiero que*, gender agreement | Explicit instruction helps and lasts (Norris & Ortega 2000; Spada & Tomita 2010). Accurate *spontaneous* use needs a great deal of practice and follows developmental stages that instruction cannot skip (Pienemann's Processability Theory) | Three separate levels: can state the rule; can apply it in a controlled exercise; uses it correctly in free, timed production. These come apart, and the gap is often large |
| **Phonology / orthography** | Sounds, prosody, a new script (kana, hangul, hanzi), sound-spelling rules | Perceptual training, a lot of listening, explicit sound-symbol drills | Perceive the contrast, produce it so others understand, decode the script fluently |
| **Pragmatics / register** | *tú* vs *usted*, politeness formulas, which slang is safe to use | Explicit notes plus exposure | Pick the right form for the situation |
| **Skills** | Listening, reading, speaking, writing, interacting in real time | Practice under real-time pressure. This is procedural knowledge that becomes automatic (DeKeyser's Skill Acquisition Theory) | Throughput and comprehension rate on real material. It cannot be reduced to item knowledge |

Contrast with the ML-paper case:

- **Procedural and automatic knowledge is the goal, not a side effect.** Knowing what "KL
  divergence" means is mostly declarative. Understanding 150 words per minute of TV dialogue
  needs word recognition in roughly 200 to 300 ms. Declarative knowledge of a word is necessary
  but not sufficient. The learner model has to represent *fluency* (speed, effortlessness), not
  only *accuracy*.
- **Input does real work.** Much language learning comes from meaning-focused exposure, not
  from lessons. Incidental vocabulary learning is real but slow. Uptake depends heavily on the
  number of encounters: about 8 to 20 or more encounters for solid gains (Webb 2007;
  Uchihara, Webb & Yanagisawa 2019 meta-analysis). Captioned viewing helps both vocabulary and
  listening (Montero Perez et al. 2013). So passive input is a learning activity that changes the
  learner model, not just a "reminder."
- **Input only helps when it is comprehensible.** Reading for pleasure needs about 98% known
  running words, with 95% as a workable minimum (Hu & Nation 2000; Laufer & Ravenhorst-Kalovski
  2010). Listening tolerates somewhat less, perhaps around 90 to 95% (van Zeeland & Schmitt 2013).
  Below these thresholds, "watch the show" practice mostly frustrates and teaches little.
- **Frequency matters more than prerequisites.** The most frequent 1,000 word families cover
  roughly 80 to 85% of typical text and more of conversation. For TV, about 3,000 families plus
  proper nouns gives about 95% coverage, and 6,000 to 7,000 gives about 98% (Webb & Rodgers 2009;
  Nation 2006). There are real dependencies (a script before reading, basic verb morphology
  before tense contrasts, developmental stages in syntax), but they are few and shallow.
  "Generality first" maps almost exactly onto "frequency first."
- **L1 changes difficulty a great deal.** For an English speaker, cognates (*información*)
  cost almost nothing, false friends (*embarazada*) are traps, and some contrasts that do not
  exist in English (Spanish *ser/estar*, Japanese particles) are hard. Item difficulty is a
  property of the pair (learner's L1 and other languages, item), not of the item alone.
- **Interference between similar items is a real cost.** Learning semantically similar new
  words together (all the kitchen utensils, all the colors) slows learning (Tinkham 1993;
  Waring 1997; Nation 2000). This works directly against naive "interest-based" batching (see
  section 4).
- **ADEPT applies only partly.** Analogy and diagram help with grammar concepts and sound
  systems, but most lexis has no "blurry-to-sharp" explanation to give. The language version of
  blurry-to-sharp is different: gist comprehension of a scene first, then detail, then form
  focus. Meaning comes first and attention to form comes after (Long's focus on form).

### 1.2 The unit of knowledge

I would model two levels.

**Knowledge item** (what the learner model tracks):

- `id` in a language-scoped namespace, such as `es:lemma:ventana`, `es:mwe:no_pasa_nada`,
  `es:gram:subjunctive_after_volition`, `ja:script:katakana`, `es:sense:banco#bench`.
- `type`: lemma, sense, multiword expression, construction, phonological feature, script unit,
  pragmatic convention, skill.
- **Granularity choice:** use the *lemma*, or the lemma split by sense where senses differ a
  lot. Do not use the word family. Recent work shows that learners below an advanced level do
  not reliably transfer knowledge across derived forms (Brown, Stoeckel et al. on lemma vs
  family counting). Track inflected forms as evidence about the lemma, not as separate items,
  except for irregular forms, which can be their own items.
- Frequency rank(s): in a general corpus (subtitle frequencies such as SUBTLEX are best for
  spoken targets) and in each active target.
- L1-relative difficulty hints: cognate, false friend, new phoneme, irregular.
- Relations: a light graph with edges such as *is part of* (chunk to lemma), *contrasts with*
  (ser/estar), *confusable with* (interference), *requires* (script to reading, used rarely).
  Do not require a DAG.

**Mastery state** (per item, split by facet):

- Facets: receptive-written, receptive-aural, productive-written, productive-spoken. For
  grammar, also explicit, controlled and spontaneous.
- Each facet keeps its own memory state (stability and retrievability, as in FSRS) and its own
  evidence log: test results *with response latency*, plus counted exposures from input.
- The facets are correlated, so evidence on one should move the others' priors, but they
  should not be merged.

**Practice prompt / card** (what the learner sees) is a separate object from the item. One item
has many prompts: cloze in a new sentence, audio recognition, L1-to-L2 production, and a clip
from the show where the word occurred. The brief's "vary the question" requirement maps directly
onto this: retrieval of the same item in varied contexts. In vocabulary research, encountering a
word in varied contexts improves later use (Joe 2010 and others on varied encounters).

---

## 2. "What to teach next" for an interest-driven language learner

### 2.1 How the target changes

A paper is a **bounded target with a dependency structure**: "what concepts, in what order,
until I can follow section 3." A show or a trip is a **corpus or situation target that grows
over time**: "maximize what fraction of upcoming episodes I can follow" or "be able to handle the
following 25 situations by 14 March."

| | Research paper | TV show | Trip |
|---|---|---|---|
| Target representation | Set of concepts with prerequisite edges | Token-frequency distribution over subtitles of upcoming episodes | List of can-do scenarios (ordering food, buying tickets, asking directions, handling a problem) with associated chunks, lexis and listening demands |
| Success metric | Can explain or apply the paper's key ideas | Estimated coverage of the next episodes, both lexical and aural (≥95% means watchable with L2 subtitles) | Can perform each scenario (role-play pass), understand numbers, times and prices by ear |
| Main skill | Conceptual understanding | Listening (fast, informal, slang) | Speaking plus listening, interaction |
| Deadline | Soft | None. It rolls episode by episode | Hard date, after which the goal decays |
| Number of items | 10s to 100s | 1,000s | 100s (mostly chunks) |
| Ordering principle | Prerequisites, generality | Coverage gain per minute of study | Scenario priority × frequency, chunks before grammar |

### 2.2 A concrete selection policy for "I'm watching show X"

1. **Ingest:** get subtitles for the next N episodes. Tokenize and lemmatize, detect multiword
   expressions, and remove proper nouns (character names count as "known" for coverage, as in
   Webb & Rodgers). Languages without spaces (Japanese, Chinese) need a real segmenter. That is
   domain-specific code.
2. **Estimate coverage** of each episode from the learner model. This needs probability-known
   for *every* lemma, including ones never tested. So the learner model has to generalize, for
   example with an IRT-style ability estimate over frequency bands combined with per-item
   evidence. A 10-minute frequency-band placement test (in the style of the Vocabulary Size
   Test or LexTALE) seeds this.
3. **Sort each unknown item into one of three groups:**
   - **Teach** (spaced, durable): unknown, and high in *both* show frequency and general
     frequency. These give the best transfer per minute.
   - **Gloss** (just-in-time, not scheduled): show-specific and rare in general use (*dragon*,
     a made-up technobabble term, a character's catchphrase). Show it as a pre-episode
     preview or a subtitle hover. Promote it to "teach" only if it keeps recurring.
   - **Ignore**: occurs once, and the context makes it clear enough.
4. **Ranking score** for "teach": roughly
   `expected coverage gain over upcoming target episodes × w_target + general-frequency utility × w_general`,
   divided by expected learning cost (cognates are cheap, false friends are expensive). Then
   apply an interference penalty for close semantic neighbours already in the new-item queue.
5. **Recommend input:** suggest the next episode when its estimated coverage is in the sweet
   spot, and suggest support (L2 subtitles, a pre-episode vocabulary preview of 5 to 10 items,
   or a slowed or LLM-simplified recap) when it is not.
6. **Close the loop:** after watching, log exposure counts for the items in that episode as
   weak evidence, and give a short check on the key items (for example, "what did X mean in
   the scene where...").

### 2.3 "I'm going on a trip"

- Deadline-aware: schedule so that retrievability is high *on the trip dates*, not for
  long-term retention. Massed-then-spaced is acceptable here, and long-term spacing is less
  important.
- Lead with chunks, not grammar: "*¿Cuánto cuesta?*", "*Quisiera...*", "*¿Me lo puede
  repetir más despacio?*" Survival chunks plus a repair strategy give more than paradigm
  tables.
- Weight receptive-aural and productive-spoken heavily, and include numbers by ear (prices,
  times, platform numbers). Learners consistently underestimate how hard these are.
- After the trip, lower the goal weight. Do not delete items. The general-frequency ones stay
  useful, and the trip-specific ones can quietly fall to low priority.

### 2.4 Comparison with "what do I need to read this paper"

Common structure: **target → required items with weights → gap against learner model → rank by
value per learner-minute → choose activity type → update from evidence.** The differences are in
the details:

- Paper ranking is driven by prerequisites and generality. Language ranking is driven by
  coverage and frequency. "Generality" in the paper case and "general frequency" in the
  language case play the same role: the transfer value of an item beyond the current target.
  Score that explicitly in both cases.
- The paper case can afford LLM reasoning per item. The language case needs the gap analysis
  done cheaply and statistically over thousands of items, with LLMs used for generating content
  and for edge cases (slang, idioms, dialect).
- The teach / gloss / ignore split is useful for papers too: a notation used once in an
  appendix should be glossed, not scheduled. I would put it in the core.
- The "flag what you don't know" requirement has a direct language counterpart. New slang,
  regional usage, a word missing from frequency lists and dictionaries, and the model's
  uncertainty about a dialect-specific meaning should all be flagged, not guessed at. LLMs
  confidently invent glosses for slang.

---

## 3. Shared core vs domain-specific, and concrete requirements now

### 3.1 What can be shared

- **Item store:** typed items in a namespace, with a light relation graph. Prerequisites are
  one edge type among several.
- **Learner model:** evidence log (every observation, with timestamp, item, facet, outcome,
  latency, activity type, evidence strength) → per-facet memory state → probability-known for
  any item, including untested items, through generalization.
- **Goals / targets:** a weighted demand over items, with an optional deadline, a priority and
  a decay. Several goals are active at once, and an item's value is summed across goals.
- **Planner:** ranks candidate learning actions by expected value per learner-minute. Value
  means goal-weighted gain plus transfer value. Gives the teach / gloss / ignore decision.
- **Scheduler:** a memory model (FSRS-like) for each item facet, plus a daily budget for new
  items and reviews.
- **Activity framework:** activity types declare which items and facets they exercise, the
  effort level, the expected time, and how their outcome maps to evidence.

### 3.2 What must be domain-specific

- **Target ingestion:** paper → concepts, versus subtitles → lemmas, MWEs, constructions,
  versus trip → scenarios → chunks. That includes language-specific NLP (lemmatizer, segmenter,
  MWE lexicon, frequency lists by variety).
- **Placement / priors:** frequency-band vocabulary tests for language, versus self-report plus
  probe questions for ML.
- **Content generation and grading rubrics:** example sentences checked for naturalness and the
  target variety, audio (TTS), speech recognition and pronunciation scoring, grammar error
  feedback.
- **Facet definitions:** the four language modalities, versus explain / apply / choose-between
  for concepts.
- **Difficulty priors:** cognates and L1 transfer, versus mathematical background.

### 3.3 Concrete requirements for the core design now

1. **Items must not assume a DAG or a hand-curated order.** Prerequisite edges are optional and
   sparse. The ranking has to work with *no* edges, using frequency and coverage alone.
2. **Scale:** support about 10^4 to 10^5 items per learner with cheap bulk operations
   (estimating probability-known for 20k lemmas in well under a second). Do not put an LLM
   call in the per-item inner loop of planning.
3. **Mastery is per (item, facet), not per item.** Facets are declared per domain. Leave room
   for a fluency or latency dimension, not only correctness. Store response time with every
   test event now. It is free to record and impossible to recover later.
4. **Evidence comes in different strengths and kinds,** including *exposure without a test*
   (saw it in an episode, heard it in a podcast), self-report ("I know this"), and tests. The
   model must accept weak evidence and not treat exposure as a successful review.
5. **Probability-known must generalize to untested items** through a learner-level ability
   estimate over item features such as frequency band, cognate status and type. Item-only
   tracking cannot estimate coverage of an episode.
6. **Targets can be distributions,** "coverage of this corpus," not just a list of required
   items. The metric is weighted coverage, and the goal is "reach a threshold," not "master
   everything."
7. **Teach / gloss / ignore is a first-class outcome** of the planner, so the system does not
   schedule every unknown item for spaced review.
8. **Items are separate from prompts.** One item has many varied prompts, and prompts can
   exercise several items at once (a sentence card tests one target word plus known context
   words). The evidence model has to credit the target item and give at most weak credit to
   the others.
9. **Several goals at once, with deadlines and decay.** Value sums across goals. Goal
   priority can change. An item supporting a finished goal keeps its transfer value.
10. **Interference relations** (`confusable_with`) affect when new items are introduced
    (spread out near-synonyms and same-category sets), not only how they are reviewed.
11. **Hard daily budgets** for new items and review minutes, set by the learner, with the
    planner deciding within them. Review debt is the main reason people abandon these apps
    (section 4).
12. **Learner profile includes L1 and other known languages, target variety (es-MX vs es-ES),
    and preferred register,** and items or content can be tagged by variety.
13. **Activities declare which facets they exercise.** Then "no effort / flashcard / quiz /
    homework" becomes "which facets and how much evidence," and new activity types such as
    shadowing, dictation or role-play can be added without schema changes.
14. **Media-anchored evidence:** an item occurrence can point to a location in a source (paper
    section, episode timestamp). Learning from the exact clip where a word occurred is one of
    the most motivating and effective things an interest-driven app can do.

---

## 4. What goes wrong in language apps that adapt to interests (ranked)

Ranked by how often I have seen each problem damage outcomes or retention, combined with how
severe it is.

1. **Review debt and the flashcard treadmill.** Interest-driven ingestion surfaces hundreds of
   "new" words per episode. Learners add them all, and within weeks they face 300 reviews a
   day and quit. *Mitigation:* the teach / gloss / ignore triage, a hard cap on new items per
   day (often 5 to 15 is right), a review time budget, an FSRS-style scheduler tuned for
   retention around 0.85 to 0.9 rather than 0.95, and counting real input as consolidation.
2. **Too much interest-specific vocabulary, too little high-frequency core.** A learner
   ends up knowing *espada, reino, traición* but not *aunque, quedar, soler*, which matter in
   every episode of every show. *Mitigation:* always blend general-frequency utility into the
   score. Report coverage gains to the learner ("these 10 words raise next episode from 91% to
   94%") so the high-frequency choice also feels interest-driven.
3. **Incomprehensible input given as practice.** Native shows for a beginner run at about
   70 to 85% coverage. Watching them is enjoyable but teaches little and discourages.
   *Mitigation:* estimate coverage before recommending. Offer support in steps: a preview of
   key words, L2 subtitles, LLM-generated graded summaries or simplified retellings of the
   episode, slower audio, and easier "bridge" content in the same genre. Be honest that
   real-time listening to native TV is a B2-level target.
4. **Receptive knowledge mistaken for ability.** The app reports "1,200 words known,"
   but the learner cannot follow speech or say anything. *Mitigation:* per-facet mastery,
   aural recognition prompts (audio-first cards), production prompts for a chosen subset, and
   dashboards split by skill.
5. **Errors and unnaturalness in LLM-generated content.** Wrong gender or agreement in rare
   cases, sentences that are grammatical but nothing a native would say, mixed varieties
   (*vosotros* in a Mexican-Spanish course), wrong register, made-up slang glosses, and TTS
   that mispronounces or gets pitch accent wrong. *Mitigation:* ground glosses in dictionaries
   and corpus examples where possible, keep the variety and register consistent, run a second
   model as a verifier with a rubric, flag low-confidence glosses, and prefer authentic
   example sentences from the learner's own media.
6. **Semantic-cluster batching.** "Words from the cooking episode" means introducing
   many near-synonyms together, which causes interference. *Mitigation:* introduce related
   items over days, and use thematic (story-linked) grouping rather than category grouping.
7. **Grammar left out or taught too early.** Interest-driven apps often become vocabulary
   apps. Others teach the subjunctive to someone who cannot reliably conjugate the present.
   *Mitigation:* model constructions as items, introduce them when they are frequent in the
   learner's input *and* developmentally plausible, and pair explicit explanation (short,
   ADEPT-style is fine here) with lots of input showing the form and some controlled practice.
8. **Optimizing engagement metrics instead of learning.** Streaks, XP and "lessons
   completed" become the goal. *Mitigation:* track outcome metrics (coverage of real content,
   comprehension checks on new episodes, timed production samples) and show them to the
   learner.
9. **Stranded goals.** The learner finishes or abandons the show, but its items still fill
   the queue. *Mitigation:* goal decay and re-weighting. Items with low general value get
   suspended or slowed.
10. **Too much correction in production, and anxiety.** Correcting every error in speech
    practice is discouraging. *Mitigation:* focus feedback on the targeted forms plus errors
    that impede meaning. Recasts and prompts are both effective (Lyster & Saito 2010; Li
    2010). Prompts that ask the learner to self-correct are a bit stronger for accuracy.
11. **Data access fragility.** Subtitles for the show may not be available, may be poorly
    timed, or may be fan translations from English rather than the original dialogue.
    *Mitigation:* support several sources (subtitle upload, ASR on audio the learner owns),
    detect translated subtitles, and treat unavailable targets gracefully.

---

## 5. Effort levels in language learning, and the evidence

A useful frame is Nation's **four strands**, each roughly a quarter of learning time:
meaning-focused input, meaning-focused output, language-focused learning, and fluency
development. The owner's effort levels map onto it, but the map is not one-to-one. In
particular, the "no effort" level is a main strand in language learning, not a reminder.

| Owner's level | Language version | Strand | Evidence |
|---|---|---|---|
| **No effort** (reminder, podcast) | Extensive listening or reading *at the right level*. Watching the target show with L2 subtitles. Graded podcast. LLM-written story or recap using target items at ≥95 to 98% coverage | Meaning-focused input. When the material is easy and plentiful, also fluency development | Incidental vocabulary gains are reliable but small per encounter and depend on frequency (Webb 2007; Uchihara et al. 2019). Captions give clear benefits for listening comprehension and vocabulary (Montero Perez et al. 2013). Extensive reading improves reading rate and vocabulary (Nakanishi 2015 meta-analysis). The input has to be comprehensible, and the benefits are long-term. It is still the only route to listening fluency and to the collocations and usage that flashcards never teach. It is not truly "no effort," but it is the most *pleasant* effort, which matters for adherence |
| **Low effort** (flashcards) | Spaced retrieval of form-meaning links, preferably audio plus sentence context. Receptive first (L2→meaning), then productive (meaning→L2) for chosen items | Language-focused learning | Strongest evidence per minute for initial vocabulary learning. Deliberate, decontextualized learning is efficient (Nation 2013; Nakata 2011 on flashcard design; Webb, Yanagisawa & Uchihara 2020 meta-analysis: flashcards among the most effective intentional activities). Spacing and retrieval effects are robust (Nakata 2015; Cepeda et al. 2006 for general memory). Effects depend on the direction of retrieval: practice in the direction you will need it (transfer-appropriate processing). Productive retrieval is harder and transfers better to production. Limits: no automaticity in real-time listening and little collocation or usage knowledge. Too much semantic elaboration during form learning can *hurt* memory for the form (Barcroft's TOPRA model) |
| **Higher effort** (quiz, written or spoken questions) | Cloze in new contexts. Dictation. Listening comprehension questions on a clip from the show. Translation or production prompts with feedback. Short spoken answers with ASR and LLM feedback. Controlled grammar practice | Language-focused learning plus meaning-focused output | Output pushes learners to notice gaps (Swain's Output Hypothesis). Corrective feedback has moderate to large effects (Li 2010; Lyster & Saito 2010). Explicit grammar instruction with practice is effective and lasting on tests (Norris & Ortega 2000; Spada & Tomita 2010), though the effect on *spontaneous* use is smaller. Spaced practice helps grammar too (Suzuki, Rogers and colleagues), with some nuance about how long the gaps should be. Dictation and listening-focused tasks address the weakest skill for most self-directed learners |
| **Very high effort** (homework) | Task-based work: role-play the trip scenario with an LLM interlocutor under time pressure. Summarize an episode aloud. Write a review of the episode and get reformulation. Shadowing. The 4/3/2 retelling activity (tell the same story in 4, then 3, then 2 minutes) | Meaning-focused output plus fluency development | Task-based language teaching has positive meta-analytic support (Bryfonski & McKay 2019). Interaction with negotiation of meaning helps acquisition (Long's Interaction Hypothesis; Mackey & Goo 2007 meta-analysis). Repeating a task and 4/3/2 improve fluency measures (Nation; Bygate). Shadowing evidence is promising but methodologically weaker. LLM conversation partners are new, and the controlled evidence is thin. My expectation is that they help mainly with willingness to speak and with automatizing chunks. They need guard rails: the partner has to stay within the learner's level and not do all the talking |

Two consequences for design:

- **Choosing an effort level on demand fits language learning well,** because adult learners'
  available time and attention vary a lot. However, the planner should choose the *facet* and
  *strand* the learner most needs within the chosen effort level. Someone who only ever picks
  flashcards should get a message like "your listening is lagging your reading by a whole
  band. Here's a 5-minute clip version."
- **Passive input must update the learner model,** as weak exposure evidence, and comprehension
  checks on input are cheap, high-value evidence. This is the clearest case where the
  research-paper framing (reminders as no-evidence nudges) would lock out the language case if
  it were built into the core.
