---
name: critique-draft-substack-note
description: Use when the user asks to review/critique a Substack Note's quality, check it for accuracy or duplication, compute its viral potential score, or explicitly invokes /critique-draft-substack-note. Runs the Critic Agent on a status:draft, platform:substack-note Draft Note, auto-revises it once if it scores low, and hands it off to approval by moving it to status:in_review.
---

# Critique Draft Substack Note (Critic Agent — Substack Notes)

Reuses `/critique-draft-x`'s short-form rubric shape (no thread-cohesion
factor needed — Notes have no thread concept), scoped to `platform:
substack-note` and `Content-Learnings/playbook-substack.md`'s Notes
section.

## Arguments

- **draft-id** (optional) — critique one specific note. If omitted, run
  against every `platform: substack-note` Draft Note currently `status:
  draft`.

## Process (per draft)

### 1. Re-verify accuracy

Same as `/critique-draft`: re-read `sources[]`, fix any drift now.

### 2. Originality / duplicate check

Scan `Content-Learnings/content-index.md` filtered to `platform:
substack-note`. Same severity split as `/critique-draft`: genuine
duplicate stops here (stay `draft`, flag, report); similar-but-distinct
pulls the Originality sub-score down and proceeds to review.

### 3. Score Viral Potential (0-10)

Average these, each 0-10:

| Factor | How to assess it |
|---|---|
| Hook strength | Does the opening line land immediately? |
| Scannability | Short and casual, no wall of text |
| Novelty / insight | Fresh beyond basic regurgitation |
| Discussion catalysis | Would this get real replies from subscribers? |
| Technical accuracy | Consistency with linked research |
| Originality | Inverse of step 2's findings |
| Historical playbook alignment | Check `playbook-substack.md`'s Notes section for a matching evidenced rule; otherwise neutral (5) |

### 4. Auto-revise once if weak

Same rule as `/critique-draft`: below 6, one targeted pass re-reading
`voice-guide-substack.md`'s Notes section, recompute, stop after one pass.

### 5. Update the Draft Note

Same field updates as `/critique-draft` — skip entirely if step 2 found a
genuine duplicate.

## Report back

Same shape as `/critique-draft`'s report.

## Notifications

Same batching rule: one notification per run.

## Hard rules

Identical to `/critique-draft`'s hard rules, scoped to Substack Notes.
