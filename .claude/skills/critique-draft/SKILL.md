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

### 2. Originality / duplicate check
Compare this draft's topic, hook, examples, and core argument against:
- `Published-Posts/` (real duplicates matter most here)
- other `Drafts/` and `Scheduled/` notes
- `Content-Learnings/playbook.md`'s "Topic Fatigue Watch" section, once it
  has entries

If something is too similar, note it in the critique. A close-but-not-
identical match is a reason to push originality lower in scoring (step 3),
not necessarily to reject outright — that judgment call belongs to the
human approver, not this skill.

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
- Set `viral_score` to the final computed value.
- Append a `history` entry: `{action: regenerated, date, note}` if step 4
  fired, otherwise `{action: critiqued, date, note}`.
- Add a `## Critic Notes` section to the body: the per-factor scores, any
  duplicate/fatigue findings from step 2, and (if revised) what changed.
- Set `status: in_review`.

## Report back

Per draft: final viral_score, per-factor breakdown, whether it was
auto-revised, and any duplicate/fatigue flags. Make clear this draft is now
waiting for human approval — nothing has been approved, scheduled, or
published.

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
- Never soften an accuracy fix by leaving the unsupported claim in place
  "just flagged" — fix it or remove it.
