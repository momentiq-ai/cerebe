"""Cerebe RAG walkthrough — embed, search, and manage documents end-to-end.

Run: `make demo` (or `uv run python demo.py`).

Pass `--verbose` to print full tracebacks on failure.
"""
from __future__ import annotations

import argparse
import os
import sys
import time
import traceback
import uuid
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

SAMPLE_DOCS_DIR = Path(__file__).parent / "sample_docs"


@dataclass
class StepResult:
    name: str
    status: str  # "ok", "fail", "skip"
    elapsed_ms: float
    note: str = ""


@dataclass
class RunState:
    console: Console
    verbose: bool
    results: list[StepResult] = field(default_factory=list)

    def record(self, name: str, status: str, elapsed_ms: float, note: str = "") -> None:
        self.results.append(StepResult(name=name, status=status, elapsed_ms=elapsed_ms, note=note))


def mask_key(key: str) -> str:
    if not key:
        return "<unset>"
    if len(key) <= 12:
        return key[:3] + "..."
    return f"{key[:8]}...{key[-3:]}"


def load_config() -> tuple[str, str]:
    load_dotenv()
    key = os.environ.get("CEREBE_API_KEY", "").strip()
    base_url = os.environ.get("CEREBE_BASE_URL", "https://api.cerebe.ai").strip()
    if not key:
        raise SystemExit(
            "CEREBE_API_KEY is not set.\n"
            "  1. Copy `.env.example` to `.env`\n"
            "  2. Paste your key (get one at https://cerebe.ai/dashboard/keys)\n"
            "  3. Re-run `make demo`"
        )
    return key, base_url


def explain_error(exc: BaseException) -> str:
    """Map common failures to actionable next steps."""
    msg = str(exc)
    name = type(exc).__name__
    lower = msg.lower()
    if "401" in msg or "unauthori" in lower or "invalid api key" in lower:
        return (
            "Authentication failed (HTTP 401). Your CEREBE_API_KEY is missing, "
            "invalid, or revoked. Check the value in `.env` and rotate it at "
            "https://cerebe.ai/dashboard/keys if needed."
        )
    if "403" in msg or "insufficient_scope" in lower or "forbidden" in lower:
        return (
            "Permission denied (HTTP 403). Your key is valid but lacks the "
            "required scope for this operation. For the RAG example you need "
            "rag:read, rag:write, and rag:delete. Update scopes at "
            "https://cerebe.ai/dashboard/keys."
        )
    if "429" in msg or "rate limit" in lower:
        return (
            "Rate limit hit (HTTP 429). Slow down or use a different key. "
            "If this happens in CI, consider a dedicated key."
        )
    if "connection" in lower or "dns" in lower or "timed out" in lower or "timeout" in lower:
        return (
            "Could not reach the Cerebe API. Check your network and verify "
            "CEREBE_BASE_URL is reachable (default https://api.cerebe.ai)."
        )
    if "404" in msg:
        return f"Got HTTP 404 — the resource was not found. Raw: {msg}"
    return f"{name}: {msg}"


# ---------------------------------------------------------------------------
# Steps
# ---------------------------------------------------------------------------

def banner(state: RunState, api_key: str, base_url: str) -> None:
    state.console.print(
        Panel.fit(
            (
                "[bold]Cerebe RAG Example[/bold]\n"
                f"base URL : [cyan]{base_url}[/cyan]\n"
                f"API key  : [cyan]{mask_key(api_key)}[/cyan]\n"
                f"sample_docs : [cyan]{SAMPLE_DOCS_DIR}[/cyan]"
            ),
            title="step 1 - config",
            border_style="blue",
        )
    )
    state.record("config", "ok", 0.0, f"base_url={base_url}")


def preflight(state: RunState, client) -> None:
    t0 = time.perf_counter()
    try:
        resp = client.rag.stats()
        data = getattr(resp, "data", {}) or {}
        elapsed = (time.perf_counter() - t0) * 1000
        state.console.print(
            Panel(
                f"[green]OK - API reachable[/green]\n"
                f"collection at start: [bold]{data}[/bold]",
                title=f"step 2 - preflight ({elapsed:.0f}ms)",
                border_style="green",
            )
        )
        state.record("preflight", "ok", elapsed, str(data))
    except Exception as exc:
        elapsed = (time.perf_counter() - t0) * 1000
        state.console.print(
            Panel(
                f"[red]FAIL - preflight failed[/red]\n{explain_error(exc)}",
                title=f"step 2 - preflight ({elapsed:.0f}ms)",
                border_style="red",
            )
        )
        if state.verbose:
            traceback.print_exc()
        state.record("preflight", "fail", elapsed, explain_error(exc))
        raise


