# Work log

Personal weekly work log across Eticas projects and other work.
Source for weekly reports.

## What this is

A weekly record of what I worked on, organised by week with sections
per project. The intended use is twofold:

- **During the week:** capture work as it happens, especially work
  that doesn't naturally land in any specific project's
  `meta/INTERNAL_LOG.md` (cross-project setup, transversal decisions,
  reading, meetings, ad-hoc requests).
- **End of week:** generate the weekly report I send by reading the
  current week's entry and, when relevant, complementing it with
  recent entries from project-specific INTERNAL_LOGs.

## Where to start

- **Current state:** [`meta/STATE.md`](meta/STATE.md) — what I'm
  working on this week and the week's pulse.
- **This week's log:** the most recent file in `log/<year>/`, named
  by ISO week (e.g. `2026-W18.md`).
- **Workflow rules and pattern alignment:**
  [`meta/README.md`](meta/README.md).

## Layout

```
work-log/
├── README.md            ← this file
├── meta/
│   ├── STATE.md         ← live "this week" view
│   └── README.md        ← workflow + deviations from the canonical pattern
└── log/
    └── 2026/
        └── 2026-WNN.md  ← one entry per ISO week
```

## Conventions

- **One file per ISO week** under `log/<year>/`.
  - ISO week 1 of a year is the week containing the first Thursday.
  - Filename: `<year>-W<NN>.md` with a zero-padded two-digit week
    number.
- **Sections per file:** project-specific sections (Career Scoops,
  Wiselook, etc.) plus optional cross-project sections (Transversal /
  Cross-project, Meetings & comms, Reading & research). Sections only
  appear if they had activity that week.
- **Append within the week, replace across weeks.** Within the
  current week, items are added as work happens. New weeks start a
  new file.
- **Commit message convention:** `log: <what changed>` for content
  added to a week's entry; `meta: <what changed>` for changes to
  `meta/` or repo structure.

## Pattern alignment

This repo follows the canonical Eticas Claude project pattern at
[`Eticas-AI/ai-ops/claude-project-pattern.md`](https://github.com/Eticas-AI/ai-ops/blob/main/claude-project-pattern.md).
It is a personal repo (not an Eticas project) but using the same
pattern keeps the workflow consistent with the projects this log
tracks.

Local deviations from the canonical pattern are documented in
[`meta/README.md`](meta/README.md).

## Status

Active. Bootstrapped 2026-05-04.
