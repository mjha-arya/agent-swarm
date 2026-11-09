# Contributing — branch, commit and PR conventions

Small rules, applied every time. They exist so that six months from now a single question — *"what did we do on the 23rd?"* — resolves in three lookups instead of an afternoon.

## Branches

- **The branch name is always asked from Manish. Never invented.**
- Format: `YYYY-MM-DD-two-or-three-words` — ISO date first, so the branch list sorts chronologically.
- The date is when the work **starts**; a branch is not renamed if work spans days.
- Lowercase, hyphens, max ~50 characters.
- A branch exists only while work is unfinished. Merged within a week, or closed.

The refinement ID does **not** go in the branch name. It goes in the commit message.

## Commits

```
<type>(R-00X): <what changed, imperative, lower case>

<why, if not obvious>
Refs: R-001, R-006
```

`type` is one of `feat`, `fix`, `docs`, `chore`, `refactor`, `test`.

Rules:

- **One layer per commit.** Soul, spec and code have different approval requirements, so they are different commits.
- **Never change the golden set and the code in the same commit** — you lose the ability to tell improvement from an easier test.
- Every commit on `main` cites a refinement ID.

## Pull requests

Every branch gets a PR. Every PR gets **both** a title and a description, written by the agent that created the branch.

**Title** — short, concrete, readable in a list. No ticket-speak.
> Add refinement ledger with index, six records, and eval baseline

**Description** — these headings, in this order:

```markdown
## What        one or two lines
## Why         the problem it solves
## Contents    what changed, grouped, file paths
## Refinements R-00X built / backfilled
## Verification what was actually checked, with numbers
## NOT CHECKED  what was not looked at — never omit this section
## Follow-up   the next step, if any
```

The `NOT CHECKED` section is mandatory. A PR without it is not ready for review.

## Merging

- `main` holds verified work only. `agents.json` status must agree with the branch.
- **Merge commits, not squash** — individual commit SHAs stay reachable from `main`.
- Auto-delete head branches is enabled.
- **Never delete a PR.** It is the audit trail: head branch name, approvals, diff and commit list survive branch deletion.

## Recovering history

Deleting a branch deletes a pointer, not history.

```bash
gh pr list --state all --json number,title,headRefName,mergedAt
git log --oneline --graph
git show <sha> --stat
git fetch origin refs/pull/<n>/head:pr-<n>   # a PR's commits, even after merge
```