def ingest(state: RunState, client, session_prefix: str) -> list[str]:
    t0 = time.perf_counter()
    documents = []
    for path in sorted(SAMPLE_DOCS_DIR.glob("*.md")):
        documents.append(
            {
                "source": f"{session_prefix}/{path.name}",
                "content": path.read_text(),
                "doc_type": "markdown",
                "metadata": {"example": "rag", "filename": path.name},
            }
        )

    resp = client.rag.embed_batch(documents)
    elapsed = (time.perf_counter() - t0) * 1000

    table = Table(title="Ingested documents", show_lines=False)
    table.add_column("source")
    table.add_column("chunks", justify="right")
    table.add_column("bytes", justify="right")

    data = getattr(resp, "data", {}) or {}
    per_doc = data.get("results") or data.get("documents") or []
    if not per_doc:
        for doc in documents:
            table.add_row(doc["source"], "?", str(len(doc["content"])))
    else:
        # zip by order; if lengths differ, fall back to showing what we sent
        for entry, doc in zip(per_doc, documents):
            chunks = entry.get("chunks_created") or entry.get("chunks") or "?"
            table.add_row(doc["source"], str(chunks), str(len(doc["content"])))

    state.console.print(Panel.fit(table, title=f"step 3 - ingest ({elapsed:.0f}ms)", border_style="green"))
    state.record("ingest", "ok", elapsed, f"{len(documents)} docs")
    return [d["source"] for d in documents]


def render_results(title: str, results: list[dict], elapsed_ms: float, console: Console, hybrid: bool = False) -> None:
    table = Table(title=title, show_lines=False)
    table.add_column("source", overflow="fold")
    table.add_column("snippet", overflow="fold")
    if hybrid:
        table.add_column("sem", justify="right")
        table.add_column("kw", justify="right")
        table.add_column("score", justify="right")
    else:
        table.add_column("score", justify="right")

    for row in results[:3]:
        source = row.get("source", "?")
        snippet = (row.get("content") or row.get("snippet") or "")[:140].replace("\n", " ")
        score = row.get("score")
        score_str = f"{score:.3f}" if isinstance(score, (int, float)) else str(score)
        if hybrid:
            semantic = row.get("semantic_score")
            keyword = row.get("keyword_score")
            table.add_row(
                source,
                snippet,
                f"{semantic:.3f}" if isinstance(semantic, (int, float)) else str(semantic),
                f"{keyword:.3f}" if isinstance(keyword, (int, float)) else str(keyword),
                score_str,
            )
        else:
            table.add_row(source, snippet, score_str)

    console.print(Panel.fit(table, title=f"{title} ({elapsed_ms:.0f}ms)", border_style="cyan"))


def search_phase(state: RunState, client) -> None:
    t0 = time.perf_counter()
    resp = client.rag.search("how do I authenticate with Cerebe?", k=3)
    results = (getattr(resp, "data", {}) or {}).get("results") or []
    elapsed = (time.perf_counter() - t0) * 1000
    render_results("step 4a - search", results, elapsed, state.console)
    state.record("search", "ok" if results else "fail", elapsed, f"{len(results)} results")

    t0 = time.perf_counter()
    resp = client.rag.hybrid_search(
        "nine memory types", k=3, semantic_weight=0.7, keyword_weight=0.3
    )
    results = (getattr(resp, "data", {}) or {}).get("results") or []
    elapsed = (time.perf_counter() - t0) * 1000
    render_results("step 4b - hybrid_search", results, elapsed, state.console, hybrid=True)
    state.record("hybrid_search", "ok" if results else "fail", elapsed, f"{len(results)} results")

    t0 = time.perf_counter()
    rag_md = (SAMPLE_DOCS_DIR / "rag.md").read_text()
    # Take the first non-title paragraph as the similarity query.
    parts = [p for p in rag_md.split("\n\n") if p.strip() and not p.strip().startswith("#")]
    query = parts[0][:400] if parts else rag_md[:400]
    resp = client.rag.find_similar(query, k=3)
    results = (getattr(resp, "data", {}) or {}).get("results") or []
    elapsed = (time.perf_counter() - t0) * 1000
    render_results("step 4c - find_similar", results, elapsed, state.console)
    state.record("find_similar", "ok" if results else "fail", elapsed, f"{len(results)} results")


