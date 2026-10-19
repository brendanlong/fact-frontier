# AI-systems review of the design plan

**Reviewed:** 2026-10-19. **Perspective:** engineering and evaluating multi-step LLM pipelines, with quality prioritized over model spend and one expert learner as the initial user.

**Sources read:** `docs/PLAN.md`, `docs/research/brief.md`, `expert-llm-systems.md`, `expert-its.md`, `devils-advocate.md`, `lit-ai-methods.md`, relevant portions of `expert-research-mentor.md` and `lit-learning-science.md`, and `DESIGN.md`. Prototype inspection covered `frontier/`, tests and the comparison script; an independent evaluation pass also consulted the learning-scientist and language reports. References below are repository-relative; line references refer to the reviewed draft.

## Overall assessment

The direction is good: paper-first support, requirements separate from learner gaps, grounded artifacts, code-owned state, typed relations, cheap disputes, and comparison against reading with chat. This is feasible as a single-user tool. It is **not** feasible as a reliably autonomous system merely by composing the proposed model calls and enforcing their JSON verdicts.

The highest risks are false measurement, false merges, and false evidence attribution. They deserve more engineering than a complete global graph. Several recommendations in the supporting reports are useful hypotheses rather than established methods: a model cannot be made ignorant by withholding a definition; two agreeing solvers do not prove unambiguity; a graph revision does not reveal which historical answer tested which new child concept; and concept-level FSRS with fractional implicit credit is not an off-the-shelf validated scheduler.

**Recommendation:** retain the architecture, but make Phase 1 a narrow, source-grounded requirements experiment before building the full concept graph. Establish source/version identities, semantic scoring, call artifacts and minimal event records early. Defer automatic splits, global hard prerequisites, learned item difficulties and fractional memory credit until there is evidence they help.

### Severity convention

- **Blocker:** must be resolved before the affected acceptance metric or automatic learner-state operation can be trusted; not a reason to stop exploratory/manual use.
- **Major:** likely to cause materially wrong content, misleading evaluation or substantial rework.
- **Minor:** localized inconsistency or avoidable complexity.

## Prioritized issues

### 1. **Blocker — Extraction recall and precision have no operational matching definition**

**Plan:** §5, requirement-set rubric (`PLAN.md:346–347`); §6, gold A and metrics (`361–379`); Phase 1 exit (`443–448`).

**Problem:** A list of concept names does not define a denominator that survives different names, depths, senses or decomposition. “Inverse-Hessian-vector products,” “solving the influence linear system,” and “CG for inverse curvature” can overlap without being equivalent. One broad “influence functions” candidate must not receive credit for every related gold requirement. Conversely, two narrower candidates may jointly satisfy one gold requirement. Exact-name matching and unconstrained embedding/judge similarity both produce misleading scores.

The owner’s quick list is incomplete: an unmatched extracted requirement is not automatically false. A stuck point is an observed need, not an exhaustive inventory. “Know it” labels are not extraction negatives: a known concept can be entirely necessary for the paper. The plan currently treats triage as precision labels (§4.3), conflating requirement correctness with teaching utility.

**Suggested change:** Freeze a requirement-level scoring protocol in Phase 0. Gold entries should state an operational competency, sense, minimum depth, served passages and importance, with acceptable aliases/decompositions. Compute evidence-backed semantic coverage, adjudicate unmatched predictions, and keep separate metrics for requirement relevance and learner-gap discovery. Report macro scores by paper, critical misses and review burden, not just pooled counts. Normalize the one-shot baseline into the same scoring format and blind the owner to which system produced it. A concrete matching procedure appears in Appendix B.

### 2. **Blocker — The leak and diagnostic checks require a capable model to forget its knowledge**

**Plan:** §4.5, item pipeline (`256–260`); §5, diagnostic and item rubrics (`351–353`).

**Problem:** “A solver given only the stem and the concept’s name must fail” is not a leak test. A capable model already knows KL divergence, LoRA or influence functions; removing the definition from context does not remove that knowledge. Correctly solving a good question would cause rejection. Asking the model to pretend not to know is not a remedy. The full-context/name-only comparison therefore cannot establish diagnostic discrimination either. This conflicts with §7’s appropriate warning against simulated-student evidence and with `expert-llm-systems.md:395–402` and `lit-ai-methods.md:483–504`.

**Suggested change:** Remove name-only solver failure as a release gate. Check surface leakage directly: identify phrases that state the required answer, paraphrased key points in the stem, answer-bearing captions, leading alternatives and trivial linguistic shortcuts. Use counterfactual variants: change the setup so the correct answer changes, redact the target relation, or use a consistently renamed synthetic concept to test dependence on supplied information. These are shortcut-detection tests, not estimates of human difficulty. Keep blind solving for key correctness, and estimate discrimination only from owner responses/spot-checks. Recognition items can be legitimate for a `recognize` objective; the blanket “retrieval, not recognition” rule should be depth-specific.

### 3. **Blocker — Concept identity, target depth and facet are not consistently represented**

**Plan:** §4.1 (`107–135`); §4.7, concept-level FSRS (`298`); §4.8, mastery per `(item, facet)` and prompts separate from items (`318–325`).

**Problem:** The plan has four depths but learner state only per `(concept, facet)`. A successful explanation can then satisfy an application requirement unless code invents an unstated conversion. ML facets `explain/apply/choose` duplicate some depths, while language changes the tracked unit from concept to item. “Items separate from prompts” later contradicts the earlier use of Item as an assessment question.

Formal and informal definitions are also not necessarily different depths: both can be explanation tasks. “Extend” is not a stronger definition of a term; it is a task under particular conditions. The three-question/5–15-minute granularity heuristic is useful for lesson planning but cannot be the sole identity rule for durable concepts.

**Suggested change:** Define these separately before schema implementation:

