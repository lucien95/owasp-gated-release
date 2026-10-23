# OWASP-Gated Release

A learning-first DevSecOps reference lab. A deliberately vulnerable service is stopped by OWASP-aligned gates; the hardened version is signed, policy-approved, and deployed; and the cluster refuses anything without signed evidence, including attempts to bypass the pipeline itself.

> **Status: Chapter 0 is done: a local three-node cluster, rebuilt on demand, and a threat model of 21 threats. The application is not built yet; Chapter 1 is next.**

## The problem

Most pipelines scan code. Far fewer can prove that what runs in the cluster is exactly what passed those scans, and fewer still defend the pipeline itself against attack. This lab builds both, in small chapters anyone can follow.

## The application

An **expense-claims API**: employees submit claims, managers approve them, finance pays them. It was chosen because every OWASP Top 10:2025 category arises naturally from its features. Money gives attackers an obvious motive, and anyone can understand why approving your own claim is a problem ([ADR-0005](docs/adr/0005-expense-claims-api-as-the-workload.md)).

## What it will demonstrate (planned)

1. A vulnerable FastAPI service is pushed: every gate catches its planted OWASP Top 10:2025 flaws, and it never reaches the cluster.
2. The hardened service is pushed: it passes, its evidence is signed, and Argo CD deploys it.
3. The pipeline is attacked (a poisoned fork pull request, a hand-built image, an over-scoped token), mapped to the OWASP Top 10 CI/CD Security Risks. The cluster still refuses, because it trusts signed evidence rather than the pipeline's word.

## Chapters

| Chapter | Topic | Status |
| --- | --- | --- |
| 0 | Setup and threat model | **Done** (`ch-00`) |
| 1 | Meet the vulnerable app | Planned |
| 2 | Secrets and code gates | Planned |
| 3 | Dependencies, images, SBOM | Planned |
| 4 | Harden the cluster | Planned |
| 5 | Sign and prove | Planned |
| 6 | The release decision and GitOps | Planned |
| 7 | Test the running app (DAST) | Planned |
| 8 | Attack the pipeline | Planned |
| 9 | Observe and operate | Planned |
| 10 | Runtime detection (optional) | Planned |

Each finished chapter becomes a Git tag (`ch-00` … `ch-10`) that you can check out and run on its own.

## How this project is documented

- [Documentation standard](docs/DOCUMENTATION_STANDARD.md): how every step, decision, and screenshot is recorded
- [Architecture Decision Records](docs/adr/): every significant decision, with the rejected alternatives
- [Threat model](docs/threat-model.md): what we protect, from whom, and the chapter that addresses each threat
- [Build log](docs/BUILD_LOG.md): what happened in each working session, including what broke
- [The course](docs/learn/README.md): the story and step-by-step chapter pages, written as each chapter is built

## Run it

Not yet. Chapter 0 adds `make up`, which creates a local cluster on your laptop. No cloud account and no cost.

## Scope and honesty

- An independent laboratory on a local kind cluster. No production users, no real traffic, and no employer code or information.
- Measurements are labelled as lab results. Simulated incidents and synthetic traffic are labelled as such.
- Planted vulnerabilities are illustrative. Real applications fail in messier ways.

## License

[MIT](LICENSE)
