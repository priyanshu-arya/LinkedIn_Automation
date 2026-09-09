---
name: generate-week
description: Use when the user asks to plan and generate this week's LinkedIn posts end to end, wants the full weekly pipeline run in one go, or explicitly invokes /generate-week. Plans the week's angles, then generates each post through its own isolated subagent (independent research, draft, critique, visual prompt), checks each against the week's history before moving on, then runs one combined review session and schedules whatever gets approved. Never pads the count to hit a quota.
---

# Generate Week (Weekly Orchestrator — Phase 13)

Runs the full pipeline for a week's worth of posts (default target 3, per
REQUIREMENTS.md §5) in one invocation, without collapsing them into
variations of one template. Plans the week's angles broadly first, then
generates each post independently — its own subagent, its own research,
its own draft, its own visual concept — while still keeping each post aware
of what the rest of the week already covered. Stops for one combined human
review session before anything gets scheduled; never approves or schedules
anything itself.

## Arguments

- **week** (optional) — passed through to `/plan-week`.
- **target_count** (optional) — passed through to `/plan-week`. Default 3.

## Process

### 1. Plan the week's angles (broad, not yet deep per-post)
Run, in order, via the Skill tool:
1. `/research-topic` with a broad scan and a count sized for weekly
   diversity — start at **8**, not the skill's own ad-hoc default of 3,
   since `target_count` slots need real category spread and some
   candidates won't survive dedup/verification.
2. `/generate-ideas` (default range).
3. `/plan-week [week] [target_count]`.

If `/plan-week` reports any unfilled slot, run one targeted
`/research-topic <missing-pillar> 2` → `/generate-ideas` → `/plan-week`
retry, capped at **2** extra rounds total. After that, accept whatever
`/plan-week` actually filled — report the honest gap, don't force it.

This step produces `status: selected` Idea Notes with a `target_date` each
— real, research-backed ideas (research-topic already verifies against
primary sources before writing a note), not placeholders. What it does
*not* do is write any post text, critique anything, or think about visuals
— that's step 2, and it happens per post, independently.

### 2. Generate each post independently, one subagent at a time
For each `status: selected` idea from step 1, **in day order** (not in
parallel — each subagent must be able to see what's already been logged
by earlier posts this week), spawn one fresh subagent (`Agent` tool,
`subagent_type: general-purpose`, `run_in_background: false` so this step
stays sequential) with a self-contained prompt that gives it:

- This slot's assigned idea id, topic, pillar, angle, hook, sources, and
  target date — everything already in its Idea Note.
- The **topic + pillar only** (not full text) of every other idea assigned
  this week, so it can keep the week coherent without copying anything.
- The current contents of `Content-Learnings/content-index.md` (read it
  yourself and paste the table in, or point the subagent at the file path —
  either works) for dedup/history context.
- An instruction to **Read and follow, directly, step by step**:
  `.claude/skills/write-draft/SKILL.md`, then
  `.claude/skills/critique-draft/SKILL.md`, then
  `.claude/skills/generate-visual/SKILL.md` — applied to its one assigned
  idea. Do not paraphrase or duplicate those skills' logic into the
  subagent prompt; point it at the real files so there's one source of
  truth.
- The **retry-on-duplicate instruction** (this is new, not in the skill
  files above): if `/critique-draft`'s step 2a fires (a genuine duplicate —
  the draft note gets left at `status: draft` with a `duplicate_flagged`
  history entry instead of advancing to `in_review`), the subagent must not
  give up or surface it as-is. Instead:
  1. Look for another unused `status: candidate` idea in the same pillar
     from the existing pool (`Post-Ideas/`). If one exists, assign it to
     this slot the same way `/plan-week` step 5 would (status → selected,
     target_week/target_date set to this slot's), and retry from
     `/write-draft`.
  2. If no usable candidate exists, run `/research-topic <pillar> 2`
     yourself, then `/generate-ideas`, then pick the strongest resulting
     idea for this slot and retry.
  3. Cap at **2 retries total** for this slot. If still stuck after that,
     stop and report this slot as genuinely unfillable this week — do not
     force a third attempt or fall back to a weaker/duplicate angle just to
     fill the day.
- An instruction to **append or update one row in
  `Content-Learnings/content-index.md`** for this post: add the row right
  after `/write-draft` creates the Draft Note (id, date, day, status:
  draft, pillar, topic, angle_summary, hook_gist), then update the same row
  after `/critique-draft` (key_examples, conclusion_type, post_format,
  viral_score, status) and after `/generate-visual` (visual_format,
  image_concept).
- An instruction to report back concisely: final status (in_review /
  unfillable), viral_score, visual format + one-line image concept, and
  whether it had to re-angle (and why).

### 3. Combined review and scheduling
Once every slot has been processed (some may have ended up genuinely
unfilled — that's fine), run:
1. `/review-drafts` with no draft-id — it already loops every
   `status: in_review` draft, so this naturally becomes one combined
   session covering however many posts made it through the quality gate.
2. `/schedule-approved` once, for whatever ended up `status: approved`.
   Scheduling stays **text-only** — the existing Buffer mutation has no
   media field, and no image-generation provider is wired in, so nothing
   about this changes; the image prompt lives only in each Visual Note.

After both steps, update `Content-Learnings/content-index.md`'s `status`
column for each row to match its real final state (approved/rejected/
scheduled) — `/review-drafts` and `/schedule-approved` don't write to the
index themselves, so mirror their outcomes in here yourself.

### 4. Final report
- A table: date | day | topic | category | viral_score | visual_format —
  covering every slot that made it to `in_review` or beyond, plus any slot
  reported unfillable and why.
- **Week-shape line**: one clause per post ("topic 1 → topic 2 → topic 3"),
  so you can sanity-check the week's arc at a glance on top of the
  per-post `/review-drafts` session.
- **Variety check**: how many distinct pillars/formats/hook styles actually
  appeared across the posts that made it through. If everything technically
  passed dedup but still reads as samey (e.g. all the same format), say so
  — this is a flag for you to weigh, not a blocking gate.
- Final counts: how many scheduled, how many approved-but-not-yet-scheduled
  (shouldn't happen given step 3 runs both), how many rejected, how many
  slots left unfillable.

## Hard rules

- Never skip `/review-drafts` before `/schedule-approved` — this skill
  never approves or schedules anything itself, only sequences the skills
  that do.
- Never let a slot's retry loop (step 2) exceed 2 retries, and never fall
  back to a weaker or duplicate idea just to fill a day.
- Never pad the week's count. Fewer genuinely distinct, valuable posts than
  `target_count` is the correct outcome when that's what the research
  supports — report it plainly, don't disguise it.
- Never attach an image to a scheduled post — no provider is configured;
  the deliverable is a prompt for you to run manually.
- If any step's required credential is missing (e.g. Buffer env vars for
  `/schedule-approved`), stop at that step and report exactly what's
  missing rather than continuing past it or skipping silently.
