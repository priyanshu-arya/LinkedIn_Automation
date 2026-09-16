---
name: generate-week-x
description: Use when the user asks to plan and generate this week's X (Twitter) posts end to end, wants the full weekly X pipeline run in one go, or explicitly invokes /generate-week-x. Plans the week's X angles from the shared idea pool, then generates each post/thread through its own isolated subagent, checks each against the week's X history, then runs one combined review + scheduling pass. Never pads the count to hit a quota.
---

# Generate Week X (Weekly Orchestrator — X pipeline)

`/generate-week`'s sibling for X, same per-post-subagent isolation pattern,
default target 5 (per REQUIREMENTS.md's X cadence). Reads from the **same
shared** `Post-Ideas/` pool `/generate-week` also draws from — an idea
tagged for both `x` and `linkedin` can be picked up by both orchestrators
independently without conflict, since each platform claims its own
`platform_schedule` entry rather than overwriting a shared one.

## Arguments

- **week** (optional) — passed through to `/plan-week-x`.
- **target_count** (optional) — passed through to `/plan-week-x`. Default 5.

## Process

### 1. Plan the week's X angles

Run, in order, via the Skill tool:
1. `/research-topic` with a broad scan sized for X's higher cadence — start
   at **10** given more slots need to clear dedup/verification than
   LinkedIn's weekly 8.
2. `/generate-ideas` (default range) — this is the **same shared research**
   `/generate-week` also draws from; don't re-research topics `/generate-week`
   already covered this week if it ran first — check `Post-Ideas/` for
   recent unclaimed ideas before assuming a fresh research pass is needed.
3. `/plan-week-x [week] [target_count]`.

If any slot is unfilled, run one targeted `/research-topic <pillar> 2` →
`/generate-ideas` → `/plan-week-x` retry, capped at **2** extra rounds.
Accept the honest gap after that.

### 2. Generate each post independently, one subagent at a time

For each idea now carrying an `x` entry in `platform_schedule`, **in day
order**, spawn one fresh subagent (`Agent` tool, `subagent_type:
general-purpose`, `run_in_background: false`) with:

- This slot's idea id, topic, pillar, angle, hook, sources, and its `x`
  date from `platform_schedule`.
- The topic + pillar only of every other idea assigned to X this week (and,
  if known, this week's LinkedIn/Substack picks too — cross-platform
  awareness prevents the account from saying the identical thing
  everywhere in the same week with zero differentiation).
- The current `Content-Learnings/content-index.md` contents.
- An instruction to **read and follow, directly**: `.claude/skills/
  write-draft-x/SKILL.md`, then `.claude/skills/critique-draft-x/SKILL.md`,
  then `.claude/skills/generate-visual/SKILL.md` (platform: x). Point at
  the real files, don't paraphrase their logic into the prompt.
- The same retry-on-duplicate instruction as `/generate-week` step 2,
  scoped to the X pool and capped at 2 retries total for the slot.
- An instruction to append/update one row in `content-index.md` for this
  post (with `platform: x`), same lifecycle as `/generate-week` describes.
- An instruction to report back: final status, viral_score, single/thread
  and tweet count, visual format, and whether it had to re-angle.

### 3. Combined review and scheduling

1. `/review-drafts` with no draft-id — naturally covers every
   `status: in_review` note regardless of platform, so if `/generate-week`
   also ran this session, this becomes one shared review pass rather than
   two separate ones. Run it once total per session, not once per
   orchestrator.
2. `/schedule-approved-x` once, for whatever ended up `platform: x`,
   `status: approved`.

After both, update `content-index.md`'s `status` column for each X row.

### 4. Final report

Same shape as `/generate-week`'s: a date|day|topic|category|viral_score|
format table, a week-shape line, a variety check, and final counts —
scoped to this week's X posts.

## Hard rules

- Never skip `/review-drafts` before `/schedule-approved-x`.
- Never exceed 2 retries per slot; never fall back to a weaker/duplicate
  idea to fill a day.
- Never pad the week's count.
- If `/schedule-approved-x`'s required env vars are missing, stop at that
  step and report exactly what's missing.
