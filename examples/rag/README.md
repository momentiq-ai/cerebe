# RAG example

Demonstrates Cerebe's **Retrieval-Augmented Generation** surface — `client.rag` — end-to-end. You'll embed a small corpus of markdown documents, run three kinds of search (semantic, hybrid, similarity), inspect collection stats, and clean up, all from a single guided script.

## Languages

- **Python** — [`./python/`](./python/) — ready to run today.
- TypeScript — coming soon.

## What this example teaches

- How to authenticate the SDK with an API key.
- How to embed one or many documents (`embed`, `embed_batch`).
- How to retrieve chunks three different ways (`search`, `hybrid_search`, `find_similar`).
- How to inspect and manage the collection (`stats`, `list_documents`, `delete_document`).
- What a Cerebe RAG response looks like in practice — scores, metadata, request IDs.

## Prerequisites

- A Cerebe API key with the RAG scopes enabled. Grab or rotate one at the [Cerebe Dashboard](https://cerebe.ai/dashboard/keys).
- The toolchain for the language variant you pick (see the language README for exact versions).

Head into the language directory to get started.
