.PHONY: install demo test clean help

help:
	@echo "Targets:"
	@echo "  install  Install dependencies (uv sync)"
	@echo "  demo     Run the guided RAG walkthrough"
	@echo "  test     Run live smoke tests against the real Cerebe API"
	@echo "  clean    Remove the local .venv and caches"

install:
	uv sync --extra dev

demo:
	uv run python demo.py

test:
	uv run pytest -v

clean:
	rm -rf .venv .pytest_cache __pycache__ */__pycache__
