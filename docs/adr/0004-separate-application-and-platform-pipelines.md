# ADR-0004: Separate application and platform pipelines; Argo CD applies both

- **Status:** Proposed
- **Date:** 2026-10-22
- **Decided by:** Pending Lucien Tanyi

## Context

The repository holds two kinds of change: application code (`apps/`), which becomes a container image, and platform configuration (`infrastructure/`: Kubernetes manifests, Kyverno policies, Argo CD settings, the kind cluster definition). The cluster runs on a laptop, so GitHub Actions cannot, and should not, reach it.

## Options considered

| Option | Benefits | Costs and risks |
| --- | --- | --- |
| A. One pipeline for everything | Simple to start | Every change runs every gate; app jobs would hold permissions to change platform policy; slow feedback |
| B. Two pipelines: application (build, scan, sign) and platform (validate, test policies); Argo CD applies from Git | Smaller blast radius per pipeline; least-privilege permissions per pipeline; faster feedback | Two workflows to maintain; shared steps must live in reusable workflows |
| C. Two pipelines where the platform pipeline applies changes directly to the cluster | Familiar push model, as in cloud Terraform pipelines | Would require exposing the local cluster or storing its credentials in CI, which is exactly what the threat model forbids (T07, A5) |

## Decision

Option B, proposed.

## Why

Pipelines are separated by what changes and what a mistake costs. An application release affects one service; a policy change affects every workload. Keeping them separate lets each pipeline hold only the permissions it needs, and keeping deployment in Argo CD means no cluster credential ever lives in CI.

## Rejected alternative

Option C. It is the right pattern when CI provisions cloud infrastructure with Terraform (plan, policy check, approval, apply), and a later cloud project will use it. Here it would break the trust model.

## Consequences

- `app-ci.yml` runs on changes under `apps/`; `platform-ci.yml` runs on changes under `infrastructure/`.
- The platform pipeline never applies anything: it validates manifests, tests policies, and scans configuration.
- Argo CD is the only component that changes what runs in the cluster.
