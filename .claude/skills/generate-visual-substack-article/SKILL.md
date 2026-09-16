---
name: generate-visual-substack-article
description: Use when the user asks for visuals/images/diagrams for a Substack article, wants the multi-image Visual Agent variant, or explicitly invokes /generate-visual-substack-article. Produces one finished header/hero image prompt plus one finished, paste-ready prompt per in-body [IMAGE: ...] marker, for a long-form Substack-Article-Note. Never calls an image-generation provider itself.
---

# Generate Visual Substack Article (Visual Agent — multi-image variant)

`/generate-visual`'s sibling for long-form content. Same provider-free,
prompt-only deliverable, but a Substack article warrants more than one
image (a feed post never does): exactly one **header/hero image** every
article gets regardless of body content (added 2026-09-14 per direct user
feedback — Substack's editor has a dedicated header-image slot, and every
published article should fill it), plus one brief per `[IMAGE: <label>]`
marker the writer left in the body.

## Arguments

- **draft-id** (optional) — generate visuals for one article. If omitted,
  run for every `type: substack-article` note with no linked visual note
  yet (a header image alone is enough reason to run this — in-body
  markers are additive, not a prerequisite).

## Process

### 1. The header/hero image (mandatory, every article)

Read the article's `title`, `subtitle`, and overall thesis (not just the
opening paragraph) and design one strong lead image that represents the
piece as a whole — this is what shows in the Substack feed/email preview
and at the top of the published post, so it needs to work as a standalone
visual, not a diagram of one specific section's content. Prefer a concept
that captures the article's central tension or claim over a generic
title-card treatment.

### 2. Find the in-body marked spots

Read the full article body and collect every `[IMAGE: <label>]` marker the
writer left. It's fine for an article to have zero markers — the header
image alone still applies — don't invent a marker that isn't there.

### 4. Decide, per marker, what the image actually needs to show

Read the surrounding section's actual content, not just the label — the
image must support that specific section's point (a mechanism diagram for
a technical section, a comparison table/graphic for a vs.-style section, a
simple chart if the section leans on real numbers). Don't default every
marker to the same visual format — vary it per what that section actually
needs, and check `Content-Learnings/content-index.md`'s
`visual_format`/`image_concept` columns so this article's own images don't
repeat each other either. The header image (step 1) and every marker image
should also look distinct from one another — the header sells the piece as
a whole, a marker image explains one specific point, and they shouldn't
read as the same graphic twice.

### 5. Research visual/design trends, when it would help

Same judgment-call gate as `/generate-visual` step 3 — skip when the
header's or a marker's concept is simple enough that trend research
wouldn't change the outcome.

### 6. Write one Visual-Brief-Note covering all of this article's images

Copy `_Templates/Visual-Brief-Note.md` into `Visuals/` as
`YYYY-MM-DD--kebab-slug.md`, `platform: substack-article`, `draft_id`. In
the body, write the header image's Brief/Trend-Research/Prompt/
Why-this-visual block first (labelled `## Header Image`), then repeat the
same block shape once per in-body marker (labelled by which section it
belongs to, e.g. `## Section Image: <label>`) — so one note covers the
whole article's image set (header plus however many markers exist,
including zero) instead of scattering several near-identical files. For
each prompt: same full spec as `/generate-visual` (subject, composition,
hierarchy, lighting, mood, color, typography, aspect ratio). Substack's
header-image slot and its in-body images both typically work well at a
wider landscape ratio (e.g. 1456×816 or similar) than a social feed image;
verify current guidance rather than assuming.

### 7. Link it back

Add the one Visual-Brief-Note's id to the article's `visual_ids[]` (a
single id covering the header plus every marker image, not one id per
image).

## Report back

Show the header image's finished prompt first, then every section label
alongside its own finished prompt — all clearly marked as prompts (not
rendered images) ready to paste into ChatGPT Images one at a time. The
header image goes in Substack's header-image slot when publishing; each
marker's image gets placed manually at that marker's spot in the body once
generated.

## Hard rules

- Never skip the header image — every article gets one, regardless of
  whether it has any in-body markers.
- Never claim an image was generated when only a prompt was written.
- Never invent a marker that isn't actually in the article body.
- Never produce an in-body visual for a purely decorative purpose (the
  header image is exempt from this — its job is representing the whole
  piece, which is a legitimate purpose on its own).
- Never reuse another article's (or another marker's) prompt wording —
  each is written fresh, including the header image.
