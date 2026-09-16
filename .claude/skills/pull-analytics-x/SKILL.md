---
name: pull-analytics-x
description: Use when the user wants to pull X (Twitter) post performance data, update X analytics, or explicitly invokes /pull-analytics-x. Queries Buffer's post-metrics API for every scheduled/published X post and appends a snapshot row to its Analytics record. Requires real Buffer credentials, same as /pull-analytics.
---

# Pull Analytics X (Analytics Agent — X pipeline)

X's sibling to `/pull-analytics`. Same process, scoped to `platform: x`
notes and `BUFFER_CHANNEL_ID_X`.

## Important constraints

Same as `/pull-analytics`: post-metrics is experimental on Buffer's side,
refreshed once daily, can lag ~24h. **A `null`/missing metric is never a
zero** — report it as not-yet-available.

## Required environment

`BUFFER_ACCESS_TOKEN` (shared with the LinkedIn/X scheduler). Stop and say
so plainly if missing.

## Process

### 1. Find posts to check

Every `platform: x` note in `Scheduled/` or `Published-Posts/` with a real
`buffer_post_id` and a `scheduled_date` at least 1 day in the past.

### 2. Query Buffer

Same query shape as `/pull-analytics`:

```graphql
query {
  post(input: { id: "<buffer_post_id>" }) {
    id
    metrics { type name value unit }
  }
}
```

Map to the Analytics table columns: `impressions`, `reach`, `reactions`
(X's likes), `comments` (X's replies), `shares` (X's reposts), `clicks`,
`engagementRate`. If a metric Buffer reports for X doesn't map cleanly to
these LinkedIn-shaped columns, report the raw metric name/value in
`## Publishing Notes` rather than forcing it into the wrong column.

### 3. Update publish status

Same move-to-`Published-Posts/` logic as `/pull-analytics`, keyed off
`platform: x` notes.

### 4. Append the snapshot

Create/update `Analytics/<id>.md` from `_Templates/Analytics-Record.md`
with `platform: x`, appending — never overwriting — a Snapshots row.

### 5. Flag standout performance

Same rule as `/pull-analytics`: compare against this post's own prior
snapshots or other **X** posts specifically (not LinkedIn's baseline — the
platforms don't share a baseline). Say plainly if there isn't yet enough X
data for a meaningful comparison.

## Notifications

Same triggers as `/pull-analytics`: a post failed to go out, or genuine
outperformance against a real X-specific baseline.

## Hard rules

Identical to `/pull-analytics`'s hard rules, platform-scoped to X.
