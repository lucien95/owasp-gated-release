# ADR-0001: Build one flagship that combines OWASP gates with a signed release gate

- **Status:** Accepted
- **Date:** 2026-10-22
- **Decided by:** Lucien Tanyi

## Context

Two project ideas competed for the first flagship: an end-to-end OWASP pipeline (a vulnerable app caught by security gates) and a release evidence gate (only signed, policy-approved releases may run). Each alone is weaker. A vulnerable app with scanners is one of the most common DevSecOps portfolio projects, and a release gate alone has nothing vivid to stop. The OWASP Top 10:2025 now ranks Software Supply Chain Failures third (A03), which makes signing and verifying releases part of OWASP coverage.

## Options considered

| Option | Benefits | Costs and risks |
| --- | --- | --- |
| A. Merged flagship on a local cluster | One demo shows app flaws caught, signed release, and pipeline attacks refused; $0; doubles as Kubernetes exam practice | Largest scope, about 12–14 weeks; needs chapter discipline |
| B. Release gate on an existing cloud project first | Fastest strong result | Some cloud spend; no Kubernetes practice; OWASP work waits months |
| C. Classic OWASP pipeline only | Quickest visible result | Common pattern with weak differentiation |

## Decision

Option A: one flagship, built in chapters, on a local kind cluster.

## Why

The combination produces a demonstration few portfolios have: the cluster refuses anything without signed evidence, even when the pipeline is attacked. It also covers DevSecOps, software supply chain, platform, Kubernetes, and SRE skills in one coherent story.

## Rejected alternative

Option B was the fastest route to a strong result. Revisit if the local cluster cannot support a chapter's requirements.

## Consequences

- Scope must be controlled with chapters, each ending in a tag and evidence.
- The repository starts public from the first commit, so secret scanning runs from commit one.
