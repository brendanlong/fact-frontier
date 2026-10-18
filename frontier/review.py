from typing import Literal

from pydantic import BaseModel

from frontier.extract import Candidate, Kind
from frontier.llm import LLM

Problem = Literal["multiple_claims", "paper_detail", "missing_context"]


class Replacement(BaseModel):
    statement: str
    kind: Kind


class Verdict(BaseModel):
    key: str
    verdict: Literal["keep", "rewrite", "split", "drop"]
    problems: list[Problem]
    replacements: list[Replacement]
    reason: str


class Verdicts(BaseModel):
    verdicts: list[Verdict]


SYSTEM = """\
You review facts before they join a learner's long-lived study pool. Each fact will be taught \
and then quizzed for months, long after the learner has forgotten the paper it came from. You \
see each fact as the learner will: without the paper. You get only the paper's title and \
opening, and the passage each fact was drawn from.

Check every fact against three rules:
- multiple_claims: a fact states one claim that one short question could test. A definition \
plus its properties, or claims joined by "and", ";" or a second sentence, are several facts.
- paper_detail: a fact must be worth knowing beyond reading this paper. Hyperparameters, \
figure-specific setups, implementation minutiae and notation choices fail. A paper's findings, \
methods and the reasons they work pass, even when only this paper shows them: they are what \
the learner is here for. If a fact is a finding with an exact number attached, rewrite it \
without the number rather than dropping it. This rule should rarely fire; when unsure, it \
passes.
- missing_context: a fact must make sense alone. Undefined symbols (θs, z_m, λ), "the \
method", "this approach" or unexplained paper-specific names fail.

Verdicts:
- keep: passes all rules. No replacements.
- rewrite: one fact, fixed. One replacement.
- split: several claims. One replacement per claim, each passing all rules; drop any piece that \
would fail paper_detail.
- drop: fails paper_detail and has nothing worth keeping. No replacements.

When rewriting, use only what the fact, its source passage and the paper opening say; do not \
add claims of your own. Spell out symbols in words. Keep rewrites as short as the claim allows.

List every problem you found in problems, even when the verdict fixes it. reason: one short \
sentence. Return exactly one verdict per fact key."""


OPENING_CHARS = 3000


def review(
    llm: LLM, model: str, title: str, text: str, candidates: list[Candidate]
) -> dict[str, Verdict]:
    opening = text[:OPENING_CHARS]
    facts = "\n\n".join(
        f"<fact key={c.key!r} kind={c.kind!r}>\n{c.statement}\n"
        f"<source_passage>{c.evidence}</source_passage>\n</fact>"
        for c in candidates
    )
    user = f"<paper title={title!r}>\n{opening}\n</paper>\n\n{facts}"
    result = llm.structured("review", model, Verdicts, SYSTEM, user, effort="low")
    return {v.key: v for v in result.verdicts}


def apply(candidates: list[Candidate], verdicts: dict[str, Verdict]) -> list[Candidate]:
    """Replace reviewed candidates by their fixed versions. Split pieces inherit the original's
    prerequisites, and anything that needed the original needs every piece. A dropped fact's
    dependents inherit its prerequisites, so dropping never disconnects the graph."""
    pieces: dict[str, list[str]] = {}
    out: list[Candidate] = []
    for c in candidates:
        v = verdicts.get(c.key)
        if v is None or v.verdict == "keep" or (v.verdict != "drop" and not v.replacements):
            pieces[c.key] = [c.key]
            out.append(c.model_copy())
            continue
        reps = [] if v.verdict == "drop" else v.replacements
        keys = [c.key] if len(reps) == 1 else [f"{c.key}.{i}" for i in range(len(reps))]
        pieces[c.key] = keys
        for key, r in zip(keys, reps, strict=True):
            out.append(c.model_copy(update={"key": key, "statement": r.statement, "kind": r.kind}))

    original = {c.key: c for c in candidates}

    def resolve(key: str, seen: frozenset[str] = frozenset()) -> list[str]:
        if pieces[key] or key in seen:
            return pieces[key]
        return [k for p in original[key].prerequisites for k in resolve(p, seen | {key})]

    for c in out:
        c.prerequisites = list(
            dict.fromkeys(k for p in c.prerequisites for k in resolve(p) if k != c.key)
        )
    return out
