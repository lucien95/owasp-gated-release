# Build log

One entry per working session, newest first. What we set out to do, what happened, including what broke, and what comes next.

## 2026-10-22: Session 1, project set up

**Goal:** Decide the flagship and create the repository with its documentation system.

**Decisions**
- One flagship combining OWASP gates and a signed release gate ([ADR-0001](adr/0001-one-flagship-release-gate-and-owasp-pipeline.md))
- Documentation and evidence live in this repository ([ADR-0002](adr/0002-documentation-as-code-in-the-repo.md), proposed)
- A local kind cluster, not a managed cloud cluster ([ADR-0003](adr/0003-local-kind-cluster-not-managed-cloud.md))
- Repository name `owasp-gated-release`, public from the first commit

**Built**
- README, license, `.gitignore`, Gitleaks pre-commit hook (v8.30.1)
- Documentation standard, chapter template, ADR template, evidence conventions

**Evidence:** none yet. No code has run.

**What broke:** nothing yet.

**Next:** Chapter 0. Install the tools, create the kind cluster, capture the first evidence, and draft the threat model.
