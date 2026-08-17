# Cerebe Examples

Runnable examples for **Cerebe's cognitive services** — the Memory, Knowledge, Models, and Meta-Learning APIs — through the Python and TypeScript SDKs. These show the cognitive-infrastructure slice of the Cerebe family; for the build lifecycle (Blueprint / Factory) see the [root README](../README.md) and [cerebe.ai](https://cerebe.ai).

Each example is self-contained — clone the repo, `cd` into it, follow its README, and it works. Every example lives under `examples/<topic>/<language>/`. The language subdirectory is always present (even when only one language ships today) so that deep links stay stable as more languages are added.

## Available examples

| Topic | What you'll learn | Python | TypeScript |
|-------|-------------------|:------:|:----------:|
| [RAG](./rag/) | Embed, search, hybrid-search, and manage documents using `client.rag` | [✓](./rag/python/) | — |

## Conventions

Every example ships:

- A `README.md` with a 30-second quickstart, prereqs, expected output, and troubleshooting.
- A dependency manifest (`pyproject.toml` for Python, `package.json` for TypeScript) pinning a minimum SDK version that exposes the feature it demonstrates.
- An `.env.example` template for `CEREBE_API_KEY` and `CEREBE_BASE_URL`.
- A `Makefile` with `install`, `demo`, `test`, and `clean` targets — so the UX is the same regardless of the underlying toolchain.
- A guided demo entrypoint (`demo.py` / `demo.ts`) that succeeds or fails with actionable output.
- Live-API smoke tests (no mocks, no recorded fixtures) that self-clean and skip cleanly when `CEREBE_API_KEY` isn't set.

## Getting an API key

Grab one from the [Cerebe Dashboard](https://cerebe.ai/dashboard/keys). Keys starting with `ck_live_` hit production; `ck_test_` keys hit the test environment. Put your key in a local `.env` file inside the example directory — `.env` is gitignored.

## Running an example

```bash
cd examples/rag/python
cp .env.example .env
# edit .env and paste your CEREBE_API_KEY
make install
make demo
```

Each example's README has the full walkthrough.

## Contributing a new example

1. Pick a topic folder name (kebab-case, one word or two).
2. Create `examples/<topic>/README.md` (language-agnostic overview) and `examples/<topic>/<lang>/` with all the artifacts above.
3. Pin the current-latest published SDK version in your manifest.
4. Add a row to the table in this README.
5. The scheduled CI workflow picks up new examples automatically — no workflow edits needed.
