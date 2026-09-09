---
name: pull-analytics
description: Use when the user wants to pull LinkedIn post performance data, update analytics, or explicitly invokes /pull-analytics. Queries Buffer's post-metrics API for every scheduled/published post and appends a snapshot row to its Analytics record. Requires real Buffer credentials, same as /schedule-approved.
---

# Pull Analytics (Analytics Agent — Phase 9)

Pulls performance metrics from Buffer for posts that have gone through
`/schedule-approved`, and appends a snapshot to each post's Analytics
record — never overwrites history (REQUIREMENTS.md §12/§13 need the full
history to detect trends, not just the latest number).

## Important constraints (verified against Buffer's docs, not assumed)

- Post-metrics is an **experimental** part of Buffer's API — the shape can
  change. Don't hard-fail the whole run if one field is missing; report
  what came back.
- Metrics are refreshed **once daily** and can lag the real network by up
  to ~24 hours, and stay `null` until that ingestion job has run. **Do not
  treat a `null`/missing metric as zero** — report it as "not yet
  available," not as a zero-engagement post. This matters: a false zero
  would corrupt Phase 10's learning.
- Reading metrics requires a **personal API key** (same `BUFFER_ACCESS_TOKEN`
  as the Scheduler).

## Required environment

Same as `/schedule-approved`: `BUFFER_ACCESS_TOKEN`. Stop and say so
plainly if it's missing.

## Process

### 1. Find posts to check
Every note in `Scheduled/` or `Published-Posts/` with a real
`buffer_post_id` and a `scheduled_date` at least 1 day in the past (no
point querying same-day — nothing will have ingested yet).

### 2. Query Buffer
```graphql
query {
  post(input: { id: "<buffer_post_id>" }) {
    id
    metrics { type name value unit }
  }
}
```
Map returned `type`s to the Analytics table columns: `impressions`,
`reach`, `reactions`, `comments`, `shares`, `clicks`, `engagementRate`.
Follower growth isn't a per-post metric — track it separately if/when a
channel-level query is needed (not built in this phase; flag as a gap if
the user wants it).

### 3. Update publish status
If Buffer's response shows the post actually went out, and the local note
is still `Scheduled/` with `publish_status: scheduled`, move the file to
`Published-Posts/` and set `publish_status: published`. If Buffer reports
a failure/deletion, set `publish_status: failed` and leave it in
`Scheduled/` — this is a Phase 11 notification trigger ("a post fails to
publish").

### 4. Append the snapshot
In the post's `Analytics/<id>.md` note (create it from
`_Templates/Analytics-Record.md` if it doesn't exist yet, with
`status: active` — never `placeholder`, that value is reserved for the
hand-written schema example), append one row to the Snapshots table with
today's date and the metric values — **append, never overwrite** existing
rows.

### 5. Flag standout performance
If a post's latest engagement_rate is meaningfully above the average of
its own prior snapshots or of other published posts (once there are
enough to compare — don't invent a baseline from a single data point),
this is a Phase 11 notification trigger ("a post significantly
outperforms normal performance"). With fewer than ~3-5 published posts,
say plainly that there isn't yet enough data for a meaningful baseline.

## Notifications (REQUIREMENTS.md §24)

Send a `PushNotification` (status: proactive) when:
- step 3 detects a post failed to actually go out.
- step 5 confirms genuine outperformance against a real baseline — e.g.
  "LinkedIn post from <date> is at 2.1x your average engagement rate."
Do not notify for routine, in-line-with-baseline results.

## Hard rules

- Never write a fabricated metric value. A missing/null metric is
  reported as unavailable, never defaulted to 0.
- Never overwrite a prior snapshot row — history must accumulate.
- Never claim "outperformance" without an actual baseline to compare
  against.
