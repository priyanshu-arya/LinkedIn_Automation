---
name: plan-week-substack-note
description: Use when the user asks to plan the week's Substack Notes, decide what gets posted when as short-form Substack content, or explicitly invokes /plan-week-substack-note. Assigns candidate ideas tagged for the substack-note platform from Post-Ideas/ to specific days under a ~3/week cadence, without drafting any note text.
---

# Plan Week Substack Note (Content Strategist — Substack Notes)

Substack Notes' sibling to `/plan-week-x`, simplified — Notes are more
conversational/evergreen and less tied to a specific optimal posting
window than X or LinkedIn, so day selection matters less than variety and
pacing across the week.

## Arguments

- **week** (optional) — same default rule as `/plan-week`.
- **target_count** (optional) — default **3**.

## Process

### 1. Load the candidate pool, filtered to this platform

Read `Post-Ideas/` for ideas with `substack-note` in `platforms`,
`status: candidate` (or already `selected` for another platform but not
yet claimed by this one).

### 2. Check recent history for fatigue

Scan `Content-Learnings/content-index.md` filtered to `platform:
substack-note` for the prior ~2 weeks, same window as `/plan-week`.

### 3. Pick the days

Read `Content-Learnings/playbook-substack.md`'s Notes section for an
evidenced day rule first. Otherwise spread the `target_count` slots across
the week with reasonable gaps (don't cluster all 3 on consecutive days by
default) — there's no research-backed "best time" claim to make for this
format yet, so say plainly this is just even spacing, not an optimized
schedule.

### 4. Match ideas to slots

Same tie-breaking as `/plan-week`: best fit, `rank_score` as tiebreaker.
Require at least 2 distinct categories across the week's Notes, same
variety rule.

### 5. Commit the assignment

Append `{platform: substack-note, week: <ISO week>, date: <date>}` to the
idea's `platform_schedule`. Advance `status` to `selected` if unclaimed.

### 6. Report

A table: date | idea (topic) | category | rank_score, with unfilled slots
called out plainly.

## Hard rules

- Never assign more than `target_count` (default 3) in one week.
- Never force the count — fewer filled slots is the correct outcome when
  the pool doesn't support more.
- Never draft note text here.
