# Memory Fabric

Most AI applications are stateless — every conversation starts from scratch. Cerebe's Memory Fabric gives applications persistent memory that lasts across sessions, users, and weeks.

## The nine memory types

Memory Fabric is organised into nine distinct memory types, each with its own retention, recall, and consolidation behaviour:

1. **Semantic** — facts about the world and the user (preferences, traits, stable beliefs).
2. **Episodic** — time-anchored events and conversations ("on Tuesday the user mentioned they prefer visual explanations").
3. **Procedural** — how to do things; sequences of actions the agent has seen work.
4. **Working** — short-horizon scratch space scoped to the current session.
5. **Sensory** — raw inputs (text, audio transcripts, images) with minimal processing.
6. **Prospective** — intentions and reminders scheduled for the future.
7. **Associative** — links between memory items to enable graph traversal.
8. **Meta** — memory about memory (confidence, provenance, last-accessed).
9. **TTL** — any of the above with an explicit time-to-live for compliance or privacy.

## Hybrid storage

Memory Fabric stores items in a **hybrid vector + graph** substrate. Vector similarity handles "give me memories semantically related to this query"; graph traversal handles "what is connected to this memory and how." Both are available through the same `client.memory` surface.

## Consolidation

Raw memories are frequently noisy. Cerebe's **consolidate** endpoint compresses a window of episodic memories into higher-quality semantic summaries while preserving provenance. This keeps search fast and the knowledge base compact.

## Harvest

The **harvest** endpoint extracts long-term-worthy facts from a recent stream of interactions and promotes them into the appropriate memory type. Use it to bridge a live session into persistent memory at the end of a conversation.

## When to use it

Memory Fabric is the right layer for any application that needs to remember *about users* across sessions. For document-level knowledge that doesn't change per user, use the RAG surface (`client.rag`) instead.
