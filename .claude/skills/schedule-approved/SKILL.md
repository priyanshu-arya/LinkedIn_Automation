---
name: schedule-approved
description: Use when the user wants to send approved LinkedIn drafts to Buffer, check the scheduling queue, or explicitly invokes /schedule-approved. Calls Buffer's real GraphQL API to schedule status:approved drafts, maintains the rolling 2-day-ahead buffer (REQUIREMENTS.md §10), and writes Scheduled Notes. Requires real Buffer credentials in the environment — never attempts a call without them, and never invents a result if a call fails.
---

# Schedule Approved (Scheduler Agent — Phase 8)

Sends `status: approved` drafts to Buffer for real scheduling, using
Buffer's current GraphQL API (verified against developers.buffer.com — the
old REST v1 API is deprecated; this is a GraphQL API at a single endpoint).
Only acts on drafts a human has already approved via `/review-drafts` —
this skill never approves anything itself.

## Required environment

Read these from the environment (a `.env` file is fine, must stay
git-ignored):

- `BUFFER_ACCESS_TOKEN` — personal API token from
  `https://publish.buffer.com/settings/api`
- `BUFFER_CHANNEL_ID` — the Buffer "channel" id for the target LinkedIn
  profile (Buffer's API calls a connected social profile a "channel," not
  a "profile" — terminology changed from the old API)

**If either is missing or empty, stop immediately and say exactly which
one is missing and how to get it. Never attempt a call with a blank or
placeholder token.**

### One-time channel discovery (only if `BUFFER_CHANNEL_ID` is unknown)

1. `query GetOrganizations { account { organizations { id } } }` — get the
   organization id.
2. `query GetChannels { channels(input: { organizationId: "<id>" }) { id name displayName service } }`
   — find the entry where `service` is the LinkedIn profile, report its
   `id` and `displayName`, and ask the user to confirm before saving it as
   `BUFFER_CHANNEL_ID`.

All requests: `POST https://api.buffer.com`, header
`Authorization: Bearer <BUFFER_ACCESS_TOKEN>`, JSON body
`{"query": "...", "variables": {...}}`.

## Process

### 1. Check the rolling buffer (REQUIREMENTS.md §10)
Count approved-or-scheduled content dated within the next 2 days from
today. If it's already below 2 days' worth, say so plainly before doing
anything else — this is the signal that more drafts need to move through
`/plan-week` → `/write-draft` → `/critique-draft` → `/review-drafts`.

### 2. Select drafts to schedule
Every `status: approved` draft with an empty `scheduled_id`. Determine
timing:
- If the draft has a `preferred_time` set (via Change Time in
  `/review-drafts`), use it.
- Otherwise use a **generic starting default of 09:00** in the user's
  local time, on the idea's `target_date`. This is an unvalidated
  starting heuristic (REQUIREMENTS.md §11), not derived from real
  performance data — say so, don't present it as optimized. Phase 10 is
  expected to replace this once real analytics exist.

### 3. Call Buffer
```graphql
mutation {
  createPost(input: {
    text: "<post text + hashtags>"
    channelId: "<BUFFER_CHANNEL_ID>"
    schedulingType: automatic
    mode: customScheduled
    dueAt: "<ISO 8601 UTC timestamp>"
  }) {
    ... on PostActionSuccess { post { id text dueAt } }
    ... on MutationError { message }
  }
}
```
If the response is a `MutationError` or an HTTP/GraphQL error, **stop for
that draft, report the exact error message, and do not write a Scheduled
Note for it.** Never fabricate a `buffer_post_id`. This is also a
notification trigger (Phase 11: "a post fails to publish").

Note: field names/shape were verified against Buffer's current docs but
not yet exercised against a live account — if the real API rejects this
shape, report the exact error back rather than guessing a fix silently.

### 4. On success
- Write a Scheduled Note in `Scheduled/` from
  `_Templates/Scheduled-Published-Note.md`: `draft_id`, `final_text`,
  `buffer_post_id` (the returned `post.id`), `scheduled_date`/
  `scheduled_time`, `publish_status: scheduled`, plus category/format/
  length/hook_style/hashtags/visual_ids/sources copied from the draft.
- Set the Draft Note's `scheduled_id` to the new Scheduled Note's id. The
  draft itself stays `status: approved` — it's the historical record;
  the Scheduled Note is now the live one.

### 5. Re-check the rolling buffer
After scheduling, recount. If still below 2 days ahead, flag it again —
this is a real, current gap, not a hypothetical one.

## Notifications (REQUIREMENTS.md §24)

Send a `PushNotification` (status: proactive) when:
- the rolling buffer is below 2 days ahead, after step 5 — e.g. "LinkedIn
  queue: only 1 day of approved posts left, need more drafts."
- a Buffer call fails (step 3) — e.g. "LinkedIn post failed to schedule:
  <short error>."
Do not notify on ordinary success — a routine schedule confirmation isn't
worth an interruption.

## Hard rules

- Never call Buffer without both required env vars actually populated —
  check their presence and non-placeholder-ness before every run.
- Never invent a `buffer_post_id` or claim success on a failed call.
- Never schedule a draft that isn't `status: approved`.
- Never schedule onto Sat/Sun unless explicitly requested.
- Never retry a failed call silently more than once — report it.
