---
name: plan-week
description: Use when the user asks to plan the week's LinkedIn content, decide what gets posted when, run the Content Strategist/Content Planner, or explicitly invokes /plan-week. Produces a 7-day calendar VIEW (Mon-Sun) but only fills the quality-gated slots that clear the bar (default ~3/week, Tue/Thu/Sat starting heuristic) per REQUIREMENTS.md §5 -- remaining days are shown explicitly empty with a stated reason, never padded. Each filled day gets a topic, format, a hook formula (from Content-Learnings/hook-formulas.md), a posting time (per §11, overridden by playbook.md evidence), and 2-3 comment-target suggestions. Does not draft post text (that's /write-draft).
---

# Plan Week (Content Strategist / Content Planner — Phase 4a, revised Phase 13, reworked Phase 21)

Assigns ranked candidate ideas to specific days under the flexible weekly
cadence (REQUIREMENTS.md §5), then — for each slot that actually gets
filled — attaches a suggested hook formula, a posting time, and 2-3
comment targets (REQUIREMENTS.md §32), and renders the whole thing as a
full Mon-Sun calendar view with unfilled days shown explicitly empty
rather than hidden. Selection and scheduling-day decisions only — does
not write post text (that's `/write-draft`) and does not touch Buffer or
actual scheduling (that's a later phase). §32 is additive to this file's
original §5 logic: it changes nothing about which ideas get picked or how
many slots get filled, only what gets attached to a slot once it's filled
and how the result is displayed.

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

### 6. Assign a hook formula (filled slots only, REQUIREMENTS.md §32)
For each slot **filled** by step 5 — never for a slot left empty — read
`Content-Learnings/hook-formulas.md` fresh (not from memory; it grows over
time via `/extract-hook` and human promotions). Filter to `status:
canonical` rows only — a `proposed` row is not trusted for use here any
more than it is in `/write-draft`.

- **Fit check:** prefer a canonical formula whose `engagement_goals` value
  matches the idea's likely engagement goal — the same precedence
  `/write-draft` step 3 uses, but non-binding here: the idea's own goal
  field if it has one and is set, else a `Content-Learnings/playbook.md`-
  evidenced pattern for the idea's category (real post ids attached as
  evidence), else default `comments` — and whose mechanic genuinely fits
  the idea's `category`/`content_type`. A formula with no
  `engagement_goals` value is general-purpose and eligible regardless of
  goal.
- **Anti-repetition — two checks, both required:**
  1. **This week's own picks:** never assign the same `formula_id` to two
     different filled slots within the same plan produced by this run.
  2. **Recent history:** scan `Content-Learnings/content-index.md`'s
     `hook_gist` column (§15/§25.4) for the last few weeks of
     published/scheduled posts and avoid a formula whose mechanic was
     just used — judge this from the `hook_gist` text and, where a row's
     linked note is easy to open, that note's own `hook_formula` field.
     If `content-index.md` doesn't exist yet or is too thin to judge from,
     this check is a no-op — don't block on it, same fallback posture as
     step 2's fatigue check.
- **No genuine fit:** if nothing in the canonical set fits this idea's
  category/content_type (a goal mismatch alone isn't disqualifying if the
  mechanic still fits — only a real mechanic mismatch is), leave that
  slot's hook-formula cell blank in the report and say why in one line —
  never force a bad fit just to populate the column.
- This assigns a **formula suggestion**, not the finished hook line —
  `/write-draft` re-reads `hook-formulas.md` itself at drafting time and
  may pick differently if circumstances have changed by then (a new
  `proposed` formula got promoted, playbook evidence shifted, etc.).
  Nothing here binds `/write-draft`'s own step 5.

### 7. Assign a posting time (filled slots only, REQUIREMENTS.md §32)
For each filled slot, attach the time exactly as REQUIREMENTS.md §11
already specifies — pure surfacing of existing logic at planning time
instead of leaving it until `/schedule-approved`; this step adds no new
rule of its own:
- **Default:** the day's row from §11's table for whichever day step 3
  assigned this slot (e.g. Tuesday → 16:00, Thursday → 17:00, Saturday →
  09:00).
- **Override:** if `Content-Learnings/playbook.md` has a
  `Best-Performing Patterns` rule with real evidence (≥3 published posts,
  post ids attached) for a better day+time+content-type combination
  covering this slot, use that time instead — the same override step 3
  already applies when *choosing which days to use*; this step applies it
  again to the *time* attached to whichever day the slot ends up on.

### 8. Assign comment targets (filled slots only, REQUIREMENTS.md §32)
For each filled slot, attach 2-3 specific external accounts/posts to
proactively comment on that day, in this priority order:
1. `Content-Learnings/comment-targets.md`, if it exists and its
   `## Targets` table has rows — a user-maintained list (new in Phase 21,
   never system-populated). Prefer entries relevant to the slot's
   topic/category; if several are equally relevant, prefer ones not
   already used earlier in this same week's plan.
2. **Fallback**, only if (1) is missing, absent, or too thin to fill the
   slot: accounts/authors/publications that came up as sources or
   citations in the research actually backing *that slot's idea* — i.e.,
   a named author or account identifiable in the `sources[]` of the
   Research Notes the idea itself cites from that week's
   `/research-topic` runs. Never a generic outlet name with no
   identifiable account, and never a source from an unrelated topic.
3. **Neither source yields anything:** leave the field explicitly empty in
   the report with a one-line reason (e.g. "no comment-targets.md entries
   and no research-cited accounts this week") — never invent a
   plausible-sounding account or post to fill the cell. This is exactly as
   unacceptable as forcing a hook-formula fit or padding the day count.

### 9. Report
Render a **Mon-Sun calendar table**, all seven days, not just the filled
ones: `date | day | status | topic | category | format | hook formula |
posting time | comment targets | rank_score`.
- **Filled rows** (`status: filled`): every column populated from steps
  4-8.
- **Empty rows** (`status: empty`): the reason already produced for that
  gap by step 4 goes directly in the row (e.g. "no Career-category ideas
  in the pool — run `/research-topic Career` then `/generate-ideas`
  before this slot can be filled") — shown in the row itself, not buried
  in separate prose below the table. `hook formula` and `comment targets`
  are blank on every empty row by construction (steps 6 and 8 only ever
  touch filled slots) — never populate them for a day that didn't clear
  the bar.
- If fewer than `target_count` slots ended up filled because the pool
  genuinely didn't support more distinct, valuable angles, say that
  plainly in the table and in a closing line — that is the correct
  outcome per §5, not a shortfall to apologize for.

## Hard rules

- Never assign more than `target_count` (default 3) posts in one week, and
  never assign to Sunday unless the user explicitly asks for it this
  invocation. Saturday is in scope by default.
- **Never force the count.** Filling fewer slots than `target_count` because
  nothing else cleared the bar is the correct, expected outcome — never pick
  a weak or duplicate idea just to reach the target.
- Never draft post text here — ideas only get a day, not content.
- Never pick a `status: placeholder` idea.
- **Hook formulas and comment targets are attached only to filled slots**
  (REQUIREMENTS.md §32). Never invent either for an empty day, and never
  let hook-formula or comment-target scarcity be a reason to fill a slot
  that otherwise wouldn't clear the quality bar. This rule carries exactly
  the same weight as the count-padding prohibition above — it is not a
  softer, secondary concern.
