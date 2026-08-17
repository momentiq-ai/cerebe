<p align="center">
  <img src="https://cerebe.ai/cerebe-logo.svg" alt="Cerebe" width="80" height="80" />
</p>

<h1 align="center">Cerebe</h1>

<p align="center">
  <strong>AI-native software factory — scaffold, build, and ship, on one cognitive stack.</strong><br/>
  Cerebe is the AI native build lifecycle and the cognitive infrastructure.
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

Cerebe spans the arc of building software — scaffold a project, 
build it behind a quorum of AI critics, and ship it behind
deterministic safety gates — and the cognitive infrastructure that arc runs on.

**One workflow, three tools you can use today:**

> **Scaffold** with Blueprint → **build & ship** through Factory → all resting on **Cognitive**.

| | What it is | How you reach it |
|---|---|---|
| **[Cerebe Factory](#cerebe-factory--the-autonomous-code-factory)** | The autonomous code factory: a quorum of rival AI critics reviews **every commit**, a live factory-floor TUI watches the loop, and deterministic gates bind reviewed evidence to each change before it ships. | the free **`cerebe`** + **`cyclone`** CLIs |
| **[Cerebe Blueprint](#cerebe-blueprint--scaffold-an-ai-native-product)** | Scaffold a production-ready agentic product (TypeScript: Bun + Hono + Svelte), pre-wired to the Cerebe stack and the Factory gate on commit one. | the public **[`df-cerebe-template`](https://github.com/momentiq-ai/df-cerebe-template)** |
| **[Cerebe Cognitive](#cerebe-cognitive--the-engine)** | The engine: persistent memory, temporal knowledge graphs, capability-based model routing, and meta-learning — behind one hosted API. | Python / TypeScript SDK |

The model is a **free tool over a paid backend**: run the lifecycle locally with the
free-to-use CLIs, or hosted on **[Cerebe Cloud](#cerebe-cloud)** — the paid backend where
fleet review, compliance evidence, and dashboards live. The CLIs are free to use (not open
source); Cloud is a managed commercial service.

---

## Cerebe Factory — the autonomous code factory

The **`cerebe`** CLI puts a **quorum of rival AI critics** — Claude, Cursor, Codex, Gemini,
Grok — on every commit, and a pre-push gate that won't let a change ship until it's bound to
reviewed evidence. It's **free to use**, a pair of static binaries (`cerebe` + `cyclone`):
no Node or Python runtime, and local review runs through your existing AI-app subscriptions
(no API keys).

Current stable release: **[v8.4.1](https://github.com/momentiq-ai/cerebe/releases/tag/v8.4.1)**
([all releases](https://github.com/momentiq-ai/cerebe/releases)).

```bash
# Install the cerebe + cyclone binaries (checksum-verified) onto PATH — macOS/Linux
curl -fsSL https://raw.githubusercontent.com/momentiq-ai/cerebe/main/install.sh | sh
cerebe --version    # cerebe v8.4.1
cyclone --version   # installed alongside
```

Pin a version with `CEREBE_VERSION=8.4.1`. On Windows, download the `cerebe_*_windows_*.zip`
and `cyclone_*_windows_*.zip` archives from the
[Releases](https://github.com/momentiq-ai/cerebe/releases) page.

Wire it into a repo:

```bash
cerebe install     # scaffold cerebe/, detect your local AI CLIs, install git hooks
cerebe doctor      # verify hooks, AI CLIs, config, and agent-context docs
```

`cerebe install` writes a `cerebe/config.json` — your critic fleet, quorum, and gate
policy — and installs two git hooks:

- **post-commit** runs the critic quorum **in the background**, so your commit stays instant,
  then nudges you to `cerebe watch`;
- **pre-push `gate-push`** blocks the push only on unresolved findings at or above your
  configured `blockingSeverities` (e.g. `blocker` / `high`). Everything below is advisory —
  so the gate always has a terminating state, not an endless wall of nits. An emergency
  bypass (`AGENT_REVIEW_BYPASS="reason" git push`) is durably audited.

```bash
cerebe review                        # run the quorum on HEAD right now
cerebe review --incremental          # re-review only the delta since last round
cerebe watch                         # live factory-floor TUI for this branch
cerebe watch --json                  # same fold, one JSON object per line (agents)
cerebe gate-push                     # the pre-push gate
cerebe status                        # terse verdict for a commit
cerebe findings --range main..HEAD   # audit findings across a range
```

**`cerebe watch`** is the factory floor. On a TTY it paints the live review loop — rounds,
lanes, findings, platform check, dirty chip. From the primary checkout with two or more
git worktrees it opens a root picker; Enter attaches, `p` comes back to the list. `--json`
is the agent face of the same fold (never multiplexed with the TUI). `--here` / `--root`
skip the picker and attach a listed worktree.

Two ways drive the **same fleet** through one verdict kernel: **`cerebe review`** uses your
local AI-app subscriptions (the dev inner loop), and **`cerebe critic`** drives them
headlessly through vendor APIs for CI.

Installed alongside, **`cyclone`** is the project-lifecycle CLI:

```bash
cyclone validate          # cycle-doc + planning validation
cyclone doc               # scaffold / write / list registered doc types
cyclone objectives        # derive and check verifiable objectives
cyclone decisions         # author + check the decision ledger
cyclone prove             # closeout proof for a cycle
cyclone publish           # publish review evidence
cyclone admit-pr          # classify a PR (plan vs code) and evaluate the plan-PR gate
```

Agents can talk to the same surface without scraping help text:

```bash
cerebe mcp                # local MCP server over stdio
cerebe onboard --dry-run  # preview an agent-context scaffold for this repo
cerebe skills list        # bundled Factory skills
cerebe schemas list       # published JSON Schemas (config, evidence, artifacts)
```

> Free to use under the [Cerebe Software License](./LICENSE) — free for any use, including
> commercial, but not open source.

---

## Cerebe Blueprint — scaffold an AI-native product

The public scaffold is
**[`df-cerebe-template`](https://github.com/momentiq-ai/df-cerebe-template)** — a
TypeScript product (Bun + Hono + LangGraph.js backend, Vite + Svelte frontend) that
runs natively and is pre-wired to Cerebe chat and the Factory gate on commit one.

```bash
# 1. Factory binaries first (one-time, per machine)
curl -fsSL https://raw.githubusercontent.com/momentiq-ai/cerebe/main/install.sh | sh

# 2. History-free copy of the template
mkdir hireflow && gh api repos/momentiq-ai/df-cerebe-template/tarball/main \
  | tar -xz --strip-components=1 -C hireflow
cd hireflow
bun run init -- --name "Hireflow"   # or interactive: bun run init
bun install && bun run dev          # http://localhost:5173 — no Docker
```

What you get on commit one:

- **One language, both ends** — TypeScript backend + frontend, types shared
- **Native dev** — `bun install` → `bun run dev`; Docker/k8s stay in `deploy/`
- **Cerebe chat** — OpenAI-compatible endpoint, memory-capable when you set a key
- **Factory gate** — critic on every commit, pre-push gate, no extra glue

The older **`@momentiq/sage-cli`** (`sage init`) scaffolder is **retired**. Do not
install it for new work. The template above is the public path.

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

## What's new in v8

Shipped in the current stable **[v8.4.1](https://github.com/momentiq-ai/cerebe/releases/tag/v8.4.1)** binary
(and the matching `cyclone`). Full notes live on the
[Releases](https://github.com/momentiq-ai/cerebe/releases) page.

| Surface | What landed |
|---|---|
| **`cerebe watch`** | Live factory-floor TUI: rounds, critic lanes, findings, platform chip. `--json` for agents. Root picker + attach + dirty chip. **v8.4.1:** on-screen live keys, inverted selected row, picker opens without blocking on a full worktree scan. |
| **`cyclone doc`** | One verb for registered doc types (scaffold, write, list, resolve). |
| **`cyclone objectives` / `decisions` / `prove`** | Verifiable objectives, the decision ledger, and closeout proof. |
| **`cerebe review --incremental`** | Re-review only the delta since the last round of the same change. |
| **`cerebe mcp` / `skills` / `schemas` / `onboard`** | Agent stdio server, bundled skills, published JSON Schemas, repo agent-context scaffold. |

The installer still fetches the **latest stable** GitHub Release. Re-run `install.sh` to pick
up a new tag.

## For AI agents

Cerebe provides machine-readable documentation for AI tools:

- **`/llms.txt`** — structured index of all documentation pages
- **`/llms-full.txt`** — complete documentation content in markdown
- **`cerebe mcp`** — the Factory surface over stdio for MCP-speaking agents
- **`cerebe watch --json`** — the live factory floor as a stream of JSON objects

If you're building with Claude Code, Cursor, or other AI-assisted tools, these endpoints let
your tools understand the Cerebe API and the Factory loop without scraping this README.

## Resources

| Resource | Link |
|----------|------|
| Site | [cerebe.ai](https://cerebe.ai) |
| Documentation | [cerebe.ai/docs](https://cerebe.ai/docs) |
| Quickstart | [cerebe.ai/docs/getting-started/quickstart](https://cerebe.ai/docs/getting-started/quickstart) |
| `cerebe` + `cyclone` (Factory) | [github.com/momentiq-ai/cerebe/releases](https://github.com/momentiq-ai/cerebe/releases) |
| Blueprint template | [github.com/momentiq-ai/df-cerebe-template](https://github.com/momentiq-ai/df-cerebe-template) |
| Python SDK (Cognitive) | [pypi.org/project/cerebe](https://pypi.org/project/cerebe/) |
| TypeScript SDK (Cognitive) | [npmjs.com/package/@cerebe/sdk](https://www.npmjs.com/package/@cerebe/sdk) |
| Sign in | [cerebe.ai/sign-in](https://cerebe.ai/sign-in) |
| AI-readable docs | [cerebe.ai/llms.txt](https://cerebe.ai/llms.txt) |

## License

The `cerebe` and `cyclone` CLIs are **free to use** under the
[Cerebe Software License](./LICENSE) — free for any use, including commercial, but not
open source (the source is proprietary). The Python / TypeScript SDKs are published
separately under the MIT License. **Cerebe Cloud** is a managed commercial service under
its own agreement.

Cerebe is operated by Momentiq AI.

---

<p align="center">
  <a href="https://cerebe.ai">cerebe.ai</a>
</p>
