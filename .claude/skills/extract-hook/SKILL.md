---
name: extract-hook
description: Use when the user wants to reverse-engineer the hook formula behind an existing viral post, or explicitly invokes /extract-hook. Takes pasted post text (URL accepted as best-effort only, per REQUIREMENTS.md §27 — never treated as reliable on its own) and classifies its opening against the shared taxonomy in Content-Learnings/hook-formulas.md, returning a blank fill-in-the-blank template. If the formula isn't in the taxonomy yet, proposes a new entry citing the source post rather than forcing a bad match or refusing to classify. Never claims a match guarantees virality — pattern-matching only, not a scoring or drafting tool.
---

# Hook Extractor (Phase 16)

Reverse-engineers the **hook formula** behind an existing post — pasted
text, ideally someone else's viral post but any post works — and returns
a blank, fill-in-the-blank template of that formula's structure. Classifies
against the shared taxonomy in `Content-Learnings/hook-formulas.md`, which
Post Writer (a later, separate build) also reads from to draft new posts.
This skill never drafts a finished post itself — output is always a blank
template, never ghostwritten content.

*Taxonomy adapted (not copied verbatim) from the MIT-licensed
`sergebulaev/linkedin-skills` project's `linkedin-post-writer` skill's
formula reference — see `Content-Learnings/hook-formulas.md`'s own header
for the full attribution.*

**Reading third-party post content:** see REQUIREMENTS.md §27 — pasted
text is the primary, reliable input; a URL is optional metadata only, and
a WebFetch attempt on it is best-effort convenience, never ground truth.

## Arguments

- **post text** (primary) — the user pastes the post they want classified,
  directly in the conversation.
- **URL** (optional, best-effort only) — if the user gives a URL instead
  of or alongside pasted text, per §27: attempt a WebFetch, but never
  treat its result as reliable on its own.

## Process

### 1. Get the input, per §27's convention
- If pasted text is provided: use it directly as ground truth.
- If only a URL is given: attempt WebFetch on it. Then look hard at what
  came back — a login wall, a truncated/partial extract, or missing the
  actual post body are all common outcomes, not edge cases. If the result
  looks truncated, gated, or otherwise unreliable, say so explicitly to
  the user and ask them to paste the full post text before proceeding.
  Never silently proceed to classify a partial or gated fetch as if it
  were the whole post.
- If neither is given, ask the user to paste the post.

### 2. Load the taxonomy fresh
Read `Content-Learnings/hook-formulas.md` in full — every row, every run.
Never rely on a cached memory of the taxonomy, since it grows over time as
this skill (and human promotions) add to it.

### 3. Isolate the hook
The hook is the first 1-3 lines / the first visible fold — what a reader
sees before "…see more". Quote it back to the user so there's no ambiguity
about what's being classified.

### 4. Classify along four dimensions
- **Opening mechanic** — how the first line grabs attention (claim,
  confession, number, contrarian statement, etc.).
- **Tension/curiosity device** — what makes a reader want line 2 (a gap,
  a contradiction, unresolved stakes).
- **Pacing** — line-break rhythm and sentence-length curve (short punchy
  fragments vs. a longer developing sentence).
- **Payoff device** — how (or whether, within the hook itself) the
  tension starts to resolve.

### 5. Match against the taxonomy, or propose a new formula
Compare the four-dimension read against every `canonical` row in
`hook-formulas.md` (never match against a `proposed` row — those aren't
trusted yet). Pick the best real match.

If nothing fits well: **never force a bad match, and never refuse to
classify.** Instead, append a new row to `hook-formulas.md`'s table per
that file's own "Adding a new formula" rule — next unused `F<n>`,
`status: proposed`, `source: extracted from <short post reference/date>`,
and a short illustrative excerpt of the hook line only (never the full
post). This is a live edit to a shared file — make it for real, don't just
describe it.

### 6. Produce the blank template
Strip the matched (or newly proposed) formula down to a fill-in-the-blank
skeleton the user can reuse for a *different* post — never the source
post's actual words, always blanked placeholders describing what goes in
each slot.

## Output shape

```
FORMULA: F10 — Contrarian + Historical Receipts (matched, canonical)
Line 1 (claim reversal): "[Everyone believes ___. Here's why that's wrong.]"
Line 2 (stakes): "[What it costs you to keep believing it]"
Body: [2-4 concrete evidence beats, one per short paragraph]
Payoff: [the reframe/insight that resolves the tension]
CTA: [question tied directly to the payoff, not generic]
```

(The exact slots vary by formula — this is illustrative of the shape, not
a fixed universal schema. Build the slots from what the actual hook is
doing, per step 4's four dimensions.)

## Report back

- Which formula matched, and whether it was `canonical` or newly
  `proposed` this run.
- The blank fill-in-the-blank template (full output shape above).
- If a new formula was proposed: say so plainly, note it was appended to
  `Content-Learnings/hook-formulas.md` as `status: proposed`, and that it
  needs explicit human promotion to `canonical` (e.g. during
  `/review-drafts`, or a manual edit) before Post Writer will draft from
  it — this skill does not promote its own proposals.

## Hard rules

- Never fabricate what a post says beyond text actually provided — pasted
  text, or a WebFetch result the user has explicitly confirmed matches
  what they see. No inferring the "rest of the post" from a login wall.
- Never claim a WebFetch succeeded when it returned a login wall, a
  paywall, or obviously partial/stripped content — say so plainly instead.
- Never assert that matching a formula "guarantees" engagement or
  virality. This is descriptive pattern-matching against past structure,
  not a scoring tool (that's `/critique-draft`'s Viral Potential Score,
  a different mechanism) and not a prediction.
- Store only a short illustrative excerpt of a source post in
  `hook-formulas.md` when proposing a new formula — the hook line only,
  never a full reproduction of someone else's post.
- Output is always a blank template, never a finished ghostwritten post —
  turning a template into an actual new post is Post Writer's job, a
  separate, not-yet-built skill.
- Never drop a hook that doesn't fit the taxonomy well, and never force it
  into a canonical formula just to avoid proposing a new one.
