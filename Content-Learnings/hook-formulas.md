---
id: hook-formulas
type: hook-formulas
version: 1
last_updated: 2026-09-17
---

Hook Formula taxonomy — the shared, canonical classification of hook
opening mechanics that `/extract-hook` (Phase 16) classifies real posts
into, and that Post Writer (a later, separate build) reads from to draft
new posts against a known-working formula rather than a blank page. This
is a single living document (same pattern as `playbook.md` and
`story-bank.md`), not one note per formula — rows accumulate here over
repeated `/extract-hook` runs.

*Taxonomy adapted (not copied verbatim) from the MIT-licensed
`sergebulaev/linkedin-skills` project's `linkedin-post-writer` skill's
formula reference, with local modifications for this repo's living-doc
conventions (single versioned file, `formula_id`-keyed table, explicit
canonical/proposed lifecycle) rather than that project's own file layout.*

## Formulas

| formula_id | name | mechanic | engagement_goals | status | source |
|---|---|---|---|---|---|
| F1 | Platform Risk Anaphora | Repeated phrase structure highlighting category vulnerabilities | | canonical | adapted from sergebulaev/linkedin-skills (MIT) |
| F2 | R.I.P. Obituary | Frame an ending era or industry pivot as a farewell | reposts | canonical | adapted from sergebulaev/linkedin-skills (MIT) |
| F3 | Year-over-Year Pivot | Identity shift or founder reflection using year-based comparison | | canonical | adapted from sergebulaev/linkedin-skills (MIT) |
| F4 | Time-Anchor Confession | Dated vulnerability revealing voice reset or audience re-targeting | comments | canonical | adapted from sergebulaev/linkedin-skills (MIT) |
| F5 | Self-Proving Meta | Public commitment or in-the-open test demonstrating accountability | | canonical | adapted from sergebulaev/linkedin-skills (MIT) |
| F6 | Comment-Gate Lead Magnet | Engagement CTA linked to real deliverable (use cautiously) | | canonical | adapted from sergebulaev/linkedin-skills (MIT) |
| F7 | Odd-Precision Money Ledger | Cost breakdown or founder build-log opening with specific numbers | saves | canonical | adapted from sergebulaev/linkedin-skills (MIT) |
| F8 | Paid-vs-Free Reversal | Free framework giveaway flipping conventional commercial logic | reposts, saves | canonical | adapted from sergebulaev/linkedin-skills (MIT) |
| F9 | Curiosity-Gap Teaser | Behind-the-scenes or emergent behavior; pay off within 2 lines | comments | canonical | adapted from sergebulaev/linkedin-skills (MIT) |
| F10 | Contrarian + Historical Receipts | Sacred-cow challenge backed by data or precedent | comments | canonical | adapted from sergebulaev/linkedin-skills (MIT) |
| F11 | Emotional Cold-Open | Real story with emotional stakes optimized for likes | likes | canonical | adapted from sergebulaev/linkedin-skills (MIT) |
| F12 | Permission Slip | Reassurance or encouragement; needs a dated fact, use with care | comments | canonical | adapted from sergebulaev/linkedin-skills (MIT) |
| F13 | Bait-and-Switch Reversal | Policy or process upgrade framed as a pleasant surprise | likes | canonical | adapted from sergebulaev/linkedin-skills (MIT) |
| F14 | Named Gratitude / Tribute | Thanking mentors, team, or departing colleagues | reposts | canonical | adapted from sergebulaev/linkedin-skills (MIT) |
| F15 | Explain-to-Kids | Demystify jargon or complex concepts | saves | canonical | adapted from sergebulaev/linkedin-skills (MIT) |
| F16 | Status-Strip Humility | Senior voice prioritizing warmth over authority | likes | canonical | adapted from sergebulaev/linkedin-skills (MIT) |
| F17 | Controlled A/B Anecdote | One-variable comparison (delegation, AI, etc.) for structured insight | comments | canonical | adapted from sergebulaev/linkedin-skills (MIT) |
| F18 | False-Binary Dissolve | "Both obvious answers fail" governance frame; use with care | | canonical | adapted from sergebulaev/linkedin-skills (MIT) |
| F19 | Anecdote-Meets-Evidence Bridge | Personal observation paired with a data stack | | canonical | adapted from sergebulaev/linkedin-skills (MIT) |
| F20 | Diverging-Curves Close | Two trajectories diverging into a quotable maxim | reposts | canonical | adapted from sergebulaev/linkedin-skills (MIT) |

## Adding a new formula

When `/extract-hook` finds a real post whose hook doesn't fit any
canonical formula well, it **appends a new row** rather than forcing a
bad match or refusing to classify — a hook is never dropped for lack of a
perfect fit. The new row uses:

- `formula_id` — next unused `F<n>` in sequence.
- `status: proposed` (never `canonical` on first append — see lifecycle
  below).
- `source: extracted from <short post reference/date>` (e.g. "extracted
  from LinkedIn post, 2026-09-20") — never the generic seed-source string
  used for the 20 rows above.
- A short illustrative excerpt of the hook **line only**, not the full
  post, in the `mechanic` or a trailing note — enough to recognize the
  pattern later, never a full reproduction of someone else's post.

**Canonical/proposed lifecycle.** `proposed` rows are visible in this
table but not yet trusted: `/extract-hook` and Post Writer both only ever
read `canonical` rows for drafting/matching purposes. A `proposed` row is
promoted to `canonical` only by explicit human confirmation — e.g. during
`/review-drafts`, or a manual edit to this file's `status` column — never
automatically, and never just because it was used once.
