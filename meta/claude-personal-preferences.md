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

## Pace and approval

**Pause and seek approval before pushing changes to GitHub.** This
applies to every operation that writes to a repo —
`create_or_update_file`, `push_files`, branch creation, PRs, merges,
tag/release creation. Before any such operation, Claude states the
plan (what files, what commit message, which repo, which branch)
and waits for Pablo's go-ahead. The default is one explicit
approval per push.

**Exception: explicit autonomous task.** When Pablo specifically
asks for a multi-step task to be executed without intervention
("hacé X, Y, Z y avisame al final", "ejecutá todo el flujo", or
equivalent), Claude executes the full sequence and reports at the
end. The exception requires Pablo's explicit framing, not Claude's
inference from context.

**Pace inside the session.** When uncertain whether to keep moving
or pause, ask Pablo rather than deciding unilaterally. The right
pace depends on the type of task — some work benefits from
momentum, some from breaks to process. If Claude has produced a
lot of output in one turn (multiple decisions, several drafts,
dense technical content), check in with Pablo before continuing
rather than assuming the next step is welcome.

**Reading-only and analysis steps don't need approval.** Fetching
files, running searches, triaging comments, drafting content for
review in chat: all proceed normally without per-step confirmation.
The bar applies to *writes to GitHub*, not to thinking out loud.

## Don't assume the session is ending

**Completing a task is not the same as ending the session.** A
finished task — even a substantial one — may be one step in a
larger flow Pablo has in mind. Before triggering any end-of-session
action, ask Pablo whether the session is wrapping up or whether
more work is coming. The end-of-session protocol runs once Pablo
confirms, not on Claude's inference that "this seems like a good
stopping point".

End-of-session actions covered by this rule include:

- Updates to the project's `meta/STATE.md` (priorities, recent
  decisions, PK cache state).
- New entries in the project's `meta/INTERNAL_LOG.md`.
- Entries in the work-log (`PabloAccuosto-ETICAS/work-log/log/...`).
- PK cache delivery (offering the updated cached file to be uploaded
  to project knowledge).
- Handover documents.

These are checkpoints, not chronological closures — they should be
proposed deliberately, after confirmation, rather than emitted
automatically when a piece of work appears finished.

## GitHub access (PAT)

**Behaviour: `PAT-preferred` for all repos.** At the start of every
session that may write to any GitHub repo, Claude assumes a PAT will
be used and asks Pablo to provide one in a code block. The PAT Pablo
provides is expected to cover both `Eticas-AI/*` and his personal
`PabloAccuosto-ETICAS/*` repos under a single token — Pablo prefers
one PAT per session, not two. If Pablo declines or skips, the
session falls back to the MCP connector — no second prompt.
Rationale: pushes via MCP send file content as Claude-generated
tokens (linear in file size), which is slow and expensive on
multi-file or large-file updates; PAT bypasses this. Empirically,
the MCP write tools also become unreliable beyond roughly 30 KB of
payload — silent truncation, partial commits with misleading commit
messages (the empirical threshold and failure mode are documented
in [`Eticas-AI/ai-ops/claude-project-pattern.md`](https://github.com/Eticas-AI/ai-ops/blob/main/claude-project-pattern.md)
§3). For any file near or above that size, the git CLI path is
required, not optional. The full protocol is in
[`Eticas-AI/ai-ops/instructions-common.md`](https://github.com/Eticas-AI/ai-ops/blob/main/instructions-common.md)
under "GitHub access beyond the MCP connector".

**Prefer git CLI for writes when the PAT is loaded.** Use `git`
command-line operations (`clone`, `commit`, `push`) for file-level
writes, and the GitHub REST API (via `curl` or equivalent) for
repo-level operations git can't do — opening PRs, merging PRs,
deleting branches, querying check runs. MCP write tools
(`create_or_update_file`, `push_files`, etc.) are the fallback when
neither git nor the REST API is available (e.g., PAT didn't
authenticate). Reads via MCP remain fine when convenient.

**Token rotation is Pablo's responsibility, done manually, ~daily —
not per session.** Claude does not need to remind Pablo to revoke
tokens at session end. Pablo handles rotation himself on his own
schedule (typically once per day on days he uses Claude). The only
exception: if a PAT is exposed in a way that warrants immediate
revocation (e.g., pasted as plain text outside a code block),
Claude flags it explicitly per the protocol.

This is a per-contributor scope refinement of the protocol's
default; it does not change the protocol itself.

## Trello access

**Behaviour: ask-when-needed.** Most sessions don't touch Trello. When a session needs to read or write a Trello card, Claude asks Pablo to paste the Trello API key and user token inside triple-backtick code blocks, saves them to `/home/claude/.trello_key` and `/home/claude/.trello_token` with mode 600, and calls `https://api.trello.com/1` directly via `bash_tool` + `curl`. Same handling rules as the PAT: never echo back, never write outside `/home/claude/`, shred on session close.

Trello tokens typically have no expiration set; rotation is Pablo's responsibility, done manually when needed (not per session).

**Reminder to surface proactively**: when Pablo wants to create a new Trello card for tracking a workstream (analogous to the existing Risk Taxonomy and Audit Methodology cards on `Eticas - Strategic Priorities`), Claude should mention the `create_trello_card.py` script in `PabloAccuosto-ETICAS/work-log/scripts/`. It reads a JSON spec (card name, description, labels, checklists with check items and their states) and creates the card end-to-end via the Trello REST API. The script reads credentials from a `.env` file in the working directory and falls back to shell-exported variables. Today the script only *creates* cards; extending it to *edit* existing cards (mark items complete, add/remove items, update description) is a future iteration worth proposing when it becomes useful.

**Composio Trello MCP** is an alternative when its tools surface via `tool_search`. In projects where they don't load (verified empirically 2026-05-26 from inside `Eticas-AI/ai-audit-methodology` project — the `composio-trello-mcp` skill is in `available_skills` but `TRELLO_*` / `COMPOSIO_*` slugs do not return from `tool_search`), fall through to the direct REST API. Both paths produce equivalent results.

Get credentials from https://trello.com/power-ups/admin. Three points of friction worth flagging when guiding Pablo through generation:

- An Atlassian API token from `id.atlassian.com` is **not** a Trello token. Trello uses its own auth system despite the Atlassian acquisition.
- Creating a Power-Up requires being a member (not guest) of at least one workspace. If Pablo is guest on the Eticas workspace, the fix is creating a personal workspace as the Power-Up container — tokens remain valid against the Eticas board because they are user-scoped, not workspace-scoped.
- The "Allowed origins" field on the API key page is required even for CLI-only use. `http://localhost` works.

## End-of-session: work-log entry

In addition to the project's own end-of-session protocol (deltas to
`STATE.md`, the day-log entry in `meta/log/<today>.md`, plus an ADR
or `CHANGELOG.md` entry as applicable per the project's conventions
— see [`Eticas-AI/ai-ops/claude-project-pattern.md`](https://github.com/Eticas-AI/ai-ops/blob/main/claude-project-pattern.md)
§2 for what each file holds), at the
end of meaningful sessions also propose a short entry for the
current week's file in
[`PabloAccuosto-ETICAS/work-log`](https://github.com/PabloAccuosto-ETICAS/work-log)
under `log/<year>/<year>-W<NN>.md`, in the section corresponding to
the project worked on.

The "Don't assume the session is ending" rule above applies — the
work-log entry is proposed only after Pablo confirms the session is
wrapping up.

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