- **Concept/sense:** the stable meaning and scope, independent of any particular teaching activity.
- **Objective:** a concept at an operational capability/depth, optional domain facet, and scope/conditions.
- **Requirement:** a goal’s need for that objective, with passage-level justification.
- **Item version:** a specific assessment, tagged to objectives per key point.
- **Presentation/attempt:** the rendered prompt, permitted resources and response modality.

At minimum key state by concept/sense **and objective depth**, with an optional namespaced facet. Make any implication between objectives explicit and conservative; do not assume all four levels form a universally valid mastery ladder. Define language vocabulary as a concept type, not a second meaning of Item. Appendix A gives a minimal contract.

### 4. **Blocker — Event sourcing preserves evidence, but cannot automatically recover its meaning after splits**

**Plan:** §4.1, replay and stable IDs (`125–132`); §4.5, dispute voiding (`269`); Phase 3 event-log delivery (`460–462`).

**Problem:** Replaying against the current graph can inflate mastery retroactively. An old item tagged “curvature approximation” may have tested only K-FAC. Splitting that concept into K-FAC and EK-FAC does not make the old response evidence for both. Re-tagging an entire item can still be wrong if its key points test different concepts. Merging two partially overlapping concepts has the same problem. A new `encompasses` edge can manufacture historical reviews that never exercised that skill.

Historical reproducibility and current best attribution are distinct views. Grading, diagnosis and user overrides are also revisable: overwriting a grade or deleting disputed evidence violates the claimed append-only design. Phase 2 already produces learner evidence, so its event records cannot wait until Phase 3.

**Suggested change:** Record immutable item/rubric/grade versions and append separate superseding grade, dispute-resolution and attribution events. Store key-point-to-objective mappings. A split requires explicit reviewed mappings of historical evidence; ambiguous old evidence remains on the retired parent or becomes unassigned/low-confidence—not full credit to every child. Keep both **as-observed** replay and **current-attribution** replay, each pinned to a projection/migration version. Require before/after state diffs and an undo path for merges, splits and edge-credit changes. Add the minimal event envelope before Phase 2’s first triage/probe; keep the reducer simple.

### 5. **Major — Provenance classes conflate origin, model familiarity and permission to generate**

**Plan:** §4.1 (`111–114`); §4.5, `background` exemption (`247–249`); §4.6 (`274–294`).

**Problem:** A standard concept can be defined in the target paper, have a defining citation and be misremembered by the model simultaneously. A global concept’s status changes when another model or paper is used. `grounding-required` is mentioned but not one of the classes. Agreement between closed-book and extracted definitions can be a shared error; disagreement can be harmless notation or a real sense collision. Publication dates are only weak familiarity signals, and an unavailable/uncertain cutoff must not be guessed.

Most importantly, the prototype’s documented mathematical errors were **standard background**—a missing minus sign and omitted assumptions—not just unfamiliar methods. Allowing `standard` background to be generated and checked against model memory leaves precisely that failure path open. A citation tag establishes neither entailment nor truth.

**Suggested change:** Separate `origin_relation` per source occurrence, `sense_collision_status`, `grounding_status` per artifact/claim, and model-specific familiarity signals. Missing cutoff metadata means `unknown`, not a fabricated date. Use collision probes as escalation signals, never as certification. Ground central background claims in an authoritative fetched source too; permit clearly labeled provisional background only for low-risk exposition. Check theorem assumptions, signs and notation explicitly, using tiny computational counterexamples where feasible. No explanation/item about an unsupported central objective should pass merely because the concept is labeled standard. Canaries should exercise the entire generation path, including collisions with familiar names and false-standard classifications.

### 6. **Major — “LaTeX ingest” omits the source contract on which every later gate depends**

**Plan:** §4.2, ingest and mechanical sweep (`158–174`); Phase 1 (`436–441`).

**Problem:** arXiv source is an archive, not a clean string: multiple entrypoints, `input/include`, local macros, custom environments, equations inside macros, appendices and missing bibliography artifacts all occur. Definitions and symbols are scope-sensitive. An equation sweep cannot establish completeness if parsing silently loses equations. Figures and tables often carry the actual evidence; LaTeX captions alone are insufficient to interpret them.

The prototype only downloads PDFs and runs `pdftotext`, discarding page breaks (`frontier/sources.py:9–31`). It identifies non-arXiv files by basename and strips arXiv version identity (`14–25`), preventing reliable revision-aware provenance. Free-text evidence is not an addressable, validated span.

**Suggested change:** Implement a `DocumentRevision → Span` adapter first, preserving raw source and normalized text with a reversible location map. Support a bounded LaTeX subset with explicit unsupported-construct warnings; do not make a full TeX interpreter a prerequisite for learning whether extraction works. Add rendered-PDF page/region fallback, figure/table images and captions, equation labels, symbol definitions and bibliography links. Persist unresolved citations and parsing omissions visibly. Give ingest its own fixtures: multi-file source, custom macros, appendix algorithms, a PDF-only paper, an unreadable figure, and an unresolved reference. Require critical evidence to be accessible before assessing the extraction stage; do not treat missing parsed material as extraction success.

### 7. **Major — Multi-run union needs reconciliation, independence and error accounting**

**Plan:** §4.2, paper map, extraction, resolution and cap (`162–192`).

**Problem:** Union increases recall but also accumulates hallucinations and duplicate granularity. Agreement is correlated, especially when all extractors inherit the same paper map; a wrong map can make all families miss the same experimental requirement. Different calls’ local identifiers collide unless namespaced. Disposition and the 30–60 cap can erase the very recall improvement the ensemble bought. A long paper may genuinely need more than 60 distinct concepts; cardinality alone cannot prove a bad granularity prompt.

The retained merge implementation searches only the pre-ingest pool, not other new candidates (`frontier/merge.py:121–134`). It therefore cannot deduplicate even an empty-store first-paper union. Reusing it unchanged would create systematic within-batch duplicates.

