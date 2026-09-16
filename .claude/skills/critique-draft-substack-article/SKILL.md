---
name: critique-draft-substack-article
description: Use when the user asks to review/critique a Substack article's quality, check it for accuracy or duplication, compute its viral potential score, or explicitly invokes /critique-draft-substack-article. Runs the Critic Agent on a status:draft substack-article note, auto-revises it once if it scores low, and hands it off to approval by moving it to status:in_review.
---

# Critique Draft Substack Article (Critic Agent — Substack Articles)

Same process shape as `/critique-draft` (re-verify, dedup-check, score,
auto-revise once, hand off) but a genuinely different rubric — an article
is judged on depth and structure, not a scroll-stopping hook.

## Arguments

- **draft-id** (optional) — critique one specific article. If omitted, run
  against every `type: substack-article` note currently `status: draft`.

## Process (per draft)

### 1. Re-verify accuracy

Re-read `sources[]`. Confirm every claim in the article body still traces
to the linked research. Fix drift now — soften or remove, don't just flag.

### 2. Originality / duplicate check

Scan `Content-Learnings/content-index.md` filtered to `platform:
substack-article` for the same underlying story/argument/structure as an
existing article. Same severity split as `/critique-draft`: a genuine
duplicate stops here (stay `status: draft`, append `duplicate_flagged`,
report plainly); a similar-but-distinct angle just pulls the Depth/
Originality sub-score down and still reaches human review.

### 3. Score Viral Potential (0-10)

Average these, each 0-10 — reweighted for long-form:

| Factor | How to assess it |
|---|---|
| Structure / flow | Do the sections actually build on each other, or could they be reordered with no loss? |
| Depth | Does this go meaningfully beyond what a feed post on the same topic would say? |
| SEO / discoverability fit | Do title, subtitle, seo_description, seo_tags actually reflect the content and a real search intent? |
| Technical accuracy | Consistency with linked research |
| Originality | Inverse of step 2's findings |
| Reader payoff | Does the closing land an actual point of view, not a restated summary? |
| Historical playbook alignment | Check `Content-Learnings/playbook-substack.md`'s Articles section for a matching evidenced rule; otherwise neutral (5), say plainly no data exists yet |

Note there is no "hook strength" factor here in the feed-post sense — the
title/subtitle/opening paragraph are judged under Structure/Reader payoff
instead, since Substack's context (a subscriber who already opted in) is
different from a scroll-stopping feed hook.

### 4. Auto-revise once if weak

Same rule as `/critique-draft`: below 6, one targeted revision pass
re-reading `voice-guide-substack.md`'s Articles section, recompute, stop
after one pass.

### 5. Update the note

Same field updates as `/critique-draft` (`viral_score`, `history`,
`## Critic Notes` in the body, `status: in_review`) — skip entirely if
step 2 found a genuine duplicate.

## Report back

Final score, per-factor breakdown, whether auto-revised, any similar-but-
distinct flags, and word count. A note that reached `in_review` is waiting
for human approval — nothing has been approved or published.

## Notifications

Same batching rule as `/critique-draft`: one notification per run.

## Hard rules

- Never invent a "historical performance" trend with no data — score
  neutral and say why.
- Never revise more than once per run.
- Never move a genuine duplicate to `in_review`.
- Never advance to anything beyond `in_review` — approval is human-only.
