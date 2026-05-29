# `meta/` — operational meta-state of the work log

This README, together with the current week's log file, is the entry
point for any session working on this repo. This file gives a session
the workflow and conventions; the most recent
`log/<year>/<year>-WNN.md` gives it what's currently in flight and
where to write.

This repo follows the canonical Eticas Claude project pattern
documented at `Eticas-AI/ai-ops/claude-project-pattern.md`. Local
deviations are listed at the bottom of this file.

## Files in this folder

- **`README.md`** — this file.

That is all. There is no `STATE.md`, no `CONTEXT.md` and no
`INTERNAL_LOG.md` here. See "Local deviations" below for the
rationale.

## Workflow

**Adding a new entry mid-week** (typical case):

1. Identify the current ISO week (e.g. 2026-W18 for the week of
   April 27 – May 03, 2026).
2. Open `log/<year>/<year>-W<NN>.md`. If it doesn't exist yet,
   create it with the standard sections (see "File template" below).
3. Append the new item under the appropriate section.
4. Commit with message `log: <project>: <what>`.

**Starting a new week**:

1. Create `log/<year>/<year>-W<NN>.md` for the new week with the
   standard sections.
2. Commit. Message: `meta: bootstrap week <year>-W<NN>`.

**Generating the weekly report**:

1. Read the current week's entry. It is the report's spine.
2. If specific projects had significant activity that didn't land in
   the entry, complement by reading the relevant project's
   `meta/INTERNAL_LOG.md` filtered by the week's dates.
3. Format for the audience (email, Teams message, etc.) — the
   in-repo entry stays in markdown.

## File template (`log/<year>/<year>-W<NN>.md`)

```markdown
# Week <year>-W<NN> (<Mon DD> – <Sun DD>)

## <Project name>
- (entries)

## <Another project>
- (entries)

## Transversal / Cross-project
- (entries that are not tied to a specific project)

## Meetings & comms
- (significant meetings, comms, decisions made elsewhere)

## Reading & research
- (papers, posts, internal docs read)
```

Sections only appear in a given week's file if they had activity that
week. There is no obligation to have all sections every week.

## Source-of-truth rule

This repo is the single source of truth for the weekly work log.
Project-specific `INTERNAL_LOG.md`s in other repos remain canonical
for project-internal session-by-session work. The two complement each
other:

- **Project `INTERNAL_LOG.md`**: what happened in a given session of
  a given project, with the level of detail useful inside that
  project.
- **This repo's weekly entries**: the cross-project view of my work,
  with the level of detail useful for the weekly report.

If a project's `INTERNAL_LOG.md` and a weekly entry contradict each
other on a fact about the project, the project's log wins. The
weekly entry should reference the project log with a short summary,
not duplicate it in detail.

## Where this repo plugs into the rest of the setup

This repo lives under my personal GitHub account
(`PabloAccuosto-ETICAS`), not under the Eticas-AI organisation.
Reasons:

- It is a personal work log, not an Eticas project. Although its
  content is largely Eticas work, the artifact itself is mine.
- The Claude GitHub MCP integration has write access to repos in this
  account, so the connector can update the log as work happens
  (verified 2026-05-04).

## Local deviations from the canonical pattern

The canonical pattern at
[`Eticas-AI/ai-ops/claude-project-pattern.md`](https://github.com/Eticas-AI/ai-ops/blob/main/claude-project-pattern.md)
defines `meta/` components as building blocks picked à la carte. The
choices here are:

### 1. No `STATE.md`

The canonical pattern uses `STATE.md` as the per-session entry point
and the home of the live, overwrite-in-place view: current focus,
standing per-project status, and what's coming up. **This repo
doesn't keep one**, for two reasons:

- **Redundancy.** The narrative "current focus" duplicated the
  current week's `log/` entry, and the standing per-project status
  duplicated state that already lives in each project's own repo
  (its `STATE.md` / `INTERNAL_LOG.md`). This log is deliberately a
  per-week *retrospective* record, not a place that re-hosts other
  projects' live state.
- **Staleness.** An overwrite-in-place file carries a real
  maintenance cost, and when it lags a session that enters through
  it gets a wrong picture — worse than having no such file. (The
  `STATE.md` that used to live here had drifted ~3 weeks before it
  was removed.)

The session entry point is therefore this `README.md` (workflow and
conventions) plus the most recent `log/<year>/<year>-WNN.md` (what's
currently in flight). Anything that would have been "what's coming
up" lives as an open bullet in the relevant week's entry until it
resolves, at which point it gets a "done" annotation in a later week.

### 2. No `INTERNAL_LOG.md`

The canonical pattern allows `INTERNAL_LOG.md` for chronological
session-by-session records. **This repo doesn't need one** because
the `log/<year>/<year>-WNN.md` files are themselves the chronological
record. Adding a session log on top of a week log would duplicate
the same information at two granularities.

### 3. No `CONTEXT.md`

The canonical pattern allows `CONTEXT.md` for stable project context
that doesn't fit `STATE.md`. **This repo doesn't need one** because
there is no static project context — each week has its own scope, and
the conventions/structure of the repo are documented in this README
rather than in a separate context file.

### 4. No `TRACKER.md`

The canonical pattern recommends `TRACKER.md` at the repo root for
decisions, action items, comms log, etc. **This repo doesn't need
one** because:

- Decisions belong to the projects whose state they affect, not to a
  personal log. Cross-project decisions of consequence go to
  `Eticas-AI/ai-ops`.
- Action items don't need a separate tracker — they live as bullets
  in the relevant week's entry until they resolve, at which point
  they get a "done" annotation in a later week.
- The comms log is a section inside the weekly entry when relevant,
  not a separate file.

### 5. The log directory is the project's actual work

In project repos, the substantive work lives in `code/`, `data/`,
`docs/`, etc. Here, the substantive work *is* the log. So `log/` is
not a side artifact — it's the centre of the repo. This is normal for
this kind of repo and not a deviation strictly speaking, but worth
noting because the layout looks unusual compared to project repos.
