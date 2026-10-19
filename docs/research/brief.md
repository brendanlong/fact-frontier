# Problem brief: an adaptive tool that teaches what you need to understand something

## Goal

Teach a user the knowledge they need to understand a target (first: a specific research
paper) as efficiently as possible, and keep that knowledge over time. "Efficiently" means
learner time, not compute: money for model calls is essentially no object right now, and
quality of *what* gets taught matters far more than latency or cost.

The owner believes the app shell (UI, storage, scheduling plumbing) is easy, and that nearly
all of the risk is in **deciding what to teach, in what order, and how to update that over
time** as the learner's goals and knowledge change.

## The user and use cases

- First user: an experienced software engineer doing ML research (training data attribution,
  emergent misalignment, interpretability). Reads recent arXiv papers and wants to understand
  them well enough to use and extend their methods, not to memorize them.
- **First use case:** give it a research paper; it works out what this user needs to know to
  read and understand the paper, teaches that, and maintains it.
- Goals change over time: new papers, new research directions, sometimes non-paper goals
  (a project, a planned activity).
- Later use cases that the design should not preclude:
  - **Language learning**, driven by the learner's interests and plans (a show they're
    watching, a trip). Lesson types will differ a lot from ML concepts.
  - Software engineering / system design skill-building.

## Requirements and preferences stated by the owner

- **Unknown prerequisites:** for very new papers, a model may not know some prerequisites
  (post-training-cutoff methods, new terminology). The system must flag what it doesn't know
  rather than guess.
- **Importance is unclear at first:** when a paper is new to the user, it's hard to know what
  matters. Track things the user *might* need to know; order by generality (more general and
  more foundational first), which may fall out of good prerequisite structure.
- **Varied effort levels, chosen on demand:**
  - no effort: a reminder (something to read, a podcast)
  - low effort: flashcards
  - higher effort: a quiz, written or spoken questions
  - very high effort: worked homework problems
- **Varied recall:** questions should vary (e.g. apply a concept in a new scenario, choose
  between methods for a given situation) rather than repeat the same card, while answers stay
  short enough to be practical.
- The owner is not attached to any of these suggestions; established best practice should
  win where they conflict.

## Open question for the MVP

Probably the MVP focuses on deciding what to teach and what comes next, but the downstream
activities (explaining, quizzing, homework, scheduling) likely constrain that design, so they
need to be considered now.

## Constraints

- Agents doing the work are LLMs (Claude Sonnet/Opus class, or others via OpenRouter); they
  need clear goals and rubrics to follow.
- Single user to start; a web app with a persistent backend.

## Appendix: a source the owner was sent (BetterExplained, "ADEPT method")

Kalid Azad's ADEPT method for explaining a difficult concept: give an **A**nalogy (what else
is it like), a **D**iagram, an **E**xample the learner works through themselves, a
**P**lain-English description in their own words, then the **T**echnical description. He
argues for **"blurry-to-sharp"** ordering: start with a rough analogy of the whole idea and
sharpen it until the technical details are covered, rather than presenting facts in
prerequisite order. He also says what survives a year later is mostly an analogy or diagram,
not the details. Style: brevity, and empathy (anticipate the learner's questions). The owner
thinks this mainly bears on how explanations are written, but it may also affect ordering
and structure.
