# Contributing to Cerebe

Thanks for your interest in Cerebe. This repository is the public front door for the
Cerebe family — the build lifecycle (Cerebe Blueprint, Cerebe Plan, Cerebe Factory) and
the cognitive infrastructure it rests on (Cerebe Memory, Cerebe Knowledge, Cerebe Models,
Cerebe Meta-Learning). What lives *here* is the public-facing surface: examples, the
front-door docs,
and — as it consolidates — the free-to-use `cerebe` CLI and its distribution. (The
`cerebe` CLI is free to use but not open source; the SDKs are MIT — see the README.)

## Where things live

- **Cognitive API + SDKs** (`cerebe` on PyPI, `@cerebe/sdk` on npm) — the runnable
  surface. Report SDK/API issues here via the issue templates.
- **Examples** ([`examples/`](./examples/)) — clone-and-run walkthroughs. New examples
  are welcome; see [`examples/README.md`](./examples/README.md) for conventions.
- **The `cerebe` CLI** — the free build-lifecycle tool. Its home is consolidating here;
  follow [cerebe.ai](https://cerebe.ai) for status.

## How to contribute

1. **Open an issue first** for anything beyond a typo or a docs fix — it saves you
   building something we can't take.
2. **Fork and branch.** Branch names: `<your-handle>/<short-slug>`.
3. **Keep PRs focused.** One logical change per PR. Fill out the PR template.
4. **Sign your work.** By contributing (to the examples or docs here) you grant Momentiq
   AI a perpetual, worldwide, royalty-free license to use, modify, and distribute your
   contribution as part of Cerebe.
5. **Be excellent to each other.** Assume good faith; keep discussion technical.

## Development

Each example is self-contained with its own README, dependency manifest, and live-API
smoke tests. There is no repo-wide build step today. To run an example:

```bash
cd examples/rag/python
cp .env.example .env   # paste your CEREBE_API_KEY
make install
make demo
```

## Reporting security issues

**Do not open a public issue for a security vulnerability.** See [SECURITY.md](./SECURITY.md).

## Questions

- Docs: [cerebe.ai/docs](https://cerebe.ai/docs)
- Account / billing: support@cerebe.ai
