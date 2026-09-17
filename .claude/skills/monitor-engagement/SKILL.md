---
name: monitor-engagement
description: Use when the user wants to check their comment threads for new author replies and get a follow-up drafted, or wants to pull a post's likers/commenters and group them by ICP fit (peer/aspirational/prospect), or explicitly invokes /monitor-engagement. Two manual-input, read-side workflows -- LinkedIn exposes neither of these programmatically anywhere in this repo (confirmed against pull-analytics's Buffer-scoped-to-own-posts limitation), so both work from text the user pastes in, never live scraping. Delegates actual reply drafting to /draft-reply rather than reimplementing it. Never posts anything itself.
---

# Engagement Monitor (Phase 24)

Two read-side workflows for tracking engagement the user already has,
rather than producing new outbound content — genuinely different from
every drafting skill in this repo so far, since this one watches for
*incoming* activity.

**Feasibility gap — stated plainly, not softened:** confirmed against
`pull-analytics/SKILL.md` (REQUIREMENTS.md §9) — Buffer's API only
returns metrics for the user's OWN scheduled/published posts. There is no
live data source anywhere in this repo for (a) knowing when someone
replied to the user's comment on someone else's post, or (b) a
likers/commenters list for an arbitrary post. **Both workflows below are
manual-input only, permanently** — the user pastes in the current thread
text or a likers/commenters list; this skill never fetches either live.

**Reading third-party post/comment content:** see REQUIREMENTS.md §27 —
pasted text is the primary, reliable input; a post URL is optional
metadata only. No scraping, no session-cookie/unofficial API access,
ever — same convention as `/extract-hook`, `/draft-comment`, and
`/draft-reply`. This is the third and last of the three skills §27 names.

## Modes

- `/monitor-engagement threads` — Workflow 1, thread watch.
- `/monitor-engagement audience <post-url-or-id>` — Workflow 2, audience
  pull.

If it's ambiguous which mode is meant (e.g. just `/monitor-engagement`
with no argument and no clear context), ask rather than guessing.

---

## Workflow 1 — Thread Watch (`/monitor-engagement threads`)

### Feasibility gap (this workflow specifically)

There is no notification/polling mechanism anywhere in this repo for
third-party reply activity — no webhook, no API, nothing that tells this
system when someone replies to the user's comment on someone else's post.
Every run is a manual snapshot: the user reads the thread themselves,
pastes its current visible text, and this skill diffs that against what's
already logged for that thread.

### Storage

One file per tracked thread: `Engagement/<post-slug>--thread.md`, created
from `_Templates/Engagement-Thread-Note.md` when the thread is new.

Frontmatter: `id`, `type: engagement-thread`, `post_url`,
`my_comment_text`, `my_comment_time` (user-supplied — no API confirms
this), `status: watching|closed`.

Body: a `## Logged Replies` table — `author | text_snippet | seen_date`.

### Process

1. The user gives the post URL, pastes the thread's current full visible
   text, and — on the first run for this thread only — their own
   comment's timestamp.
2. Find or create the tracking note:
   - New thread → create `Engagement/<post-slug>--thread.md` from the
     template, filling `post_url`, `my_comment_text`, `my_comment_time`,
     `status: watching`.
   - Existing thread → load it; reuse its stored `my_comment_time`.
3. Diff the freshly pasted thread text against the note's
   `## Logged Replies` table. Entries not already present (matched by
   author + text) are "new." Never fabricate a reply that isn't actually
   present in the pasted text, and never claim "no new replies" beyond
   what was actually pasted this run.
4. For each new reply, compute elapsed time from `my_comment_time` to
   today (the diff run's date, not necessarily when the reply actually
   posted — **state plainly this is an approximation, not a guaranteed
   reply-time measurement**):
   - **Under 6h elapsed** → log the reply in the table; defer drafting —
     too soon to know if more replies are still coming in on this thread.
   - **6-24h elapsed** → delegate to `/draft-reply`'s single-reply mode
     (passing the reply's text and any available post context) to draft
     a follow-up now. Do not reimplement drafting logic here — always
     call `/draft-reply` for the actual draft.
   - **Over 24h elapsed** → log the reply, still delegate to
     `/draft-reply` for a draft, but flag in the report: "window likely
     passed, lower priority."
5. Write the updated `## Logged Replies` table back to the note —
   append new rows, never remove or overwrite existing ones — so the
   next run only reports genuinely new activity.

### Report back

For each new reply: author, text snippet, elapsed-time bucket, and either
the `/draft-reply`-delegated draft or "logged, drafting deferred" (the
under-6h case). If the pasted text contains nothing beyond what's already
logged, say that plainly rather than inventing something to report.

---

## Workflow 2 — Audience Pull (`/monitor-engagement audience <post-url-or-id>`)

### Storage

One file per captured snapshot: `Engagement/<post-slug>--audience.md`,
created from `_Templates/Engagement-Audience-Note.md`.

Frontmatter: `id`, `type: engagement-audience`, `post_url`,
`captured_date`.

Body: one table per ICP category — Peer / Aspirational / Prospect —
columns `name | title_or_headline | notes`.

### ICP rubric

Applied to whatever job title/headline text the user actually pasted —
always a suggestion the user can correct, never asserted as settled fact:

- **Peer** — an individual-contributor/similar-seniority title in
  AI/ML/data/engineering, doing comparable work.
- **Aspirational** — a senior/leadership title (Director, VP, Head of,
  Principal, Founder) or a recognizable figure the user doesn't already
  have an existing peer relationship with.
- **Prospect** — a title with hiring/buying power relevant to the user
  (recruiter, hiring/engineering manager, founder hiring).

### Process

1. The user gives a post URL/id and pastes the likers/commenters list —
   name plus title/headline, whatever's actually visible on the post.
   Per §27, this is never fetched live.
2. Classify each person via the rubric above.
3. Before finalizing each classification, check
   `Content-Learnings/icp-map.md`'s `## Mappings` table for that name.
   - If found, reuse the existing category instead of re-guessing — but
     still surface it in the report so the user can correct a stale
     classification if the person's role has changed since it was last
     confirmed.
   - If the name isn't there, or the classification is genuinely
     ambiguous (e.g. a title that could plausibly be Peer or
     Aspirational), ask the user to confirm before finalizing it.
4. Write confirmed classifications into `Content-Learnings/icp-map.md`
   (append-only: a new row for a first-time name, an updated
   `last_confirmed_date` for a re-confirmed one — never delete history)
   and write the full snapshot (every name captured this run, not just
   the newly classified ones) into the new
   `Engagement-Audience-Note.md`.

### Report back

The classified list grouped by ICP category (Peer / Aspirational /
Prospect), with each name flagged as either "from icp-map.md" (reused) or
"classified this run" (fresh) — so the user can see at a glance which
entries were newly judged versus carried over from a prior run.

---

## Hard rules

- Never fabricate a reply, liker, or commenter not present in what the
  user actually pasted.
- Never claim "no new replies" beyond what was actually pasted this run.
- Never auto-post a follow-up, a comment, or anything else — Workflow 1's
  drafting is always delegated to `/draft-reply`, which itself never
  auto-posts (its output is copy-paste text for manual posting).
- ICP labels are suggestions pending the user's confirmation, never
  asserted as settled fact.
- No scraping, no session-cookie/unofficial API access, ever — same
  convention as every other skill referencing REQUIREMENTS.md §27, and
  this rule never changes: no live-polling or scraping capability gets
  added to this skill later.
- Elapsed-time buckets in Workflow 1 only decide *whether/when* to
  delegate a draft — never invent what a reply says based on how much
  time has passed.
