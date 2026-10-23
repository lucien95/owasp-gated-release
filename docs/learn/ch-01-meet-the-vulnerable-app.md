# Chapter 1: Meet the vulnerable app

> **Status:** In progress
> **Time:** about 6 hours · **Cost:** $0 · **You will need:** the Chapter 0 cluster (`make up`), Python 3.12, Docker

## Goal

By the end of this chapter, an expense-claims API is running in your cluster, you have broken it ten different ways by hand (one for each OWASP Top 10:2025 category), and a basic pipeline still gives it a green tick.

## Why this matters

You cannot judge a security gate until you have seen the attack it is meant to stop. This chapter is the "before" picture for everything that follows. Its most important lesson is uncomfortable: **a green pipeline does not mean a secure application.**

## Concepts first

*Written as each step is built.*

## The application

An expense-claims API ([ADR-0005](../adr/0005-expense-claims-api-as-the-workload.md)). Three seeded users with synthetic data:

| User | Role | Should be able to |
| --- | --- | --- |
| `alice` | employee | Submit claims and see only her own |
| `bob` | manager | Approve or reject his team's claims, but never his own |
| `carol` | finance | See approved claims and mark them paid |

| Method and path | What it does |
| --- | --- |
| `POST /auth/login` | Username and password → access token |
| `POST /claims` | Submit a claim |
| `GET /claims` | List claims, with `?search=` |
| `GET /claims/{id}` | View one claim |
| `POST /claims/{id}/approve` | Manager approves a claim |
| `POST /claims/{id}/pay` | Finance marks a claim paid |
| `POST /claims/import` | Bulk-import claims from a file |
| `GET /health` | Liveness check for Kubernetes |

## Steps

### Step 1: Create the application skeleton and run it locally

Why: start with the smallest thing that runs, prove it works, then add to it. A single `/health` endpoint is enough to check the toolchain, the test setup, and the server before any real logic exists.

**Concepts**

- **FastAPI** is a Python web framework. You write a normal function, put a decorator such as `@app.get("/health")` above it, and FastAPI turns it into a web endpoint. It also generates interactive API documentation automatically.
- **Uvicorn** is the server that runs a FastAPI app and listens for HTTP requests. FastAPI defines *what* to answer; Uvicorn handles the network.
- **A virtual environment (`.venv`)** is a private folder of Python packages for one project, so this project's versions never clash with another's. It is listed in `.gitignore`, so it is never committed.
- **Pinned versions** (`fastapi==0.161.1`, not `fastapi`) mean every install is identical. Without pins, the same code can behave differently next month. This matters again in Chapter 3, where dependencies become an attack surface.
- **Two requirements files:** `requirements.txt` is what the app needs to *run*; `requirements-dev.txt` adds what is needed only to *test*. The production image will contain only the first, which keeps test tools out of what attackers can reach.

**The files** (in [`apps/vulnerable/`](../../apps/vulnerable/)):

| File | Purpose |
| --- | --- |
| `README.md` | A loud warning that this app is deliberately insecure |
| `requirements.txt` | Runtime dependencies, pinned |
| `requirements-dev.txt` | Adds the test tools |
| `app/main.py` | The application, with one endpoint so far |
| `tests/test_health.py` | Proves `/health` answers `{"status": "ok"}` |

**Run the test first:**

```bash
cd apps/vulnerable
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q 2>&1 | tee ../../docs/evidence/ch-01/01-01-pytest.txt
```

Expected result: `1 passed`.

**Then run the server and call it.** Start the server in one terminal:

```bash
uvicorn app.main:app --port 8000
```

`app.main:app` means "in the file `app/main.py`, use the object named `app`". Leave it running. In a second terminal, from the repository root:

```bash
curl -s http://localhost:8000/health | tee docs/evidence/ch-01/01-01-health.txt
```

Expected result: `{"status":"ok"}`.

Finally, open <http://localhost:8000/docs> in your browser. This is the interactive documentation FastAPI generated, called Swagger UI. Every endpoint we add will appear here, and Chapter 1's attacks can be run from this page as well as from `curl`.

Evidence: *pending*
2. Add the database, users, and claims (*planned*)
3. Add the endpoints, including the planted flaws (*planned*)
4. Package it as a container and run it in the cluster (*planned*)
5. Attack it by hand: ten OWASP categories (*planned*)
6. Add a basic pipeline that stays green anyway (*planned*)
7. Start `VULNERABILITIES.md` (*planned*)

## What broke

*Recorded as it happens.*
