---
id: humanizer-rules
type: humanizer-rules
version: 1
last_updated: 2026-09-17
---

Humanizer rule set — the scored, numeric 2026 AI-writing-tell reference that
`/humanize-draft` (Phase 18) applies to a draft's surface style. Single
living document (same pattern as `playbook.md`, `story-bank.md`, and
`hook-formulas.md`), not one note per rule — this file grows only by
explicit human edit, not by an automated run appending to it (unlike
`hook-formulas.md`, which `/extract-hook` appends to automatically).

**Why this exists, in one stat:** when human readers are asked what tips
them off that text was AI-written, they cite vocabulary most often (53%)
and sentence structure second (36%) — this rule set is built around those
two axes because that's where the actual signal is. The stakes for getting
it wrong aren't abstract either: LinkedIn's own slop-detection flag is
estimated to cost a flagged post roughly 40% of its normal views.

*Rules adapted (not copied verbatim) from the MIT-licensed
`sergebulaev/linkedin-skills` project's `linkedin-humanizer` skill, with
local modifications for this repo's living-doc conventions and its
manual-only, no-detector-API stance (see `.claude/skills/humanize-draft/
SKILL.md` and REQUIREMENTS.md §29).*

## AI vocabulary markers

**Durable 2026 markers** (score these — still active tells, not decaying):
significant, crucial, notably, particularly, comprehensive, insights,
robust, leverage, foster, landscape, nuanced, multifaceted, holistic,
streamline, elevate, empower.

**Decaying 2023-24 terms** (flag for scrutiny, but note they're now mostly
harmless — audiences and detectors have adapted to them and they no longer
carry much signal on their own): delve, tapestry, realm, journey, paradigm.

**Density threshold:** 3 or more markers (durable or decaying, combined)
in one paragraph triggers a rewrite of that paragraph. A single marker
alone does not warrant editing — don't chase a paragraph down to zero
just because one instance of "leverage" appears in it.

## Em-dash cap

Cap at **~1 per 100 words** — a cap, not a ban. Zero em dashes reads as
"trying too hard to look human," so removing every one is itself a tell.
For reference: GPT-5.4-era text emits roughly 1.43 em dashes per 1,000
words, well below the ~3.23-per-1,000 human baseline — meaning the ~1-per-
100-words cap here (10 per 1,000 words) is deliberately generous, not
restrictive; it's set well above both figures so it only catches genuine
overuse, not normal usage.

Excess em dashes convert to commas, colons, or parentheses — **never
periods**, since splitting into two sentences changes the rhythm too much
to count as a same-meaning style fix.

## Reveal bridges

Each of these has a measured real-world reach-impact figure. Every hit is
flagged for rewrite — there's no free allowance for these the way there is
for triads or fragments, because each one carries a documented reach cost
on its own:

| Phrase | Reach impact |
|---|---|
| "The result?" | −4.8% |
| "It's not X, it's Y" | −4.9% |
| "Stop X, start Y" | −6.7% |
| "Here's what/how" | −4.3% |

## Staccato fragment stacks

**Banned outright**, not just capped — these specific patterns get zero
tolerance regardless of count:

- "The X? Y." pseudo-questions.
- "No X. No Y. Just Z."
- "All the X. None of the Y."
- "Simple. Effective. Easy." — adjective stacks.
- One-word paragraphs ("Still." "Mostly.").

**Fragment cap:** separately from the banned patterns above, max **2**
standalone fragments per post for any other legitimate fragment use. A
3rd (non-banned-pattern) fragment triggers a rewrite of at least one of
them back into a full sentence.

## Stacked triads

A perfectly parallel rule-of-three runs at roughly 2x the rate found in
expert human writing when 3+ triads appear in one post, or when a triad is
heavily parallel-structured. Allow **one natural triad per post** — this
roughly matches the ~26% of top-performing posts that contain one — and
scrub anything beyond that.

## Performed sincerity

2026 tells, each flagged on every occurrence: "Let me be honest," "I'll be
real," "Can I be vulnerable for a second," and "Unpopular opinion:"
immediately preceding a claim that is, in fact, widely held (the setup
promises a contrarian take the sentence doesn't deliver).

Also flag inserted hedges ("perhaps," "I might be wrong") as a related
tell — performed hesitancy of this kind appears at roughly 2x the rate in
LLM-generated text versus human-written text.

## Readability target

Flesch reading ease **> 55**. No mandatory sentence-length-variance floor
beyond clearing that number.

## Odd-precision numbers

A specific, oddly-precise number (e.g. "37%" or "$4,212") only counts as a
genuine human fingerprint when it has a **named referent** attached — who
measured it, what it describes, when it happened, or what it cost. A bare
precise-looking number with no referent attached is not automatically a
positive signal — it can just as easily be a fabricated-looking or
LLM-generated-looking number wearing a human costume, so don't credit
precision alone.
