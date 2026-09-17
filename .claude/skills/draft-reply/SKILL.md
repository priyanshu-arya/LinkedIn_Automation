---
name: draft-reply
description: Use when the user wants to draft a reply to a LinkedIn comment, wants replies drafted for an entire post's comment thread at once, or explicitly invokes /draft-reply. Given a single pasted comment, drafts one reply. Given a pasted full thread export, sweeps every top-level comment and reply, filters out low-value ones, and drafts the rest in one batch — correctly attributing who each reply is addressed to across LinkedIn's 2-level thread flattening. Input follows REQUIREMENTS.md §27 (pasted text primary; a post URL alone is not reliable). Never posts anything itself — output is copy-ready text for manual posting, and no vault artifact is created.
---

# Reply Handler

Drafts replies to comments on the user's own (or anyone else's) LinkedIn
post — either one comment at a time, or a full-thread sweep. Same
lightweight, mostly ephemeral shape as Comment Drafter (`/draft-comment`):
not part of the Drafts/ approval pipeline. Output is copy-paste text in
the response; there is no Draft Note, no vault schema, no file write.

**Reading third-party post/comment content:** see REQUIREMENTS.md §27 —
pasted text is the primary, reliable input; a post URL is optional
metadata only, and a WebFetch attempt on it is best-effort convenience,
never ground truth.

## Modes

- **Single-reply** — the user pastes one comment (optionally plus the
  original post's text/topic for context) and wants one reply drafted.
- **Sweep** — the user pastes a full thread export (all top-level comments
  and their replies, as copied from the post) and wants a reply drafted
  for every comment/reply worth answering, in one batch. A post URL may
  come along as best-effort/reference-only metadata per §27 — never relied
  on to reconstruct thread content that wasn't actually pasted.

If it's ambiguous which mode applies (e.g. a short paste with no visible
reply structure), ask, or default to single-reply for one comment / sweep
for anything with multiple comments.

## Flattening-handling design (sweep mode)

LinkedIn's UI only nests one level deep: a reply to a reply gets flattened
into the same top-level-reply list, with LinkedIn auto-inserting an
"@Name" prefix on the reply's text to show who it was actually meant for
— it is not real nesting, and the export the user pastes will preserve
that flattened, one-level shape.

On parse, build a flat list **per top-level comment**:

```
{author, text, replied_to}
```

- `replied_to` is inferred from an explicit "@Name" at the *start* of a
  reply's text (LinkedIn's own flattening marker).
- If no such @mention is present, `replied_to` defaults to the top-level
  comment's author (the reply is assumed to address the thread starter,
  not some other repliers further down).
- Never guess a `replied_to` target beyond these two rules — if the text
  is ambiguous even with the @mention convention, say so rather than
  picking a guess silently.

When drafting, label every reply output as:

> **Reply to [Author] (responding to [X] in this thread)**

and have the drafted reply text itself open by naming or otherwise
clearly addressing that specific person's point — never a generic reply
that could float under any comment in the thread. If two different people
replied to two different targets within the same top-level thread, keep
their drafted outputs visually grouped under that thread for one
scan-through, but each still carries its own explicit target label so
nothing gets misattributed when the user copies them back individually.

## Low-value filter (sweep mode only)

Single-reply mode always drafts what's asked — the filter only runs in
sweep mode, to avoid wasting a drafted reply on a comment not worth
answering. Skip, and log as skipped with a reason, anything that is:

- **Pure emoji/reaction-only** — "🔥🔥", "👏", no words.
- **Generic praise with zero specific reference to post content** —
  "Great post!", "So true", "Well said" and nothing else.
- **Off-topic self-promotion/spam** — an unrelated link drop, "check out
  my profile/product".
- **A near-duplicate of a comment already answered earlier in the same
  thread** — same point, no new angle.
- **A tag/mention with no added content** — "@friend check this out" and
  nothing else.

Keep everything else — including a short-but-substantive disagreement, a
real question, a correction, or a personal anecdote tied to the post,
even if brief. When in doubt, keep it rather than skip it.

**Always report which comments were skipped and why.** Never silently
drop a comment from the output — the skipped-comment log is a required
part of every sweep report.

## Process

### Single-reply mode
1. Take the pasted comment, plus the original post's text/topic if given,
   per §27 (pasted text primary; a URL alone is not reliable).
2. Read `Content-Learnings/voice-guide.md` in full, fresh — never rely on
   a cached memory of it.
3. Draft one reply: short, specific to what the comment actually said,
   in the user's own voice, no throat-clearing, no generic filler.
4. Output as copy-ready text.

### Sweep mode
1. Ingest the pasted full thread export.
2. Parse into top-level comments plus attributed replies per the
   flattening design above — build the `{author, text, replied_to}` list
   for each top-level thread.
3. Apply the low-value filter to every comment and reply, logging what's
   skipped and why.
4. Read `Content-Learnings/voice-guide.md` in full, fresh.
5. Draft a reply for each surviving comment/reply, each carrying its
   explicit "Reply to [Author] (responding to [X])" addressee label.
6. Present the full batch grouped by original top-level thread, so the
   user can scan one thread at a time.
7. Report counts: total parsed / filtered out / drafted.

## Report back

- The drafted repl(ies) as copy-ready text.
- In sweep mode: each reply labeled with who it's addressed to, grouped
  by top-level thread; the skipped-comment log with reasons; and the
  parsed/filtered/drafted counts.

## Hard rules

- Never auto-post a reply, and never imply one was posted — there is no
  comment-posting API anywhere in this repo, same limitation as
  `/draft-comment` (REQUIREMENTS.md §27, §33). Output is always
  copy-paste text for manual posting.
- Never fabricate a comment's content, author, or thread structure beyond
  what was actually pasted. If the pasted thread is ambiguous or
  incomplete, say so rather than inventing the missing shape.
- Never invent context about the original post beyond what the user
  actually gave.
- Every drafted reply follows `Content-Learnings/voice-guide.md`'s tone —
  conversational, direct, no AI-writing tells.
- Never silently drop a low-value comment from the sweep report — always
  state that it was skipped and why.
- No vault artifact: no Draft Note, no `Drafts/` entry, no approval-
  pipeline lifecycle, for either mode.
