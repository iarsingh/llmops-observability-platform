# llmops-observability-platform — interview questions and answers

[README](README.md) · [Project architecture](PROJECT_ARCHITECTURE.md)

Answers below use this repository’s files and implementation. They distinguish existing behavior from suggested extensions; source links let you verify each walkthrough.

## 1. What problem does llmops-observability-platform address, and what can you demonstrate?

Prompt → model → retrieval → tools → tokens/latency/cost/quality/errors.

I would demonstrate the linked implementation or examples and distinguish that evidence from any planned production features. Start with [`README.md`](README.md).

## 2. How is this repository organized?

- [`src/plat/main.py`](src/plat/main.py): Implementation or supporting configuration.
- [`src/plat/gate.py`](src/plat/gate.py): Implementation or supporting configuration.
- [`requirements.txt`](requirements.txt): Implementation or supporting configuration.
- [`tests/test_gate.py`](tests/test_gate.py): Executable checks and regression examples.
- [`.github/workflows/ci.yml`](.github/workflows/ci.yml): GitHub Actions job definitions.
- [`README.md`](README.md): Project explanations or operating notes.

[PROJECT_ARCHITECTURE.md](PROJECT_ARCHITECTURE.md) contains the component diagram and the implementation walkthrough.

## 3. Can you walk through `check` and explain the decision it makes?

The main walkthrough here is `check(body, approved=False)` in [`src/plat/gate.py`](src/plat/gate.py#L1).

```python
def check(body, approved=False):
    failed = []

    for key in ("model", "tokens", "latency_ms"):
        if body.get(key) in (None, ""): failed.append(key)
    if int(body.get("tokens") or 0) < 0: failed.append("tokens")
    return {"passed": not failed, "failed": failed, "applied": False, "approved": bool(approved)}
```

The implementation calls `body.get`, `bool`, `failed.append`, `int`. In an interview, trace those calls in execution order using a fixture input.

## 4. Where would you add input-validation tests?

Start with the handlers `healthz` in [`src/plat/main.py`](src/plat/main.py#L6), `post_check` in [`src/plat/main.py`](src/plat/main.py#L10). Use the request schema or body access in each handler to build valid, missing-field, wrong-type, and boundary inputs. I would inspect existing tests before claiming coverage.

## 5. Which test would you use to demonstrate correctness?

[`tests/test_gate.py`](tests/test_gate.py#L5) contains `test_pass_fail`:

```python
def test_pass_fail():
    assert client.post("/check", json={'model': 'local-small', 'tokens': 42, 'latency_ms': 12, 'cost_usd': 0.0, 'quality': 0.8}).json()["passed"] is True
    bad = client.post("/check", json={'model': 'local-small', 'latency_ms': 12}).json()
    assert bad["passed"] is False
    assert "tokens" in bad["failed"]
```

This is a concrete regression example from the repository. Its assertions establish that case; they do not establish behavior for every input or under production load.

## 6. What HTTP interface does the code expose?

- `GET /healthz` → `healthz` in [`src/plat/main.py`](src/plat/main.py#L6).
- `POST /check` → `post_check` in [`src/plat/main.py`](src/plat/main.py#L10).

These are literal decorators. Application/router prefixes, authentication, and middleware must be checked in the corresponding setup code.

## 7. How would you investigate data ownership and persistence?

Trace the data/configuration files and the code that reads or writes them in the component table. Identify which files are examples, which records are mutable, and which external store is actually configured. I would document those facts before discussing retention, backup, or tenant isolation.

## 8. How would another engineer reproduce your walkthrough?

Start from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

These commands follow repository manifests; environment setup and command results still need to be checked on the target machine.

## 9. What does automation verify, and what does it not prove?

Inspect [`.github/workflows/ci.yml`](.github/workflows/ci.yml) for triggers, permissions, and job commands. I would name the checks that those definitions run and show the latest run separately. A workflow definition alone does not establish a successful deployment, security review, or production SLO.

## 10. How would you present this project in a Forward Deployed Engineer interview?

Start with the user and operational problem described in [`README.md`](README.md). Explain one constraint that changes the implementation, show the linked code or example, and walk through a success case and a failure case. Agree on a measurable acceptance criterion before expanding the solution, and leave a handoff with data boundaries and rollback ownership. Any proposed production or business metric should be identified as a target until measured.

## 11. What is the input-to-output contract of `check`?

In [`src/plat/gate.py`](src/plat/gate.py#L1), `check(body, approved=False)` receives the inputs. The function computes these intermediate values:

- `failed = []`

Its result is defined by:

- `{'passed': not failed, 'failed': failed, 'applied': False, 'approved': bool(approved)}`

## 12. Which decision rules or boundary conditions should an interviewer challenge?

The implementation in [`src/plat/gate.py`](src/plat/gate.py#L1) branches on:

- `int(body.get('tokens') or 0) < 0`
- `body.get(key) in (None, '')`

A useful extension is a table-driven test that covers each condition just below, at, and above its boundary where applicable. These expressions are the current rules; changing them changes behavior and should be justified by the project’s acceptance criteria.
