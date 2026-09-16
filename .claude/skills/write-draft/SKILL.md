---
name: write-draft
description: Use when the user asks to draft a LinkedIn post from a selected idea or a Story Bank Post Spine, run the LinkedIn Writer/Post Writer, or explicitly invokes /write-draft. Converts a status:selected Idea Note (default path) OR a Content-Learnings/story-bank.md Post Spine (--spine <id>) into a post draft in Drafts/, picking a hook formula from Content-Learnings/hook-formulas.md and optionally a founders angle from Content-Learnings/founders-angle-library.md by engagement goal, grounded in linked research (idea path) or the cited Story Bank entries (spine path), following Content-Learnings/voice-guide.md. Does not assign posting days (/plan-week) or handle approval/scheduling.
---

# Write Draft / Post Writer (LinkedIn Writer — Phase 4b, reworked Phase 17)

Converts either a `status: selected` Idea Note (default, primary path) or a
`Content-Learnings/story-bank.md` Post Spine (`--spine <id>`, new path) into
an actual LinkedIn post draft, written to `Drafts/` using
`_Templates/Draft-Note.md`. Also selects a hook formula from
`Content-Learnings/hook-formulas.md` by engagement goal, and — for Career /
Interview Prep categories, or whenever asked — an optional founders angle
from `Content-Learnings/founders-angle-library.md`, grounded in real Story
Bank material. Assumes `/plan-week` has already assigned a day to the idea
(idea path only — a spine has no day assignment to assume).

## Arguments

- **idea-id** (optional, default path) — draft one specific idea. If
  omitted, and no `--spine` is given, draft every idea currently
  `status: selected` that doesn't already have a draft linked to it.
- **--spine \<spine_id\>** (optional, new path) — draft from a Post Spine
  row in `Content-Learnings/story-bank.md`'s `## Post Spines` table
  instead of an Idea Note. Mutually exclusive with idea-id.
- **--goal \<goal\>** (optional, either path) — explicit engagement goal
  override. Closed list: `likes`, `comments`, `shares`, `saves`,
  `profile-visits`.
- **--founders** (optional, either path) — force-consider a founders angle
  even outside Career / Interview Prep categories. Still subject to the
  same real-Story-Bank-match-or-skip rule below — this flag only widens
  *when* the attempt happens, never lowers the bar for using one.

## Process

### 1. Determine the entry path
- **idea-id given, or no `--spine`** (default): the existing idea-based
  flow below, unchanged in spirit — this stays the primary path.
- **`--spine <spine_id>` given**: load that row from
  `Content-Learnings/story-bank.md`'s `## Post Spines` table by `id`. Its
  `receipt_id` / `position_id` cross-references, if set, **are the
  grounding** for this draft — treat them with the exact same
  never-fabricate discipline as an idea's linked research notes: every
  factual claim in the draft must trace back to the spine's own fields
  (`hook_angle`, `story_beat`, `position`, `suggested close`) or the Story
  Bank row(s) it cross-references. If the spine sets no `receipt_id` /
  `position_id`, the draft must not invent one — work only from what the
  spine itself states. There is no idea for this path, so there's no idea
  status to flip at the end; instead the Draft Note records `spine_id` (see
  step 7) so its provenance is traceable.

### 2. Load context (idea path) / load the spine (spine path)
- **Idea path**: read the Idea Note and every research note in its
  `sources[]`. All factual claims in the draft must trace back to something
  in those research notes' Summary/Key Findings — never introduce a new
  statistic, quote, or claim that isn't already there.
- **Spine path**: read the spine row plus every Story Bank row it
  cross-references (by `receipt_id`/`position_id`). Those rows are this
  draft's entire factual grounding — there is no research note to fall
  back on.

### 3. Determine the engagement goal (both paths)
Precedence: explicit `--goal <goal>` argument > the idea's own goal field
if it has one and is set (idea path only) > a `Content-Learnings/
playbook.md`-evidenced pattern for this category (real post ids attached
as evidence), if one exists > default `comments`. Closed list, exactly
these five values: **likes, comments, shares, saves, profile-visits**.
Never invent a sixth value.

### 4. Read the voice guide and playbook
Read `Content-Learnings/voice-guide.md` in full before drafting. This is
the current source of truth for hook style, structure, length, tone, and
things to avoid — it starts as a documented default and will be updated by
later phases as real approval/edit data accumulates. Always re-read it
fresh each run; don't rely on a cached memory of it, since it can change.

Also check `Content-Learnings/playbook.md` for any evidenced rule about
length, hook style, or hashtags for this category/content_type. If one
exists (with real post ids attached as evidence), prefer it over the
voice guide's generic defaults for that specific dimension.

