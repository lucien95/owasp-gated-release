# Build log

One entry per working session, newest first. What we set out to do, what happened, including what broke, and what comes next.

## 2026-11-17 to 2026-11-18: Session 3, Chapter 1 Steps 1 to 3b

**Goal:** Build the vulnerable expense-claims API one slice at a time, planting each flaw on purpose.

**Done**
- Step 1: FastAPI skeleton with `/health` and its first test
- Step 2: PostgreSQL 18 in Docker Compose (bound to `127.0.0.1` only), `users` and `claims` tables, seed data; planted A04 (unsalted MD5 passwords)
- Step 3a: login and `/auth/me` with JWTs; planted A04 (hard-coded signing key), A07 (no token expiry), A10 (token check fails open)
- Step 3b: submit, list and view claims; planted A05 (SQL injection), A01 (any user reads any claim), A02 (debug mode leaks stack traces)
- 11 tests pass against the real database, none of them hostile: every flaw ships green

**Decisions**
- [ADR-0006](adr/0006-vulnerable-and-hardened-as-side-by-side-folders.md): vulnerable and hardened apps live side by side in `apps/`
- [ADR-0007](adr/0007-vulnerable-app-as-known-bad-fixture.md): the vulnerable app is a known-bad fixture with inverted expectations
- Step 3 split into 3a, 3b and 3c so each flaw is understood before it is attacked
- A wildcard CORS policy was dropped as a planted flaw: with bearer tokens it is a scanner finding with almost no attack behind it (reasoning on the Chapter 1 page)

**What broke**
- Commands run from the repository root instead of `apps/vulnerable` (twice: `pip`, then `docker compose`)
- `ModuleNotFoundError: No module named 'app'` with plain `pytest`; fixed with `pytest.ini`. Lesson: verify with exactly the command you document
- Gitleaks flagged a saved login response holding a real, non-expiring token; the signature was redacted instead of bypassing the hook
- `uvicorn` could not bind port 8000 because the previous server was still running old code; found with `lsof -P -i :8000`

**Next:** Step 3c (approve, pay, import: A06, A08, A09), then the container image (A03), then attack every flaw by hand on camera.

## 2026-10-22: Session 2, Chapter 0 built

**Goal:** Protect the repository, create the local cluster, and write the threat model.

**Done**
- Installed the Gitleaks hook and scanned every already-published file: passed
- Recorded tool versions: Docker 28.5.1, kind v0.33.0, kubectl v1.37.1
- Created a three-node kind cluster (Kubernetes v1.37.0); all nodes `Ready`
- Added `make up`, `make down`, `make status`; proved the cluster rebuilds from the repository alone
- Wrote the threat model v0.1: 8 assets, 7 actors, 7 trust boundaries, 21 threats

**Decisions**
- [ADR-0004](adr/0004-separate-application-and-platform-pipelines.md): separate application and platform pipelines; Argo CD is the only thing that applies changes
- [ADR-0005](adr/0005-expense-claims-api-as-the-workload.md): the workload is an expense-claims API
- [ADR-0002](adr/0002-documentation-as-code-in-the-repo.md) accepted: documentation stays as Markdown in this repository

**What broke**
- The commit command was missing its closing quote, and the shell waited at `dquote>`
- The first commit was pushed without the secret scan; fixed and verified in Chapter 0, Step 1
- `make up` printed `No kind clusters found.` into the evidence; the Makefile now discards it

**Not yet verified:** reproduction from a clean clone (scheduled before v1.0)

**Next:** Chapter 1. Build the vulnerable expense-claims API and attack it by hand.

## 2026-10-22: Session 1, project set up

**Goal:** Decide the flagship and create the repository with its documentation system.

**Decisions**
- One flagship combining OWASP gates and a signed release gate ([ADR-0001](adr/0001-one-flagship-release-gate-and-owasp-pipeline.md))
- Documentation and evidence live in this repository ([ADR-0002](adr/0002-documentation-as-code-in-the-repo.md))
- A local kind cluster, not a managed cloud cluster ([ADR-0003](adr/0003-local-kind-cluster-not-managed-cloud.md))
- Repository name `owasp-gated-release`, public from the first commit

**Built**
- README, license, `.gitignore`, Gitleaks pre-commit hook (v8.30.1)
- Documentation standard, chapter template, ADR template, evidence conventions

**Evidence:** none yet. No code has run.

**What broke**
- The commit command was missing its closing quote, so the shell waited at `dquote>` and absorbed the next commands into the message. Fixed with `Ctrl + C` and one command per line.
- `pre-commit install` was skipped, so the first commit was pushed **without** the Gitleaks scan. Nothing secret was in it, but the protection was not in place. Chapter 0, Step 1 installs the hook and scans every existing file.

**Next:** Chapter 0, starting with Step 1 (install the hook and scan what is already published). Then install the tools, create the kind cluster, capture the first evidence, and draft the threat model.
