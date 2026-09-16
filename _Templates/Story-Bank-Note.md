---
id: story-bank
type: story-bank
version: 1
last_updated: ""
---

Story Bank — the system's accumulated, direct-from-interview record of the
user's real career material: roles, receipts with real numbers, turning
points, scars, positions they'd defend, and told-out-loud stories. Populated
and updated only by `/interviewer` (Phase 15), directly from what the user
actually says — never inferred, estimated, or fabricated. Every content-
generation skill reads this instead of prompting the user mid-draft for a
specific it doesn't have.

This is a single living document (same pattern as `Content-Learnings/
playbook.md`), not one note per item — rows accumulate here over repeated
`/interviewer` runs. Each row carries a stable `id`; other notes and Post
Spine rows below reference rows by `id`, never by position, since rows are
appended, not reordered.

Rows marked `status: placeholder` in the example rows below are
hand-written schema examples, not real data — real pipeline code must
filter them out the same way every other placeholder-status note in this
vault is filtered.

## Roles

| id | title | scope | period | notes |
|---|---|---|---|---|
| role-2026-01-01--placeholder-example | PLACEHOLDER — Senior Data Engineer | Owned ingestion pipelines for 3 product teams | 2022-01–2024-06 | PLACEHOLDER EXAMPLE ROW — not real data |

## Receipts

| id | claim | real_number | context | date_added | status |
|---|---|---|---|---|---|
| receipt-2026-01-01--placeholder-example | PLACEHOLDER — cut onboarding time | 6 weeks → 9 days | New-hire data-platform onboarding, measured across 2023 cohort | 2026-01-01 | placeholder |

## Turning Points

| id | story | what_changed | date_added | status |
|---|---|---|---|---|
| turning-2026-01-01--placeholder-example | PLACEHOLDER — believed more dashboards meant more trust; a stakeholder ignored all of them during an incident | Stopped building dashboards nobody asked for; started asking what decision the dashboard needed to support first | 2026-01-01 | placeholder |

## Scars

| id | what_happened | what_it_taught | date_added | status |
|---|---|---|---|---|
| scar-2026-01-01--placeholder-example | PLACEHOLDER — shipped a migration without a rollback plan; it broke prod for 4 hours | Never ship a migration without a tested rollback, no matter the deadline pressure | 2026-01-01 | placeholder |

## Defensible Positions

| id | position | why_i_hold_it | date_added | status |
|---|---|---|---|---|
| position-2026-01-01--placeholder-example | PLACEHOLDER — most "data quality" tooling spend is wasted without an owner for each check | Watched two teams buy the same tool and get zero adoption because no one was accountable for acting on alerts | 2026-01-01 | placeholder |

## Told-Out-Loud Stories

| id | story | when_i_tell_it | date_added | status |
|---|---|---|---|---|
| story-2026-01-01--placeholder-example | PLACEHOLDER — the time a "quick fix" during an on-call incident took down a downstream billing job | Told in interviews when asked about a mistake; told to new hires during on-call training | 2026-01-01 | placeholder |

## Post Spines

| id | topic | hook_angle | story_beat | receipt_id | position_id | date_added |
|---|---|---|---|---|---|---|
| spine-2026-01-01--placeholder-example | PLACEHOLDER — data quality tooling | "Everyone bought the same tool. Only one team's alerts got acted on." | The tool wasn't the differentiator — ownership was | receipt-2026-01-01--placeholder-example | position-2026-01-01--placeholder-example | 2026-01-01 |
