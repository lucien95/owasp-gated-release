# ADR-0007: Run the pipeline on both versions; the vulnerable app is a known-bad test fixture

- **Status:** Proposed
- **Date:** 2026-10-22
- **Decided by:** Pending Lucien Tanyi

## Context

Security gates are only trustworthy if we can show they catch what they claim to catch. A gate that has only ever run against secure code has never been shown to fail. At the same time, a pipeline that is permanently red on `main` trains everyone to ignore red.

## Options considered

| Option | Benefits | Costs and risks |
| --- | --- | --- |
| A. Pipeline on the hardened app only | Always green; simple | Nobody can tell whether the gates actually catch anything |
| B. Pipeline on both, and the vulnerable job is allowed to fail | Shows the gates catching flaws | `main` is always red; real failures hide among expected ones |
| C. Pipeline on both, with **inverted expectations** for the vulnerable app: its job passes only if every gate *catches* its planted flaws | Proves the gates work on every run; stays green; turns red if a gate stops catching a flaw (for example, after a scanner update) | More complex: each planted flaw needs an expected finding |

## Decision

Option C, proposed. Like pressing the test button on a smoke alarm, the vulnerable app is a known-bad sample the gates must detect every time.

## Why

It turns the vulnerable app from a demo into a permanent regression test for the security gates themselves.

## Rejected alternative

Option B is how many tutorials do it. It shows the gates once, then teaches readers to ignore a red pipeline.

## Consequences

- Chapter 1 ships a deliberately ordinary pipeline (build and unit tests) that is **green on the vulnerable app**. That is the "before" picture: a green tick does not mean secure.
- From Chapter 2, each new gate adds an expected finding for the vulnerable app and a clean result for the hardened app.
- Only the hardened image is ever signed.