**Suggested change:** Use complementary extraction passes: full-paper reader requirements, claim/evidence requirements, and equation/algorithm/**measurement** sweep. At least one pass should work directly from the paper without the generated map. Namespace candidates by `(run, pass, local_id)`. Preserve all raw outputs, reconcile within the union and then against the frozen registry, and keep separate evidence attachments for distinct passage uses. An unsupported singleton must be checked, not silently counted or automatically discarded. Track recall/precision after raw union, reconciliation, resolution and disposition to locate losses. Cap the default visible queue, not the persisted extraction set; flag very large sets for review. Ablate extra runs and families against a strong single-call baseline before committing to ensemble complexity.

### 8. **Major — The target exam shares the teaching map’s blind spots and is reused as an intervention**

**Plan:** §1 (`50–55`); §4.2, exam written against paper map (`165–166`, `193`); stopping rule (`232`).

**Problem:** A separate model call that reads the same generated map is not an independent coverage check. The map can omit a critical limitation and the exam then rewards exactly that omission. The plan also calls the exam “never used in teaching,” but gives some questions before instruction and repeats all questions after and weeks later. Pretesting and repeated retrieval are themselves learning interventions. Retesting the same exposed questions measures familiarity as well as durable transfer. Pass criteria, source access and grading conditions are unspecified.

**Suggested change:** Build a frozen assessment blueprint directly from the full source/evidence package, with no teaching map or practice outputs. Audit coverage of core claims, assumptions, evaluation and at least one new application. Freeze keys, rubrics and the pass rule with it. Reserve unseen matched transfer questions for the delayed endpoint; report repeated anchors separately. State whether tests are closed-book/unassisted or source-open, and log that condition. Blind graders to intervention and test occasion. Once an exam answer is exposed for feedback, do not count its later repetition as untouched held-out evidence. No need to withhold useful feedback permanently: use a fresh endpoint form.

### 9. **Major — κ and defect sensitivity are not sufficient automation criteria**

**Plan:** §5 (`332–341`); §6 (`369–381`); Phase 2 (`455–458`).

**Problem:** κ ≥ 0.6 on 30–50 owner labels is an initial agreement signal, not validation of every rubric. It is prevalence-sensitive and uncertain at that sample size. Full/partial/none requires an explicit nominal or weighted convention. Several key-point labels on one answer are clustered, not independent answers. A judge can achieve ≥90% injected-defect detection by rejecting every output; a canary system can achieve zero confident errors by refusing everything. Cross-family judging reduces one bias but does not establish independent correctness, particularly when the extractor already uses all three families.

**Suggested change:** Keep κ as a diagnostic alongside confusion matrices, class counts, paper/artifact-clustered uncertainty and the consequential errors: false full credit, false-known inference, false merge and false approval of wrong content. Report abstention coverage and accepted-output defect rate. Pair every defect class with clean, owner-confirmed controls; measure clean rejection as well as sensitivity. Separate natural-production and balanced challenge results. Calibrate family/role assignments empirically, blind judges to the producer, and require fresh evidence-based reasoning—not inherited rationales. Revalidate when the judge or rubric changes. A provisional human-confirmed mode is a better response to sparse labels than pretending a threshold proves reliability.

### 10. **Major — The label budget and active-selection policy miss shared confident errors**

**Plan:** §5 (`356–357`); §6, gold and live labels (`361–371`); Phase 0/owner decisions (`427–434`, `478–479`).

**Problem:** Three hours covers paper lists, not 30–50 labels per criterion across roughly ten decision types, 100 item reviews, 50 answer grades, canary truth and merge-pair labels. Some criteria cannot honestly be checked in a minute: necessity, theorem validity and application-key correctness require context. “Only cases where judges disagree” misses unanimous hallucinations. Disputes are valuable but selection-biased; a low dispute rate is not a low grading-error rate.

**Suggested change:** Budget owner effort explicitly by phase and prioritize three instruments first: requirement matching, false-merge decisions and high-impact content/item correctness. Reuse a small set of artifacts across criteria when appropriate, without treating their labels as independent samples. Reserve a recurring random audit of unanimous accepted outputs; use the rest of the budget for disagreement/active selection. Blind the owner to judge decisions, and repeat-label a small delayed sample to estimate their own consistency. Keep random, active and dispute samples separate in metrics. “Needs human” should mean queued/unresolved until reviewed, not silently accepted or silently dropped.

### 11. **Major — Regression and canary exit criteria need locked data, denominators and useful coverage**

**Plan:** §4.6 (`291–294`); §6 (`373–381`); Phase 0/1 (`431–448`).

**Problem:** Repeatedly selecting prompts on all 8–15 papers turns the acceptance set into development data. Three runs of the same papers estimate sampling variation, not generalization to independent papers. A reused canary template can be recognized without robust novelty handling. “Confident-error rate ≈0” has no executable denominator, and no distinction between a small sentinel suite and a real-world risk estimate.

**Suggested change:** Split by paper before tuning: development cases, a small locked acceptance set and prospective new-paper cases. Freeze source, parser, registry and learner-state snapshots; a warm concept store must not advantage only the new system. Have fixed regression canaries plus fresh generated/owner-checked variants, including familiar-name collisions, altered signs/conditions, missing definitions, unresolved citations and unchanged standard controls. Count claim-level wrong assertions among answered claims and useful-answer/abstention coverage, including errors following an “I’m unsure” preamble. State counts and confidence bounds. With zero errors in 30 independent cases, a one-sided 95% binomial upper bound is still about 9.5%; about 300 independent zero-error cases put it near 1%. Repeats of the same canary do not supply 300 independent cases. Small suites are valuable smoke gates, not a near-zero error guarantee.

### 12. **Major — Resolution needs retrieval evaluation and conservative identity semantics**

**Plan:** §4.2, matching and reuse metric (`175–181`); §5, concept-match rubric (`348`); §7, drift warning (`417`).

**Problem:** A good adjudicator cannot match a concept absent from its retrieved candidate set. Similarity favors same-topic hard negatives and misses cross-name synonyms. “Same / specializes / homonym / new” omits broader/generalizes, related-but-distinct, overlap and uncertain. Pairwise same-decisions can be non-transitive: A≈B and B≈C does not make A and C equivalent at the same scope. A rising resolution fraction can mean better reuse **or aggressive over-merging**; a genuinely novel paper should not be penalized for adding concepts.

**Suggested change:** Build a small labeled retrieval-and-resolution suite with synonyms, acronym collisions, assumptions, formal/informal versions and overlapping scopes. Measure candidate recall@k separately from adjudication accuracy. Retrieve over definitions, aliases, local sense and source context, with an expanded second pass for uncertain/new cases. Store directional relation decisions explicitly, include abstention, and do not merge until scope and objective compatibility are checked against the whole destination concept—not only one pair. Version embeddings and rebuild retrieval indexes when models change. Start with owner-approved borderline merges; prioritize avoiding false merges over eliminating every duplicate. Report false merges and duplicate fragmentation alongside reuse rate, and freeze insertion order/snapshot for comparative evaluation.

### 13. **Major — Hard prerequisite edges are context- and depth-dependent, not universal concept facts**

**Plan:** §4.2 (`182–189`); §4.3, inferred-known ancestors (`207–209`); §4.4, readiness (`215–217`); §5 (`349`).

**Problem:** “Could a competent learner understand B without A?” is ambiguous without depth, task and allowed resources. Understanding the intuition behind influence functions need not require deriving the implicit function theorem. A verifier seeing only definitions cannot assess the particular paper’s required capability. Two calls can agree on the same curricular convention without it being a hard necessity. Alternative routes create OR-dependencies that a flat list of parents treats as AND. Cycles can also reflect inconsistent depths or mutual helpfulness rather than true gating.

A correct answer on B does not establish every prerequisite at every facet/depth: the item may not exercise them, may be scaffolded or may be guessable. This makes top-down inference a high-impact false-known path.

**Suggested change:** Represent prerequisite rules over objectives with required depths, scope and evidence. Require a concrete blocked task/counterexample, allow `helps`, `uncertain` and alternative routes, and validate the hard-edge DAG with explicit cycle review. Keep definitions-only review as a bias check, not the final source of truth. Default to soft ordering for Phase 1; add hard gates only for demonstrated blocking dependencies, with user override. Infer weak known evidence only for objectives the specific item/key points necessarily exercise, and spot-check it. Do not turn the universal graph’s transitive closure into mastery.

### 14. **Major — Item validation lacks independent key/rubric validation and permits consensus on a shared mistake**

**Plan:** §4.1, item spec (`120–124`); §4.5 (`256–270`); §5, item rubric (`353`).

**Problem:** Blind solving helps, but matching the generator’s key is not sufficient. Both solvers can reproduce a paper’s ambiguous convention or omit the same condition. Seeing the source spans tests source-open answerability, not whether the eventual learner prompt is self-contained. Two solvers agreeing demonstrates consistency, not “exactly one defensible answer.” Choose/apply/extend questions often have multiple valid answers under stated tradeoffs. Grading against an incomplete key can reject a correct alternative even if every solver agreed on another answer.

**Suggested change:** Make the item spec include operational objective, allowed resources, assumptions, difficulty tier, answer budget and evidence links. Produce a **versioned rubric with the item**, then independently check each key point for correctness, necessity, allowed equivalents and objective tagging. Blind solvers must not see the answer key or each other’s reasoning. Add an adversarial alternative-solution search and an explicit ambiguity/insufficient-information outcome. For research tasks, require a bounded acceptable-answer space, not one string or one opinion. Use executable toy calculations/tests for signs, equations and small code tasks where possible. Log all rejected candidates and regeneration attempts, bound retries, and owner-audit accepted items so selection does not merely overfit a permissive checker.

### 15. **Major — Grading, diagnosis and evidence application need different contracts**

**Plan:** §4.1, evidence weighting and blame (`138–149`); §4.5, grading (`262–270`); Phase 2 (`451–458`).

**Problem:** A grader can quote a correct phrase while ignoring a contradiction elsewhere in the answer. Conversely, the “must not say” list may penalize the learner for quoting a misconception in order to refute it. An absent key point does not identify the causal gap: it may be a terse answer, a broken item, a slip or an alternate solution. The plan’s single diagnosed concept invites overconfident blame. Repeated grading needs an aggregation/abstention policy; “grade several times” leaves tie handling and false-full-credit behavior undefined.

**Suggested change:** Separate: (1) semantic per-point evaluation; (2) global contradiction/misconception check in context; (3) optional diagnosis; (4) deterministic evidence update. Validate answer quotes as exact offsets, but do not mistake quote validity for semantic correctness. Constrain diagnosis to tagged objectives/direct tested prerequisites plus `slip`, `item_defect`, `alternative_valid` and `undetermined`. Uncertain diagnosis should trigger a follow-up probe, not a penalty elsewhere. Define full/partial/none aggregation, veto/abstention rules and owner override semantics. Until resolution, uncertain/disputed grades do not create strong mastery or memory updates. Test fluent near-misses, terse answers, negated misconceptions, contradictions, synonymous notation and off-key correct alternatives.

### 16. **Major — The acquisition/memory model is over-specified relative to the available data**

**Plan:** §4.1 (`133–149`); §4.7 (`298–308`); Phase 4 (`468–470`).

**Problem:** One user answering mostly new variants cannot reliably disentangle per-item difficulty, skill acquisition, forgetting and grading noise. Elo ability and item difficulty trade off; an immediate worked-example application is not the same memory observation as an unassisted delayed recall. Ordinary FSRS consumes a defined review history and rating scale, not arbitrary “fractional reviews” through a noisy graph. A concept-level state with variable objectives can lengthen intervals after success on an easy variant and then mistake a harder variant for forgetting.

**Suggested change:** Keep acquisition evidence and memory evidence separate. Begin with fixed difficulty tiers, conservative explicit known/uncertain objective states, and stable anchor retrieval items for scheduling. Only unassisted, resource-appropriate attempts feed the anchor’s FSRS history; log open-book, hints, recent explanation and elapsed time explicitly. Store application performance separately. Disable automatic `encompasses` memory credit initially, or run it only in shadow predictions against a no-propagation baseline. Do not fit both arbitrary item difficulty and ability from sparse single-user data. Add fractional updates only after specifying the algorithm, rating mapping and predictive/delayed-retention tests.

### 17. **Major — Phase 1 is too broad, while feedback and safe state foundations arrive too late**

**Plan:** phase ordering (`424–425`); Phase 1 (`436–448`); Phases 2/3 (`450–466`).

**Problem:** The first implementation bundles LaTeX, bibliography resolution, literature retrieval, ensemble extraction, global entity resolution, graph verification, disposition and an exam. Many are not needed to answer the first product question: does this identify and resolve the learner’s actual reading blockers better than a reading guide? It risks spending weeks validating a global graph before seeing a real stuck point. Conversely, full call artifacts, minimal learner events and source identities are prerequisites for Phase 0/2 experiments, yet the phase list delays parts of them. The strict “no phase starts” rule can deadlock on noisy statistical gates.

**Suggested change:** Split Phase 1 into **1a: grounded per-paper requirements + baseline + stuck-point report** and **1b: conservative cross-paper resolution on 2–3 related papers**. Permit PDF input with honest coverage warnings before broad LaTeX support. Add a minimal span-linked “stuck/irrelevant/wrong” capture surface immediately; no full reading app is required. Move call/artifact records to Phase 0 and evidence envelopes before Phase 2. Defer graph visualization, automatic splitting, universal hard edges, `encompasses` weights and a full domain-plugin framework. Treat early gates as specified operational smoke tests with human-confirmed fallbacks, not proof of learning efficacy. Appendix D proposes executable exits.

### 18. **Major — The retained runtime needs resumable artifacts and fail-closed semantic validation**

**Plan:** §3, retained infrastructure (`75–79`); §4.2 (`156`); §5/6, pinned versions and logs (`340–341`, `403–405`).

**Problem:** “Steps 0, 3, 5 and 6 are code” conflicts with their own descriptions: resolution uses a model, the target exam is a call, and central full-text fetching depends on extraction. This is a dependency graph, not a single linear transaction. New citation or validation failures should not require repeating successful expensive stages or partially mutating the registry.

The prototype already detects output truncation and validates JSON shape (`frontier/llm.py:53–79`), so these are **not absent**. However, it has no bounded semantic-repair policy, input token budgeting or full artifact cache. A syntactically valid missing review verdict defaults to keep (`review.py:74–87`), and a missing merge decision defaults to new (`merge.py:143–156`). Cost logs omit full inputs/outputs, actual response identity, prompt/schema hashes and retry lineage (`llm.py:93–115`). Logging commits on the same connection (`108–115`), which can commit unintended mutations on failure paths; the standalone recluster command is one such existing path (`cli.py:79–86`, `cluster.py:78–88`).

**Suggested change:** Use a small persisted stage/artifact DAG with immutable inputs and hashes, bounded retries, explicit failed/partial/unknown states, and idempotent application transactions. Preflight input context and provider output limits; use section-local passes plus global reconciliation for long papers. Validate exact decision coverage, unique keys, valid span/ID references, action-dependent fields and allowed enums in code; missing judgments fail closed. Log attempts durably outside graph-mutation transactions, including failures, finish status, requested/served model metadata when available, routing/provider, reasoning settings and schema/prompt versions. Do not promise exact reproducibility from a floating model alias: detect drift with sentinels and rerun acceptance cases. Precompute item checks; keep multi-judge generation off the interactive path.

### 19. **Major — Citation resolution and literature context need explicit uncertainty and authority rules**

**Plan:** §4.2, ingest and paper map (`158–166`); §4.6, from-citation/unknown (`274–294`).

**Problem:** Citation resolution can select the wrong version or a similarly titled paper; dates are not defining-source evidence. Fetching every abstract and “anything central” lacks a centrality dependency, recursion bound and degraded mode. The target paper’s bibliography does not contain later replications or critiques, so “place in its literature, retrieved rather than recalled” also needs a separate retrieval policy. A span-faithful summary can still present an author’s speculative explanation as established truth. The mentor report explicitly warns against this (`expert-research-mentor.md:192–193`).

**Suggested change:** Persist citation occurrences separately from bibliographic entities and fetched revisions. Prefer exact DOI/arXiv IDs; use title/authors/year matching with candidates, confidence and `unresolved/ambiguous` outcomes. Distinguish metadata-only, abstract-only and full-text grounding. Fetch full text on demand for central unresolved objectives with a bounded one-hop expansion, then escalate rather than invent. For “what happened later,” use a dated, bounded literature-retrieval task and cite the retrieved evidence; say when it was not searched or not found. Represent assertions as `paper_claim`, `reported_observation`, `derivation`, `external_background` or `hypothesis`, with assumptions and supports/contradicts links. Preserve disagreement rather than forcing all sources into one canonical truth.

### 20. **Major — The n=1 outcome checks can pass without an instructional benefit**

**Plan:** §6, holdouts and alternate papers (`396–401`); Phase 3 exit (`463–466`); Phase 4 (`468–470`).

**Problem:** Holding out a concept’s lesson does not withhold the concept: downstream explanations, glosses, multi-concept items, exams and the paper itself can teach it. With only 3–8 real gaps, a 20% holdout is about one control per paper. Alternating papers confounds intervention with difficulty, prior knowledge and order. Faster paper 3 can reflect ordinary domain learning or a simpler paper, even if the registry adds no value. Replay evaluates predictions on observed responses, not the counterfactual responses a different teaching policy would have produced.

**Suggested change:** Define the estimand as the incremental value of offering explicit teaching beyond supported reading. Randomize separable concept bundles where possible, pre-map outcome items, and log incidental exposure, rescue teaching and overrides; analyze assignment rather than pretending exposure was absent. For tool/chat comparisons, preselect comparable papers and target depths, randomize order within blocks, record pretest/familiarity, and specify a worthwhile time/score difference. Include triage, annotation, disputes and mandatory tests in learner-time accounting; distinguish one-off setup from recurring cost. A 3–4-paper run is a usability/feasibility pilot, not a causal superiority test. Falling time only passes with maintained competence. Compare learner predictors chronologically on later observed answers with log loss/Brier score; evaluate policy changes prospectively, not by replay alone. Give Phase 4 an explicit operational exit and a separate delayed-retention checkpoint.

### 21. **Major — Preserving the prototype needs a schema migration and provenance-retention decision**

**Plan:** §3 (`73–91`); §4.1 (`125–132`); §9, rework in place (`483–484`).

**Problem:** The redesign does not make old bugs or wrong facts disappear. Current `fact_sources` holds one evidence string per fact/source, and same-source duplicate attachment updates importance/role without retaining additional evidence (`frontier/merge.py:159–165`). Repeated support for an existing edge is dropped (`178–180`). The schema has no real migration/version mechanism or concept-lifecycle events (`frontier/db.py:7–57`, `97–104`). Automatically promoting old untyped edges to verified `requires` or old background claims to trusted definitions imports the known errors.

**Suggested change:** Keep the current pool read-only as legacy input; start new concept/objective tables with explicit schema migrations. Reuse the client, retrieval helpers and report machinery, not their trust assumptions. Import useful old facts as unverified claim seeds with legacy IDs, reviewed mappings and all available provenance. Use many-to-many support/assertion rows so additional spans, contradictory sources and repeated edge evidence are never overwritten. Add migration, merge/undo and replay fixtures before ingesting live learner evidence. This does not require a new application or a sophisticated graph database.

### 22. **Major — Source and answer text need a trust boundary, especially with LaTeX and linked code**

**Plan:** §4.2, sources/citations/repository discovery (`158–161`); §4.5, items/grading (`256–270`); §6, full input/output logging (`403–405`).

**Problem:** Papers, repository READMEs, citation responses and learner answers are untrusted data, not instructions to pipeline agents. A source can tell a model to ignore the rubric or fabricate a supporting citation. Moving to source archives introduces filesystem and compilation hazards; “use the code repo” must not quietly mean execute downloaded code. The single-user context reduces malicious learner incentives, not risks from fetched material or accidental instruction-like content. Full logs may also contain unpublished research or private code.

**Suggested change:** Delimit source/answer data and explicitly instruct models not to follow embedded directives; enforce tool/retrieval permissions outside prompts. Give extraction/judge calls no mutation capability. Resolve source IDs against a code-owned allowlist and verify quoted spans. Extract each archive into a fresh bounded directory, reject traversal/symlink escapes, never enable shell escape, and sandbox any optional rendering; prefer static parsing. Treat linked code as immutable text at a commit hash unless the owner separately approves sandboxed execution. Add a few injected-document/answer fixtures. Keep logs local by default and make provider data handling, secret redaction and retention explicit before sending private material.

### 23. **Minor — Disposition and requirement lifecycle need independent fields and a user escape hatch**

**Plan:** §4.1, requirement (`115–119`); §4.2, disposition (`190–192`); §4.8 (`323`).

**Problem:** Teach/gloss/ignore currently mixes durable requirement metadata with a planner decision. A one-off paper-local procedure can deserve an active lesson because it blocks reproduction, even if it is not worth maintaining. A reusable standard concept may deserve no teaching because it is known. A new concept cannot have observed reuse across goals yet. Candidate/confirmed/dismissed/satisfied states from the supporting report disappear from the concrete plan.

**Suggested change:** Keep `necessity/centrality`, `review_status`, `required_objective`, `learner_gap`, current `delivery_mode` and `retention_policy` separate. Compute delivery after diagnosis and allow owner overrides; never let “not reusable” imply “not worth teaching now.” Preserve the requirement and its evidence even when its current delivery is ignore/gloss. Emit an explicit ignored-requirements report so missed depth can be corrected.

### 24. **Minor — Generative examples need a source relation richer than sentence citations**

**Plan:** §4.5, explanation sentences span-tagged or background (`247–255`); §5, explanation rubric (`352`).

**Problem:** A useful new numeric example, counterfactual or analogy is not literally stated in the paper. A rigid entailment-only checker either rejects it or launders it through a broad background tag. Conversely, a sentence containing several claims can cite one span that supports only one clause. Paper notation can also conflict with a global concept’s notation.

**Suggested change:** Validate at claim/key-point granularity with evidence relations such as `quoted/paraphrased`, `derived`, `illustrative_assumption` and `analogy`. Derived claims cite premises and an optional executable check; examples declare their synthetic assumptions; analogies remain explicitly nonliteral and bounded. Keep a local notation/symbol map per document section. This supports useful teaching without pretending every generated example is a quoted research result.

## Appendix A — Minimal Phase 0/1 schema contract

This is a proposed contract, not a request for a large framework. SQLite tables plus Pydantic discriminated schemas are enough. Start with sources, requirements, artifacts and judgments; add learner-specific records when Phase 2 begins.

```text
Source(
  source_id, kind, canonical_identifiers
)
DocumentRevision(
  revision_id, source_id, external_version, content_hash,
  publication_date, retrieved_at, retrieval_status, raw_blob_ref,
  parser_version, coverage_warnings
)
Span(
  span_id, revision_id, kind, section_path,
  original_locator, normalized_text, text_hash, render_locator
)
Assertion(
  assertion_id, scope, statement, assertion_kind, assumptions,
  evidence_links[{span_id, relation, quote_offsets}], validation_status
)
Concept(
  concept_id, type, sense_scope, lifecycle_status
)
ConceptRevision(
  concept_revision_id, concept_id, definition, aliases,
  defining_assertion_ids, notation_scope, valid_from_event
)
Objective(
  objective_id, concept_id, capability, optional_facet,
  operational_success_criterion, conditions
)
Requirement(
  requirement_id, goal_id, objective_id, served_span_ids,
  necessity, centrality, review_status, extraction_candidate_ids
)
ResolutionDecision(
  decision_id, candidate_ids, registry_snapshot,
  proposed_target, directional_relation, evidence, status
)
PrerequisiteRule(
  rule_id, target_objective_id, prerequisite_alternatives,
  scope, hard_or_soft, evidence, verification_status, graph_revision
)
```

Important constraints:

- Source identity is not document revision identity. Use explicit arXiv versions/DOIs plus content hashes; a local basename is not a unique source ID.
- Span IDs are immutable within a revision; source path/offset plus occurrence identity must distinguish repeated identical text. Cross-revision alignment is a separate mapping, not assumed ID stability.
- Store many-to-many evidence attachments. A concept’s definition, a paper’s use of it and an edge’s support are different records.
- Extraction candidates are not yet canonical concepts. Their local IDs and all originating runs survive reconciliation.
- Store origin/provenance per occurrence; grounding validation per assertion/artifact; model familiarity per model/probe. Do not compress all three into one concept badge.
- Do not fill four depth definitions merely to satisfy a schema. Create objectives the goal needs, with anchored success criteria.

Before the first probe, add:

```text
ItemVersion(
  item_version_id, spec_version, stem, allowed_resources, response_modality,
  assumptions, answer_budget, rubric_version,
  key_points[{point_id, criterion, accepted_equivalents, objective_tags}],
  misconception_rules, grounding_assertion_ids, validation_artifact_ids
)
Event(
  event_id, event_type, occurred_at, recorded_at, session_id,
  causation_id, supersedes_event_id, immutable_payload
)
```

The payload for an attempt links the exact presented item, objective tags, graph/learner-projection versions, pre-answer prediction, permitted resources/hints, raw answer and timing. Grade events link exact rubric/grader versions. Attribution revisions and dispute resolutions append new events; they do not erase the original attempt. Minimal deterministic reducers are preferable to implementing a general event-bus system.

For every model stage, from Phase 0:

```text
Artifact(
  artifact_id, stage, input_artifact_ids, source_snapshot, registry_snapshot,
  schema_version, prompt_hash, requested_model, served_metadata,
  generation_parameters, run_id, attempt_id, raw_input_ref, raw_output_ref,
  parse_status, semantic_validation_status, outcome, error, usage
)
```

`served_metadata` may be incomplete; record that fact. Hashes and snapshots make changes inspectable, not a guarantee that a hosted model is bitwise reproducible.

## Appendix B — Scoring recall when names differ

### Gold annotation

For each owner entry, record a capability, not just a label. For example:

```json
{
  "gold_id": "p1-g07",
  "label": "EM operational measurement",
  "sense": "the target paper's evaluation protocol, not generic misalignment",
  "capability": "explain how the alignment/coherency judge scores and thresholds define an EM outcome",
  "minimum_depth": "explain",
  "served_spans": ["p1-r1-eval-03"],
  "importance": "core",
  "aliases": ["misalignment metric", "EM judge protocol"],
  "required_elements": ["score meanings", "threshold decision rule"],
  "acceptable_decompositions": [["judge scores", "threshold rule"]]
}
```

These are annotation categories, not a new fact claim about every EM paper. The actual thresholds and score meanings must be taken from the particular source revision.

### Matching procedure

1. **Freeze input snapshots.** Run both systems on identical source revisions, declared learner scope and cold/warm registry conditions. Save every raw output. For the new-paper stuck-point audit, obtain stuck points before showing either output.
2. **Normalize without collapsing senses.** Normalize notation, aliases and lexical variants; retrieve possible gold–prediction pairs using both lexical and embedding search. On a few dozen entries, an exhaustive fallback is affordable. Retrieval cannot be the unmeasured ceiling on recall.
3. **Adjudicate coverage, not similarity.** A calibrated, producer-blind matcher receives the gold capability, predicted requirement/definition, served passages and depth criteria. It returns `equivalent`, `covers_part`, `broader_but_not_explicit`, `different_sense`, `unrelated` or `uncertain`, with the exact supported elements and evidence. Owner-review uncertain/boundary matches and audit a random subset of accepted ones. Use independent matcher-calibration examples, not the acceptance papers, to tune this rubric.
4. **Aggregate required elements.** A gold requirement is fully covered only if the extracted requirements explicitly cover all required elements at the needed depth and correct sense. Several narrow predictions may jointly cover one gold entry. One broad name gets no blanket credit; one genuinely composite prediction can cover several entries only through explicit supported subcomponents. Duplicates never increase recall. Report partial coverage separately rather than silently rounding it up.
5. **Compute recall.** `macro_recall = mean_papers(fully_covered_gold / eligible_gold)`. Also report importance-weighted recall, depth-correct recall, core misses and post-disposition coverage. Track stuck-point coverage as its own observed-needs metric; it is not an exhaustive recall denominator.
6. **Compute precision on adjudicated predictions.** Judge unmatched predictions for necessity/relevance from the actual paper; absence from a quick owner list is not sufficient for a false positive. Report `unknown/unreviewed` separately and count unsupported claims explicitly. Deduplicate semantic requirements for quality precision, while also reporting raw candidates, duplicates and owner triage minutes so over-fragmentation is not free.
7. **Separate learner utility.** Report the subset actually unknown to the owner, and whether the associated content would unblock the marked passage. “Necessary but already known” remains a correct requirement and an unnecessary lesson. Define top-5 priority recall as `|owner_top3 ∩ system_top5| / 3` using the same semantic matching, not string overlap.

Keep gold amendments versioned. A valid novel prediction can improve the reference set, but first preserve its original acceptance score; do not retroactively tune a test without recording the change.

## Appendix C — Prompt and validation boundaries for Phase 1

Use small, versioned prompts with separate instructions, trusted task configuration and explicitly untrusted source blocks. Do not ask one agent to extract, reconcile, classify truth and mutate the store.

1. **Ingest inventory:** code supplies valid span IDs, equation/algorithm/table/figure inventories, parser omissions and citation status. No model may invent source identifiers.
2. **Independent map/extraction passes:** one map pass produces claim–evidence structure. Separate extraction passes each return candidates with `local_id`, sense/definition, operational required capability, served spans, evidence quotes, necessity, centrality, origin hints and explicit `uncertain`. Include anchor examples of over-coarse, over-fine, relevant-known, experimental-protocol and implicit requirements. Do not let the profile silently suppress known-but-required concepts; prune teaching later.
3. **Set reconciliation:** operate on the preserved union, joining equivalent candidates and their evidence without increasing asserted depth. Return a mapping of every candidate, including unresolved ones. Check cardinality and referential integrity in code.
4. **Resolution:** supply retrieved concept revisions, scope/definition and relevant objectives. Ask for directional relation plus a short evidence-based explanation and uncertainty. The call proposes; deterministic code validates and applies approved decisions. No candidate means `not retrieved/new/uncertain`, not proof of novelty.
5. **Grounding review:** check each technical assertion, its assumptions and source relation. Output `supported`, `contradicted`, `not_enough_evidence` or `not_applicable`. Code enforces the permitted uses. Quote existence is a separate check from entailment.
6. **Exam generation:** full frozen paper evidence and a goal-depth blueprint, but no generated teaching map or practice items. Keys/rubrics get their own validation before use.

Across calls: require exact ID coverage where applicable, bounded lists rather than silently clipped output, abstention fields, schema and semantic validation, and an explicit error/partial artifact when context or retrieval is inadequate. Blind validators to previous verdicts and producer identity where possible. Cross-family roles are useful but must be evaluated; family diversity is not an accuracy proof.

## Appendix D — Smaller phase slices and executable exits

These are proposed initial operational rules, **not statistically established efficacy thresholds**. Pre-register sample counts and confidence reporting before running them.

### Phase 0: make the measurement executable

- Choose roughly 8–10 owner-familiar papers, allocating development and locked acceptance papers in advance; retain the new-paper stuck-point audit as a distinct prospective case.
- Implement immutable source/artifact records and the semantic matcher. Validate it on a small synonym/sense/decomposition challenge set before using its scores to accept extraction changes.
- Prepare clean/defective artifact pairs and diverse canaries, with owner-confirmed labels and explicit denominator/abstention rules.
- Define the one-shot reading-guide baseline, target-depth assumptions and learner-time accounting.
- **Exit:** both systems can be scored from saved artifacts; owners can inspect every match and critical miss; frozen acceptance inputs and scoring rules exist. This is the right first build.

### Phase 1a: requirements that actually help a reading

- Parse a bounded source set; produce a span-linked map, reconciled requirements, grounding states and explicit unresolved needs. Add simple triage/stuck-point capture.
- No automatic global hard-edge inference, historical retagging or fractional review credit.
- **Exit:** use the plan's recall ≥0.8 and precision ≥0.5 as provisional **per-paper-macro** smoke gates under Appendix B; require separate review of every core miss/unsupported core assertion, report uncertainty, and beat the one-shot guide on the same acceptance inputs. Canary suite: no ungrounded factual assertions accepted, with clean-control rejection and useful coverage also reported. An unsupported core claim blocks its teaching path, not the entire exploratory application.

### Phase 1b: demonstrate safe cross-paper reuse

- Ingest 2–3 related papers with conservative resolution and explicit many-to-many provenance. Test ordering sensitivity, duplicate candidates, false friends, false merges and missing retrieval candidates.
- **Exit:** owner-reviewed high-impact merges, no unexplained evidence loss, reproducible registry diffs and tested undo; measured retrieval and adjudication errors reported separately. Do not require an arbitrary high existing-concept fraction on genuinely new material.

### Phase 2: limited diagnosis and validated practice

- Start with short explanation/application items and a small owner-audited bank, minimal pre-answer prediction/events, rubric grading and disputes. Use soft ordering and conservative objective state.
- **Exit:** retain the <10% accepted-item defect and κ ≥0.6 figures only as provisional calibration targets on declared samples. Also require false-full-credit reporting, clean-control pass rates, abstention handling, random accepted-output audits and no strong state updates from unresolved grades. Diagnostic removal must pass a random false-known audit, not merely remove 60% of candidates quickly.

### Phase 3/4: real use, then retention

- Run 3–4 live papers to identify overhead, content errors and whether paper understanding reaches a specified floor. Do not claim superiority from that pilot alone.
- For later comparisons, use prospective matched/randomized paper blocks and novel delayed transfer endpoints. Do not accept lower time at lower competence.
- Add anchor-based retention first. **Phase 4 operational exit:** bounded review queue, tested budget/archival behavior, reproducible evidence replay and no unsupported implicit-credit updates; **later evidence checkpoint:** delayed performance and calibration against a no-implicit-credit baseline.

## Bottom line

The plan should not be discarded. Its strongest idea is a paper-grounded assistant with a reusable, inspectable knowledge layer—not an autonomous universal tutor. First prove that the requirements report identifies real blockers and that the measurements mean what they claim. Then prove that resolving a second paper into the store preserves meanings and evidence. Everything involving mastery propagation, historical reinterpretation or long-term scheduling should be deliberately conservative until those foundations are demonstrated.
