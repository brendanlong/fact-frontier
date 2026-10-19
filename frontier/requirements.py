"""The comparable requirement record every system's output is normalized into, and the guidance
shared by every prompt that produces one."""

import json
import sqlite3
import uuid
from typing import Literal

from pydantic import BaseModel, Field

Depth = Literal["recognize", "explain", "derive", "apply", "choose", "critique", "extend"]
Centrality = Literal[
    "core_contribution",
    "method",
    "experimental_setup",
    "evaluation",
    "background",
    "passing_mention",
]


class Requirement(BaseModel):
    label: str = Field(description="Short name, as a reader would search for it.")
    sense: str = Field(
        description="Which meaning of the label this is, in one sentence, so it can't be "
        "confused with other uses of the same words."
    )
    capability: str = Field(
        description="What the reader must be able to do with it to follow this paper, as an "
        "operational statement (e.g. 'explain why damping is added before inverting the "
        "Gauss-Newton matrix and what happens as it goes to zero')."
    )
    depth: Depth
    required_elements: list[str] = Field(
        description="1-4 specific pieces that must all be understood for the capability."
    )
    served_span_ids: list[str] = Field(
        description="IDs of the spans (e.g. 'S41') where the paper relies on this."
    )
    centrality: Centrality
    why_needed: str = Field(
        description="Which claim, equation or step would be misunderstood without it."
    )


DEPTH_GUIDE = """\
Depth, by how the paper uses the concept:
- recognize: know what the term refers to well enough to keep reading.
- explain: say what it is and why it works, in your own words.
- derive: follow (or reproduce) the paper's derivation or calculation that uses it.
- apply: use it in a new setting.
- choose: pick between it and alternatives for a given situation, with reasons.
- critique: judge whether the paper's use of it supports its claims.
- extend: modify it for a new purpose and predict the effect.

Granularity: one requirement is something a 5-15 minute lesson could teach to a strong
engineer. "Transformers" or "deep learning" is too coarse; a single symbol is too fine unless the
paper hinges on it. Include experimental setups and measurement conventions (how an outcome is
measured, what a threshold means, what a baseline is) when understanding the results depends on
them; they are requirements too."""


def store_candidates(
    conn: sqlite3.Connection,
    revision_id: str,
    system: str,
    artifact_id: str,
    reqs: list[Requirement],
    valid_spans: set[str],
) -> list[str]:
    """Insert requirements, dropping span IDs that don't exist in the revision. Raises if most
    citations are invalid, since that means the output isn't about this document."""
    cited = [s for r in reqs for s in r.served_span_ids]
    invalid = [s for s in cited if s not in valid_spans]
    if cited and len(invalid) > 0.2 * len(cited):
        raise ValueError(f"{len(invalid)}/{len(cited)} cited spans don't exist in {revision_id}")
    ids = []
    with conn:
        for r in reqs:
            cid = f"{system}-{uuid.uuid4().hex[:10]}"
            ids.append(cid)
            conn.execute(
                "INSERT INTO requirement_candidates (candidate_id, revision_id, system,"
                " artifact_id, label, sense, capability, depth, required_elements,"
                " served_span_ids, centrality, why_needed) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    cid,
                    revision_id,
                    system,
                    artifact_id,
                    r.label,
                    r.sense,
                    r.capability,
                    r.depth,
                    json.dumps(r.required_elements),
                    json.dumps([s for s in r.served_span_ids if s in valid_spans]),
                    r.centrality,
                    r.why_needed,
                ),
            )
    return ids
