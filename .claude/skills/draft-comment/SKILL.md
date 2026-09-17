---
name: draft-comment
description: Use when the user wants a comment drafted for someone else's LinkedIn post, or explicitly invokes /draft-comment. Takes the post's pasted text (a URL alone is not reliable input — see REQUIREMENTS.md §27) plus optional context, and writes 1-2 copy-paste-ready comment options in the user's own voice per Content-Learnings/voice-guide.md. Never posts anything itself — there is no comment-posting API in this pipeline, same as there's no read API for arbitrary third-party posts.
---

# Comment Drafter

Drafts a comment to leave on **someone else's** LinkedIn post, in the
user's own voice. Lightweight, mostly ephemeral utility — not part of the
Drafts/ approval pipeline. Output is copy-paste text in the response; there
is no Draft Note, no vault schema, no file write, for a single ad-hoc
comment.

**Reading third-party post content:** see REQUIREMENTS.md §27 — pasted
text is the primary, reliable input; a URL is optional metadata only, and
a WebFetch attempt on it is best-effort convenience, never ground truth.

## Arguments

- **post text** (primary) — the user pastes the post they want to comment
  on, directly in the conversation.
- **URL** (optional, best-effort only) — if the user gives a URL instead
  of or alongside pasted text, per §27: attempt a WebFetch, but never treat
  its result as reliable on its own.
- **author/relationship context** (optional) — who wrote it, and the
  user's relationship to them (peer, someone they want to network with,
  their own manager, etc.) — shapes tone/familiarity, never shapes facts.
- **desired angle** (optional) — agree / add-on / counterpoint / question.
  If omitted, pick whichever angle best fits what the post actually says.

## Process

### 1. Get the input, per §27's convention
- Pasted text given: use it directly as ground truth.
- Only a URL given: attempt WebFetch. If the result looks gated,
  truncated, or otherwise unreliable (a common outcome, not an edge case),
  say so explicitly and ask the user to paste/confirm the full text before
  drafting anything. Never draft off an unconfirmed partial fetch.
- Neither given: ask the user to paste the post.

### 2. Read the voice guide fresh
Read `Content-Learnings/voice-guide.md` in full, every run — never rely on
a cached memory of it. This is the same source of truth `/write-draft` and
every other drafting skill in this repo uses for tone and the avoid-list.

### 3. Draft 1-2 comment options
Each option:
- **Short** — 1-3 sentences, the LinkedIn-comment length norm. Not a
  mini-post.
- **Adds genuine value** — a specific reaction to something actually in
  the post, a related point that ties back to a detail the post actually
  contains, or a real question. Per Van der Blom's 2026 analysis
  (`Content-Learnings/algorithm-rules.md`), semantic quality and thread
  depth outweigh raw comment counts — a few substantive replies beat many
  generic ones, which is the reason to make this specific rather than a
  generic "Great post!" or "So true!".
- **Grounded only in what's actually in the post or what the user actually
  told this skill.** Never fabricate a stat, a credential, an anecdote, or
  agreement the user hasn't actually expressed.
- If the desired angle is `agree`, the comment must reflect a view the
  user plausibly holds given the post's content — not a manufactured
  enthusiasm.
- If the comment states a view rather than a fact, let it read as a view
  ("I'd push back on...", "what stood out to me...") rather than in the
  same declarative register as a stated fact — same opinion/fact
  discipline as REQUIREMENTS.md §21.

### 4. Apply the voice guide's avoid-list explicitly
Check each option against it before presenting: no throat-clearing opener
("Great post!", "Thanks for sharing"), no stacked/decorative emoji, no
generic CTA, no hedging every sentence. A comment that reads like every
other comment on the post has failed this step.

### 5. Output
Plain copy-paste text in the response — no file write, no Draft Note, this
never touches the Drafts/ pipeline.

## Report back

The comment option(s), plain text, ready to copy-paste. If a URL couldn't
be reliably fetched, say that plainly instead of drafting on a guess.

## Hard rules

- Never post the comment automatically, and never imply it was posted —
  there is no comment-posting API anywhere in this repo. Output is always
  for the user to paste in manually.
- Never fabricate agreement, a stat, a personal anecdote, or a credential
  the user didn't actually provide.
- Never treat a WebFetch result as ground truth for the post's content
  without the user explicitly confirming it matches what they see.
- Keep the opinion/fact distinction (REQUIREMENTS.md §21) whenever a
  comment states a view.
- No vault artifact for a single ad-hoc comment — no Draft Note, no new
  file, nothing added to the approval pipeline.
