---
name: critique-draft-x
description: Use when the user asks to review/critique an X draft's quality, check it for accuracy or duplication, compute its viral potential score, or explicitly invokes /critique-draft-x. Runs the Critic Agent on a status:draft, platform:x Draft Note, auto-revises it once if it scores low, and hands it off to approval by moving it to status:in_review.
---

# Critique Draft X (Critic Agent — X pipeline)

X's sibling to `/critique-draft`. Same process shape and same evidence-gated
rules — re-verify, dedup-check, score, auto-revise once if weak, hand off
to human review. Never approves, schedules, or publishes.

## Arguments

- **draft-id** (optional) — critique one specific X draft. If omitted, run
  against every `platform: x` Draft Note currently `status: draft`.

## Process (per draft)

### 1. Re-verify accuracy

Same as `/critique-draft`: re-read `sources[]`, confirm every claim still
traces to the linked research. Fix drift now, don't just flag it.

### 2. Originality / duplicate check

Scan `Content-Learnings/content-index.md` filtered to `platform: x` rows
(plus a spot-check against LinkedIn/Substack rows for the *same underlying
story*, since publishing the identical angle same-week across platforms
without differentiation is still worth flagging, even if it's not a
same-platform duplicate). Same severity split as `/critique-draft`:

- **Genuine duplicate** (same story/example/hook/conclusion as an existing
  X post) — stop here, don't score, keep `status: draft`, append a
  `duplicate_flagged` history entry, report plainly.
- **Merely similar but distinct** — note it, let it pull the Originality
  sub-score down, still goes to human review.

### 3. Score Viral Potential (0-10)

Average these, each 0-10 — same shape as `/critique-draft` with one added
factor for threads:

| Factor | How to assess it |
|---|---|
| Hook strength | Does tweet 1 stand alone and stop the scroll? |
| Scannability | Short, punchy, no wall-of-text tweet in the sequence |
| Novelty / insight | Fresh beyond basic regurgitation |
| Discussion catalysis | Would this get real replies, not just likes? |
| Technical accuracy | Consistency with linked research |
| Thread cohesion (threads only; score 10 for a single post) | Does each tweet stand alone reasonably well while the sequence still reads as one throughline, no filler tweets just to extend the thread? |
| Originality | Inverse of step 2's findings |
| Historical playbook alignment | Check `Content-Learnings/playbook-x.md` for a matching evidenced rule; otherwise neutral (5), say plainly no data exists yet |

### 4. Auto-revise once if weak

Same rule as `/critique-draft`: below 6, exactly one targeted revision pass
re-reading `voice-guide-x.md`, recompute, stop after one pass regardless.

### 5. Update the Draft Note

Same field updates as `/critique-draft` (`viral_score`, `history`,
`## Critic Notes`, `status: in_review`) — skip entirely if step 2 found a
genuine duplicate.

## Report back

Same shape as `/critique-draft`'s report, plus whether this draft is a
single post or a thread and its tweet count.

## Notifications

Same batching rule as `/critique-draft`: one batched notification per run
covering however many X drafts reached `in_review`.

## Hard rules

Identical to `/critique-draft`'s hard rules, platform-scoped to X drafts.
