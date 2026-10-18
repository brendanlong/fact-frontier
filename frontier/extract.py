from typing import Literal

from pydantic import BaseModel, Field

from frontier.llm import LLM

Kind = Literal["definition", "mechanism", "property", "when_to_use", "method", "result"]
Role = Literal["prerequisite", "contribution"]


class Candidate(BaseModel):
    key: str = Field(description="Short local ID, unique within this response, e.g. 'f12'.")
    statement: str
    kind: Kind
    role: Role
    importance: int = Field(description="1 = peripheral, 2 = useful, 3 = essential")
    prerequisites: list[str] = Field(description="Keys of other facts in this response.")
    evidence: str = Field(
        description="Where this comes from: a short quote or section reference for "
        "contributions; for prerequisites, the passage that relies on it."
    )


class Extraction(BaseModel):
    title: str
    facts: list[Candidate]


SYSTEM = """\
You build the knowledge a specific learner needs in order to understand a paper, as a set of \
atomic facts. The facts join a long-lived pool that grows as the learner reads more, and each \
fact will be taught with a short explanation and then practiced with varied questions over \
months. Your output decides what the learner spends that time on.

What to extract:
- prerequisite: background the paper uses but does not teach. This is the most valuable part: \
papers skip exactly the things a reader is missing. Go as deep as this learner needs and no \
deeper. Stop at facts the learner profile says they already know solidly; do not stop at facts \
that are merely "standard" in the field.
- contribution: what the paper itself establishes — its methods, the key ideas that make them \
work, and its main results.

What makes a good fact:
- Atomic: one claim, which one short question could test — usually a single sentence of under \
about 35 words. A fact with several sentences, or with "and"/"also" joining independent claims, \
is several facts: split it, and link the pieces with prerequisites where one builds on another. \
A definition plus its properties is a definition fact and separate property facts.
- Standalone: readable months later with no paper at hand. Never write "this paper", "the \
authors", "our method", or undefined symbols. Name things ("EK-FAC", "the PBRF") and attribute \
results ("Grosse et al. (2023) found ...").
- Conceptual, not trivia: prefer why and when over what. Include mechanism facts (why \
something works), when_to_use facts (when to choose it over alternatives, and its failure \
modes), and the facts that connect ideas. Skip exact hyperparameters, dataset sizes, table \
numbers and author lists unless they are the point.
- Results should state the finding and what it implies, with enough qualifiers to be true.

Prerequisites between facts: list a fact's prerequisites when understanding it genuinely \
requires them, using keys from this same response. Only direct dependencies; the graph \
supplies the transitive ones. No cycles.

Size: a typical paper yields 40-80 facts; a long one may need more. Cover what matters for \
understanding rather than paraphrasing every paragraph.
"""


def extract(llm: LLM, profile: str, text: str) -> Extraction:
    user = f"<learner_profile>\n{profile}\n</learner_profile>\n\n<paper>\n{text}\n</paper>"
    result = llm.structured(
        "extract", llm.models.extract, Extraction, SYSTEM, user, effort="medium"
    )
    return drop_dangling(result)


def drop_dangling(result: Extraction) -> Extraction:
    keys = {c.key for c in result.facts}
    for c in result.facts:
        c.prerequisites = [k for k in dict.fromkeys(c.prerequisites) if k in keys and k != c.key]
    return result
