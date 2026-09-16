---
name: generate-week-substack
description: Use when the user asks to plan and generate this week's Substack content end to end (1 article + a few Notes), wants the full weekly Substack pipeline run in one go, or explicitly invokes /generate-week-substack. Plans the week's Substack angles from the shared idea pool, generates the article and each Note through isolated subagents, then runs one combined review pass and hands approved items to /publish-substack for manual publishing.
---

# Generate Week Substack (Weekly Orchestrator — Substack pipeline)

`/generate-week`'s sibling for Substack, covering both formats in one run:
one Article (default target 1/week) and several Notes (default target 3/
week). Same shared `Post-Ideas/` pool as the other two orchestrators.
Never approves or schedules/publishes anything itself — only sequences the
skills that do, ending at `/publish-substack`'s manual handoff instead of a
Buffer call.

## Arguments

- **week** (optional) — passed through to both planning skills.
- **article_count** (optional) — passed to `/plan-week-substack-article`.
  Default 1.
- **note_count** (optional) — passed to `/plan-week-substack-note`. Default 3.

## Process

### 1. Plan the week's Substack angles

1. `/research-topic` — reuse this week's existing research/idea pool if
   `/generate-week` or `/generate-week-x` already ran; otherwise run a
   scan sized for one deep article + a few lighter Notes (start at **6**).
2. `/generate-ideas` (default range).
3. `/plan-week-substack-article [week]` — may honestly find no idea deep
   enough this week; that's a valid outcome, not a failure.
4. `/plan-week-substack-note [week] [note_count]`.

If the Notes slots come up short, run one targeted `/research-topic
<pillar> 2` → `/generate-ideas` → `/plan-week-substack-note` retry, capped
at 2 extra rounds. The Article slot does not get a forced retry loop — an
empty article slot this week is reported honestly, not chased.

### 2. Generate the article, if one was assigned

One subagent (`Agent` tool, `general-purpose`, `run_in_background: false`)
given the idea's full context (same shape as `/generate-week`'s subagent
briefing) and instructed to **read and follow directly**: `.claude/skills/
write-draft-substack-article/SKILL.md`, then `.claude/skills/
critique-draft-substack-article/SKILL.md`, then `.claude/skills/
generate-visual-substack-article/SKILL.md`. Same retry-on-duplicate
instruction as `/generate-week`, capped at 2 retries. Append/update its
`content-index.md` row (`platform: substack-article`).

### 3. Generate each Note, one subagent at a time, in day order

Same per-slot subagent pattern as `/generate-week-x`, pointed at
`.claude/skills/write-draft-substack-note/SKILL.md` then `.claude/skills/
critique-draft-substack-note/SKILL.md` then `.claude/skills/
generate-visual/SKILL.md` (platform: substack-note). Same 2-retry cap.
Append/update `content-index.md` rows (`platform: substack-note`).

### 4. Combined review, then manual-publish handoff

1. `/review-drafts` with no draft-id — shared across whatever orchestrators
   ran this session, run once total.
2. `/publish-substack` once, for whatever ended up `status: approved` with
   `platform` in {`substack-article`, `substack-note`}. This produces
   copy-ready `Substack-Ready/` notes and asks the user, per item, whether
   it's actually been published — it does not assume publication happened.

After both, update `content-index.md`'s `status` for each Substack row.

### 5. Final report

A table (article + Notes together): date | platform | topic | category |
viral_score | visual format — plus a variety check and final counts
(scheduled has no Buffer meaning here; report ready_to_publish vs.
confirmed-published counts instead).

## Hard rules

- Never skip `/review-drafts` before `/publish-substack`.
- Never call any Substack API — `/publish-substack` is manual by design.
- Never mark anything published without the user's explicit confirmation
  during `/publish-substack`.
- Never exceed 2 retries per slot; never pad the week's counts, for either
  the article or the Notes.
