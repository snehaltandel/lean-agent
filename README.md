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

## Running the Application

The Lean Concepts Agent can be run in several ways:

### Interactive Mode (Default)
Run the agent interactively to analyze processes in real-time:
```bash
python main.py
```

### Demo Mode
See the agent in action with pre-built examples:
```bash
python main.py --demo
```

### File Analysis Mode
Analyze a process description from a text file:
```bash
python main.py --file your_process.txt
```

### Programmatic Usage
Use the tools directly in your own Python code:
```python
from app.tools.waste_detector import WasteDetector

detector = WasteDetector()
result = detector.run({
    "process_description": "Your process description here..."
})
print(result["summary"])
```

### Testing Individual Components
Run the simple demo to test the WasteDetector tool:
```bash
python simple_demo.py
```

## Roadmap Alignment

This repository bootstraps **Phase 1** of the product roadmap by shipping a
rule-based `WasteDetector` tool, prompt scaffolding, and a LangGraph skeleton that can
be extended with additional tools (VSM builder, visualisations, simulations) in later
phases.
