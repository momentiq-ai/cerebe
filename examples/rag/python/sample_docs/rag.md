# Retrieval-Augmented Generation

Cerebe's RAG surface (`client.rag`) provides document embedding and retrieval for knowledge that doesn't change per user. Use it for product docs, knowledge bases, policies, and any corpus you want an agent to search against.

## How it works

When you embed a document, Cerebe chunks the content into overlapping windows, computes a vector embedding for each chunk, and stores both the raw text and its embedding against a unique `source` identifier. Later searches use that embedding index to return the most relevant chunks with similarity scores.

## Search modes

Three retrieval modes are available:

- **Semantic search** (`search`) — vector similarity only. Best for conceptual questions where the answer may not use the same words as the query.
- **Hybrid search** (`hybrid_search`) — weighted combination of semantic similarity and keyword match. Configurable weights (`semantic_weight`, `keyword_weight`) let you bias toward concept or lexical match depending on the query style. Results include both `semantic_score` and `keyword_score` so downstream code can see the breakdown, along with a combined `score` used for ranking.
- **Similarity search** (`find_similar`) — take an existing piece of content and find other documents like it, without composing a text query.

All three accept an optional `k` parameter (number of results) and optional filters on `doc_type` and, for `search`, `source_pattern`.

## Document management

Documents are identified by a `source` string you choose (a URL, a path, an ID — whatever makes sense for your application). `embed` adds or replaces a single document; `embed_batch` handles many at once and returns per-document chunk counts. `list_documents` enumerates what's stored, and `delete_document` removes a source along with all its chunks. `stats` returns a summary of the collection — total chunks, unique sources, doc-type breakdown, and the embedding model in use.

## Metadata and doc types

Every document can carry an optional `metadata` dict and a `doc_type` tag (default `"markdown"`). Use `doc_type` to separate different corpora (docs vs. policies vs. examples) when searching — the `doc_type` filter on `search` scopes results to a single type.
