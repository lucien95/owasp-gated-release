# Documentation standard

This project is documented as it is built, so that a newcomer with a laptop and a terminal can rebuild every chapter, understand why each step exists, and see the evidence that it worked.

## Principles

1. **Evidence before prose.** A step is documented as done only after its evidence exists. Planned work is labelled *Planned*.
2. **Command, expected result, actual evidence.** Every step shows the exact command, what you should see, and the captured output or screenshot from this repo's own run.
3. **Every decision has a reason.** Significant choices get an Architecture Decision Record (ADR) with the options considered, the tradeoff, and the rejected alternative.
4. **Failures are part of the record.** Errors we hit, wrong turns, and debugging steps go in the chapter's "What broke" section and in the build log. They are often the most useful part for a learner.
5. **The newcomer test.** If a reader would need to ask a question to continue, the page is not finished.
6. **Label everything.** Lab measurement, simulated incident, synthetic traffic, estimate, or assumption: say which.
7. **Nothing confidential.** No secrets, tokens, account IDs, personal data, or employer information. Every screenshot passes the redaction checklist below.

## Where things live

| What | Where | When it is written |
| --- | --- | --- |
| Chapter guide (the learner's page) | `docs/learn/ch-NN-<topic>.md`, from `docs/learn/_TEMPLATE.md` | During the chapter, finished before the chapter's tag |
| Decisions | `docs/adr/NNNN-<title>.md`, from `docs/adr/0000-template.md` | When the decision is made, before the code that depends on it |
| Evidence | `docs/evidence/ch-NN/` | The moment it is produced |
| Session history | `docs/BUILD_LOG.md` | At the end of every working session |
| Coverage map | `VULNERABILITIES.md` | From Chapter 1, one row per planted flaw |

## Evidence types: which one to use

| Type | Use it for | Why |
| --- | --- | --- |
| **Text capture** (default) | Terminal output: commands, scan results, `kubectl` output, refusals | Searchable, diffable, small, and a reader can copy it |
| **Screenshot** | Things that only exist in a UI: GitHub Security tab, Argo CD, Grafana, ZAP reports | The only way to show them |
| **Short recording** (GIF or asciinema, 30 s or less) | Key moments: a deploy being refused, an alert firing | The "watch it happen" proof for readers and videos |

Text capture example (the `tee` saves output while you still see it):

```bash
kubectl get nodes 2>&1 | tee docs/evidence/ch-00/00-02-kind-nodes.txt
```

## Naming

`docs/evidence/ch-NN/NN-SS-short-description.ext`, where `NN` is the chapter and `SS` the step.
Example: `docs/evidence/ch-05/05-04-kyverno-refuses-unsigned-image.png`

## Screenshot workflow (macOS)

1. One-time setup: press `Cmd + Shift + 5`, open **Options**, choose **Other Location…**, and select this repo's `docs/evidence/_inbox/` folder.
2. While working: capture with `Cmd + Shift + 4` (area) or `Cmd + Shift + 4`, then `Space` (one window).
3. `_inbox/` is ignored by Git, so raw captures can never be pushed by accident.
4. At the end of a step, each capture is reviewed against the checklist, renamed with the convention, moved to `docs/evidence/ch-NN/`, and linked from the chapter page with a one-line caption saying what it proves.

## Redaction checklist (every screenshot and capture)

- [ ] No tokens, keys, passwords, or secret values, including partial ones
- [ ] No cloud account, project, or billing identifiers
- [ ] No personal email addresses or phone numbers
- [ ] No employer names, internal hostnames, or internal URLs
- [ ] No browser tabs, bookmarks, or notifications from unrelated work
- [ ] Caption states what the image proves, and whether it is a lab result

## Definition of done for a chapter

- [ ] Every step in the chapter guide has command, expected result, and linked evidence
- [ ] The "break it, catch it, fix it, prove it" sequence is shown with evidence
- [ ] Decisions made during the chapter have ADRs
- [ ] "What broke" records the real problems we hit
- [ ] A clean checkout of the chapter's tag reproduces the result
- [ ] Build log updated; README chapter table updated
- [ ] Tag `ch-NN` created

## Roles

- **Lucien** runs every command, takes screenshots, makes and approves decisions, and reviews each page against the newcomer test.
- **Claude** explains concepts and tradeoffs, drafts pages from real captured output, reviews for gaps and accuracy, and flags any claim that evidence doesn't support yet.
