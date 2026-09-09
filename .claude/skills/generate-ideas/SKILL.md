---
name: generate-ideas
description: Use when the user asks to generate LinkedIn content ideas from the research backlog, run the Idea Ranker/Idea Engine, or explicitly invokes /generate-ideas. Turns unused Research Notes into scored, ranked candidate Idea Notes in Post-Ideas/. Does not assign ideas to specific days or draft post text — that's the Content Strategist / LinkedIn Writer (later phase).
---

# Generate Ideas (Idea Ranker — Phase 3)

Converts unused research into a pool of scored, ranked candidate LinkedIn
post ideas, written to `Post-Ideas/` using `_Templates/Idea-Note.md`. This
does not pick what gets posted this week or write any post text — it only
builds and ranks the candidate pool. Content Strategist (a later phase)
consumes this pool to plan the week; LinkedIn Writer (a later phase) drafts
the actual posts.

## Arguments

Parse from the invocation (e.g. `/generate-ideas AI 5`):
- **domain-filter** (optional) — restrict to one category folder under
  `Content-Research/`. If omitted, consider all categories.
- **count** (optional) — target number of new ideas to generate this run.
  Default target range is **10–20**, but this is a ceiling, not a quota:
  only generate from research notes that are actually usable. If the
  backlog can only support fewer good ideas, generate fewer and say so in
  the report — never pad with filler ideas to hit a number.

## Process

### 1. Gather eligible research
Read frontmatter across `Content-Research/**/*.md` (optionally filtered to
`domain-filter`). Eligible = `status: new`. Explicitly exclude
`status: placeholder` and `status: used` — placeholders are hand-written
schema examples, never real input.

### 2. Dedup against existing ideas
Before turning a research note into an idea, scan `Post-Ideas/*.md`
(frontmatter `topic`/`angle`, any status except `placeholder`) for close
matches. If a near-duplicate idea already exists, either give the new idea
a materially different angle or skip that research note this run.

### 3. Generate one idea per eligible research note
Fields (per REQUIREMENTS.md §6): `topic`, `angle`, `why_it_matters`,
`target_audience`, `format`, `hook`, `estimated_engagement` (0-10, your
judgment of how engaging this specific angle is), `suggested_visual`,
`category`, `content_type`, `sources` (the research note id(s) actually
used), `target_week` (leave blank — Content Strategist fills this in).

You may synthesize 2 closely-related research notes into a single
comparison-style idea when it is clearly stronger than two separate ideas
(e.g. an "X vs Y" format) — but only then, and only citing sources actually
used. Do not force synthesis to hit a count target.

### 4. Score `rank_score` (0-10)
Average these five, each scored 0-10:

| Factor | What it measures |
|---|---|
| Hook Strength | Is the hook specific and attention-grabbing, or generic? |
| Educational/Practical Value | Will the reader walk away with something concrete? |
| Audience Fit | Relevance to AI/dev/career LinkedIn audience |
| Non-repetition / Freshness | How different is this from existing ideas/published posts (from the dedup check in step 2) |
| Format-Content Fit | Does the chosen format actually suit this material? |

This is a static formula. Once Phase 10 (Growth Agent) has real published-post
performance data, expect these weights to be replaced with learned ones —
don't treat this rubric as permanent.

### 5. Write the Idea Note
Copy `_Templates/Idea-Note.md` into `Post-Ideas/` as
`YYYY-MM-DD--kebab-slug.md`. Fill in all fields from steps 3-4.
`status: candidate`.

### 6. Close the loop on used research
For every research note used as a source in step 3:
- Append the new idea's id to that research note's `used_in[]`.
- Flip its `status` from `new` to `used`.
This is what makes Phase 2's dedup check (skip topics already turned into
ideas) actually work over time.

## Report back

- List each new idea: filename, topic, category, content_type, rank_score.
- A diversity breakdown of the **full** candidate pool in `Post-Ideas/`
  (not just this run's additions): counts by `category` and by
  `content_type`, across all `status: candidate` ideas (excluding
  `placeholder`). If the pool is thin
  or skewed toward one category, say so plainly — that's a signal more
  `/research-topic` runs are needed before Content Strategist can build a
  properly diverse week, not something to paper over.

## Hard rules

- Never fabricate an idea from a research note that doesn't exist or is a
  placeholder.
- Never invent facts beyond what the source research note actually
  supports — an idea's `why_it_matters` and `hook` must be grounded in the
  research note's Summary/Key Findings, not embellished.
- Never assign a specific posting day/date — that's out of scope here.
- Never write LinkedIn post copy — ideas only, not drafts.
