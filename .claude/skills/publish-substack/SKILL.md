---
name: publish-substack
description: Use when the user wants to move an approved Substack article or Note toward publishing, get the copy-ready final content, or explicitly invokes /publish-substack. Substack has no Buffer channel and no safe official publishing API, so this never calls an external API — it hands off a copy-ready Substack-Ready note and only marks something published once the user explicitly confirms they posted it themselves. Never claims a publish happened without that confirmation.
---

# Publish Substack (manual publish handoff — Substack Articles + Notes)

Substack's sibling to `/schedule-approved`/`/schedule-approved-x`, adapted
for the one real constraint that makes those skills' approach impossible
here: **Substack has no Buffer channel and no supported API for posting**.
Rather than reach for an unofficial, session-cookie-based API (ToS-risky,
undocumented, could break silently), this skill does what the pipeline
already does for image generation — hand off a finished, ready-to-paste
deliverable and let the human do the actual publish action, then record
that confirmation honestly rather than assuming it happened.

## Arguments

- **note-id** (optional) — hand off one specific approved item. If omitted,
  process every `status: approved` note with `platform` in
  {`substack-article`, `substack-note`} and no `ready_id` yet.

## Process (per note)

### 1. Move to Substack-Ready/

Copy `_Templates/Substack-Ready-Note.md` into `Substack-Ready/` as
`YYYY-MM-DD--kebab-slug.md`. Fill in `draft_id`, `platform`, and:
- For `substack-article`: `title`, and the full article body copied into
  `## Final Content` verbatim (in-body images already generated should be
  noted as "insert image: <label>" at their marker positions, since this
  handoff step doesn't embed files). Call out the header/hero image
  separately in `## Publishing Notes` — it goes in Substack's dedicated
  header-image slot in the editor, not inline in the body, so don't leave
  it looking like just another in-body marker.
- For `substack-note`: `final_text` and the same text mirrored into
  `## Final Content`.

`publish_status: ready_to_publish`. Copy `category`/`format`/`hashtags`/
`visual_ids`/`sources` from the source note; compute `length` from the
final text/body. Set the source Draft/Article note's `ready_id` to this
new note's id.

### 2. Present the copy-ready deliverable

Show the full final content exactly as it should be pasted into Substack's
editor, plus a reminder of any images still needing manual insertion at
their marked spots. State plainly: **this is not published yet** — nothing
external has happened, this is the same "prompt not a picture" honesty
`/generate-visual` already applies, just for the whole piece.

### 3. Ask for publish confirmation

Ask the user directly (AskUserQuestion when interactive): has this actually
been published on Substack yet? Do not assume yes because time has passed
or because the user moved on to another task.

- **If confirmed published:** set `publish_confirmed_date` to today,
  `publish_status: published`, move the file from `Substack-Ready/` to
  `Published-Posts/`. Update the source Draft/Article note's `status`
  unchanged (it stays `approved` — the historical record, same pattern as
  `/schedule-approved`'s Draft Notes) but append `{action: scheduled,
  date, note: "published manually via publish-substack"}` — reusing the
  existing history action name since it means the same thing here: this
  note left the approval stage for real, external distribution.
- **If not yet published:** leave it in `Substack-Ready/` at
  `publish_status: ready_to_publish`. This is a normal, expected state —
  not an error — for however long it takes the user to actually paste it
  in.

## Report back

Which notes moved to `Substack-Ready/`, which were confirmed published
this run (with their `publish_confirmed_date`), and which are still
waiting on the user to actually publish them.

## Hard rules

- Never call any Substack API, official or unofficial — this skill is
  manual-handoff by design, not a missing feature.
- Never set `publish_status: published` or `publish_confirmed_date`
  without an explicit user confirmation this run.
- Never invent or guess a publish date from context (e.g. "they probably
  posted it by now") — ask.
- Never process a note that isn't `status: approved`.
