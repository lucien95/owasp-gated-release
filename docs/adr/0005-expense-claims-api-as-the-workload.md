# ADR-0005: The workload is an expense-claims API

- **Status:** Accepted
- **Date:** 2026-10-22
- **Decided by:** Lucien Tanyi

## Context

The project needs an application to protect. For the OWASP demonstrations to be convincing, every OWASP Top 10:2025 category must arise *naturally* from the application's features, not be bolted on. The application must also stay small, so that time goes into security rather than features, and be instantly understandable to newcomers watching a video.

## Options considered

| Option | Benefits | Costs and risks |
| --- | --- | --- |
| A. Expense-claims API: employees submit claims, managers approve, finance pays | Money gives an obvious attacker motive; roles, per-user records, search, and an approval rule produce all ten categories naturally; everyone understands it | Scope creep if real payments are added |
| B. Notes or to-do API | Simplest to build | Weak attacker motive; only about six categories arise naturally; looks like a tutorial clone |
| C. Change-approval API for production deployments | Strong motive, covers all ten categories | Its "approval" blurs with the pipeline's own approval gates, which confuses newcomers |

## Decision

Option A: one FastAPI service with PostgreSQL, three roles (employee, manager, finance), about 6–8 endpoints, synthetic data, and no frontend (Swagger UI and `curl` instead). It is built in two versions, `vulnerable` and `hardened`.

## Why

A reader immediately understands why someone would want to approve their own claim or read a colleague's reimbursements. That turns each OWASP category into a story, which is what makes the course, the articles, and the videos land.

## Rejected alternative

Option C was the closest contender: it covers every category just as well. It was rejected for clarity, not for technical reasons.

## Consequences

- Every OWASP category gets one planted flaw, the gate that catches it (or, for A06 Insecure Design, the design review and abuse test that catch it), a fix, and evidence, recorded in `VULNERABILITIES.md` from Chapter 1.
- No real payments, no frontend, and no personal data. Requests to add them are out of scope.
