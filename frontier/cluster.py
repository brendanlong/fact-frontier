import sqlite3

import networkx as nx
import numpy as np
from pydantic import BaseModel

from frontier.llm import LLM
from frontier.merge import load_pool

SIMILAR_NEIGHBORS = 5
# Prerequisite links say two facts belong together more reliably than wording does.
PREREQ_WEIGHT = 1.0
# Below this, a cluster is treated as new and renamed rather than keeping an old identity.
KEEP_IDENTITY = 0.5


class ClusterName(BaseModel):
    name: str
    summary: str


SYSTEM = """\
Name a group of related facts a learner is studying. The name is a short topic label (2-6 \
words) shown on a map of what they know; the summary is one sentence saying what the group \
covers. Name the shared topic, not a list of its parts."""


def fact_graph(conn: sqlite3.Connection) -> nx.Graph:
    pool = load_pool(conn)
    graph = nx.Graph()
    graph.add_nodes_from(f.id for f in pool)
    if len(pool) < 2:
        return graph
    matrix = np.stack([f.embedding for f in pool])
    sims = matrix @ matrix.T
    np.fill_diagonal(sims, -1)
    for i, row in enumerate(sims):
        for j in np.argsort(-row)[:SIMILAR_NEIGHBORS]:
            a, b = pool[i].id, pool[int(j)].id
            w = float(max(row[j], 0))
            if w > graph.get_edge_data(a, b, {"weight": 0})["weight"]:
                graph.add_edge(a, b, weight=w)
    for prereq, fact in conn.execute("SELECT prereq_id, fact_id FROM fact_edges"):
        prior = graph.get_edge_data(prereq, fact, {"weight": 0})["weight"]
        graph.add_edge(prereq, fact, weight=prior + PREREQ_WEIGHT)
    return graph


def match_previous(communities: list[set[int]], previous: dict[int, set[int]]) -> dict[int, int]:
    """Map community index -> previous cluster ID, greedily by overlap, so clusters keep their
    identity (and name) across reclustering when their membership mostly survives."""
    pairs = []
    for ci, members in enumerate(communities):
        for cid, old in previous.items():
            overlap = len(members & old) / len(members | old)
            if overlap >= KEEP_IDENTITY:
                pairs.append((overlap, ci, cid))
    matched: dict[int, int] = {}
    used: set[int] = set()
    for _, ci, cid in sorted(pairs, reverse=True):
        if ci not in matched and cid not in used:
            matched[ci] = cid
            used.add(cid)
    return matched


def recluster(conn: sqlite3.Connection, llm: LLM, resolution: float = 1.0) -> None:
    graph = fact_graph(conn)
    communities = [
        set(c) for c in nx.community.louvain_communities(graph, seed=0, resolution=resolution)
    ]
    previous: dict[int, set[int]] = {}
    for fact_id, cluster_id in conn.execute("SELECT fact_id, cluster_id FROM fact_clusters"):
        previous.setdefault(cluster_id, set()).add(fact_id)
    matched = match_previous(communities, previous)

    statements = dict(conn.execute("SELECT id, statement FROM facts").fetchall())
    conn.execute("DELETE FROM fact_clusters")
    for ci, members in enumerate(communities):
        cluster_id = matched.get(ci)
        if cluster_id is None:
            listing = "\n".join(f"- {statements[f]}" for f in sorted(members))
            named = llm.structured(
                "name_cluster", llm.models.name_clusters, ClusterName, SYSTEM, listing, effort="low"
            )
            cluster_id = conn.execute(
                "INSERT INTO clusters (name, summary) VALUES (?, ?)", (named.name, named.summary)
            ).lastrowid
        conn.executemany(
            "INSERT INTO fact_clusters (fact_id, cluster_id) VALUES (?, ?)",
            [(f, cluster_id) for f in members],
        )
    conn.execute("DELETE FROM clusters WHERE id NOT IN (SELECT cluster_id FROM fact_clusters)")
