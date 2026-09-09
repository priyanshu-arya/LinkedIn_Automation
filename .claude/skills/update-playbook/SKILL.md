---
name: update-playbook
description: Use when the user wants to analyze content performance, update the Content Playbook, run the Growth Agent, or explicitly invokes /update-playbook. Derives evidence-backed rules from Analytics/ data and updates Content-Learnings/playbook.md. Refuses to invent a pattern when the sample size is too small.
---

# Update Playbook (Growth Agent — Phase 10)

Turns real Analytics data into structured, evidence-cited rules in
`Content-Learnings/playbook.md`, closing the loop described in
REQUIREMENTS.md §17-18. This is the only skill that writes to the
playbook.

## Minimum evidence bar

**Do not add or change a rule unless at least 3 published posts support
it**, and always cite their ids and the sample size next to the rule
(e.g. "n=4"). With fewer than 3 published posts total, run the report step
only and say plainly there isn't enough data yet — do not lower the bar to
produce something to write.

## Process

### 1. Gather data
For every note in `Published-Posts/`, read its metadata (category, format,
length, hook_style, hashtags, posting day/time) and its linked
`Analytics/` snapshot history (latest values, and trend across snapshots
if there are several).

### 2. Look for patterns, only where the evidence bar is met
Compare average `engagementRate` (and other metrics where meaningful)
across groupings: by category, by content_type, by hook_style, by length
bucket (e.g. <1000 / 1000-2000 / >2000 chars), by posting weekday, by
hashtag set. A pattern is reportable only if:
- at least 3 posts sit in each side of the comparison, and
- the difference is large enough to plausibly not be noise (use judgment,
  but a marginal 5% difference on n=3 is not a rule — say so).

### 3. Update the Playbook
For each pattern meeting the bar, add or update a row in
`Content-Learnings/playbook.md`'s Best-Performing Patterns or
Anti-Patterns table: the rule in plain language, the evidence (post ids),
a confidence level (`low` for n=3-4, `medium` for n=5-9, `high` for n=10+),
and today's date. Bump `version` and `last_updated` in the frontmatter.

If a previously-recorded rule is contradicted by newer data, update or
remove it rather than leaving stale, wrong guidance in place — note the
reversal explicitly rather than silently deleting the old row.

### 4. Topic Fatigue Watch
Flag categories/topics posted 3+ times in the last ~4 weeks with flat or
declining engagement across those posts, in the Topic Fatigue Watch
section.

## Report back

State plainly: how many published posts exist, how many met the evidence
bar for any comparison, which rules were added/updated/removed, and — just
as important — which comparisons were attempted but skipped for
insufficient data. A playbook that honestly says "not enough data yet" is
more useful than one padded with weak inferences.

## Hard rules

- Never add a rule backed by fewer than 3 posts.
- Never treat a missing/null metric (see `/pull-analytics`) as a zero when
  computing averages — exclude it, don't count it against the post.
- Never silently overwrite a rule's evidence trail — corrections are
  logged, not erased.
