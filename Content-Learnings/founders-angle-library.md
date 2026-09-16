---
id: founders-angle-library
type: founders-angle-library
version: 1
last_updated: 2026-09-17
---

Founders Angle library — the shared, canonical set of narrative structures
Post Writer (`/write-draft`, Phase 17) can optionally reach for when a draft
is grounded in the user's own Story Bank material
(`Content-Learnings/story-bank.md`) rather than research. Unlike a hook
formula (`Content-Learnings/hook-formulas.md`), which shapes only the
opening line, a founders angle shapes the **whole structure** of the post —
so it is only ever used when a real Story Bank entry (Receipt, Turning
Point, Scar, or Defensible Position) genuinely fills its bracketed
template slots. This is a single living document (same pattern as
`hook-formulas.md` and `playbook.md`), not one note per angle — rows
accumulate here over time.

*Angles adapted (not copied verbatim) from the MIT-licensed
`sergebulaev/linkedin-skills` project's `linkedin-post-writer` skill's
founder-angle reference, with local modifications for this repo's
living-doc conventions (single versioned file, `angle_id`-keyed table,
explicit canonical/proposed lifecycle, and a hard tie to Story Bank
citations) rather than that project's own file layout.*

## Angles

| angle_id | name | mechanic | pins_formulas | status | source |
|---|---|---|---|---|---|
| A1 | Reprice the Category | Correct a lazy label by exposing the mechanism behind what you sell | F10, F2 | canonical | adapted from sergebulaev/linkedin-skills (MIT) |
| A2 | Content Became Pipeline | Show how an unpopular post reached one critical person and created an outcome | F9, F11 | canonical | adapted from sergebulaev/linkedin-skills (MIT) |
| A3 | Audience of One | Demonstrate the tactic of writing for a single named person, not a generic audience | F5, F7 | canonical | adapted from sergebulaev/linkedin-skills (MIT) |
| A4 | Scarce-Shots Math | Reframe optimization around your actual constraint: a tiny number of high-stakes attempts | F10, F4 | canonical | adapted from sergebulaev/linkedin-skills (MIT) |
| A5 | Unglamorous Bet | Tell a turnaround story with real starting numbers and the unloved asset nobody priced | F7, F3 | canonical | adapted from sergebulaev/linkedin-skills (MIT) |
| A6 | Limit of Delegation | Name what AI or teams cannot absorb: the core judgment about what matters | F4, F9 | canonical | adapted from sergebulaev/linkedin-skills (MIT) |
| A7 | Designed Serendipity | Argue that controlled randomness, not pure optimization, produces distinctive output | F10, F5 | canonical | adapted from sergebulaev/linkedin-skills (MIT) |
| A8 | Evasive-Sentence Test | Surface the polished-but-hollow sentence type and name your bar for catching it | F4, F15 | canonical | adapted from sergebulaev/linkedin-skills (MIT) |
| A9 | Delegation Line | Draw a boundary between what machines may do as you and what stays human | F17 | canonical | adapted from sergebulaev/linkedin-skills (MIT) |
| A10 | Learning Gate | Dissolve the ban-vs.-review false binary with a governance system that lightens over time | F18, F20 | canonical | adapted from sergebulaev/linkedin-skills (MIT) |

Each angle's fill-in-the-blank **template** — the bracketed structure a real
Story Bank entry's slots get poured into — is kept as a bullet under the
angle's own heading below, rather than crammed into a table cell, since
several templates contain literal `|` characters that would otherwise break
the table above.

### A1 — Reprice the Category

"Everyone calls it {label}. That label sets the price—and it's wrong.
Because {mechanism} means it behaves like {high-status category}:
— {property 1}
— {property 2}
— {property 3}.
{One-line reframe.}"

### A2 — Content Became Pipeline

"{Publication} I almost didn't share turned into {concrete outcome}. It
didn't go viral—{low reach}. But one person was {role}. They {what
happened next}. [What that taught you.]"

### A3 — Audience of One

"I wrote for exactly one person: {role} at {company type}. I named
{specific thing}. I referenced {detail only they'd notice}. {What
happened.} The lesson: one person gets a hundred."

### A4 — Scarce-Shots Math

"My cycle is {N months}. Runway gives me {M} attempts—just {M}. I stopped
optimizing for {vanity metric} and started {targeted move}. When you have
{M} shots, {principle}."

### A5 — Unglamorous Bet

"{Thing} started at {tiny state—real number}. Everyone saw {reason to
pass}. I saw {one asset}. {N months} later: {current state—real number}.
The unglamorous truth: {reframe}."

### A6 — Limit of Delegation

"I delegated {list} to {agents/team}. It's faster. But it cannot do:
{un-transferable judgment}. {Concrete moment revealing the gap.} Half the
meaning was in who decides what matters."

### A7 — Designed Serendipity

"Optimize everything and you get {averaged result}. The best {things} come
from unpredictability. So I built in {deliberate randomness} with one
rule: {constraint}. {What it produced.}"

### A8 — Evasive-Sentence Test

"There's a sentence: technically correct, spiritually evasive. {Short
example.} My test: {specific question to catch it}. It's slower. It's
also the whole product."

### A9 — Delegation Line

"{Action by machine} → {outcome}. {Same action by me} → {opposite
outcome}. Only variable: who acted. So I drew a line. The agent may
{allowed acts}. It may never {human-only acts}. {Rule of thumb.}"

### A10 — Learning Gate

"Everyone reaches for {ban it} or {review everything}. Both fail because
{shared flaw}. Third option: {gate that learns}. Month one: {high
oversight}. Month six: {low oversight}. A review queue grows. A learning
system shrinks."

## Never fabricate a founder angle

An angle from this library is only ever used when the founder's own real
numbers/specifics — pulled from an actual row in
`Content-Learnings/story-bank.md` (a Receipt, Turning Point, Scar, or
Defensible Position) — genuinely fill its bracketed template slots. If no
Story Bank entry actually fits an angle's slots for the topic at hand, that
angle is **skipped entirely** for this draft, never filled with an invented
placeholder that merely looks real (a plausible-sounding number, a vague
"a company I worked with," an unnamed role). This is the same
never-fabricate discipline REQUIREMENTS.md §21 and the Story Bank (§26)
already apply — extended here to angle selection, not just fact-checking.

## Adding a new angle

Only `canonical` angles are used for drafting; `proposed` angles are visible
in this table but not yet trusted. The same append-a-`proposed`-row
lifecycle documented in `Content-Learnings/hook-formulas.md`'s "Adding a new
formula" section applies here for consistency, should this library ever
need an 11th angle: next unused `A<n>`, `status: proposed`, a `source`
naming what it was derived from, and explicit human promotion to
`canonical` before Post Writer will draft from it — never automatic, and
never just because it was used once. **`/extract-hook` does not read or
write this file** — it only ever touches `hook-formulas.md`. Building the
actual proposal mechanism for this file is out of scope for this build;
only the 10 seed angles above exist today.
