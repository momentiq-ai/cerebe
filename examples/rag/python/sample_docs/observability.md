# Observability

Cerebe's observability surface makes agent behaviour inspectable. Every interaction an agent has with the platform — memory reads and writes, RAG queries, chat completions — is captured as a structured trace you can replay, analyse, and alert on.

## Traces

An **execution trace** is the complete sequence of steps the agent took to produce a response: which memories it read, which documents it retrieved, which tools it called, and which LLM calls it made, all with timestamps and token counts. Traces are exposed through `client.agents.traces` and are retrievable by trace ID, by user, or by time range.

Each span in a trace records:

- The operation name (e.g. `memory.search`, `rag.hybrid_search`, `llm.chat`).
- Inputs (query text, filters) and outputs (result count, score distribution).
- Latency (wall-clock and server time).
- Any errors raised and their class.

## Cognitive profiling

Beyond raw traces, Cerebe computes aggregate **cognitive profiles**: how does the agent spend its time across memory, retrieval, and reasoning? Which memory types does a user access most? Where are latency hotspots? These are helpful for tuning context-window usage and for debugging regressions when an agent's behaviour changes unexpectedly.

## Using traces in development

During development, pulling the most recent trace for a failed interaction is often faster than re-instrumenting your own logging. The dashboard shows each trace as a timeline with per-span latencies, and the API returns the same data structured so you can diff traces programmatically.

## MCP for Claude Code and Cursor

Cerebe ships an MCP server that exposes traces, memory, and the RAG surface to AI-coding tools like Claude Code and Cursor. Developers debugging an application against Cerebe can query traces directly from their editor without switching to the dashboard.

## Privacy

Trace payloads include the prompts and responses that flowed through Cerebe. They live in the same workspace as your memory and knowledge data and inherit the same retention settings. If you need shorter retention for traces specifically, configure it in the dashboard.