### 5. Select a hook formula
Read `Content-Learnings/hook-formulas.md` fresh each run — never rely on a
cached memory of it, since `/extract-hook` and human promotions grow it
over time. Filter to `status: canonical` rows only (never select a
`proposed` row — those aren't trusted for drafting yet) tagged for the
chosen engagement goal; a formula with no `engagement_goals` value is
general-purpose and eligible for any goal. Among the eligible set, prefer
a formula not used in the last ~5 drafts — check recent `Drafts/` notes'
`hook_formula` field (new frontmatter field, see step 7) to avoid
repetition. If every eligible formula was used recently, repetition is
acceptable rather than forcing a worse goal-fit; goal match beats novelty.

### 6. Optional founders angle
Triggered automatically if the idea's (or spine's) category is **Career**
or **Interview Prep**, or if the user passed `--founders`. Otherwise
skipped without comment (it's simply not applicable this run).

If triggered:
1. Read `Content-Learnings/founders-angle-library.md` fresh each run.
2. Look for a `canonical` angle (never `proposed`) whose bracketed
   template slots can genuinely be filled from an actual
   `Content-Learnings/story-bank.md` entry (a Receipt, Turning Point, Scar,
   or Defensible Position) matching the topic.
3. **Real fit found** → use it. Fill every bracket with the real Story
   Bank value, nothing invented or rounded, and cite that Story Bank row's
   `id` in the Draft Note's `sources`/founders_angle note.
4. **No real fit** → drop the founders angle entirely for this draft,
   silently in the draft text (don't leave a half-filled template) but
   *not* silently in the report — call this out explicitly in "Report
   back" below. Never invent a plausible-sounding number or anecdote just
   to complete a bracket.

### 7. Draft the post
- Hook: idea path uses the idea's `hook` field, refined if needed and
  shaped by the selected hook formula's opening mechanic; spine path uses
  the spine's `hook_angle`, similarly shaped. The hook formula shapes the
  **opening line only** — it never overrides step 9's opinion/fact
  separation, and it must never misrepresent certainty (e.g. don't let a
  "contrarian claim" formula state a personal opinion with the same
  declarative confidence as a sourced fact).
- If a founders angle was used (step 6), it shapes the **whole structure**
  of the post per its template — the angle's bracketed narrative arc
  becomes the post's body, still filled only with real Story Bank
  specifics and still following the same fact-discipline as everything
  else here.
- If no founders angle is in play: hook → the substantive content → an
  optional closing discussion question, only if the voice guide's CTA
  guidance supports one here.
- If the idea's `format` is `opinion` (or the content otherwise includes a
  subjective take, not just what the research/Story Bank supports), frame
  it explicitly as a view — "I think," "the mistake I keep seeing," "my
  take" — rather than stating it with the same declarative confidence as
  a sourced fact (REQUIREMENTS.md §21: clearly distinguish opinions from
  facts). Sourced claims and personal opinions should read differently to
  the reader, not blend together.
- Length: per the voice guide's default (~1,200–1,500 characters,
  comfortably under LinkedIn's ~3,000 limit) unless the material genuinely
  needs more room.
- Follow the voice guide's "avoid" list explicitly — check the draft
  against it before finalizing, don't just aim for the tone and hope.

### 8. Hashtags
3–5, directly tied to topic/category, no stuffing. Unchanged from before.

### 9. Write the Draft Note
Copy `_Templates/Draft-Note.md` into `Drafts/` as
`YYYY-MM-DD--kebab-slug.md` (idea path: use the idea's target_date, not
today, if the two differ; spine path: use today's date, since a spine has
no target_date — the filename should reflect when it's meant to post).

Fill in: `category`, `format`, `hook_style`, `hashtags`, `status: draft`,
`history: [{action: created, date: today, note: ...}]`, plus the new
frontmatter fields:
- `hook_formula`: the matched `formula_id` from step 5 (e.g. `F10`).
- `engagement_goal`: the goal determined in step 3.
- `founders_angle`: the matched `angle_id` from step 6 if one was used
  (e.g. `A5`), else left empty.
- **Idea path**: `idea_id` set to the idea's id, `spine_id` left empty.
  `sources` inherited from the idea (research note ids), plus the Story
  Bank row id if a founders angle was used.
- **Spine path**: `spine_id` set to the spine's id, `idea_id` left empty.
  `sources` populated from whatever Story Bank row ids actually grounded
  the draft (the spine's own cross-references, and/or a founders-angle
  Story Bank row) — never a research note, since none exists for this
  path.

Leave `viral_score` at 0 and `visual_ids` empty — scoring the draft and
generating visuals are later phases (Quality/Critic Agent, Visual Agent),
not this skill's job.

### 10. Update the idea (idea path only)
Flip the Idea Note's `status: selected → drafted`. Spine path: no status
flip — Story Bank rows aren't a status-driven lifecycle, so the spine stays
as-is and can be reused or referenced again later.

## Report back

Show the full draft text, hashtags, character count, and:
- Which research sources (idea path) or Story Bank row(s) (spine path)
  backed it.
- Which hook formula was used, and why — the engagement-goal match and the
  anti-repetition check against recent drafts.
- Whether a founders angle was attempted, and its outcome: used, with the
  Story Bank row it cited — or explicitly skipped because no real fit
  existed (never omit this without saying so).

This is pre-approval content, not ready to schedule. Remind the user that
approval/edit/regenerate workflow (Phase 7) doesn't exist yet, so right now
this just produces a file for manual review.

## Hard rules

- Never invent a fact, statistic, or quote not present in the linked
  research notes (idea path) or the cited Story Bank rows (spine path). If
  the grounding doesn't support a specific claim the hook implies, soften
  the claim rather than fabricate support.
- Never draft an idea that isn't `status: selected` (run `/plan-week`
  first).
- Never invent a founder anecdote or number that isn't present in
  `Content-Learnings/story-bank.md` — no genuine match means no founders
  angle for this draft, not a fabricated one.
- Never select a `proposed`-status hook formula or founders angle for
  drafting — both must be `canonical`.
- A hook formula shapes phrasing only; it must never misrepresent
  certainty or blend a personal opinion into the same declarative register
  as a sourced fact (REQUIREMENTS.md §21).
- The `--spine` path is grounded in Story Bank citations with the same
  rigor the idea path applies to research citations — never looser, never
  treated as "softer" evidence just because it's personal material.
- Never mark anything as approved, scheduled, or published — this skill
  only produces a draft file.
