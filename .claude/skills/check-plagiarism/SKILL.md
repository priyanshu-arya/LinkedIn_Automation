---
name: check-plagiarism
description: Use when the user wants to check a draft for plagiarism or originality risk before publishing, or explicitly invokes /check-plagiarism. Two layers: (1) an automated internal-overlap check that invokes the plagiarism-remover skill against spans of the draft that summarize a specific cited Content-Research/ source, catching patchwriting even between the draft and its own legitimately-fetched research; (2) an honest external-check layer that is manual-only (no plagiarism-detection API is configured in this repo) -- produces the draft plus instructions to run it through a real checker (Copyscape, Originality.ai, Turnitin, Grammarly), recording only user-supplied results, never assuming a clean result without one actually being run. Callable standalone or as a step from /audit-draft via its documented input/output contract.
---

# Plagiarism / Originality Check (Phase 25)

Checks whether a draft too closely echoes existing third-party content —
distinguishing a properly cited/paraphrased claim (expected and fine,
especially for Research-pillar posts per REQUIREMENTS.md §2, which
requires reading the actual paper and explaining it in the author's own
plain-language take) from an uncredited near-verbatim lift. Two layers,
both honestly scoped, neither pretending to be more than it is.

**Designed to be called by other skills, not just run standalone.**
`/audit-draft` (Phase 19) reads the Input/Output Contract below to invoke
this skill as one more sub-step, the same way it already calls
`/humanize-draft`'s contract. That contract is the most load-bearing
section of this file — change it carefully, since `/audit-draft`'s own
SKILL.md assumes it holds exactly as written here.

## Why two layers, and why layer 2 is permanently manual

1. **Internal-overlap layer** — real, automated, buildable today. Every
   Research Note this vault's own pipeline fetched may itself quote or
   closely paraphrase the original paper/article in its Summary/Key
   Findings sections (`_Templates/Research-Note.md`). A draft that
   summarizes that source (per `sources[]`, the same field
   `/write-draft` populates from an idea's linked research — see
   `.claude/skills/write-draft/SKILL.md` step 2) can end up patchwriting
   the research note's own phrasing without anyone noticing, since both
   documents already legitimately live in this vault. This is a
   structural-closeness problem, not a copy-paste problem, and it can be
   checked automatically against material this repo already has on disk.
2. **External-check layer** — honest, manual-only, permanently. This
   layer, even at its best, only ever catches overlap with sources the
   vault's own research pipeline already fetched into `Content-Research/`.
   It says nothing about whether the draft's phrasing happens to closely
   match some OTHER webpage or post nobody cited — checking that requires
   a real web-scale plagiarism-detection service. No Copyscape,
   Originality.ai, Turnitin, or Grammarly API key exists anywhere in this
   repo (confirmed the same way `/humanize-draft`'s build confirmed no
   GPTZero/Originality.ai/ZeroGPT/Sapling/Copyleaks keys exist — see
   REQUIREMENTS.md §29). This is a permanent design stance, not a
   "for now" limitation: the skill produces the finished draft text plus
   a short instruction block asking the user to run it through a real
   checker themselves and report back whatever result they get. If
   supplied, it's recorded verbatim; if not, the output stays honestly
   `not_run` — never assumed clean.

## Input / Output Contract

This is the stable interface. Anything calling this skill programmatically
(a slash-command invocation from another skill, not just a direct user
request) should assume this shape holds across versions of this file —
modeled directly on `/humanize-draft`'s own contract
(`.claude/skills/humanize-draft/SKILL.md`).

**Input:**
- `text` (required) — the draft body to check.
- `sources` (required, may be empty) — the draft's `sources[]` list of
  Research Note ids (or Story Bank row ids, on a `--spine`-path draft —
  see below). An empty list is valid and simply means the internal-overlap
  layer has nothing to check against; it is not an error.
- `draft_id` (optional) — if given, and a real Draft Note with that `id`
  exists in `Drafts/`, this skill appends a `history` entry to it:
  `{action: edited, date: today, note: "Plagiarism/originality check via
  /check-plagiarism — <one-line summary, e.g. '1 source flagged
  patchwriting, external check not run'>"}`. If `draft_id` is given but no
  matching Draft Note exists, say so plainly and proceed with the check
  anyway — never fabricate a Draft Note or silently skip the mismatch.

