# ADR-0006: Keep the vulnerable and hardened apps as side-by-side folders

- **Status:** Accepted
- **Date:** 2026-10-22
- **Decided by:** Lucien Tanyi

## Context

The expense-claims API exists in two versions: one with planted OWASP flaws and one with each flaw fixed. Learners need to compare them, and the pipelines need to build and test both.

## Options considered

| Option | Benefits | Costs and risks |
| --- | --- | --- |
| A. Two folders: `apps/vulnerable/` and `apps/hardened/` | Both versions visible at once; one click to compare a flaw with its fix; one pipeline can test both | Duplicated code that must be kept in step |
| B. Two long-lived branches | No duplication | Readers must switch branches to compare; branch-specific pipelines; the two drift apart silently |

## Decision

Option A.

## Why

This repository exists to teach. Seeing the flawed line and the fixed line side by side is the lesson, and duplication is an acceptable price for that clarity.

## Rejected alternative

Option B suits real products, where a vulnerable version should never exist. Here the vulnerable version is a deliberate teaching artifact.

## Consequences

- Shared, harmless code (models, seed data) may later move to a common folder to limit duplication.
- The vulnerable app is never signed and never deployable once admission control exists (Chapter 5).
