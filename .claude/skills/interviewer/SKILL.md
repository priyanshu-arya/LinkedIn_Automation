---
name: interviewer
description: Use when the user wants to build or add to their Story Bank of real career material (roles, receipts with real numbers, turning points, scars, positions they'd defend, told-out-loud stories), wants a guided interview to extract that material, has never posted before and has no archive for other skills to learn voice/facts from, or explicitly invokes /interviewer. Runs a full onboarding interview that populates Content-Learnings/story-bank.md from scratch (or resumes it, skipping already-filled sections), or — given a topic argument — a focused single-topic interview that turns one idea into a reusable Post Spine entry, handed off to /write-draft. Never invents an answer on the user's behalf; only records what they actually say, preserving vivid phrasing verbatim rather than paraphrasing it away.
---

# Interviewer (Story Bank — Phase 15)

Interviews the user directly and keeps the answers in a single living doc,
`Content-Learnings/story-bank.md` — roles, receipts with real numbers,
turning points, scars, positions they'd defend, and told-out-loud stories —
so other content-generation skills (`/write-draft`, `/plan-week`,
`/generate-week`, and any future repurposing skill) can pull a real specific
instead of prompting the user mid-draft. This is the only skill that works
for a user with no post archive yet, since it draws on career history
directly, not prior content.

This skill never drafts, critiques, schedules, or publishes anything — it
only produces or updates the Story Bank.

*Schema adapted (not copied verbatim) from the MIT-licensed
`sergebulaev/linkedin-skills` project's `linkedin-interviewer` skill, with
local modifications for this repo's living-doc conventions (single
versioned file, `id`-keyed tables, cross-referenced Post Spines) rather than
that project's own file layout.*

## Arguments

- **topic** (optional) — if given, run **Mode B** (focused single-topic
  interview → Post Spine). If omitted, run **Mode A** (full/onboarding
  interview, default).

## Process — Mode A (full/onboarding, default)

### 1. Load or initialize the Story Bank
Check if `Content-Learnings/story-bank.md` exists.
- If yes: read it in full. For each of the six category sections (Roles,
  Receipts, Turning Points, Scars, Defensible Positions, Told-Out-Loud
  Stories), count real (non-placeholder) rows and judge it thin (0-1 real
  rows) or filled. Tell the user what's already there — section by section,
  with counts — **before** asking anything. Never re-ask a question whose
  answer is already recorded.
- If no: create it from `_Templates/Story-Bank-Note.md`, with `id:
  story-bank`, `type: story-bank`, `version: 1`, `last_updated:` today's
  date.

### 2. Run structured question rounds, one category at a time
Conversational, not a form dump — react to what the user says before moving
on. Fixed order:

1. **Roles** — what you've actually done: titles, scope, time periods.
2. **Receipts** — real numbers you can defend. Press for the actual
   number with a named referent (what/when/cost/scale) — never accept "a
   lot," "significantly," or "a huge improvement" as a final answer.
3. **Turning Points** — beliefs you abandoned, and what it cost you.
4. **Scars** — hard lessons from a reversal or failure.
5. **Defensible Positions** — contrarian views your peers would dispute,
   and their cost to hold.
6. **Told-Out-Loud Stories** — 3 narratives you already tell people
   verbally (pre-tested by real reactions, not written for the first time
   here).

### 3. Reflect and follow up, once, per answer
After each answer, reflect it back briefly in your own words to confirm you
captured it correctly. If the answer is vague (no concrete number, no named
example, no specific stakes), ask **exactly one** follow-up for
specificity — then move on regardless of whether it lands. Never loop
indefinitely on a single question; a thin answer, honestly recorded as
thin, beats stalling the interview.

### 4. Preserve vivid phrasing verbatim
When the user's own phrasing is specific or memorable, store it verbatim in
the row (in quotes if useful) rather than smoothing it into generic prose.
The system's other skills lose exactly this texture if it gets paraphrased
away here.

### 5. Write or update the Story Bank
- New file: start from `_Templates/Story-Bank-Note.md`, remove nothing,
  fill in real rows as answers come in.
- Existing file: **append new rows only**. Never silently overwrite or
  delete an existing row — a correction to a previously recorded answer is
  an explicit, user-requested edit, logged as such (note in the row or a
  trailing note what changed and why), not an automatic rewrite.
- Row `id` format: `<category-prefix>-YYYY-MM-DD--kebab-slug` (e.g.
  `receipt-2026-09-16--cut-onboarding-time`), matching the vault's existing
  `YYYY-MM-DD--kebab-slug` id convention.
- Update `last_updated` to today's date.

### 6. Report back
See "Report back" below.

## Process — Mode B (focused, `/interviewer <topic>`)

### 1. Ask 4-6 targeted questions, specific to that topic only
- The concrete story or example (not a generality).
- The number, if any (same never-accept-"a lot" discipline as Mode A).
- The tension or contrarian angle — what would most people in this space
  say, and why does the user disagree or see it differently?
- Why this matters *now* (what makes it worth posting today, not evergreen
  filler).
- 1-2 more as needed to fill gaps specific to the topic raised.

### 2. Assemble a Post Spine
A Post Spine is a compact, reusable handoff packet, not prose:
- **hook_angle** — the sharpest one-line framing of the idea.
- **story_beat** — the concrete narrative arc in a sentence or two.
- **receipt_id / position_id** — cross-reference an existing Roles/
  Receipts/Turning Points/Scars/Defensible Positions row by its `id` if
  this topic genuinely matches one already recorded; otherwise record the
  specific/position inline in the spine row itself rather than inventing a
  fake cross-reference.
- **position** — the view being defended (only if the user actually stated
  it as their own opinion — see Hard rules).
- **suggested close** — a plausible ending beat (question, call-back, or
  statement) for whoever drafts the post.

### 3. Append the spine to the same file
Add one new row under `## Post Spines` in `Content-Learnings/story-bank.md`
— never a separate scratch file. Row `id` format:
`spine-YYYY-MM-DD--kebab-slug`.

### 4. Report back
See "Report back" below.

## Report back

**Mode A:** entry counts per section (e.g. "Roles: 2, Receipts: 0, Turning
Points: 1, Scars: 1, Defensible Positions: 0, Told-Out-Loud Stories: 3").
Explicitly flag any section left thin or empty — don't bury it — e.g. "0
receipts recorded — other skills will have nothing to cite for numbers
until you add some." Never describe the interview as "complete" if any
category got zero real answers; name the gap plainly instead.

**Mode B:** show the full assembled Post Spine (all fields) and its `id`.
Tell the user it's ready to hand to `/write-draft --spine <spine_id>` —
and note explicitly that this `--spine` argument doesn't exist in
`/write-draft` yet; wiring it in is a separate, not-yet-built change to
that skill, not part of this one.

## Hard rules

- Never invent, round, estimate, or "smooth over" a number, story detail,
  or quote. Record only what was actually said — ask a follow-up instead
  of filling in a plausible-sounding value.
- Never overwrite or delete an existing entry silently. Corrections are
  explicit, user-requested, logged edits — never an automatic rewrite of a
  prior row.
- Never fabricate a "position" the user didn't actually state as their own
  view. Distinguish stated opinion from stated fact — same discipline as
  REQUIREMENTS.md §21 (never blend a subjective take into the record as if
  it were a settled claim).
- Never mark an interview "complete" if a category got zero real answers —
  report the gap plainly instead of padding it with generic placeholder
  content.
- This skill never drafts, critiques, schedules, or publishes anything —
  it only produces or updates the Story Bank.