**Output:**
- `internal_overlap_report` — a list of `{source_id, span, verdict}`
  entries, one per `(source, draft span discussing that source)` pair
  actually found. `verdict` is exactly one of:
  - `cited-paraphrase-ok` — the span is a genuine paraphrase (different
    structure/order, own words) of a source properly listed in `sources`.
  - `flagged-patchwriting` — `plagiarism-remover` found the span tracks
    the source's sentence order/shape too closely; includes the rewrite
    `plagiarism-remover` produced.
  - `no-overlap-detected` — the source is listed in `sources` but no span
    of `text` actually summarizes or draws on it closely enough to check
    (e.g. it's cited only in passing, or as background context).
  A `source_id` that doesn't resolve to a real `Content-Research/` note
  (or, on a spine-path draft, a real Story Bank row) is reported
  separately as `unresolved_source`, never silently dropped.
- `external_check` — `{status: "not_run" | "manual_results_provided",
  service?, result?, note}`. `status` starts and stays `"not_run"` until
  the user actually supplies a result from a real service, in this run
  or a later one. `service`/`result` are populated only when
  `manual_results_provided`.
- `caveats` — a string, **always present, every call, no exceptions**,
  stating plainly that a `not_run` external check means no real
  originality verification against the broader web has happened yet, and
  that even a `manual_results_provided` result from one service is not a
  guarantee (mirrors `/humanize-draft`'s own detector-disagreement
  honesty — no single service, and no combination of them, is ground
  truth).

## Process

### 1. Load the target draft
Read `text` and `sources[]` — either passed directly (standalone call) or
supplied by a calling skill via the contract above (e.g. `/audit-draft`).
If given a `draft-id` argument instead of raw `text`/`sources`, load the
Draft Note from `Drafts/` and pull its `## Post Text` body and `sources`
frontmatter field.

### 2. Resolve each source
For each id in `sources[]`:
- **Idea-path draft** (see `.claude/skills/write-draft/SKILL.md` step 9):
  the id should resolve to a real note in `Content-Research/`. If it
  doesn't, record it as `unresolved_source` and move on — never invent a
  research note to satisfy a mismatched id.
- **Spine-path draft**: `sources[]` holds Story Bank row ids instead of
  research note ids (per `write-draft`'s spine-path frontmatter rule).
  There is no `Content-Research/` note to compare against for these —
  record each as `no-overlap-detected` with a note that this is personal
  Story Bank material, not third-party research, so the internal-overlap
  check does not apply to it. This is expected, not a gap: a Story Bank
  Post Spine is the user's own material, not a cited external source.
- For each source that does resolve to a real `Content-Research/` note,
  read its `## Summary` and `## Key Findings` sections — the two sections
  most likely to themselves quote or closely paraphrase the original
  paper/article, per `_Templates/Research-Note.md`.

### 3. Find the draft's corresponding span for each resolved source
Identify the sentence(s) in `text` that summarize or draw specifically on
that source (the same "sentences that describe one specific cited source"
identification `plagiarism-remover` itself starts from). If no such span
exists — the source is cited but the draft never actually summarizes its
findings — record `no-overlap-detected` and move to the next source
without invoking `plagiarism-remover` (there is nothing to compare).

### 4. Invoke `plagiarism-remover` for each span found
For each draft span identified in step 3, invoke the `plagiarism-remover`
skill (a pre-existing, globally-available Claude Code skill — **not part
of this repo**) with the draft span as the text to check and the
source note's Summary/Key Findings text as the cited source to compare
against. This skill is invoked, never reimplemented: `check-plagiarism`
does not duplicate `plagiarism-remover`'s own patchwriting/
structural-closeness detection logic (clause-order comparison, the
source-by-source symmetry check across multiple citations, etc.) — it
only calls it and records what it returns.
- If `plagiarism-remover` finds the span tracks the source's structure
  too closely (patchwriting), record `flagged-patchwriting` with its
  suggested rewrite attached.
- If it finds the span is a genuine paraphrase (different structure, own
  words, source's factual content intact), record `cited-paraphrase-ok`.

### 5. Assemble `internal_overlap_report`
One entry per `(source_id, span)` pair actually evaluated, plus a
separate `unresolved_source` entry for any id from step 2 that didn't
resolve.

### 6. Present the external-check instruction block
Regardless of what step 4/5 found, present:

> This only checked the draft against sources this vault's own research
> pipeline already fetched. It says nothing about the wider internet. To
> check that, paste the finished draft into a real plagiarism checker —
> Copyscape, Originality.ai, Turnitin, or Grammarly — yourself, and tell
> me what it reports (a similarity %, a match list, whatever that service
> returns). I'll record whatever you report verbatim; I never fabricate
> or estimate this number on your behalf, and I never assume the draft is
> clean just because no result has come back yet.

If the user supplies a result (this turn or a later one), record it
verbatim in `external_check.result` (with `service` set to whichever tool
they used) and set `external_check.status` to
`"manual_results_provided"`. If they never supply one, `external_check`
stays `{status: "not_run", note: "no external plagiarism checker has been
run against this draft yet"}` indefinitely — never invent a plausible
result to fill the gap, and never let a stale prior "not_run" quietly
become an assumed-clean result just because time passed.

### 7. Always attach `caveats`
Every call, unconditionally, per the contract above.

### 8. If `draft_id` was given and resolves to a real Draft Note
Append a `history` entry: `{action: edited, date: today, note:
"Plagiarism/originality check via /check-plagiarism — <one-line
summary>"}`. If it doesn't resolve, say so and proceed anyway (same rule
as `/humanize-draft`'s `draft_id` handling).

## Report back

Every call reports, unconditionally:
- The `internal_overlap_report`, per source: which verdict, and (for any
  `flagged-patchwriting` entry) the specific span and `plagiarism-remover`'s
  suggested rewrite.
- Any `unresolved_source` entries, called out explicitly rather than
  silently dropped.
- The external-check instruction block, or the recorded result if one was
  already supplied this run or a prior one.
- The `caveats` string, verbatim, every time.
- Whether a `draft_id` history entry was logged (or why not, if a
  `draft_id` was given but no matching Draft Note existed).

## Hard rules

- Never claims an external check happened when it didn't —
  `external_check.status` starts and stays `"not_run"` until the user
  actually supplies a result from a real service. No amount of time
  passing, and no clean-looking internal-overlap result, ever converts a
  `not_run` into an assumed pass.
- Never calls any plagiarism-detection API (Copyscape, Originality.ai,
  Turnitin, Grammarly, or any other). None are configured in this repo,
  and none should be added — this is the same permanent manual-only
  stance `/humanize-draft` already takes for its detector spread check
  (REQUIREMENTS.md §29), not a placeholder for a future integration.
- Never fabricates a similarity score, a match percentage, or a "this is
  X% original" number, under any circumstance — not even as a rough
  estimate framed with hedging language.
- The internal-overlap layer only ever compares a draft against sources
  this vault's own research pipeline already legitimately fetched into
  `Content-Research/`. It makes no claim, implicit or explicit, about the
  wider internet — that claim belongs to layer 2 alone, and only once a
  real result has actually been supplied.
- Never reimplements `plagiarism-remover`'s own patchwriting/structural-
  closeness detection logic — always invokes the actual skill and records
  what it returns, the same discipline `/audit-draft` already applies to
  `/humanize-draft`'s detection logic.
- Never invents a `Content-Research/` note or Story Bank row to satisfy a
  `source_id` that doesn't actually resolve — reports it as
  `unresolved_source` instead.
- Never invents a `Draft Note` to satisfy a `draft_id` that doesn't
  actually exist — reports the mismatch instead.
- The `caveats` string is always present in the output, every call, no
  exceptions — even when every source came back `cited-paraphrase-ok` and
  nothing else seems worth flagging.
- This skill checks phrasing/structural closeness only — it never
  fact-checks a claim, never changes a claim/source/number, and never
  scores viral potential or approves/rejects a draft. Those stay
  `/critique-draft`'s and `/review-drafts`'s jobs respectively.
