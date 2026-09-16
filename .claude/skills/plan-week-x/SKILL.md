---
name: plan-week-x
description: Use when the user asks to plan the week's X (Twitter) content, decide what gets posted when on X, or explicitly invokes /plan-week-x. Assigns candidate ideas tagged for the x platform from Post-Ideas/ to specific days under X's own cadence (default ~5/week, mix of singles and threads), without drafting any post text.
---

# Plan Week X (Content Strategist — X pipeline)

X's sibling to `/plan-week`. Same algorithm, same shared candidate pool
(`Post-Ideas/`) — only the cadence, day-heuristic, and platform filter
differ. Selection and scheduling-day decisions only; does not write post
text (that's `/write-draft-x`) and does not touch Buffer.

## Arguments

- **week** (optional) — an ISO week (e.g. `2026-W38`) or a Monday date. If
  omitted, default to the next full week from today, same rule as
  `/plan-week`.
- **target_count** (optional) — how many X posts to aim for this week.
  Default **5**. A ceiling to aim toward, not a quota to force.

## Process

### 1. Load the candidate pool, filtered to this platform

Read all Idea Notes in `Post-Ideas/` with `status: candidate` **and** `x` in
their `platforms` list. An idea with `platforms: [linkedin, x]` is eligible
here too — it just gets its own independent draft via `/write-draft-x`, not
a copy of the LinkedIn version.

### 2. Check recent history for fatigue

Scan `Content-Learnings/content-index.md`, filtered to `platform: x` rows,
for topic/format repetition in the prior ~2 weeks. Fall back to reading
`Drafts/`/`Scheduled/`/`Published-Posts/` directly (filtered to `platform:
x`) if the index is thin.

### 3. Pick the days, then apply the content-type variety rule

**Days:** read `Content-Learnings/playbook-x.md` first — if it has a
day-performance rule with real evidence (≥3 published X posts) attached,
use those days. Otherwise fall back to a starting heuristic sourced from
current (2026) X/Twitter best-posting-time research — **look this up live
via WebSearch when this skill first runs rather than reusing LinkedIn's
Tue/Thu/Sat/IST table**, since X's audience behavior and this account's own
mix of singles/threads don't necessarily match LinkedIn's pattern. Record
whatever heuristic gets sourced back into this file's own notes so future
runs don't re-research it every time, and say plainly that it's an
unvalidated starting point until `playbook-x.md` has real evidence.

**Sourced 2026-09-14** (aggregated from Buffer's and SocialPilot's 2026
studies, 700k+ and 1M+ post datasets respectively): Tuesday 9:00 AM is the
single strongest slot; Wednesday 9-10 AM is a close second; Tue-Thu overall
outperforms other weekdays; peak windows otherwise run 8-11 AM and
12-6 PM on weekdays. Starting default until `playbook-x.md` has real
evidence: **Tue/Wed/Thu 09:00 local**. This does not need re-researching on
every run — reuse this note, refresh it only if it's been a long time or
the account's own data starts contradicting it.

**Content-type & format variety:** across however many slots this run
fills, require at least 2 distinct `category`/`content_type` values, same
rule as `/plan-week`. Additionally, don't let every slot default to the
same single-vs-thread shape — `/write-draft-x` makes the final call per
idea, but flag here if the pool looks like it would produce, say, 5 threads
in a row with no singles.

### 4. Match ideas to slots

Same tie-breaking as `/plan-week`: best `category`/`content_type` fit,
`rank_score` as tiebreaker, variety rule respected. Never force a
mismatched or duplicate idea into a slot.

### 5. Commit the assignment

For each idea assigned to an X slot, append an entry to the idea's
`platform_schedule` list: `{platform: x, week: <ISO week>, date:
<date>}`. **Never touch `target_week`/`target_date`** — those belong to
`/plan-week`'s LinkedIn assignment exclusively, even for an idea that isn't
going to LinkedIn at all (they just stay blank in that case). If `status`
is still `candidate` (no platform has claimed it yet), advance it to
`selected`; if another platform already advanced it, leave `status` as-is
— `status` reflects "has at least one platform claimed this," not
"claimed by every platform in its `platforms` list."

### 6. Report

A table: date | day | idea (topic) | category | format (single/thread
judgment call, finalized at write-time) | rank_score — with unfilled slots
called out plainly, same honesty rule as `/plan-week`.

## Hard rules

- Never assign more than `target_count` (default 5) X posts in one week.
- Never force the count — fewer filled slots than target is the correct
  outcome when the pool doesn't support more.
- Never draft post text here — ideas only get a day.
- Never pick a `status: placeholder` idea, or an idea without `x` in its
  `platforms` list.
