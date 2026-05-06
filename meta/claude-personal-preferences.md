# Pablo's personal preferences for Claude

> Loaded at the start of every session in any Eticas project where
> Pablo is the contributor. This file holds Pablo's personal working
> preferences — things that are true regardless of which project the
> session is about, but that don't generalise to other contributors.
>
> Project-specific notes go in the project's own instructions block.
> Eticas-wide workflow lives in `Eticas-AI/ai-ops/instructions-common.md`.

---

## Working style

**Pablo works solo on his projects by default.** If a project's
instructions don't say otherwise, assume single-contributor.

**Routine updates to state files** (`STATE.md`, `INTERNAL_LOG.md`,
`TRACKER.md`, `meta/`) can go directly to `main`. Use feature
branches and PRs only for changes that are large, risky, or benefit
from a diff view — typically: changes to repo structure, project
instructions, or the canonical pattern in `ai-ops`.

When in doubt about whether a change is "routine", branch.

## Communication

**Direct recommendations over option lists.** When one option is
clearly better given what you know, recommend it — don't present a
menu and ask Pablo to pick. Pablo prefers a clear lead followed by
the rationale to a balanced presentation of alternatives that defers
the call.

**Clarifying questions only when a decision genuinely needs Pablo's
input** and you cannot recommend without it. If you have enough
context to make a defensible call, make it; if you're not sure but
the cost of being wrong is small, make it and explain. Use
clarification for genuine forks, not for hedging.

**State assumptions inline rather than asking permission.** If you
need to assume something to proceed (e.g., a default value, an
interpretation of an ambiguous request), state the assumption in
your response and continue — Pablo can correct in the next turn if
the assumption was wrong.

## End-of-session: work-log entry

In addition to the project's own end-of-session protocol (deltas to
`STATE.md`, `INTERNAL_LOG.md`, `TRACKER.md` as applicable), at the
end of meaningful sessions also propose a short entry for the
current week's file in
[`PabloAccuosto-ETICAS/work-log`](https://github.com/PabloAccuosto-ETICAS/work-log)
under `log/<year>/<year>-W<NN>.md`, in the section corresponding to
the project worked on.

Conventions for the entry:

- **Report-grade.** One to three bullets summarising what was done,
  in language suitable for a weekly report to others — not a
  conversational summary.
- **Skip if the session produced no substantive work.** Trivial
  exchanges, course corrections, debugging that didn't land
  anywhere useful: don't log.
- **Don't duplicate.** If another session in this same project
  already added an entry for the current ISO week, propose adding
  to that existing entry only if the new work meaningfully extends
  it. Otherwise skip.

The ISO week number is the one containing the current date's first
Thursday. The work-log repo's README documents the format if needed.

## Reading this file

This file is referenced from the instructions block of every project
where Pablo is the contributor. If the project's own instructions
contradict something here, the project's instructions win for that
session — but flag the discrepancy so the divergence is intentional,
not accidental.
