---
name: plan-week-substack-article
description: Use when the user asks to plan this week's Substack article, decide which idea becomes the week's long-form piece, or explicitly invokes /plan-week-substack-article. Assigns one candidate idea tagged for the substack-article platform from Post-Ideas/ to a single weekly slot, without drafting any article text.
---

# Plan Week Substack Article (Content Strategist — Substack Articles)

Substack Articles' sibling to `/plan-week`, simplified for a 1/week cadence.
Same shared candidate pool (`Post-Ideas/`); only the cadence and depth
requirement differ. Selection only — does not write article text (that's
`/write-draft-substack-article`) and never touches publishing.

## Arguments

- **week** (optional) — an ISO week or Monday date. Same default rule as
  `/plan-week`.

## Process

### 1. Load the candidate pool, filtered to this platform

Read `Post-Ideas/` for `status: candidate` (or `selected` but not yet
claimed by `substack-article`) ideas with `substack-article` in
`platforms`. Prefer ideas whose depth genuinely supports 800+ words of
real substance — a thin idea that works fine as a single LinkedIn post
doesn't automatically deserve a full article. If nothing in the pool
clears that bar, say so plainly rather than stretching a shallow idea.

### 2. Check recent history for fatigue

Scan `Content-Learnings/content-index.md` filtered to `platform:
substack-article` for topic repetition in the prior ~4 weeks (a longer
window than the feed platforms, since articles are lower-frequency and a
repeat is more noticeable to subscribers).

### 3. Pick the day

Read `Content-Learnings/playbook-substack.md`'s Articles section first for
an evidenced day-performance rule (≥3 published articles). Otherwise, since
this is a new format for the account, source a starting heuristic from
real research on Substack publishing-day norms (many newsletters do better
on a consistent, predictable day — check current guidance via WebSearch
rather than assuming one) and record it back into this file once found.

### 4. Commit the assignment

Append `{platform: substack-article, week: <ISO week>, date: <date>}` to
the idea's `platform_schedule`. Advance `status: candidate → selected` if
this is the idea's first platform claim.

### 5. Report

One line: which idea, why it earns the depth of a full article (not just a
feed post), and the assigned date — or, honestly, that no idea in the pool
currently clears the depth bar and what topic area would need more
research first.

## Hard rules

- Never assign more than 1 article per week without the user explicitly
  asking for more this run.
- Never force a shallow idea into article form just to fill the slot —
  an honest "nothing qualifies this week" is the correct outcome.
- Never draft article text here.
