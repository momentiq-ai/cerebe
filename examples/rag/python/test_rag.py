"""Live smoke tests for the RAG example.

These hit the real Cerebe API — no mocks. Each test namespaces its state
with a session ID so parallel runs don't collide, and the module-scoped
fixture cleans up after itself on both pass and fail paths.

Skips cleanly with an actionable message when CEREBE_API_KEY isn't set.
"""
from __future__ import annotations

import os
import uuid

import pytest
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("CEREBE_API_KEY", "").strip()
BASE_URL = os.environ.get("CEREBE_BASE_URL", "https://api.cerebe.ai").strip()

if not API_KEY:
    pytest.skip(
        "set CEREBE_API_KEY (e.g. in .env) to run live RAG smoke tests",
        allow_module_level=True,
    )


SESSION_ID = f"test-rag-{uuid.uuid4().hex[:8]}"


def _src(name: str) -> str:
    return f"{SESSION_ID}/{name}"


class _TrackingClient:
    """Thin wrapper so tests can record sources they created for cleanup."""

    def __init__(self, inner, created: list[str]) -> None:
        self._inner = inner
        self._created = created

    @property
    def rag(self):
        return self._inner.rag

    def track(self, source: str) -> None:
        self._created.append(source)


@pytest.fixture(scope="module")
def client():
    from cerebe import Cerebe

    c = Cerebe(api_key=API_KEY, base_url=BASE_URL)
    created: list[str] = []
    yield _TrackingClient(c, created)

    for source in created:
        try:
            c.rag.delete_document(source)
        except Exception:
            # best effort — never fail the suite on cleanup
            pass


def test_stats_reachable(client):
    """API key + base URL work end-to-end."""
    resp = client.rag.stats()
    assert resp is not None
    assert hasattr(resp, "data"), "response missing .data attribute"


def test_embed_and_list(client):
    """Embedding a doc makes it appear in list_documents."""
    source = _src("embed_and_list.md")
    client.rag.embed(
        source=source,
        content="Integration test marker — embed-and-list.",
        doc_type="markdown",
        metadata={"test": "embed_and_list"},
    )
    client.track(source)

    resp = client.rag.list_documents()
    documents = (getattr(resp, "data", {}) or {}).get("documents") or []
    sources = [d.get("source") for d in documents]
    assert source in sources, f"expected {source} in {sources[:10]}"


def test_search_finds_embedded(client):
    """Searching for a unique phrase returns the doc containing it."""
    source = _src("search_finds.md")
    marker = "zaphaelith anomaly protocol"  # a phrase that won't appear elsewhere
    client.rag.embed(
        source=source,
        content=f"This document describes the {marker} in detail.",
        doc_type="markdown",
    )
    client.track(source)

    resp = client.rag.search(marker, k=5)
    results = (getattr(resp, "data", {}) or {}).get("results") or []
    sources = [r.get("source") for r in results]
    assert source in sources, f"expected {source} in search results; got {sources}"


def test_hybrid_search_returns_score_breakdown(client):
    """hybrid_search responses carry both semantic_score and keyword_score."""
    source = _src("hybrid_score.md")
    client.rag.embed(
        source=source,
        content="Hybrid search combines semantic similarity with keyword matching.",
        doc_type="markdown",
    )
    client.track(source)

    resp = client.rag.hybrid_search(
        "hybrid search scoring", k=3, semantic_weight=0.7, keyword_weight=0.3
    )
    results = (getattr(resp, "data", {}) or {}).get("results") or []
    assert results, "expected at least one hybrid result"
    first = results[0]
    assert "semantic_score" in first, f"missing semantic_score in {list(first.keys())}"
    assert "keyword_score" in first, f"missing keyword_score in {list(first.keys())}"


def test_delete_removes_doc(client):
    """Deleting a source removes it from list_documents."""
    source = _src("delete_removes.md")
    client.rag.embed(
        source=source,
        content="Will be deleted.",
        doc_type="markdown",
    )
    client.track(source)

    client.rag.delete_document(source)
    # Once deleted, list_documents should no longer include it.
    resp = client.rag.list_documents()
    documents = (getattr(resp, "data", {}) or {}).get("documents") or []
    sources = [d.get("source") for d in documents]
    assert source not in sources, f"{source} still present after delete: {sources[:10]}"
