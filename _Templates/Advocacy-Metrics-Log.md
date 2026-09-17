---
id: YYYY-MM-DD--company-slug-metrics-log
type: advocacy-metrics-log
program_id: YYYY-MM-DD--company-slug-program
last_updated: YYYY-MM-DD
---

Advocacy Metrics Log — one shared, self-reported metrics log for the
whole team program tracked in `program_id` above, per `/plan-advocacy`
(REQUIREMENTS.md §36). **Every row is self-reported by the team member**
(screenshot-sourced), never pulled from an API — Buffer has no access to
any team member's individual LinkedIn account (REQUIREMENTS.md §12),
and this is a **permanent architectural constraint, not a TODO to fix
later**. A missing self-report is never treated as a zero — it's simply
absent from this table until the person submits it.

## Self-Reported Entries

| name | post_url | date | impressions | reactions | comments | note |
|---|---|---|---|---|---|---|

Rows accumulate here across the program's lifetime — append only, never
remove or rewrite a prior row. This table ships empty; it is filled in
only by real self-reports team members provide.

## Rollup

No entries yet.

Populated on a re-run of `/plan-advocacy` against this existing program,
computed only from whatever rows above actually exist — never inventing a
number for someone who didn't submit one:

- **Most-active contributor:** —
- **Most-engaged post (by self-reported numbers):** —
- **Participation rate:** — (# of roster members who submitted at least
  one entry / roster size — a completion-rate statistic, not an
  engagement/performance metric)
