---
name: plan-week
description: Use when the user asks to plan the week's LinkedIn content, decide what gets posted when, run the Content Strategist, or explicitly invokes /plan-week. Assigns candidate ideas from Post-Ideas/ to specific weekdays (Mon-Fri) following the content-mix cadence in REQUIREMENTS.md, without drafting any post text.
---

# Plan Week (Content Strategist — Phase 4a)

Assigns ranked candidate ideas to specific weekdays under the 5-post
Mon–Fri cadence (REQUIREMENTS.md §7). Selection and scheduling-day decisions
only — does not write post text (that's `/write-draft`) and does not touch
Buffer or actual scheduling (that's a later phase).

## Arguments

- **week** (optional) — an ISO week (e.g. `2026-W38`) or a Monday date to
  plan for. If omitted, default to the next full Mon–Fri window from
  today's actual date (if today is on or before Sunday of a week that
  hasn't started posting yet, that week; otherwise the following week).
  Never plan into a week that already has all 5 weekdays filled with
  `status: selected` or later.

## Process

### 1. Load the candidate pool
Read all Idea Notes in `Post-Ideas/` with `status: candidate` (never
`placeholder`). Note each one's `category`, `content_type`, `format`,
`rank_score`.

### 2. Check recent history for fatigue
Look at ideas/drafts/posts from the prior ~2 weeks (`Drafts/`, `Scheduled/`,
`Published-Posts/`) for category/format repetition. Avoid assigning two
similar posts back-to-back across week boundaries, not just within the
week being planned.

### 3. Check the Playbook, then apply the weekday mix
Read `Content-Learnings/playbook.md` first. If it contains a
`Best-Performing Patterns` rule about which weekday/content-type
combinations perform better, with real evidence (post ids) attached, use
that instead of the default below for the day(s) it covers. Otherwise fall
back to this fixed starting heuristic (REQUIREMENTS.md §7):

| Day | Intended content type |
|---|---|
| Mon | Educational / tutorial |
| Tue | AI tool or emerging technology |
| Wed | High-value technical post / cheat sheet |
| Thu | Opinion / psychology / career discussion |
| Fri | Resources / lessons / practical advice |

### 4. Match ideas to slots
For each weekday, pick the unassigned candidate idea whose `category`/
`content_type` best fits that slot's intent, breaking ties by
`rank_score`. **Do not force a mismatched or duplicate idea into a slot
just to fill it.** If no good fit exists for a day, leave it unfilled.

### 5. Commit the assignment
For each idea assigned to a slot:
- `status: candidate → selected`
- `target_week`: the ISO week being planned
- `target_date`: the specific weekday date

### 6. Report
A table: date | day | idea (topic) | category | rank_score — with any
unfilled days explicitly called out, plus a one-line note on what's needed
to fill them (e.g. "no Career-category ideas in the pool — run
`/research-topic Career` then `/generate-ideas` before this slot can be
filled"). Do not soften or hide an unfilled week — an honest gap is more
useful than a forced bad fit.

## Hard rules

- Never assign more than 5 posts to Mon–Fri, and never assign to Sat/Sun
  unless the user explicitly asks for a weekend post in this invocation.
- Never draft post text here — ideas only get a day, not content.
- Never pick a `status: placeholder` idea.
