"""Score one system's requirements against another's (usually: a predicted list against the
owner-labelled draft) when names, senses and granularity differ.

A model judges coverage element by element; code aggregates. A gold requirement counts as
covered only when its required elements are all covered, at the right sense, by one or more
predictions together. A broad prediction gets no blanket credit for narrow gold entries.
"""

import json
import random
import sqlite3
from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel, Field

from frontier.calls import Client

Relation = Literal[
    "equivalent", "covers_part", "broader_but_not_explicit", "different_sense", "uncertain"
]
COVERING = ("equivalent", "covers_part")
BATCH = 8


@dataclass
class Req:
    rid: str
    label: str
    sense: str
    capability: str
    depth: str
    elements: list[str]


class Link(BaseModel):
    predicted: str = Field(description="ID of a predicted requirement, e.g. 'P7'.")
    relation: Relation
    covered_elements: list[int] = Field(
        description="Indices of the gold requirement's elements this prediction explicitly covers."
    )
    evidence: str = Field(description="One sentence: what in the prediction covers them.")


class GoldJudgement(BaseModel):
    gold_id: str
    links: list[Link] = Field(description="Only predictions that relate; omit unrelated ones.")


class Judgements(BaseModel):
    judgements: list[GoldJudgement]


SYSTEM = """\
You check whether a list of predicted requirements (things a reader needs to know to follow a
paper) covers each gold requirement. Judge coverage, not topical similarity.

For each gold requirement, list every prediction that relates to it, with:
- equivalent: the same capability in the same sense, at least at the gold depth.
- covers_part: explicitly covers some of the gold requirement's numbered elements.
- broader_but_not_explicit: a broader topic that would plausibly include it but doesn't state
  the gold elements. This earns no credit.
- different_sense: the same words used with a different meaning.
- uncertain: you can't tell.
covered_elements lists the indices (0-based) of the gold elements the prediction states
explicitly or unmistakably implies. A prediction about a related but distinct idea covers
nothing. Several narrow predictions may together cover one gold requirement."""


def render(r: Req, prefix: str) -> str:
    elements = "; ".join(f"[{i}] {e}" for i, e in enumerate(r.elements))
    return (
        f"{prefix}{r.rid}: {r.label} ({r.depth}). Sense: {r.sense} "
        f"Capability: {r.capability} Elements: {elements}"
    )


def judge(
    client: Client, gold: list[Req], predicted: list[Req], subject: str
) -> dict[str, list[Link]]:
    """Map gold ID -> links, with predicted IDs translated back to the caller's IDs. Predictions
    are shuffled and relabelled P1..Pn so the judge can't tell which system wrote them."""
    order = predicted[:]
    random.Random(subject).shuffle(order)
    alias = {f"P{i + 1}": r.rid for i, r in enumerate(order)}
    pred_block = "\n".join(
        render(Req(f"P{i + 1}", r.label, r.sense, r.capability, r.depth, r.elements), "")
        for i, r in enumerate(order)
    )
    out: dict[str, list[Link]] = {}
    for i in range(0, len(gold), BATCH):
        batch = gold[i : i + BATCH]
        user = (
            f"<predicted>\n{pred_block}\n</predicted>\n\n<gold>\n"
            + "\n".join(render(g, "") for g in batch)
            + "\n</gold>"
        )
        result, _ = client.structured(
            "match",
            client.roles.matcher,
            Judgements,
            SYSTEM,
            user,
            subject=subject,
            effort="medium",
        )
        returned = {j.gold_id for j in result.judgements}
        missing = {g.rid for g in batch} - returned
        if missing:
            raise ValueError(f"matcher skipped gold entries {sorted(missing)}")
        for j in result.judgements:
            if j.gold_id not in {g.rid for g in batch}:
                continue
            n_elements = len(next(g for g in batch if g.rid == j.gold_id).elements)
            out[j.gold_id] = [
                link.model_copy(
                    update={
                        "predicted": alias[link.predicted],
                        "covered_elements": [
                            e for e in link.covered_elements if 0 <= e < n_elements
                        ],
                    }
                )
                for link in j.links
                if link.predicted in alias
            ]
    return out


def coverage(gold: Req, links: list[Link]) -> float:
    covered: set[int] = set()
    for link in links:
        if link.relation in COVERING:
            covered |= set(link.covered_elements)
            if link.relation == "equivalent":
                covered |= set(range(len(gold.elements)))
    return len(covered) / len(gold.elements) if gold.elements else 0.0


def load(conn: sqlite3.Connection, revision_id: str, system: str) -> list[Req]:
    rows = conn.execute(
        "SELECT candidate_id, label, sense, capability, depth, required_elements"
        " FROM requirement_candidates WHERE revision_id = ? AND system = ?",
        (revision_id, system),
    )
    return [Req(r[0], r[1], r[2], r[3], r[4], json.loads(r[5])) for r in rows]
