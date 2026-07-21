<p align="center">
  <img src="https://cerebe.ai/cerebe-logo.svg" alt="Cerebe" width="80" height="80" />
</p>

<h1 align="center">Cerebe</h1>

<p align="center">
  <strong>The AI-native software company — scaffold, build, and ship, on one cognitive stack.</strong><br/>
  Cerebe is the house brand for the whole family: the build lifecycle and the cognitive infrastructure it runs on.
</p>

<p align="center">
  <a href="https://cerebe.ai"><img src="https://img.shields.io/badge/site-cerebe.ai-black" alt="cerebe.ai" /></a>
  <a href="https://cerebe.ai/docs"><img src="https://img.shields.io/badge/docs-cerebe.ai-green" alt="Docs" /></a>
  <a href="https://github.com/momentiq-ai/cerebe/releases"><img src="https://img.shields.io/github/v/release/momentiq-ai/cerebe?label=cerebe%20CLI&color=black" alt="cerebe CLI release" /></a>
  <a href="https://www.npmjs.com/package/@cerebe/sdk"><img src="https://img.shields.io/npm/v/@cerebe/sdk?label=%40cerebe%2Fsdk&color=blue" alt="npm" /></a>
  <a href="https://pypi.org/project/cerebe/"><img src="https://img.shields.io/pypi/v/cerebe?color=blue" alt="PyPI" /></a>
  <a href="./LICENSE"><img src="https://img.shields.io/badge/CLI-free%20to%20use-brightgreen" alt="Free to use" /></a>
</p>

---

## What is Cerebe?

Cerebe is one brand over an AI-native software company. It spans the arc of building
software — scaffold a project, build it behind a quorum of AI critics, and ship it behind
deterministic safety gates — and the cognitive infrastructure that arc runs on. The name
is meant to work the way Docker's does: the bare word for the free tool, a modifier for
everything else.

**One workflow, three tools you can use today:**

> **Scaffold** with Blueprint → **build & ship** through Factory → all resting on **Cognitive**.

