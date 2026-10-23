# The course: OWASP-Gated Release

Eleven chapters, each one a working snapshot you can check out and run. Every chapter follows the same rhythm: **break it, catch it, fix it, prove it.**

## The story in one paragraph

A small team ships an expense-claims service: employees submit claims, managers approve them, finance pays. It has the usual flaws: an injectable query, a hard-coded secret, a container running as root. Chapter by chapter we add the gates that catch each flaw, then go further: we sign what passed, teach the cluster to refuse anything unsigned, and finally attack our own pipeline to show the cluster still holds. By the end, "the tests passed" is no longer a claim. It is signed evidence the cluster checks for itself.

## Chapters

| # | Chapter | You will see | Status |
| --- | --- | --- | --- |
| 0 | [Setup and threat model](ch-00-setup-and-threat-model.md) | A 3-node cluster on your laptop, and the attacks we plan to stop | Done |
| 1 | [Meet the vulnerable app](ch-01-meet-the-vulnerable-app.md) | Ten OWASP attacks done by hand, and a pipeline that stays green anyway | In progress |
| 2 | Secrets and code gates | The vulnerable branch blocked before it builds | Planned |
| 3 | Dependencies, images, SBOM | A known CVE and a root container flagged | Planned |
| 4 | Harden the cluster | A privileged pod rejected at the door | Planned |
| 5 | Sign and prove | An unsigned image refused by the cluster | Planned |
| 6 | The release decision and GitOps | Only the hardened version ever deploys | Planned |
| 7 | Test the running app | Information leaks found in the live service | Planned |
| 8 | Attack the pipeline | Every pipeline attack fails, with evidence | Planned |
| 9 | Observe and operate | An alert firing during a simulated incident | Planned |
| 10 | Runtime detection (optional) | A shell inside a container, detected | Planned |

## What you need

A laptop with 16 GB of RAM or more, Docker, a free GitHub account, and comfort with a terminal. No cloud account and no money.
