# Chapter 0: Setup and threat model

> **Status:** In progress
> **Time:** about 2 hours · **Cost:** $0 · **You will need:** a Mac or Linux laptop with 16 GB of RAM or more, Docker, Homebrew (on macOS), and a GitHub account

## Goal

By the end of this chapter you have a protected repository, a three-node Kubernetes cluster running on your laptop, and a written list of the attacks this project will stop.

## Why this matters

Security work that starts with tools tends to protect the wrong things. This chapter starts by protecting the repository itself, because it is public from the first commit, and then writes down what we are defending against before writing any application code.

## Concepts first

- **Pre-commit hook.** A script Git runs on your machine before it records a commit. Ours runs Gitleaks, which refuses the commit if it finds something that looks like a password or key. It works like a metal detector at the door: cheap, fast, and it stops the obvious mistakes before they leave the building.
- **kind (Kubernetes in Docker).** Runs a real Kubernetes cluster as Docker containers on your laptop. Each "node" is a container. It is not production, but it behaves like Kubernetes where it matters for this course: admission control, RBAC, and network policy.
- **Threat model.** A short written answer to four questions: what are we building, what can go wrong, what will we do about it, and did we do a good job? Writing it first keeps the later chapters honest.

## Before you start

You should have cloned or created this repository, and `git log --oneline` should show at least one commit.

## Steps

### Step 1: Install the secret-scanning hook and scan what is already published

Why: the hook only protects commits made *after* it is installed. If you skipped it, as we did on the first commit of this repository, anything already pushed was never scanned. So install it, then scan every file now.

```bash
brew install pre-commit
pre-commit install
mkdir -p docs/evidence/ch-00
pre-commit run --all-files 2>&1 | tee docs/evidence/ch-00/00-01-gitleaks-all-files.txt
```

Expected result:

```text
pre-commit installed at .git/hooks/pre-commit
Detect hardcoded secrets.................................................Passed
```

Evidence: *pending*

### Step 2: Check your tools

Why: every later chapter assumes these exact tools. Recording their versions means a reader with a different version knows where a difference might come from.

```bash
brew install kind kubectl
{ echo "docker: $(docker version --format '{{.Server.Version}}')"; kind version; kubectl version --client; } 2>&1 | tee docs/evidence/ch-00/00-02-tool-versions.txt
```

Expected result: three lines with a version for Docker, kind, and kubectl. If the Docker line shows an error, Docker Desktop (or your Docker runtime) is not running; start it and run the command again.

Evidence: *pending*

### Step 3: Create the cluster

*Planned. Written when we do it.*

### Step 4: One-command start and stop (`make up`, `make down`)

*Planned. Written when we do it.*

### Step 5: Write the threat model

*Planned. Written when we do it.*

## What broke

1. **The commit message never closed.** The `git commit -m "...` line was missing its closing quote, so the shell showed `dquote>` and kept waiting, swallowing the next commands into the message. Fix: press `Ctrl + C`, then run one command per line. Any `dquote>` or `quote>` prompt means an open quote.
2. **The first commit was pushed without the secret scan.** `pre-commit install` was skipped, so the hook never ran on the first commit. Nothing secret was in it, but the protection we claimed was not in place. Fix: Step 1 installs the hook and scans every existing file.

## Checkpoint

- [ ] `pre-commit run --all-files` passes
- [ ] Tool versions are recorded
- [ ] `kubectl get nodes` shows 3 nodes in `Ready` state
- [ ] `docs/threat-model.md` lists at least five abuse cases

## Check your understanding

1. Why does installing a pre-commit hook not protect commits that were already pushed?
2. A teammate clones this repository. Is the hook active on their machine? What would make it active?

## Next

Chapter 1: Meet the vulnerable app
