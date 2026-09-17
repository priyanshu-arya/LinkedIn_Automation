---
name: humanize-draft
description: Use when the user asks to de-AI-ify a draft, remove AI-writing tells, score AI-vocabulary/em-dash/pattern density, run a multi-detector spread check, or explicitly invokes /humanize-draft. Rewrites a draft's surface style against the scored rule set in Content-Learnings/humanizer-rules.md and produces a before/after report. Never promises to beat or guarantee undetectability by any AI-detection service — no edit reliably does; the multi-detector sub-tool only documents how much GPTZero/Originality.ai/ZeroGPT/Sapling/Copyleaks disagree, since no API keys for any of them exist in this repo. Callable standalone or as a step from another skill (Post Audit, Repurposer) via its documented input/output contract.
---

# Humanizer (Style De-AI-ification — Phase 18)

Scores and rewrites a draft's **surface style** — vocabulary density, em
dashes, reveal bridges, fragment stacks, triads, performed sincerity,
readability — against the real, numeric 2026 rule set in
`Content-Learnings/humanizer-rules.md`. It also documents, but never
claims to close, the disagreement between AI-detection services. This
skill touches style and surface only: it never re-verifies a fact, never
changes a claim/source/number, and never runs a quality/virality/accuracy
pass — that's `/critique-draft`'s job, a separate skill this one does not
call and is not called by.

*Rules adapted (not copied verbatim) from the MIT-licensed
`sergebulaev/linkedin-skills` project's `linkedin-humanizer` skill — see
`Content-Learnings/humanizer-rules.md`'s own header for the full
attribution.*

**Designed to be called by other skills, not just run standalone.** Two
later builds — Post Audit and Repurposer — read the Input/Output Contract
below to invoke this skill as a shared step. That contract is the most
load-bearing section of this file: change it carefully, since a later
build's own SKILL.md will assume it holds exactly as written here.

## Input / Output Contract

This is the stable interface. Anything calling this skill programmatically
(a slash-command invocation from another skill, not just a direct user
request) should assume this shape holds across versions of this file.

