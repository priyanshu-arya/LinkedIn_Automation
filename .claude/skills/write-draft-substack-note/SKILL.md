---
name: write-draft-substack-note
description: Use when the user asks to draft a Substack Note from a selected idea, run the Substack Notes Writer, or explicitly invokes /write-draft-substack-note. Converts an Idea Note claimed for the substack-note platform into a Draft Note in Drafts/ (platform:substack-note), grounded in its linked research and following Content-Learnings/voice-guide-substack.md's Notes section. Does not handle approval or publishing.
---

# Write Draft Substack Note (Substack Notes Writer)

Substack Notes' sibling to `/write-draft-x` — same short-form, single-post
shape (Substack Notes have no thread concept), reusing `Draft-Note.md`
rather than a new template, just a different voice source.

## Arguments

- **idea-id** (optional) — draft one specific idea for a Substack Note. If
  omitted, draft every idea with a `substack-note` entry in
  `platform_schedule` that doesn't already have a Substack Note draft
  linked to it.

## Process (per idea)

### 1. Load context

Read the Idea Note and every research note in its `sources[]`. Same
verify-or-drop discipline as every writer skill in this pipeline.

### 2. Read the voice guide and playbook

Read `Content-Learnings/voice-guide-substack.md`'s Notes section, fresh
each run. Check `Content-Learnings/playbook-substack.md`'s Notes tables for
an evidenced rule before falling back to the generic default.

### 3. Draft the note

Short, casual, conversational — more off-the-cuff than a polished feed
post, per `voice-guide-substack.md`. No hashtags (Substack Notes don't use
them). No thread concept — if an idea genuinely needs more room than one
Note comfortably holds, that's a signal it belongs to `/write-draft-x` (as
a thread) or `/write-draft-substack-article` instead, not a reason to force
it into an oversized single Note.

### 4. Write the Draft Note

Copy `_Templates/Draft-Note.md` into `Drafts/` as
`YYYY-MM-DD--kebab-slug.md`, using the idea's `platform_schedule` entry for
`substack-note`. Fill in `idea_id`, `platform: substack-note`, `category`,
`format`, `hook_style`, `hashtags: []`, `thread: []` (always empty here),
`sources`, `status: draft`, `history: [{action: created, date: today,
note: ...}]`.

### 5. Update the idea

Same rule as the other writer skills: flip `status: selected → drafted`
only if this was its last unclaimed platform.

## Report back

Show the full note text and character count, and which research sources
backed it.

## Hard rules

- Never invent a fact, statistic, or quote not present in the linked
  research notes.
- Never draft an idea that doesn't have a `substack-note` entry in
  `platform_schedule`.
- Never use hashtags — not a Substack Notes convention.
- Never mark anything approved, ready-to-publish, or published.
