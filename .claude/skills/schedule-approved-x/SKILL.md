---
name: schedule-approved-x
description: Use when the user wants to send approved X (Twitter) drafts to Buffer, check the X scheduling queue, or explicitly invokes /schedule-approved-x. Calls Buffer's real GraphQL API to schedule status:approved, platform:x Draft Notes, and writes Scheduled Notes (platform:x). Requires real Buffer X-channel credentials — never attempts a call without them, and never invents a result if a call fails.
---

# Schedule Approved X (Scheduler Agent — X pipeline)

X's sibling to `/schedule-approved`. Same proven Buffer GraphQL pattern for
single posts. Thread posting uses the same `createPost` mutation with an
added `metadata.twitter.thread` field — confirmed live 2026-09-14 (see step
4), the same verify-don't-guess discipline that caught the `channelId`
type correction on the original LinkedIn build.

## Required environment

- `BUFFER_ACCESS_TOKEN` — same token as `/schedule-approved` (one Buffer
  account, multiple channels).
- `BUFFER_CHANNEL_ID_X` — the Buffer channel id for the connected X
  profile. If unknown, run the same one-time discovery query
  `/schedule-approved` documents (`channels(input: { organizationId })`),
  find the entry where `service` indicates X/Twitter, confirm with the
  user, save as `BUFFER_CHANNEL_ID_X`.

**If either is missing or a placeholder, stop immediately and say exactly
which one and how to get it. Never attempt a call with a blank token.**

## Process

### 1. Check the rolling buffer

Same §10-style check as `/schedule-approved`, scoped to `platform: x`
content: count approved-or-scheduled X posts dated within the next 2 days.
If below that, say so before doing anything else.

### 2. Select drafts to schedule

Every `platform: x`, `status: approved` Draft Note with an empty
`scheduled_id`. Timing: `preferred_time` if set via `/review-drafts`'
Change Time action, otherwise the day's default from whatever X-specific
posting-time heuristic `/plan-week-x` sourced (recorded in that skill's own
notes/`playbook-x.md`) — say plainly if it's still the unvalidated starting
heuristic.

### 3. Call Buffer — single posts

Reuse the exact proven mutation from `/schedule-approved`, with
`channelId: <BUFFER_CHANNEL_ID_X>` instead of the LinkedIn channel:

```graphql
mutation CreatePost($text: String!, $channelId: ChannelId!, $dueAt: DateTime!) {
  createPost(input: {
    text: $text
    channelId: $channelId
    schedulingType: automatic
    mode: customScheduled
    dueAt: $dueAt
  }) {
    ... on PostActionSuccess { post { id text dueAt } }
    ... on MutationError { message }
  }
}
```

### 4. Call Buffer — threads

**Confirmed live 2026-09-14** (via `developers.buffer.com/examples/
create-threaded-post.html`, then verified with a real scheduled call, post
id `6aa7685295d6303fe830531d`, `status: scheduled`): threads use the same
`createPost` mutation as a single post, with the sequence carried in a
service-specific `metadata` field — `metadata: { twitter: { thread: [...] }
}`, an array of `{ text: "..." }` objects, one per tweet **including the
first one** (Buffer's docs are explicit that the top-level `text` argument
should duplicate the first thread entry). Full confirmed shape:

```graphql
mutation CreateThreadedPost($text: String!, $channelId: ChannelId!, $dueAt: DateTime!) {
  createPost(input: {
    text: $text
    channelId: $channelId
    schedulingType: automatic
    mode: customScheduled
    dueAt: $dueAt
    metadata: { twitter: { thread: [
      { text: "First tweet, same as $text above" }
      { text: "Second tweet" }
      { text: "Third tweet, and so on" }
    ] } }
  }) {
    ... on PostActionSuccess { post { id status dueAt } }
    ... on MutationError { message }
  }
}
```

The `thread` array's item type wasn't named in Buffer's docs, so inline the
tweet objects directly in the mutation body (as above) rather than
declaring a typed GraphQL variable for it — declaring `$thread` against a
guessed input type name risks a validation error the same way an
unconfirmed scalar type would. `$text`/`$channelId`/`$dueAt` stay real
variables since their types are already confirmed from the single-post
mutation.

If the response is a `MutationError` or an HTTP/GraphQL error, stop for
that draft, report the exact message, don't write a Scheduled Note. Never
fabricate a `buffer_post_id`.

### 5. On success

Write a Scheduled Note in `Scheduled/` from
`_Templates/Scheduled-Published-Note.md`: `platform: x`, `draft_id`,
`final_text` (first tweet, or the whole thread text joined with a clear
separator for readability), `buffer_post_id`, `scheduled_date`/
`scheduled_time`, `publish_status: scheduled`, plus category/format/
length/hook_style/hashtags/visual_ids/sources from the draft. Set the
Draft Note's `scheduled_id`.

### 6. Re-check the rolling buffer

Same as `/schedule-approved` step 5.

## Notifications

Same triggers as `/schedule-approved`: rolling buffer below 2 days, or a
Buffer call failure. Don't notify on routine success.

## Hard rules

- Never call Buffer without both env vars actually populated.
- Never invent a `buffer_post_id` or a thread mutation shape — confirm
  live, same as the original scheduler's `channelId` fix.
- Never schedule a draft that isn't `platform: x`, `status: approved`.
- Never retry a failed call silently more than once.
