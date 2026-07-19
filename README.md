<p align="center">
  <img src="https://cerebe.ai/cerebe-logo.svg" alt="Cerebe" width="80" height="80" />
</p>

<h1 align="center">Cerebe</h1>

<p align="center">
  <strong>The AI-native software company — scaffold, plan, build, and ship, on one cognitive stack.</strong><br/>
  Cerebe is the house brand for the whole family: the build lifecycle and the cognitive infrastructure it runs on.
</p>

<p align="center">
  <a href="https://cerebe.ai"><img src="https://img.shields.io/badge/site-cerebe.ai-black" alt="cerebe.ai" /></a>
  <a href="https://cerebe.ai/docs"><img src="https://img.shields.io/badge/docs-cerebe.ai-green" alt="Docs" /></a>
  <a href="https://www.npmjs.com/package/@cerebe/sdk"><img src="https://img.shields.io/npm/v/@cerebe/sdk?label=%40cerebe%2Fsdk&color=blue" alt="npm" /></a>
  <a href="https://pypi.org/project/cerebe/"><img src="https://img.shields.io/pypi/v/cerebe?color=blue" alt="PyPI" /></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/CLI-free%20to%20use-brightgreen" alt="Free to use" /></a>
</p>

---

## What is Cerebe?

Cerebe is one brand over an AI-native software company. It spans the arc of building
software — scaffold a project, plan the change, build and ship it behind safety gates —
and the cognitive infrastructure that arc runs on. The name is meant to work the way
Docker's does: the bare word for the free tool, a modifier for everything else.

**What you can use today:** Cerebe's **cognitive services** — a hosted API with Python
and TypeScript SDKs ([quick start below](#quick-start--the-cognitive-api)). The **build
lifecycle** tooling is consolidating under the Cerebe brand now; this repo is its front
door as it lands. Follow [cerebe.ai](https://cerebe.ai) for availability.

### The build lifecycle (consolidating under Cerebe)

The build lifecycle will span three stages:

| Stage | What it will be |
|---|---|
| **Cerebe Blueprint** | Scaffolds a complete AI-native project (API + web + deploy), pre-wired to the Cerebe stack on commit one. |
| **Cerebe Plan** | Turns intent into an agreed, proof-bound plan — brainstorming, specs, verifiable objectives — before code is written. |
| **Cerebe Factory** | The autonomous code factory: agents implement, a quorum of rival AI critics reviews every change, and deterministic gates bind evidence to each commit before it ships. |

The model is a free tool over a paid backend: run the lifecycle locally with the
**free-to-use `cerebe`** CLI, or hosted with **Cerebe Cloud** — the paid backend where
fleet review, compliance evidence, and dashboards live. (Both are planned as the tooling
consolidates here; the CLI is free to use, not open source.)

### The cognitive infrastructure

The lifecycle — and your own AI applications — rest on Cerebe's cognitive services,
available today through one API and SDK:

| Service | What it does |
|---|---|
| **Cerebe Memory** | Hybrid vector + graph memory that persists across sessions — semantic, episodic, procedural, and working memory with consolidation and decay. |
| **Cerebe Knowledge** | Temporal knowledge graphs (ingest, query, traverse, point-in-time) and retrieval (RAG + hybrid search) — behind one client. |
| **Cerebe Models** | Capability-based LLM routing — request a model by capability and cost tier, not by hardcoded name. |
| **Cerebe Meta-Learning** | The PLRE loop and cognitive-profile store — pattern analysis across domains, learner state, and phase transitions. |

## Quick start — the cognitive API

The cognitive services ship today as a hosted API with Python and TypeScript SDKs.

```bash
# Python
pip install cerebe

# TypeScript / Node.js
npm install @cerebe/sdk
```

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

Get an API key by following the
[quickstart](https://cerebe.ai/docs/getting-started/quickstart). Keys use the format
`ck_live_...` for production and `ck_test_...` for testing.

Runnable, clone-and-run walkthroughs live under [`examples/`](./examples/).

> **On "dark factory":** Cerebe Factory (above) will deliver what the industry calls a
> *dark factory* — a software pipeline that runs lights-out, autonomously, behind
> deterministic safety gates. We use the term as a description of the capability, not as
> a product name.

## API overview

| Domain | Endpoints | Description |
|--------|-----------|-------------|
| **Memory** | `add`, `search`, `harvest`, `consolidate` | Store, retrieve, and manage persistent memory |
| **Knowledge** | `ingest`, `query`, `traverse`, `visualize` | Build and query temporal knowledge graphs |
| **Meta-Learning** | `analyze`, `profile`, `plre` | Understand learning patterns and cognitive state |
| **Agents** | `traces` | Execution history and agent observability |
| **LLM** | `chat` | OpenAI-compatible chat with cognitive context |
| **Storage** | `upload`, `retrieve` | Object storage for files and media |

## For AI agents

Cerebe provides machine-readable documentation for AI tools:

- **`/llms.txt`** — structured index of all documentation pages
- **`/llms-full.txt`** — complete documentation content in markdown

If you're building with Claude Code, Cursor, or other AI-assisted tools, these
endpoints let your tools understand the full Cerebe API surface automatically.

## Resources

| Resource | Link |
|----------|------|
| Site | [cerebe.ai](https://cerebe.ai) |
| Documentation | [cerebe.ai/docs](https://cerebe.ai/docs) |
| Quickstart | [cerebe.ai/docs/getting-started/quickstart](https://cerebe.ai/docs/getting-started/quickstart) |
| Python SDK | [pypi.org/project/cerebe](https://pypi.org/project/cerebe/) |
| TypeScript SDK | [npmjs.com/package/@cerebe/sdk](https://www.npmjs.com/package/@cerebe/sdk) |
| Sign in | [cerebe.ai/sign-in](https://cerebe.ai/sign-in) |
| AI-readable docs | [cerebe.ai/llms.txt](https://cerebe.ai/llms.txt) |

## License

The `cerebe` CLI is **free to use** under the [Cerebe Software License](./LICENSE) — free
for any use, including commercial, but not open source (the source is proprietary).
**Cerebe Cloud** is a managed commercial service under its own agreement. The Python and
TypeScript SDKs are published separately under the MIT License.

Cerebe is operated by Momentiq AI.

---

<p align="center">
  <a href="https://cerebe.ai">cerebe.ai</a>
</p>