| | What it is | How you reach it |
|---|---|---|
| **[Cerebe Factory](#cerebe-factory--the-autonomous-code-factory)** | The autonomous code factory: a quorum of rival AI critics reviews **every commit**, and deterministic gates bind reviewed evidence to each change before it ships. | the free **`cerebe`** CLI |
| **[Cerebe Blueprint](#cerebe-blueprint--scaffold-an-ai-native-product)** | Scaffold a production-ready agentic product (FastAPI + Next.js + LangGraph + Helm), pre-wired to the Cerebe stack and the Factory gate on commit one. | the **`sage`** CLI |
| **[Cerebe Cognitive](#cerebe-cognitive--the-engine)** | The engine: persistent memory, temporal knowledge graphs, capability-based model routing, and meta-learning — behind one hosted API. | Python / TypeScript SDK |

The model is a **free tool over a paid backend**: run the lifecycle locally with the
free-to-use CLIs, or hosted on **[Cerebe Cloud](#cerebe-cloud)** — the paid backend where
fleet review, compliance evidence, and dashboards live. The CLIs are free to use (not open
source); Cloud is a managed commercial service.

---

## Cerebe Factory — the autonomous code factory

The **`cerebe`** CLI puts a **quorum of rival AI critics** — Claude, Cursor, Codex, Gemini,
Grok — on every commit, and a pre-push gate that won't let a change ship until it's bound to
reviewed evidence. It's **free to use**, a single static binary: no Node or Python runtime,
and local review runs through your existing AI-app subscriptions (no API keys).

```bash
# Install the cerebe + cyclone binaries (checksum-verified) onto PATH — macOS/Linux
curl -fsSL https://raw.githubusercontent.com/momentiq-ai/cerebe/main/install.sh | sh
cerebe --version
```

Wire it into a repo:

```bash
cerebe install     # scaffold cerebe/, detect your local AI CLIs, install git hooks
cerebe doctor      # verify hooks, AI CLIs, config, and agent-context docs
```

`cerebe install` commits a `cerebe/config.json` — your critic fleet, quorum, and gate
policy — and installs two git hooks:

- **post-commit** runs the critic quorum **in the background**, so your commit stays instant;
- **pre-push `gate-push`** blocks the push only on unresolved findings at or above your
  configured `blockingSeverities` (e.g. `blocker` / `high`). Everything below is advisory —
  so the gate always has a terminating state, not an endless wall of nits. An emergency
  bypass (`AGENT_REVIEW_BYPASS="reason" git push`) is durably audited.

```bash
cerebe review                        # run the quorum on HEAD right now
cerebe gate-push                     # the pre-push gate
cerebe status                        # terse verdict for a commit
cerebe findings --range main..HEAD   # audit findings across a range
```

Two ways drive the **same fleet** through one verdict kernel: **`cerebe review`** uses your
local AI-app subscriptions (the dev inner loop), and **`cerebe critic`** drives them
headlessly through vendor APIs for CI. Installed alongside, **`cyclone`** runs the
cycle/project lifecycle — cycle-doc validation, branch-protection audit, verifiable
objectives, and closeout proof.

> Free to use under the [Cerebe Software License](./LICENSE) — free for any use, including
> commercial, but not open source.

---

## Cerebe Blueprint — scaffold an AI-native product

**`sage`** scaffolds a production-ready agentic product in one command and wires it to the
Cerebe stack and the Factory gate on commit one — no boilerplate, no glue code.

```bash
npm install -g @momentiq/sage-cli
sage init hireflow --primary-persona employer --domain hireflow.ai
# or one-shot, with interactive prompts:  npx @momentiq/sage-cli init hireflow
```

What you get on commit one:

- **FastAPI** backend (async PostgreSQL, Redis) + **Next.js 14** frontend (App Router,
  Tailwind, an `assistant-ui` chat surface)
- a **LangGraph** agent runtime (ReAct + dynamic skill selection)
- **Clerk** auth, **Doppler** secrets, **Helm** charts (local k3d + production GKE),
  **OpenTelemetry** observability
- the **Cerebe SDK** pre-installed and pointed at the engine, and the **Cerebe Factory
  gate** pre-wired (hooks, config, CI workflow)

---

## Cerebe Cognitive — the engine

The lifecycle — and your own AI applications — rest on Cerebe's cognitive services,
available today through one hosted API with Python and TypeScript SDKs.

| Service | What it does |
|---|---|
| **Cerebe Memory** | Hybrid vector + graph memory that persists across sessions — semantic, episodic, procedural, and working memory with consolidation and decay. |
| **Cerebe Knowledge** | Temporal knowledge graphs (ingest, query, traverse, point-in-time) and retrieval (RAG + hybrid search) — behind one client. |
| **Cerebe Models** | Capability-based LLM routing — request a model by capability and cost tier, not by hardcoded name. |
| **Cerebe Meta-Learning** | The PLRE loop and cognitive-profile store — pattern analysis across domains, learner state, and phase transitions. |

```bash
pip install cerebe          # Python
npm install @cerebe/sdk     # TypeScript / Node.js
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

Get an API key from the
[quickstart](https://cerebe.ai/docs/getting-started/quickstart). Keys use the format
`ck_live_...` for production and `ck_test_...` for testing. Runnable, clone-and-run
walkthroughs live under [`examples/`](./examples/).

### API overview

| Domain | Endpoints | Description |
|--------|-----------|-------------|
| **Memory** | `add`, `search`, `harvest`, `consolidate` | Store, retrieve, and manage persistent memory |
| **Knowledge** | `ingest`, `query`, `traverse`, `visualize` | Build and query temporal knowledge graphs |
| **Meta-Learning** | `analyze`, `profile`, `plre` | Understand learning patterns and cognitive state |
| **Agents** | `traces` | Execution history and agent observability |
| **LLM** | `chat` | OpenAI-compatible chat with cognitive context |
| **Storage** | `upload`, `retrieve` | Object storage for files and media |

---

## Cerebe Cloud

The paid backend the lifecycle runs against when hosted — fleet review at scale,
centralized compliance evidence, and dashboards over your critic runs and cycles. The CLIs
work fully offline against your local subscriptions for free; Cloud adds the managed
backend. See [cerebe.ai](https://cerebe.ai).

> **On "dark factory":** Cerebe Factory delivers what the industry calls a *dark factory* —
> a software pipeline that runs lights-out, autonomously, behind deterministic safety gates.
> We use the term as a description of the capability, not as a product name.

## For AI agents

Cerebe provides machine-readable documentation for AI tools:

- **`/llms.txt`** — structured index of all documentation pages
- **`/llms-full.txt`** — complete documentation content in markdown

If you're building with Claude Code, Cursor, or other AI-assisted tools, these endpoints let
your tools understand the full Cerebe API surface automatically.

## Resources

| Resource | Link |
|----------|------|
| Site | [cerebe.ai](https://cerebe.ai) |
| Documentation | [cerebe.ai/docs](https://cerebe.ai/docs) |
| Quickstart | [cerebe.ai/docs/getting-started/quickstart](https://cerebe.ai/docs/getting-started/quickstart) |
| `cerebe` CLI (Factory) | [github.com/momentiq-ai/cerebe/releases](https://github.com/momentiq-ai/cerebe/releases) |
| `sage` CLI (Blueprint) | [npmjs.com/package/@momentiq/sage-cli](https://www.npmjs.com/package/@momentiq/sage-cli) |
| Python SDK (Cognitive) | [pypi.org/project/cerebe](https://pypi.org/project/cerebe/) |
| TypeScript SDK (Cognitive) | [npmjs.com/package/@cerebe/sdk](https://www.npmjs.com/package/@cerebe/sdk) |
| Sign in | [cerebe.ai/sign-in](https://cerebe.ai/sign-in) |
| AI-readable docs | [cerebe.ai/llms.txt](https://cerebe.ai/llms.txt) |

## License

The `cerebe` CLI is **free to use** under the [Cerebe Software License](./LICENSE) — free for
any use, including commercial, but not open source (the source is proprietary). The `sage`
scaffolder and the Python / TypeScript SDKs are published separately under the MIT License.
**Cerebe Cloud** is a managed commercial service under its own agreement.

Cerebe is operated by Momentiq AI.

---

<p align="center">
  <a href="https://cerebe.ai">cerebe.ai</a>
</p>
