---
name: critique-draft
description: Use when the user asks to review/critique a draft's quality, check a draft for accuracy or duplication, compute its viral potential score, or explicitly invokes /critique-draft. Runs the Quality/Critic Agent on a status:draft Draft Note, auto-revises it once if it scores low, and hands it off to the approval workflow by moving it to status:in_review.
---

# Critique Draft (Quality/Critic Agent — Phase 5)

Checks a draft for accuracy, originality, and overall strength, computes a
Viral Potential Score, auto-revises once if the score is weak, and moves the
draft to `status: in_review` — ready for human approval (Phase 7). This
skill never approves, schedules, or publishes anything itself.

## Arguments

- **draft-id** (optional) — critique one specific draft. If omitted, run
  against every Draft Note currently `status: draft` (i.e. not yet
  critiqued).

## Process (per draft)

### 1. Re-verify accuracy
Re-read the draft's `sources[]` research notes. Confirm every factual claim
in the post text still traces to something in those notes' Summary/Key
Findings. If drift is found (a claim not actually supported), fix it now —
soften or remove the claim, don't just flag it and move on.

### 2. Originality / duplicate check (expanded, Phase 13)
First pass: scan `Content-Learnings/content-index.md` (fast, compact) across
seven dimensions — topic, hook, storytelling structure, examples,
conclusion type, image concept, and category/format — for anything close to
this draft. For anything the index flags, read the actual flagged note in
full (`Published-Posts/`, other `Drafts/`, `Scheduled/`) to confirm before
acting on it. Also check `Content-Learnings/playbook.md`'s "Topic Fatigue
Watch" section. If `content-index.md` doesn't exist yet or is too thin to
trust, fall back to reading the folders directly, as before.

Draw a hard line between two severities:
- **Genuine duplicate** — the same underlying story/news item, example,
  hook, or conclusion as an existing note from the same or a recent week.
  This is not a scoring matter — see step 3a below, it skips normal
  scoring entirely.
- **Merely similar but substantively distinct** — same general topic or
  style, different angle/argument/example. Note it in the critique and let
  it pull the Originality sub-score down in step 3, same as before; still
  goes to human review, the human approver makes the final call.

### 2a. If a genuine duplicate was found, stop here — don't score or revise
A genuine duplicate isn't fixable by rewording — it needs a different
underlying angle entirely. Skip steps 3-4 (scoring, auto-revise) for this
draft. Keep `status: draft` (do **not** advance to `in_review`, since
advancing would surface a known duplicate to human review, which defeats
the point of catching it here). Append `{action: duplicate_flagged, date,
note: "<what it duplicates and how>"}` to history, and say so plainly and
directly in the report — this draft's idea needs to be replaced with a
genuinely different angle before it can be redrafted, not merely revised.

### 3. Score Viral Potential (0-10)
Average these factors, each 0-10:

| Factor | How to assess it |
|---|---|
| Hook strength | Specific and attention-grabbing vs. generic |
| Topic freshness | Inherited from the source research note's `freshness_score` |
| Audience relevance | Fit with the AI/dev/career LinkedIn audience |
| Educational value | Inherited from the source research note's `educational_value`, adjusted for how well the draft actually delivers it |
| Shareability / discussion potential | Would someone repost this or comment with a real opinion? |
| Originality | Inverse of step 2's findings |
| Credibility | Inherited from the source research note's `authority_score` |
| Historical performance of similar posts | Check `Content-Learnings/playbook.md` for a rule matching this draft's category/format/hook_style with real evidence attached — use it if present. Otherwise score neutral (5) and say plainly that no data exists yet. Do not fabricate a trend either way. |

### 4. Auto-revise once if the score is weak
If the averaged score is **below 6**, make exactly one revision pass
targeting the specific weak factors (e.g. if hook strength is low, rewrite
only the hook; if originality is low, shift the angle) — re-reading
`Content-Learnings/voice-guide.md` so the revision doesn't drift from
voice. Recompute the score after revising. Do not loop more than once —
if it's still below 6 after one revision, say so plainly in the report
rather than repeatedly regenerating.

### 5. Update the Draft Note
(Skip this step entirely if 2a fired — that path already updated the note
and stopped.)
- Set `viral_score` to the final computed value.
- Append a `history` entry: `{action: regenerated, date, note}` if step 4
  fired, otherwise `{action: critiqued, date, note}`.
- Add a `## Critic Notes` section to the body: the per-factor scores, any
  duplicate/fatigue findings from step 2, and (if revised) what changed.
- Set `status: in_review`.

## Report back

Per draft: either "HARD DUPLICATE — needs a new angle" (if 2a fired, name
what it duplicates) or the final viral_score, per-factor breakdown, whether
it was auto-revised, and any similar-but-distinct flags. Make clear a draft
that reached `in_review` is now waiting for human approval — nothing has
been approved, scheduled, or published. A draft left at `status: draft`
with a duplicate flag is not waiting for anything — it needs a replacement
idea before this skill can be run on it again.

## Notifications (REQUIREMENTS.md §24)

After a run that moves one or more drafts to `in_review`, send a single
batched `PushNotification` (status: proactive) — e.g. "3 LinkedIn drafts
ready for your review." Batch across the whole run; don't send one per
draft.

## Hard rules

- Never invent a "historical performance" trend when no analytics data
  exists — score that factor neutral and say why.
- Never revise more than once per critique run.
- Never move a draft straight to `approved` or `scheduled` — only
  `in_review`. Approval is a human action (Phase 7).
- Never advance a draft flagged as a genuine duplicate (2a) to `in_review`
  — a known duplicate must never reach human review as if it were novel.
- Never soften an accuracy fix by leaving the unsupported claim in place
  "just flagged" — fix it or remove it.
