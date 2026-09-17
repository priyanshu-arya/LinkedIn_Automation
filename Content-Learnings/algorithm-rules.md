---
id: algorithm-rules
type: algorithm-rules
version: 1
last_updated: 2026-09-17
---

Algorithm/ranking-mechanics rule set — the reference `/audit-draft` (Phase
19, Post Audit) checks a `status: in_review` Draft Note against before it
reaches human review. Single living document (same pattern as
`playbook.md`, `story-bank.md`, `hook-formulas.md`, and
`humanizer-rules.md`), not one note per rule.

**This file is organized into exactly three confidence tiers, and they are
never blended.** Per REQUIREMENTS.md §21 (never present an unconfirmed
claim with the same confidence as a verified one), every finding
`/audit-draft` cites must carry its tier along with it: a **Sourced
Finding** names its source, a **Verified Numeric Threshold** is a hard
number to check the draft against, and an **Unconfirmed / Third-Party
Claim** is always presented as "reported, unconfirmed" — never stated as
fact, never silently upgraded to sound as certain as the first two tiers.

*Rules adapted (not copied verbatim) from the MIT-licensed
`sergebulaev/linkedin-skills` project's reference material, with local
modifications for this repo's living-doc conventions and its explicit
three-tier confidence structure (that project does not itself distinguish
sourced/verified/unconfirmed) — see `.claude/skills/audit-draft/SKILL.md`
and REQUIREMENTS.md §30.*

## Sourced Findings

Each finding below names its real source. Cite the source alongside the
finding whenever `/audit-draft` references it — never just the number.

- **360Brew Paper (arXiv 2501.16450).** Document carousels yield 1.7–2.3x
  reach vs. a baseline single image. Hashtag behavior: semantic embeddings
  now replace tag-matching, and 5+ hashtags correlate with spam signals.
  Over-posting penalty: accounts posting 2+/day face deprioritization.
  Dwell sweet spot: 31–60 seconds generates the optimal ranking boost.
- **Gyanda Sachdeva (LinkedIn VP Product, via Social Media Today).** "We
  may limit how many comments a member can make in a time period" —
  enforcement targets automation/pods, not organic CTAs asking readers to
  comment.
- **AuthoredUp 2026 Reach Data.** Multi-image posts (3–4 personal photos)
  measure a 6.60% engagement rate, the highest measured format. Native
  video reach declined 35% YoY. Carousels show ~6x engagement vs.
  text-only. A single image now underperforms text-only by ~30%.
- **Van der Blom Algorithm Insights 2026 (~1.3M posts analyzed).** Semantic
  quality and thread depth outweigh raw comment counts — three distinct
  professional replies beat ten generic ones.

## Verified Numeric Thresholds

Hard numbers to check a draft against directly.

- **Hook cutoff:** 210 characters (desktop), 140 characters (mobile) — the
  point after which "see more" truncation applies.
- **Momentum window:** 60–90 minutes determines 80% of a post's total
  reach.
- **Length sweet spot:** 900–1,300 characters for standard posts.
- **Best posting windows:** Tue/Wed 7:30–9:00 AM in the audience's
  timezone.
- **External-link-in-body penalty:** 40–60% reach suppression — this is
  why Repurposer (a later build) moves links to the first comment instead
  of the post body.
- **Hashtag recommendation:** 0–2, placed at the end of the post.
- **Specific closing question:** 20–40% engagement lift vs. a generic CTA.

## Unconfirmed / Third-Party Claims

Explicitly low-confidence. `/audit-draft` never treats any of these as
fact in an audit's output — cite each one as "reported, unconfirmed"
every single time, not just on first mention.

- Pod detection accuracy: ~97% (unconfirmed third-party claim).
- Comment pod penalty: 60–90% reach cut, 3–14 day shadowban (unconfirmed).
- Link-in-first-comment lift: 2.1x impressions vs. in-body (reported, not
  officially confirmed).
- Save-to-like weight ratio: a save reportedly weighs 5x a like, 2x a
  comment (reported signal weight).
- Author reply visibility bump: +35% lift within the first hour (reported
  metric).
- Engagement-bait suppression: an active penalty exists per directional
  consensus, no % specified.
- Pod recovery window: 6–8 weeks (reported recovery time).

## Refresh policy

Treat this file as **stale after 90 days from `last_updated`**.
`/audit-draft` checks that gap on every run — if this file is missing, or
`last_updated` is more than 90 days old, it re-researches via `WebSearch`
against official LinkedIn engineering/creator statements and reputable
aggregators (Buffer, Hootsuite, Social Insider, AuthoredUp — same sourcing
bar as REQUIREMENTS.md §11's posting-time research) before applying the
audit, then rewrites this file with fresh findings, preserving the same
three-tier confidence structure above. This is the same lazy
"self-refresh on use" pattern `/generate-visual` already applies to live
visual-trend research (REQUIREMENTS.md §7) — there is no separate
cron/scheduled job that keeps this file current.