def collection_summary(state: RunState, client) -> None:
    t0 = time.perf_counter()
    stats = client.rag.stats()
    docs = client.rag.list_documents()
    elapsed = (time.perf_counter() - t0) * 1000

    stats_data = getattr(stats, "data", {}) or {}
    docs_data = getattr(docs, "data", {}) or {}
    doc_count = len(docs_data.get("documents") or [])
    total_reported = docs_data.get("total_documents")

    state.console.print(
        Panel.fit(
            (
                f"[bold]stats[/bold]: {stats_data}\n"
                f"[bold]documents[/bold]: {doc_count} listed"
                + (f" (total_documents={total_reported})" if total_reported is not None else "")
            ),
            title=f"step 5 - collection summary ({elapsed:.0f}ms)",
            border_style="magenta",
        )
    )
    state.record("summary", "ok", elapsed)


def cleanup(state: RunState, client, sources: list[str]) -> None:
    t0 = time.perf_counter()
    deleted = 0
    failures = 0
    for source in sources:
        try:
            client.rag.delete_document(source)
            deleted += 1
        except Exception as exc:
            failures += 1
            state.console.print(f"[yellow]warn: cleanup failed for {source}: {explain_error(exc)}[/yellow]")
    elapsed = (time.perf_counter() - t0) * 1000
    status = "ok" if failures == 0 else "fail"
    state.console.print(
        Panel.fit(
            f"[green]deleted[/green]: {deleted}\n[yellow]failures[/yellow]: {failures}",
            title=f"step 6 - cleanup ({elapsed:.0f}ms)",
            border_style="green" if failures == 0 else "yellow",
        )
    )
    state.record("cleanup", status, elapsed, f"{deleted} deleted, {failures} failed")


def final_summary(state: RunState) -> int:
    table = Table(title="Summary", show_lines=True)
    table.add_column("step")
    table.add_column("status")
    table.add_column("elapsed", justify="right")
    table.add_column("notes", overflow="fold")

    exit_code = 0
    for r in state.results:
        marker = {"ok": "[green]OK[/green]", "fail": "[red]FAIL[/red]", "skip": "[yellow]SKIP[/yellow]"}.get(r.status, r.status)
        table.add_row(r.name, marker, f"{r.elapsed_ms:.0f} ms", r.note)
        if r.status == "fail":
            exit_code = 1

    state.console.print(Panel.fit(table, title="step 7 - summary", border_style="blue" if exit_code == 0 else "red"))
    return exit_code


def main() -> int:
    parser = argparse.ArgumentParser(description="Cerebe RAG walkthrough")
    parser.add_argument("--verbose", action="store_true", help="print full tracebacks on failure")
    args = parser.parse_args()

    console = Console()
    state = RunState(console=console, verbose=args.verbose)

    try:
        from cerebe import Cerebe
    except ImportError:
        console.print("[red]The `cerebe` package is not installed. Run `make install` first.[/red]")
        return 1

    api_key, base_url = load_config()
    client = Cerebe(api_key=api_key, base_url=base_url)

    banner(state, api_key, base_url)

    try:
        preflight(state, client)
    except Exception:
        return final_summary(state)

    session_prefix = f"rag-demo-{uuid.uuid4().hex[:8]}"
    sources: list[str] = []
    try:
        sources = ingest(state, client, session_prefix)
        search_phase(state, client)
        collection_summary(state, client)
    except Exception as exc:
        console.print(f"[red]{explain_error(exc)}[/red]")
        if args.verbose:
            traceback.print_exc()
        state.record("error", "fail", 0.0, explain_error(exc))
    finally:
        if sources:
            cleanup(state, client, sources)

    return final_summary(state)


if __name__ == "__main__":
    sys.exit(main())
