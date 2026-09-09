---
name: plan-week
description: Use when the user asks to plan the week's LinkedIn content, decide what gets posted when, run the Content Strategist, or explicitly invokes /plan-week. Assigns candidate ideas from Post-Ideas/ to specific days under a flexible, quality-gated weekly cadence (default 3/week, Tue/Thu/Sat starting heuristic) per REQUIREMENTS.md §5, without drafting any post text.
---

# Plan Week (Content Strategist — Phase 4a, revised Phase 13)

Assigns ranked candidate ideas to specific days under the flexible weekly
cadence (REQUIREMENTS.md §5). Selection and scheduling-day decisions
only — does not write post text (that's `/write-draft`) and does not touch
Buffer or actual scheduling (that's a later phase).

## Arguments

- **week** (optional) — an ISO week (e.g. `2026-W38`) or a Monday date to
  plan for. If omitted, default to the next full week from today's actual
  date (if today is on or before Saturday of a week that hasn't started
  posting yet, that week; otherwise the following week). Never plan into a
  week that already has `target_count` slots filled with `status: selected`
  or later.
- **target_count** (optional) — how many posts to aim for this week.
  Default **3**. This is a ceiling to aim toward, not a quota to force —
  see the hard rules below.

## Process

### 1. Load the candidate pool
Read all Idea Notes in `Post-Ideas/` with `status: candidate` (never
`placeholder`). Note each one's `category`, `content_type`, `format`,
`rank_score`.

### 2. Check recent history for fatigue
First scan `Content-Learnings/content-index.md` (fast, compact) for
category/format/topic repetition in the prior ~2 weeks. For anything it
flags as close, confirm against the actual note (`Drafts/`, `Scheduled/`,
`Published-Posts/`). Avoid assigning two similar posts back-to-back across
week boundaries, not just within the week being planned. If
`content-index.md` doesn't exist yet or is still thin, fall back to reading
the folders directly, as before.

### 3. Pick the days, then apply the content-type variety rule
**Days:** read `Content-Learnings/playbook.md` first. If it has a
`Best-Performing Patterns` rule about which specific days perform better,
with real evidence (post ids, ≥3 published posts) attached, use those days
instead of the default below. Otherwise fall back to the starting
heuristic (REQUIREMENTS.md §5): **Tue, Thu, Sat**, trimmed to
however many slots `target_count` actually calls for (e.g. `target_count:
2` → Tue/Thu). Sunday is never used unless explicitly requested this
invocation.

**Content-type variety:** unlike the old fixed Mon–Fri table, a specific
content type is no longer bound to a specific day. Instead, across however
many slots this run fills, require at least 2 distinct `category`/
`content_type` values among them (checked against the Playbook's evidenced
patterns first, this variety rule otherwise) — don't let 3 slots
accidentally all be the same content type.

### 4. Match ideas to slots
For each day slot, pick the unassigned candidate idea whose `category`/
`content_type` best fits, breaking ties by `rank_score`, while keeping the
variety rule from step 3 satisfied across the slots filled so far. **Do not
force a mismatched or duplicate idea into a slot just to fill it.** If no
good fit exists for a slot, leave it unfilled.

### 5. Commit the assignment
For each idea assigned to a slot:
- `status: candidate → selected`
- `target_week`: the ISO week being planned
- `target_date`: the specific date

### 6. Report
A table: date | day | idea (topic) | category | rank_score — with any
unfilled slots explicitly called out, plus a one-line note on what's needed
to fill them (e.g. "no Career-category ideas in the pool — run
`/research-topic Career` then `/generate-ideas` before this slot can be
filled"). If fewer than `target_count` slots ended up filled because the
pool genuinely didn't support more distinct, valuable angles, say that
plainly too — that is the correct outcome, not a shortfall to apologize
for.

## Hard rules

- Never assign more than `target_count` (default 3) posts in one week, and
  never assign to Sunday unless the user explicitly asks for it this
  invocation. Saturday is in scope by default.
- **Never force the count.** Filling fewer slots than `target_count` because
  nothing else cleared the bar is the correct, expected outcome — never pick
  a weak or duplicate idea just to reach the target.
- Never draft post text here — ideas only get a day, not content.
- Never pick a `status: placeholder` idea.
