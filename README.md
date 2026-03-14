<p align="center">
  <img src="https://cerebe.ai/cerebe-logo.svg" alt="Cerebe" width="80" height="80" />
</p>

<h1 align="center">Cerebe</h1>

<p align="center">
  <strong>Cognitive services platform for AI applications.</strong><br/>
  Memory, knowledge graphs, and meta-learning — through a simple API.
</p>

<p align="center">
  <a href="https://www.npmjs.com/package/@cerebe/sdk"><img src="https://img.shields.io/npm/v/@cerebe/sdk?label=npm&color=blue" alt="npm" /></a>
  <a href="https://pypi.org/project/cerebe/"><img src="https://img.shields.io/pypi/v/cerebe?color=blue" alt="PyPI" /></a>
  <a href="https://cerebe.ai/docs"><img src="https://img.shields.io/badge/docs-cerebe.ai-green" alt="Docs" /></a>
  <a href="https://cerebe.ai/llms.txt"><img src="https://img.shields.io/badge/llms.txt-available-purple" alt="llms.txt" /></a>
</p>

---

## What is Cerebe?

Most AI applications are stateless — every conversation starts from scratch. Cerebe changes that.

Cerebe provides cognitive infrastructure as an API:

- **Memory Fabric** — Hybrid vector + graph memory that persists across sessions. 9 memory types including semantic, episodic, procedural, and working memory with TTL.
- **Knowledge Graph** — Temporal knowledge that evolves with full provenance. Ingest, query, traverse, and visualize.
- **Meta-Learning** — PLRE (Perception, Learning, Reasoning, Expression) framework that understands how users learn and adapts.
- **Agent Tooling** — Execution traces, cognitive profiling, and MCP server for Claude Code and Cursor.
- **LLM Router** — OpenAI-compatible chat with automatic cognitive context enrichment.

## Quick Start

### Install

```bash
# Python
pip install cerebe

# TypeScript / Node.js
npm install @cerebe/sdk
```

### Store and Search Memory

```python
from cerebe import AsyncCerebe

client = AsyncCerebe(api_key="ck_live_...")

# Store a memory
await client.memory.add(
    content="User prefers visual explanations over text",
    user_id="user_123",
    session_id="onboarding",
    type="semantic",
    importance=0.8,
)

# Search across sessions
results = await client.memory.search(
    query="What kind of explanations does the user like?",
    user_id="user_123",
)
# -> "User prefers visual explanations over text"
```

```typescript
import Cerebe from '@cerebe/sdk'

const client = new Cerebe({ apiKey: 'ck_live_...' })

await client.memory.add({
  content: 'User prefers visual explanations over text',
  userId: 'user_123',
  sessionId: 'onboarding',
  type: 'semantic',
  importance: 0.8,
})

const results = await client.memory.search({
  query: 'What kind of explanations does the user like?',
  userId: 'user_123',
})
```

## API Overview

| Domain | Endpoints | Description |
|--------|-----------|-------------|
| **Memory** | `add`, `search`, `harvest`, `consolidate` | Store, retrieve, and manage persistent memory |
| **Knowledge** | `ingest`, `query`, `traverse`, `visualize` | Build and query temporal knowledge graphs |
| **Meta-Learning** | `analyze`, `profile`, `plre` | Understand learning patterns and cognitive state |
| **Agents** | `traces` | Execution history and agent observability |
| **LLM** | `chat` | OpenAI-compatible chat with cognitive context |
| **Storage** | `upload`, `retrieve` | Object storage for files and media |

## Resources

| Resource | Link |
|----------|------|
| Documentation | [cerebe.ai/docs](https://cerebe.ai/docs) |
| Quickstart | [cerebe.ai/docs/getting-started/quickstart](https://cerebe.ai/docs/getting-started/quickstart) |
| Python SDK | [pypi.org/project/cerebe](https://pypi.org/project/cerebe/) |
| TypeScript SDK | [npmjs.com/package/@cerebe/sdk](https://www.npmjs.com/package/@cerebe/sdk) |
| Dashboard | [cerebe.ai/dashboard](https://cerebe.ai/dashboard) |
| AI-readable docs | [cerebe.ai/llms.txt](https://cerebe.ai/llms.txt) |

## For AI Agents

Cerebe provides machine-readable documentation for AI tools:

- **`/llms.txt`** — Structured index of all documentation pages
- **`/llms-full.txt`** — Complete documentation content in markdown

If you're building with Claude Code, Cursor, or other AI-assisted tools, these endpoints let your tools understand the full Cerebe API surface automatically.

## Authentication

Get your API key from the [Cerebe Dashboard](https://cerebe.ai/dashboard/keys). Keys use the format `ck_live_...` for production and `ck_test_...` for testing.

```bash
curl https://api.cerebe.ai/api/v1/memory/search \
  -H "X-API-Key: ck_live_your_key" \
  -H "Content-Type: application/json" \
  -d '{"query": "user preferences", "entity_id": "user_123"}'
```

## License

Cerebe is a managed platform. SDKs are MIT licensed.

---

<p align="center">
  Built by <a href="https://momentiq.ai">MomentiQ</a>
</p>
