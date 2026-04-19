# Knowledge Graphs

Cerebe's knowledge-graph surface (`client.knowledge`) stores facts and the relationships between them, and preserves how that knowledge evolves over time. Use it when you need to reason about connections — who is related to whom, which project depends on which, what changed when — rather than retrieve matching text.

## Ingest

New facts enter the graph through `client.knowledge.ingest`. You can pass raw text (the platform extracts entities and relationships) or structured triples when you already have them. Each ingested fact carries provenance — the source document and the ingestion timestamp — so you can always trace a claim back to its origin.

## Query

`client.knowledge.query` returns matching nodes or edges. Queries support property filters, relationship types, and hop count. Unlike RAG search, results come back as typed graph nodes with their attributes, not prose chunks.

## Traverse

`client.knowledge.traverse` walks outward from a starting node. You specify the start, the edge types to follow, and the maximum depth. Traversal is how you answer "what projects does this person own?" or "which memory items cite this document?" Cycles are detected and reported rather than expanded forever.

## Temporal evolution

The graph is temporal: facts have valid-from and valid-to timestamps, and queries can be scoped to "as of" a particular moment. This matters when the truth changes — an employee's role, a product's availability, a policy's text. Rather than overwriting, ingesting a contradicting fact creates a new temporal edge and closes out the old one, and the full history is traversable.

## Visualise

`client.knowledge.visualize` produces a renderable representation of a subgraph — the set of nodes and edges around a focal node — suitable for drawing in the dashboard or exporting to tools like Graphviz. Use it to sanity-check what the graph actually contains for a given entity.
