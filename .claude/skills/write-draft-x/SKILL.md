---
name: write-draft-x
description: Use when the user asks to draft an X (Twitter) post or thread from a selected idea, run the X Writer, or explicitly invokes /write-draft-x. Converts an Idea Note claimed for the x platform into a Draft Note in Drafts/ (platform:x), grounded in its linked research and following Content-Learnings/voice-guide-x.md. Decides single-post vs. thread from the idea's depth. Does not assign posting days and does not handle approval or scheduling.
---

# Write Draft X (X Writer — X pipeline)

X's sibling to `/write-draft`. Converts one or more Idea Notes with an `x`
entry in `platform_schedule` into Draft Notes (`platform: x`), written to
`Drafts/` using `_Templates/Draft-Note.md`. Assumes `/plan-week-x` has
already assigned a day.

## Arguments

- **idea-id** (optional) — draft one specific idea for X. If omitted, draft
  every idea with an `x` entry in `platform_schedule` that doesn't already
  have an X draft linked to it (an idea can have both a LinkedIn draft and
  an X draft — they're independent notes, never copies of each other).

## Process (per idea)

### 1. Load context

Read the Idea Note and every research note in its `sources[]` — same
verify-or-drop discipline as `/write-draft`: nothing in the post that isn't
already in the linked research's Summary/Key Findings.

### 2. Read the X voice guide and playbook

Read `Content-Learnings/voice-guide-x.md` in full, fresh each run. Also
check `Content-Learnings/playbook-x.md` for an evidenced rule (real X post
ids attached) about length, hook style, or single-vs-thread performance for
this category — prefer it over the voice guide's generic defaults where one
exists.

### 3. Decide single post vs. thread

Judge from the idea's actual depth, not a coin flip: if the point lands in
one tight statement, write a single post. If it genuinely needs several
connected beats (a numbered breakdown, a before/after, a multi-step
argument), write a thread. Don't pad a single-post idea into a thread to
look more substantial, and don't cram a multi-beat idea into one
over-stuffed post.

### 4. Draft the post

- **Single post:** hook-as-the-whole-post, tight, well under the character
  ceiling in `voice-guide-x.md`. Write the full text into `## Post Text`
  and leave `thread: []` empty.
- **Thread:** first tweet is the hook (must stand alone if someone only
  sees tweet 1), each following tweet one beat, closing tweet lands the
  point without just recapping. Write the first tweet into `## Post Text`
  (for at-a-glance consistency with single posts) and the **full ordered
  sequence**, first tweet included, into the `thread: []` frontmatter list.
- Same opinion/fact framing rule as `/write-draft`: a subjective take reads
  as a take ("I think," "my read"), not blended into declarative fact-voice.

### 5. Hashtags

0–2, only if genuinely useful for discovery, per `voice-guide-x.md` — don't
default to LinkedIn's 3–5 convention here.

### 6. Write the Draft Note

Copy `_Templates/Draft-Note.md` into `Drafts/` as `YYYY-MM-DD--kebab-slug.md`
using the idea's `platform_schedule` entry for `x` (not `target_date`,
which is LinkedIn's). Fill in: `idea_id`, `platform: x`, `category`,
`format`, `hook_style`, `hashtags`, `thread` (per step 4), `sources`
(inherited from the idea), `status: draft`, `history: [{action: created,
date: today, note: ...}]`. Leave `viral_score` at 0 and `visual_ids` empty.

### 7. Update the idea

If this was the idea's only remaining unclaimed platform, flip `status:
selected → drafted`. If other platforms in its `platforms` list haven't
drafted yet, leave `status: selected` so they can still pick it up.

## Report back

Show the full draft (all tweets in order if a thread), hashtags, per-tweet
character counts, and which research sources backed it.

## Hard rules

- Never invent a fact, statistic, or quote not present in the linked
  research notes.
- Never draft an idea that doesn't have an `x` entry in `platform_schedule`
  (run `/plan-week-x` first).
- Never silently copy another platform's draft text — this idea's X version
  is written fresh from the research, in `voice-guide-x.md`'s voice, even
  if a LinkedIn draft for the same idea already exists.
- Never mark anything approved, scheduled, or published.
