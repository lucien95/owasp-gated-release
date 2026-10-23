# ADR-0002: Keep all documentation and evidence in this repository

- **Status:** Proposed
- **Date:** 2026-10-22
- **Decided by:** Pending review by Lucien Tanyi

## Context

The project is documented while it is built, step by step, with screenshots and captured output, so that a newcomer can follow it. That documentation has to stay accurate as the code changes.

## Options considered

| Option | Benefits | Costs and risks |
| --- | --- | --- |
| A. Markdown in the repo | Versioned with the code; each chapter tag contains matching docs; reviewable in pull requests | Plain formatting; screenshots add repository size |
| B. External document tool | Rich formatting, easy comments | Drifts from the code; not part of the tag a learner checks out |
| C. Generated documentation site (for example MkDocs) | Best reading experience, search, navigation | Another tool to maintain before there is content |

## Decision

Option A now. Assess Option C at the v1.0 release, generated from the same Markdown files.

## Why

Documentation that lives beside the code it describes is checked in the same pull request and tagged in the same release, so it cannot silently go stale.

## Rejected alternative

Option B, an external tool. It is fine for planning, but not as the learner's source of truth.

## Consequences

- Evidence goes in `docs/evidence/`, and text captures are preferred over screenshots to keep the repository small.
- Each chapter's definition of done includes its documentation.
