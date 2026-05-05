# State — Pablo's work log

> Live view of the current week. Edit in place; don't append history
> (that's what `log/<year>/<year>-WNN.md` is for).

**Current week:** 2026-W19 (May 04 – May 10, 2026)
**Last updated:** 2026-05-05

---

## This week's focus

Monday opened as a *plumbing day*: pattern alignment across the
Eticas project repos and consolidation of the work setup itself
(project knowledge cleanup, M365 connector configuration, this
work-log repo bootstrap). Tuesday shifted to post-release work on
the risk taxonomy: documentation refresh, an internal nav fix, the
taxonomy itself adopting the Claude project pattern, and
incorporating a stress-test review with corrections for the next
release. v0.3.0 itself shipped last week.

Wiselook content remains paused on partner API credentials. Career
Scoops has no active client work.

## Active across projects

| Project | Status this week | Notes |
|---|---|---|
| Career Scoops audit | Repo bootstrap complete + pattern aligned | No client activity. Awaiting any Gates follow-up signal. |
| Wiselook audit | Pattern aligned; awaiting partner API credentials | Repo bootstrap and rename to `meta/` completed Monday May 04. No audit-content activity this week — Phase 1 (Bias & Fairness) blocked on partner API credentials from Wiselook (requested 27 April, reminded 29 April). |
| Risk taxonomy | Post-release work + Claude pattern adoption | Two PRs merged this week: documentation refresh and internal nav fix. Claude project pattern adoption underway (the repo gets `meta/`; new dedicated Claude project on Eticas Team account). Validation review and TC260+CoE proposal queued for next release. Cloudflare migration scheduled for next week. v0.3.0 itself shipped last week. |
| ai-ops (transversal) | Pattern stable; in use across three projects | Pattern was stabilised last week. Career Scoops and Wiselook were aligned then; risk taxonomy aligning this week. |
| Work log (this repo) | Bootstrapped Monday May 04 | First week's entry written for W19. |

## What's coming up

- Apply the updated project Claude instructions to Career Scoops
  (Pablo's manual step in the UI). → Done Monday May 04.
- Reset Claude memory entries (Pablo's manual step). → Done Monday
  May 04.
- Clean up project knowledge for Career Scoops (delete the 9 legacy
  files).
- Apply the work-log Personal customisation bullet to Wiselook's
  project instructions. → Done Monday May 04.
- Continue Wiselook Phase 1 work once partner API credentials land
  (or in parallel: vignette drafting for the 5 ECOs).
- Apply `meta/` folder and instructions block to `ai-risk-taxonomy`.
  Update the inventory entry in `Eticas-AI/ai-ops/inventory.md`.
- Create the new Claude project for risk taxonomy on the Eticas Team
  account. Paste the instructions block. Validate with a
  session-start prompt; verify Claude enters via `meta/STATE.md` in
  the order specified by the instructions.
- Cloudflare migration setup for `ai-risk-taxonomy` (~2 hours,
  scheduled for next week). Make repo private; configure GitHub
  Actions to deploy outputs to Cloudflare Pages; configure Cloudflare
  Access on `/risk-internal/`.

## Where to look

- Current week's entry: [`log/2026/2026-W19.md`](../log/2026/2026-W19.md).
- Workflow rules and conventions: [`meta/README.md`](README.md).

## Pulse

The week opened with a *plumbing day*: lots of structural changes
that produced no client-facing output but make future work easier.
Tuesday shifted toward post-release work on the risk taxonomy —
documentation refresh, internal nav fix, the migration to the
Claude project pattern (the operational layer the other projects
already use), and incorporation of a stress-test review for the
next release. v0.3.0 itself shipped last week. Wiselook content
remains blocked on partner API credentials; Career Scoops has no
active work. The rest of the week is open.
