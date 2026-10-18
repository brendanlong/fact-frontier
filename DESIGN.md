# Design

A pool of **atomic facts** is the unit of everything: what gets taught, practiced and tracked.
Groupings (clusters) are derived and disposable, so restructuring them never touches history.

## Ingesting a source (`frontier ingest`)

1. **Extract** (`extract.py`): one call reads the whole paper and the learner profile, and
   returns candidate facts, each a *prerequisite* (background the paper assumes) or a
   *contribution* (what it establishes), with importance and prerequisite links among them.
   The profile sets how deep prerequisites go.
2. **Merge** (`merge.py`): each candidate is embedded, and its nearest existing facts are found
   by embedding similarity plus FTS5 keyword search. A model decides, per candidate, whether
   it duplicates one of those facts or is new, and which of them it depends on or supports.
   Duplicates attach the new source to the existing fact. Links that would create a cycle in
   the prerequisite graph are dropped.
3. **Cluster** (`cluster.py`): Louvain community detection over a graph of embedding
   nearest-neighbor edges plus prerequisite edges. Clusters that keep most of their membership
   keep their ID and name; new ones are named by a model.
4. **Report** (`report.py`): an HTML snapshot of the pool after each source.

Each source is one transaction: a failure leaves the pool as it was, but the spend is still
logged.

## Storage

One SQLite file. Embeddings are float32 blobs searched by brute force, which is fine to a few
tens of thousands of facts.
