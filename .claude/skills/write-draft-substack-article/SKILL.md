---
name: write-draft-substack-article
description: Use when the user asks to draft a Substack article from a selected idea, run the Substack Writer for long-form content, or explicitly invokes /write-draft-substack-article. Converts an Idea Note claimed for the substack-article platform into a Substack-Article-Note in Drafts/, grounded in its linked research and following Content-Learnings/voice-guide-substack.md. Does not handle approval or publishing.
---

# Write Draft Substack Article (Substack Writer — long-form)

Converts an Idea Note with a `substack-article` entry in `platform_schedule`
into a long-form Substack-Article-Note, written to `Drafts/` using
`_Templates/Substack-Article-Note.md`. Built fresh rather than copied from
`/write-draft` — the format (title/subtitle/sections, no character ceiling,
depth over hook-brevity) is genuinely different, not a parameterized
variant.

## Arguments

- **idea-id** (optional) — draft one specific idea. If omitted, draft every
  idea with a `substack-article` entry in `platform_schedule` that doesn't
  already have an article draft linked to it.

## Process (per idea)

### 1. Load context

Read the Idea Note and every research note in its `sources[]`. Same
verify-or-drop discipline as every other writer skill in this pipeline —
nothing in the article that isn't grounded in the linked research's
Summary/Key Findings. Since this format has room for real depth, it's
worth re-reading the *full* research note body (Key Findings, not just the
Summary) more thoroughly than a feed-post writer would need to.

### 2. Read the voice guide and playbook

Read `Content-Learnings/voice-guide-substack.md` in full, its Articles
section specifically. Check `Content-Learnings/playbook-substack.md`'s
Articles tables for an evidenced rule (real published-article ids attached)
on structure/length/topic performance — prefer it over the generic default.

### 3. Structure the article

- **Title**: specific and concrete, earns a click from someone who already
  knows the topic exists — not a generic "Understanding X" label.
- **Subtitle**: one sentence sharpening what the piece actually delivers.
- **Body**: real sections with headings — an opening that states the
  stake, a middle that develops the argument/mechanism/finding in genuine
  depth (this is where Substack earns its place over a feed post — use the
  room), and a closing with an actual point of view, not a summary.
- If the idea's angle includes a subjective take, frame it explicitly as
  one — same opinion/fact separation rule as every writer skill here.
- Mark spots for visuals inline as `[IMAGE: <short label>]` where a diagram
  or chart would genuinely help — this feeds `/generate-visual-substack-article`
  later, don't skip it just because visuals aren't generated yet. A header
  image is generated separately and automatically by that skill — never add
  a marker for it here.

### 4. Standing sign-off (every article, added 2026-09-14 per direct user feedback)

End every article with this fixed closing block, verbatim (a stable
sign-off, not something to vary per piece — the *actual* point-of-view
closing from step 3 comes right before this, as its own paragraph; this
block is purely the reader-facing sign-off underneath it):

```
---

**Thanks for reading.** If this was useful, subscribe for more deep dives
on AI, dev tools, and tech careers — and follow along on
[X](https://x.com/Prithetechintel) and
[LinkedIn](https://www.linkedin.com/in/priyanshu-arya/) for shorter takes
between posts.
```

### 5. SEO fields

Write `seo_description` (1-2 sentences, accurate to the actual content) and
`seo_tags` (a handful of real topic tags) — per `voice-guide-substack.md`,
these should reflect the piece, not be keyword-stuffed guesses.

### 6. Write the Substack-Article-Note

Copy `_Templates/Substack-Article-Note.md` into `Drafts/` as
`YYYY-MM-DD--kebab-slug.md`, using the idea's `platform_schedule` entry for
`substack-article`. Fill in `idea_id`, `platform: substack-article`,
`category`, `title`, `subtitle`, `seo_description`, `seo_tags`, `sources`
(inherited), `status: draft`, `history: [{action: created, date: today,
note: ...}]`. Leave `viral_score` at 0 and `visual_ids` empty.

### 7. Update the idea

Flip `status: selected → drafted` only if this was its last unclaimed
platform, same rule as `/write-draft-x`.

## Report back

Show the full article (title, subtitle, all sections), word count, SEO
fields, and which research sources backed it. This is pre-approval
content — not ready to publish.

## Hard rules

- Never invent a fact, statistic, or quote not present in the linked
  research notes.
- Never draft an idea that doesn't have a `substack-article` entry in
  `platform_schedule`.
- Never pad a thin idea with filler sections to look substantial — if the
  research doesn't support real depth, say so in the report rather than
  writing around the gap.
- Never omit or reword the step 4 sign-off block — it's a stable,
  recognizable signature across every article, not per-piece content.
- Never mark anything approved, ready-to-publish, or published.
