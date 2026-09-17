---
name: repurpose-post
description: Use when the user wants to turn content from another platform (a tweet/thread, YouTube video, blog post, or newsletter) into a native LinkedIn post, or explicitly invokes /repurpose-post. Re-hooks the source for LinkedIn's fold, expands it into the 900-1,300 character sweet spot (REQUIREMENTS.md §30's verified threshold) with added context — never padding — moves any link out of the body into a first-comment field (per §30's documented 40-60% in-body-link reach penalty), runs the result through /humanize-draft, and writes it to Drafts/ via the standard Draft-Note.md status:draft flow. Never fabricates what a source said — if it can't be reliably read (per REQUIREMENTS.md §27), it asks for a manual paste instead of guessing.
---

# Repurposer (Cross-Platform → LinkedIn — Phase 20)

Turns content from another platform — a tweet/thread, YouTube video, blog
post, or newsletter — into a native LinkedIn post: re-hooked for the fold,
expanded into the algorithm's verified length sweet spot, with any link
moved out of the body, run through the Humanizer, and written to `Drafts/`
via the same `status: draft` flow every other draft uses. This is the
first skill in this repo that goes **other platform's content → LinkedIn**
— every existing multi-platform writer (`write-draft-x`,
`write-draft-substack-article`/`-note`) goes the opposite direction,
LinkedIn-pipeline idea → another platform. This skill adds a new *input*
path only; it never adds a new approval path (REQUIREMENTS.md §31).

## Arguments

- **source-type** (required) — one of `tweet`, `thread`, `youtube`, `blog`,
  `newsletter`. Determines which input-handling rule below applies.
- **source** (required) — either a URL or pasted content (text, transcript
  excerpt, or summary), per the source-type-specific rules below. Both a
  URL and pasted text may be given together (e.g. URL for reference/dedup
  filing, pasted text as the actual content to draft from).

## Input handling (per source type)

All four source types sit under REQUIREMENTS.md §27's shared "reading
third-party post content" convention: **no official API exists anywhere in
this repo for reading an arbitrary third-party post/page/video from just a
URL**; pasted text is the primary, reliable input; a URL is best-effort
metadata only; no skill in this repo scrapes, uses session cookies, or
otherwise bypasses login/ToS. This skill cross-references §27 rather than
restating it — what follows is only the source-specific judgment call on
top of it.

- **Tweet/thread:** per §27, pasted text is primary. A URL may be attempted
  via `WebFetch` as a best-effort convenience, but X/Twitter typically
  requires login for full content server-side — treat any fetch result as
  unverified. Show the user what was fetched and ask them to confirm it
  matches what they actually see when they view the post themselves, or
  ask for the text pasted directly, before proceeding to extraction.
- **YouTube video:** a **mandatory manual-paste case, permanently**. No
  tool in this session's toolset retrieves YouTube captions/transcripts,
  and `WebFetch` on a YouTube URL returns the page shell (title,
  description, metadata), not the transcript. Always ask for a pasted
  transcript excerpt or a written summary of the key point(s) — never
  attempt a fetch expecting transcript content, and never claim to have
  "watched" or reliably retrieved the video's content. This is a
  deliberate, permanent design stance, not a gap to fill later.
- **Blog/newsletter:** `WebFetch` is genuinely plausible here (ordinary
  HTML renders fine) — attempt it as the primary path. Fall back to asking
  for pasted text only if the fetch fails outright or returns unusable
  content (a paywall, a JS-rendered body that comes back empty/garbled, or
  a result that's mostly navigation/boilerplate rather than the article
  itself).

If nothing usable is obtained through any of the above — fetch failed,
fetch returned unverified/unusable content and the user didn't confirm or
paste an alternative, or no source was given at all — **stop and ask for a
manual paste**. Never proceed to extraction or drafting on a guess.

## Process

### 1. Get source content
Per the input-handling rules above. Do not proceed past this step without
usable, confirmed-or-pasted content.

### 2. Extract the core claim(s) and any link(s)
Identify the core argument/claim(s) the source actually makes, and any
link(s) worth preserving (the source's own URL, or a link it cites). Do
not carry over any statistic, quote, or claim not literally present in
what was actually retrieved or pasted — the same never-fabricate
discipline every drafting skill in this repo applies to its own grounding
material (REQUIREMENTS.md §21).

### 3. Dedup / fatigue check
Check `Content-Learnings/content-index.md` for topic/hook/argument overlap
with existing drafts or published posts — the same discipline
`/write-draft`'s pipeline (via `/critique-draft`) and `/generate-ideas`
already apply (REQUIREMENTS.md §15/§25.4). If `content-index.md` doesn't
exist yet or is too thin to trust, fall back to scanning `Drafts/` and
`Published-Posts/` directly. Flag — don't silently draft — if this
repurposed angle duplicates something recent; a flag doesn't block
drafting, but it must be surfaced plainly in the report back.

### 4. Read the voice guide
Read `Content-Learnings/voice-guide.md` fresh (never a cached memory of
it, since it's a living document) before drafting.

### 5. Re-hook for the fold
LinkedIn truncates behind a "see more" click after roughly the hook-cutoff
thresholds in `Content-Learnings/algorithm-rules.md`: **210 characters on
desktop, 140 on mobile** (REQUIREMENTS.md §30, Verified Numeric
Threshold). Write a genuinely **new** first 1-2 sentences that state the
concrete claim/tension on their own — this is a rewrite of the opening,
not a trim of the source's own opening line, which was written for a
different platform's context/audience assumptions (a tweet's first line
assumes a very different reader attention pattern than a LinkedIn feed
scroller does).

### 6. Expand to the length sweet spot
Expand into the **900–1,300 character** sweet spot (REQUIREMENTS.md §30,
Verified Numeric Threshold — cited, not re-derived) via:
- (a) a concrete example or analogy **consistent with but not present in**
  the source,
- (b) unpacking an implication the source stated tersely,
- (c) adding the personal-take framing LinkedIn favors ("here's what I'd
  add...", "the part I keep coming back to...").

Never add a new *factual* claim beyond what the source actually said —
expansion is framing/elaboration only, never new unverifiable facts.

### 7. Move any link to the first-comment field
Per REQUIREMENTS.md §30's documented **40-60% external-link-in-body reach
penalty** (Verified Numeric Threshold), any link worth preserving does not
go in `## Post Text`. Store it in the Draft Note's `source_link`
frontmatter field instead (see step 10), and note explicitly in the
"Report back" that it needs to be posted as the first comment manually
after the LinkedIn post itself goes live — this repo has no mechanism to
auto-post a follow-up comment (same deliberate-manual precedent as visuals,
REQUIREMENTS.md §7, and Substack publishing, §25.3).

### 8. Hashtags
3-5, directly tied to topic/category, no stuffing — same convention
`/write-draft` uses.

### 9. Humanize the draft
Call `/humanize-draft`'s documented Input/Output Contract
(`.claude/skills/humanize-draft/SKILL.md`) as the final style pass:
- `text` = the drafted body from steps 5-8.
- `platform` = `"linkedin"`.
- `draft_id` = left unset on this first call (the Draft Note doesn't exist
  yet — it's created in step 10, immediately after).

Use the returned `revised_text` as the final post copy. Do not
re-implement any of Humanizer's own vocabulary/em-dash/pattern-density
detection logic here — call the contract, use its output.

### 10. Write the Draft Note
Copy `_Templates/Draft-Note.md` into `Drafts/` as
`YYYY-MM-DD--kebab-slug.md` (today's date — a repurposed post has no
`target_date` to inherit from an Idea Note). Fill in:
- `platform: linkedin`, `status: draft`.
- `category`, `format`, `hook_style` — same judgment call `/write-draft`
  applies, based on the repurposed content's actual topic/shape.
- `hashtags` from step 8.
- `source_type` — the `source-type` argument (`tweet | thread | youtube |
  blog | newsletter`).
- `source_link` — the link from step 7, or left blank if the source had
  none or none was worth preserving.
- `idea_id` and `spine_id` both left empty — this draft has neither; it did
  not come from an Idea Note or a Story Bank Post Spine. Its grounding is
  the `source_type`/`source_link` fields instead; `scripts/validate_vault.py`
  treats a non-empty, non-"none" `source_type` as a third valid grounding
  for the vault schema's idea/spine check, so this is expected to validate
  cleanly, not an error to work around. Never fabricate an `idea_id` or
  `spine_id` to satisfy a check that doesn't apply to this path.
- `sources`: the vault schema requires this list non-empty on every Draft
  Note (same as the idea/spine paths), and there's no research-note or
  Story Bank row id to cite here — populate it instead with the source
  reference itself (the URL if one exists, e.g. `"https://x.com/..."`, or
  a short descriptive string like `"pasted tweet, no URL given"` /
  `"pasted YouTube transcript excerpt, no URL given"` if none does). This
  keeps the citation-retention discipline (REQUIREMENTS.md §17) intact even
  though the grounding is external content, not an internal Research Note.
- `hook_formula`, `engagement_goal`, `founders_angle`: leave blank — this
  skill doesn't select a canonical hook formula or founders angle; its
  hook comes from the re-hook step (5), not the shared formula taxonomy.
- `history`: `[{action: created, date: today, note: "Repurposed via
  /repurpose-post from <source_type>: <one-line description or URL of the
  actual source>"}]`.
- `## Post Text`: the Humanizer's `revised_text` from step 9.
- `## Sources (internal — not part of the post)`: the source content's own
  reference (URL if given, or "pasted <source_type> content, no URL
  given") — for traceability, not for publication.

Leave `viral_score` at 0 and `visual_ids` empty — scoring and visuals are
`/critique-draft` and `/generate-visual`'s jobs, not this skill's.

## Report back

- The full drafted post text and its character count (confirm it lands in
  the 900-1,300 sweet spot, or say by how much it doesn't and why).
- The hashtags used.
- The first-comment link text, if any, and an explicit reminder that
  posting it is a manual step after the LinkedIn post goes live.
- Which piece of source content backed each claim/example in the draft —
  traceable back to what was actually fetched/pasted.
- The `content-index.md` dedup check result (clean, or what it flagged).
- The Humanizer pass's `caveats` string, surfaced verbatim, plus its
  `score_report` and `changes_made` if non-trivial.
- A plain statement that this is `status: draft`, waiting for
  `/critique-draft` next — nothing has been approved, scheduled, or
  published, and no comment has been auto-posted anywhere.

## Hard rules

- Never carry over a stat, quote, or claim from the source that isn't
  literally present in the fetched-and-confirmed or pasted content.
- Never fabricate what a tweet/thread/video/article said if the fetch
  attempt failed or returned unusable content — stop and ask for a manual
  paste instead of guessing or paraphrasing from a title/preview alone.
- Never claim a YouTube transcript was "watched" or reliably retrieved —
  this is always a manual-paste case, permanently, not a temporary
  limitation.
- Never treat an unconfirmed WebFetch result (tweet/thread) as ground
  truth — get the user's explicit confirmation, or a direct paste, first.
- Never auto-publish or auto-post the first comment. Output is always
  `status: draft`, flowing through the existing `/critique-draft` →
  `/audit-draft` → `/review-drafts` → `/schedule-approved` pipeline
  unchanged.
- Expansion (step 6) adds framing, examples, and elaboration only — never
  a new unverifiable fact, statistic, or quote beyond what the source
  actually said.
- Never leave a link in `## Post Text` — it always moves to `source_link`
  once one exists worth preserving.
- Never silently draft a near-duplicate of a recent post — the
  `content-index.md` check must be run and its result reported, even when
  clean.
