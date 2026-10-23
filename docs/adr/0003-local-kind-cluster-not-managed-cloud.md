# ADR-0003: Run the lab on a local kind cluster instead of a managed cloud cluster

- **Status:** Accepted
- **Date:** 2026-10-22
- **Decided by:** Lucien Tanyi

## Context

The lab needs real Kubernetes behaviour, including admission control, RBAC, and NetworkPolicy. The budget target is $0–$20 a month, learners should be able to rebuild it without a cloud account, and it doubles as practice for the Certified Kubernetes Administrator exam.

## Options considered

| Option | Benefits | Costs and risks |
| --- | --- | --- |
| A. kind (Kubernetes in Docker) on a laptop | $0; anyone can reproduce it; full control of the cluster, as the exam requires | Not a production environment; limited by laptop memory; some kernel-level tools may not run |
| B. A managed cloud cluster (for example GKE Autopilot) | Real cloud networking and identity | Ongoing cost; learners need a billing account; less control over cluster internals |
| C. Docker Compose, no Kubernetes | Simplest | No admission control, RBAC, or NetworkPolicy; the core of the lab would be impossible |

## Decision

Option A, a three-node kind cluster.

## Why

It keeps the lab free and reproducible by anyone, and it is the environment where the cluster-level controls this project depends on can be practised hands-on.

## Rejected alternative

Option B. Revisit for a later project that needs real cloud identity, networking, or cost data.

## Consequences

- The README states clearly that this is a laboratory, not production.
- Runtime detection (Chapter 10) depends on a spike to confirm it works on Docker for Mac.
