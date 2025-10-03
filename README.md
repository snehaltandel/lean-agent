# Lean Concepts Agent

The Lean Concepts Agent is a LangGraph + OpenAI powered assistant that guides teams
through Lean and continuous improvement exercises. The project is organised around a
modular tool catalogue, externalised prompts, and a future-proof architecture that can
expand from a Streamlit proof-of-concept to a production deployment.

## Project Layout

- `app/agent/` – LangGraph state definitions and orchestration utilities.
- `app/tools/` – Tool implementations with strict pydantic schemas.
- `prompts/` – Versioned Jinja templates for system, planner, critic, and finaliser roles.
- `tests/` – Unit and integration tests.
- `ui/` – Placeholder for the Streamlit and future Next.js interfaces.

## Getting Started

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Run the test suite to validate tool behaviour:
   ```bash
   pytest
   ```

3. Configure environment variables in `.env` as needed (OpenAI keys, database URLs).

## Roadmap Alignment

This repository bootstraps **Phase 1** of the product roadmap by shipping a
rule-based `WasteDetector` tool, prompt scaffolding, and a LangGraph skeleton that can
be extended with additional tools (VSM builder, visualisations, simulations) in later
phases.
