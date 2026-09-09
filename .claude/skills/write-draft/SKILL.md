---
name: write-draft
description: Use when the user asks to draft a LinkedIn post from a selected idea, run the LinkedIn Writer, or explicitly invokes /write-draft. Converts a status:selected Idea Note into an actual post draft in Drafts/, grounded in its linked research and following Content-Learnings/voice-guide.md. Does not assign posting days (that's /plan-week) and does not handle approval or scheduling.
---

# Write Draft (LinkedIn Writer — Phase 4b)

Converts one or more `status: selected` Idea Notes into actual LinkedIn post
drafts, written to `Drafts/` using `_Templates/Draft-Note.md`. Assumes
`/plan-week` has already assigned a day to the idea.

## Arguments

- **idea-id** (optional) — draft one specific idea. If omitted, draft every
  idea currently `status: selected` that doesn't already have a draft
  linked to it.

## Process (per idea)

### 1. Load context
Read the Idea Note and every research note in its `sources[]`. All factual
claims in the draft must trace back to something in those research notes'
Summary/Key Findings — never introduce a new statistic, quote, or claim
that isn't already there.

### 2. Read the voice guide and playbook
Read `Content-Learnings/voice-guide.md` in full before drafting. This is
the current source of truth for hook style, structure, length, tone, and
things to avoid — it starts as a documented default and will be updated by
later phases as real approval/edit data accumulates. Always re-read it
fresh each run; don't rely on a cached memory of it, since it can change.

Also check `Content-Learnings/playbook.md` for any evidenced rule about
length, hook style, or hashtags for this category/content_type. If one
exists (with real post ids attached as evidence), prefer it over the
voice guide's generic defaults for that specific dimension.

### 3. Draft the post
- Hook (from the idea's `hook` field, refined if needed) → the substantive
  content → an optional closing discussion question, only if the voice
  guide's CTA guidance supports one here.
- If the idea's `format` is `opinion` (or the content otherwise includes a
  subjective take, not just what the research supports), frame it
  explicitly as a view — "I think," "the mistake I keep seeing," "my
  take" — rather than stating it with the same declarative confidence as
  a sourced fact (REQUIREMENTS.md §21: clearly distinguish opinions from
  facts). Sourced claims and personal opinions should read differently to
  the reader, not blend together.
- Length: per the voice guide's default (~1,200–1,500 characters,
  comfortably under LinkedIn's ~3,000 limit) unless the material genuinely
  needs more room.
- Follow the voice guide's "avoid" list explicitly — check the draft
  against it before finalizing, don't just aim for the tone and hope.

### 4. Hashtags
3–5, directly tied to topic/category, no stuffing.

### 5. Write the Draft Note
Copy `_Templates/Draft-Note.md` into `Drafts/` as
`YYYY-MM-DD--kebab-slug.md` (use the idea's target_date, not today, if the
two differ — the filename should reflect when it's meant to post).
Fill in: `idea_id`, `category`, `format`, `hook_style`, `hashtags`,
`sources` (inherited from the idea), `status: draft`, `history: [{action:
created, date: today, note: ...}]`. Leave `viral_score` at 0 and
`visual_ids` empty — scoring the draft and generating visuals are later
phases (Quality/Critic Agent, Visual Agent), not this skill's job.

### 6. Update the idea
Flip the Idea Note's `status: selected → drafted`.

## Report back

Show the full draft text, hashtags, character count, and which research
sources backed it — this is pre-approval content, not ready to schedule.
Remind the user that approval/edit/regenerate workflow (Phase 7) doesn't
exist yet, so right now this just produces a file for manual review.

## Hard rules

- Never invent a fact, statistic, or quote not present in the linked
  research notes. If the research doesn't support a specific claim the
  idea's hook implies, soften the claim rather than fabricate support.
- Never draft an idea that isn't `status: selected` (run `/plan-week`
  first).
- Never mark anything as approved, scheduled, or published — this skill
  only produces a draft file.