**Input:**
- `text` (required) — the draft body to humanize.
- `platform` (required) — one of `linkedin | x | substack-note |
  substack-article`. Used only to sanity-check length/format expectations
  when rewriting (e.g. an X post's fragment/brevity norms differ from a
  LinkedIn post's) — it does not change which rules apply; the rule set is
  platform-agnostic.
- `draft_id` (optional) — if given, and a real Draft Note with that `id`
  exists in `Drafts/`, this skill appends a `history` entry to it: `{action:
  edited, date: today, note: "Humanized via /humanize-draft — <one-line
  score_report summary>"}`. If `draft_id` is given but no matching Draft
  Note exists, say so plainly and proceed with the humanize pass anyway
  (a missing draft_id is not a reason to refuse the rest of the work) —
  never fabricate a Draft Note or silently skip the mismatch without
  mentioning it.

**Output:**
- `revised_text` — the rewritten draft body.
- `score_report` — one entry per rule category in `humanizer-rules.md`:
  vocabulary density (per paragraph), em-dash count vs. cap, reveal-bridge
  hits, fragment-stack hits, triad count, performed-sincerity hits.
- `detector_spread` — starts as `{status: "not_run"}`. Only becomes
  `{status: "manual_results_provided", results: [...]}` if the user
  actually pastes in scores they obtained by running the draft through the
  5 services themselves. Never any other status value.
- `changes_made` — a list of `{rule, before, after}` entries, one per
  actual edit made.
- `caveats` — a string, **always present, every call, no exceptions**,
  stating plainly that no detector-proof or guaranteed-undetectable claim
  is being made.

## Process

### 1. AI-vocabulary/pattern density scorer

Read `Content-Learnings/humanizer-rules.md` fresh every run — never rely
on a cached memory of it, since it's a living document a human may have
edited.

Tokenize `text` into paragraphs. For each paragraph, and then again at the
whole-document level where the rule is a per-post cap, apply every rule:

- **Vocabulary markers** — count durable + decaying marker hits per
  paragraph. 3+ in one paragraph flags that paragraph for rewrite; a lone
  marker is left alone. Decaying terms (delve, tapestry, realm, journey,
  paradigm) count toward the same threshold but get a lighter touch when
  rewritten, per the rule doc's "mostly harmless" note.
- **Em dashes** — count per paragraph and across the whole document; compute
  the whole-document rate per 100 words. If the document rate exceeds the
  ~1-per-100-words cap, convert excess dashes to commas, colons, or
  parentheses — starting with the paragraph(s) contributing the most dashes
  — never converting to periods, and never reducing the document to zero
  em dashes (a 0-em-dash rewrite is itself an over-correction tell, per
  the rule doc — leave at least the cap's worth of natural use in place
  when the source material had any).
- **Reveal bridges** — scan every paragraph for each of the four phrases.
  Every hit is flagged and rewritten (no per-post allowance for these,
  unlike triads/fragments) — cite the phrase's real reach-impact % in
  `changes_made`.
- **Fragment stacks** — the five banned patterns (pseudo-question
  fragments, "No X. No Y. Just Z.", "All the X. None of the Y.", adjective
  stacks like "Simple. Effective. Easy.", one-word paragraphs) are rewritten
  on sight, zero tolerance. Separately, count any other legitimate
  standalone fragment across the whole document; the 3rd such fragment
  (not one of the banned patterns) gets folded back into a full sentence
  to stay at the cap of 2.
- **Stacked triads** — count parallel rule-of-three constructions across
  the whole document. Allow the first natural one; scrub the 2nd and
  beyond (break the parallel structure or reduce to two items).
- **Performed sincerity** — flag every occurrence of "Let me be honest,"
  "I'll be real," "Can I be vulnerable for a second," and "Unpopular
  opinion:" immediately preceding a widely-held claim, plus inserted
  hedges ("perhaps," "I might be wrong"). Rewrite to remove the performed
  framing without softening or hardening the actual claim underneath it.
- **Readability** — estimate Flesch reading ease for the revised text.
  Target > 55; if the rewrite still lands under that, simplify sentence
  structure (not vocabulary substitution alone) until it clears.
- **Odd-precision numbers** — this one is never rewritten as a "tell" —
  it's a note-only check. If a specific number in the draft has no named
  referent, note that in `score_report` as "precise but uncredited," but
  do not alter, round, or remove the number itself (that would risk
  changing a claim, which this skill never does — see Hard Rules).

Log every actual edit in `changes_made` as `{rule, before, after}` — the
literal before/after text for that specific change, not a paraphrase of
what changed.

### 2. Multi-detector spread tester

This skill never calls any of GPTZero's, Originality.ai's, ZeroGPT's,
Sapling's, or Copyleaks's APIs, and never scrapes their web UIs — none are
configured in this repo (no API keys exist for any of the five), and this
is a permanent design stance, not a "for now" limitation.

Instead: output the finished `revised_text` plus a short instruction block
telling the user to paste it into each of the five services manually and
report back the scores, e.g.:

> Paste the revised draft into GPTZero, Originality.ai, ZeroGPT, Sapling,
> and Copyleaks yourself, and tell me what each one reports (a % AI-likely
> score, or whatever scale that service uses). I'll log whatever you
> report — I never fabricate or estimate these numbers on your behalf.

If the user supplies results (in this turn or a later one), record them
verbatim in `detector_spread.results` as `[{service, score, notes}]` and
set `detector_spread.status` to `"manual_results_provided"`. Add a spread
note alongside it, e.g. "scores ranged X–Y across services; treat none of
them as ground truth, and never average them into a single verdict" —
report the range, don't collapse it into one number.

If the user never supplies results, `detector_spread` stays
`{status: "not_run"}` indefinitely — never invent a plausible-looking
result to fill the gap.

### 3. Rule-explainer

Given one specific flagged pattern (e.g. "why was this em dash flagged,"
"why did you cut my triad"), look up the matching rule in
`Content-Learnings/humanizer-rules.md`, and return:
- The rule itself, as stated in that file.
- The real stat behind it (the reach-impact %, the density-rate comparison,
  the 26%/2x figures — whichever applies).
- Phrasing the user could paste directly into a reply to a human editor
  who pushed back on the change, if they want to defend the original
  stylistic choice instead of accepting the edit.

This sub-tool can run standalone, independent of a full humanize pass —
the user may ask about one flagged item without wanting the whole draft
rewritten.

## Report back

Every call reports, unconditionally:
- The full `score_report`.
- The `revised_text`.
- The `caveats` string.

Plus, when applicable: the `changes_made` list, the `detector_spread`
object (even when it's still `{status: "not_run"}` — say so explicitly
rather than omitting the field), and whether a `draft_id` history entry
was logged (or why not, if a `draft_id` was given but no matching Draft
Note existed).

## Hard rules

- Never state or imply a detector-proof, guaranteed-undetectable, or
  "will pass GPTZero" result. Always frame this as documented disagreement
  between detectors — never a pass/fail verdict.
- Never call any of the five detectors' APIs, and never scrape their web
  UIs. This is permanent, not contingent on whether keys get added later —
  if that ever changes, it's a deliberate future decision this skill does
  not make on its own.
- Never fabricate a detector score the user didn't actually supply. No
  plausible-sounding placeholder numbers, ever.
- Never silently strip all em dashes to zero. A 0-em-dash rewrite is
  itself flaggable as over-correction, per the cap being a cap, not a ban.
- Never change a claim, source, or number in the draft. This skill touches
  style/surface only — it does not re-verify or re-fact-check anything
  (that's `/critique-draft`'s job, a separate skill).
- The `caveats` string is always present in the output, every call, no
  exceptions — even when `detector_spread` is `{status: "not_run"}` and
  nothing else seems worth flagging.
- Never invent a `Draft Note` to satisfy a `draft_id` that doesn't
  actually exist — report the mismatch instead.
