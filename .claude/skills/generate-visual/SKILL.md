---
name: generate-visual
description: Use when the user asks for a visual/image/diagram for a LinkedIn draft, wants the Visual Agent to run, or explicitly invokes /generate-visual. Produces a detailed image brief (composition, style, text) for a draft's suggested visual and links it to the Draft Note. Does not call any image-generation provider yet — no provider is configured (REQUIREMENTS.md §11 provider-independence: this is designed so a real provider can be wired in later without changing the Draft/Visual schema).
---

# Generate Visual (Visual Agent — Phase 6)

Produces a **written image brief**, not a rendered image — no image-
generation provider is configured yet (by explicit choice, to avoid
building against a provider/key that doesn't exist). The schema is
provider-independent: `_Templates/Visual-Brief-Note.md` has a `provider`
field (`none` for now) and an `image_path` field that stays empty until a
real provider is wired in and actually fills it. Nothing else in the
pipeline needs to change when that happens.

## Arguments

- **draft-id** (optional) — generate a visual brief for one draft. If
  omitted, generate for every draft in `Drafts/` or `Post-Ideas/` that has
  a non-empty `suggested_visual` and no linked visual brief yet.

## Process

### 1. Decide if a visual is warranted
Per REQUIREMENTS.md §11, a visual must support the point, not decorate. If
the draft's idea already has a `suggested_visual`, use that as the seed. If
it's vague ("some kind of diagram"), sharpen it into something concrete
based on the actual post content — don't generate a brief for a visual that
wouldn't add anything beyond the text.

### 2. Write the brief
Copy `_Templates/Visual-Brief-Note.md` into `Visuals/` as
`YYYY-MM-DD--kebab-slug.md`. Fill in `format`, `draft_id`, and the brief
body: what it shows, composition, exact key text/labels (short strings,
not paragraphs), style notes, and why this specific visual earns its place
next to this specific post.

### 3. Link it back
Add the visual brief's id to the Draft Note's `visual_ids[]`.

## Report back

Show the full brief. State plainly that this is a brief, not an image —
someone (the user, or a wired-in provider in a later phase) still needs to
actually produce the artwork before this post can carry a real visual.

## Hard rules

- Never claim an image was generated when only a brief was written.
- Never invent a provider name or pretend an API call happened.
- Never produce a brief for a purely decorative visual with no
  informational purpose.
