# LLMOps & AI Observability Platform

## Overview

A small lab for observing LLM calls along the path from prompt to model, retrieval and tools, and the signals that matter at each step: tokens, latency, cost, quality and errors. A Python HTTP service exposes a health endpoint and a `POST /check` gate, and a versioned ops API under `/v1` adds workspaces, tenant isolation, job approval and audit records. Tests run with pytest in GitHub Actions.

- **Built with:** Python, pytest, GitHub Actions
- **Scope:** Laptop lab; it calls no hosted model, and cluster apply stays false until a human approves.

<!-- project-guide:start -->
## Project guide

[Project architecture](PROJECT_ARCHITECTURE.md) · [Interview questions and answers](INTERVIEW_QA.md)

Use the architecture document for the component diagram, implementation boundaries, and verification entry points. The interview guide includes source-backed answers and project walkthroughs.

### Implementation map

| Component | Responsibility |
| --- | --- |
| [`src/plat/main.py`](src/plat/main.py) | HTTP handlers: `GET /healthz`, `POST /check` |
| [`src/plat/gate.py`](src/plat/gate.py) | Functions: `check` |
| [`requirements.txt`](requirements.txt) | Implementation or supporting configuration |
| [`tests/test_gate.py`](tests/test_gate.py) | Executable checks and regression examples |
| [`.github/workflows/ci.yml`](.github/workflows/ci.yml) | GitHub Actions job definitions |
| [`README.md`](README.md) | Project explanations or operating notes |

### Local setup and verification

From the repository root (the commands follow the checked-in manifests):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

To serve the FastAPI application locally, install the server separately if it is not already available:

```bash
python -m pip install uvicorn
PYTHONPATH=src python -m uvicorn plat.main:app --reload
```

<!-- project-guide:end -->

Phase 8

Skills: traces, tokens, latency, cost, quality

Prompt → model → retrieval → tools → tokens/latency/cost/quality/errors.

```bash
pip install -r requirements.txt
pytest -q
```

Laptop proof. No hosted model. Cluster apply stays false until a human approves.

## Ops plane

Workspaces, tenant isolation, job approval, and audit live under `/v1`. Production apply is refused. See `docs/ARCHITECTURE.md`.

## Documentation checks

Project architecture, interview guides, and local source links are checked automatically on pushes and pull requests. Run the same check locally:

```bash
python3 .github/scripts/validate_project_docs.py
```

See [service improvements and local run instructions](docs/UPGRADES.md).
