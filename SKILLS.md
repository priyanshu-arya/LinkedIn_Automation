# System Capabilities (Living List)

What the system can actually do right now, updated at the end of each
approved phase. This is the "what exists" complement to REQUIREMENTS.md
("what we want") and DECISIONS.md ("why it's built this way").

Status legend: ✅ done · 🚧 in progress · ⬜ not started

---

## Phase 1 — Knowledge Manager (Obsidian schema)
✅ Done

- Obsidian vault structure created in-repo: `Content-Research/{AI, GenAI,
  Machine-Learning, Mathematics, Psychology-AI, Developer-Tools,
  Research-Papers, Interview-Preparation, Career, Resources}`, plus
  top-level `Post-Ideas/`, `Drafts/`, `Scheduled/`, `Published-Posts/`,
  `Analytics/`, `Content-Learnings/`, `_Templates/`.
- Frontmatter templates for all 6 note types in `_Templates/`: Research,
  Idea, Draft, Scheduled/Published, Analytics, Playbook.
- ID scheme: `YYYY-MM-DD--kebab-slug` filenames, mirrored in frontmatter
  `id`. Cross-links stored as plain-string ids (machine-parseable) and as
  `[[wikilinks]]` in a `## Related` section (Obsidian-native).
- One hand-written, clearly-labeled placeholder example per note type,
  verifying the schema and cross-links (research → idea → draft →
  scheduled → analytics) round-trip correctly.
- Real, empty Content Playbook (`Content-Learnings/playbook.md`) — no
  fabricated rules, ready for Phase 10 to populate from actual data.
- **Not yet possible:** nothing writes to this vault automatically. No
  research, ranking, drafting, visuals, approval routing, scheduling, or
  analytics collection exists yet — that's Phases 2–10.

## Phase 2 — Research pipeline (Trend Scout + Research Agent)
✅ Done

- New project skill: `.claude/skills/research-topic/SKILL.md`, invoked as
  `/research-topic <domain> [count]` (available from next session/message —
  Claude Code loads project skills at session start).
- Process per topic: WebSearch to find candidates → dedup check against
  existing vault notes in that category → WebFetch to verify against
  primary sources → score on a fixed 0-10 rubric (7 dimensions) → write a
  Research Note using the Phase 1 schema.
- Hard safety rules baked into the skill: no fabricated stats/quotes/
  benchmarks, no note without a real fetched source, no LinkedIn copy
  generated from this skill, no scheduling/Buffer access.
- Validated manually end-to-end this session (before the skill could be
  invoked by slash command): produced a real note,
  `Content-Research/Developer-Tools/2026-09-09--crewai-multi-agent-orchestration.md`.
  The run caught a real bad claim from a secondary source (stale star
  count) via primary-source verification, and dropped an unverifiable claim
  (release date) instead of guessing — the safety behavior worked in
  practice, not just on paper.
- **Not yet possible:** no automatic/scheduled research cadence (manual
  trigger only), no specialized research sources beyond general web
  search, no idea generation from research notes yet (Phase 3), no
  model cost-tiering (everything runs on the session's main model).

## Phase 3 — Idea Engine (Idea Ranker)
✅ Done

- New project skill: `.claude/skills/generate-ideas/SKILL.md`, invoked as
  `/generate-ideas [domain-filter] [count]` (available from next
  session/message).
- Process: gather unused (`status: new`, non-placeholder) research →
  dedup against existing ideas → generate idea(s) per REQUIREMENTS.md §6
  fields → score `rank_score` on a fixed 5-factor rubric → write Idea Note
  → flip source research note(s) `status: new → used` and populate
  `used_in`, closing the loop with Phase 2's dedup check.
- Explicitly out of scope here: assigning ideas to specific weekdays,
  enforcing the 5-post weekly cadence, drafting post text — that's Content
  Strategist / LinkedIn Writer, a later phase.
- Bug fix in passing: placeholder Research/Idea notes from Phase 1 were
  tagged with real statuses (`new`/`candidate`), which would have let fake
  schema-example content leak into real pipeline input. Both templates now
  support an explicit `placeholder` status, always excluded.
- Validated manually end-to-end: produced a real idea,
  `Post-Ideas/2026-09-09--crewai-crews-vs-flows.md` (rank_score 8.0),
  correctly derived from and linked back to the CrewAI research note.
- **Not yet possible:** the candidate pool is currently thin (1 real idea,
  1 category) — needs more `/research-topic` runs across domains before
  there's enough diversity for a real weekly plan. No day/date assignment,
  no draft generation, no visuals yet.

## Phase 4 — Content Strategist + LinkedIn Writer
✅ Done

- Two new project skills: `.claude/skills/plan-week/SKILL.md`
  (`/plan-week [week]`) and `.claude/skills/write-draft/SKILL.md`
  (`/write-draft [idea-id]`).
- `/plan-week`: assigns `status: candidate` ideas to specific Mon-Fri dates
  using the fixed REQUIREMENTS.md §7 content-mix heuristic, never forcing
  a mismatched idea into an empty slot — unfilled days are reported, not
  hidden.
- `/write-draft`: drafts LinkedIn post text for `status: selected` ideas,
  grounded strictly in the idea's linked research notes, following
  `Content-Learnings/voice-guide.md`. Writes to `Drafts/`, flips idea
  status to `drafted`.
- New living doc: `Content-Learnings/voice-guide.md` — a documented
  default voice/style guide (hooks, structure, length, tone, an explicit
  "avoid" list of AI-writing tells, hashtag/CTA rules). Marked
  `seeded_from: default`; expected to be replaced by real learned style
  once Phase 7 produces approval/edit history.
- Schema addition: Idea Notes now have a `target_date` field (specific
  weekday), alongside the existing `target_week`.
- Validated for real (both skills actually invoked, not simulated): the
  CrewAI idea was planned into Wed 2026-09-16 and drafted into a real
  1,451-character post,
  `Drafts/2026-09-16--crewai-crews-vs-flows.md`.
- **Not yet possible:** most of the week is still unfilled (only 1 real
  idea exists) — needs more `/research-topic` + `/generate-ideas` runs. No
  approval workflow, no visuals, no viral-potential scoring, no
  scheduling/Buffer, no personalized voice yet.

## Phase 5 — Quality/Critic Agent
✅ Done

- New skill: `.claude/skills/critique-draft/SKILL.md` (`/critique-draft
  [draft-id]`). Re-verifies accuracy against linked research, checks for
  duplicates/fatigue, scores Viral Potential (0-10, 8 factors), auto-
  revises once if score <6, moves draft to `status: in_review`.
- Sends a batched `PushNotification` when drafts become ready for review
  (Phase 11 wiring).
- Validated for real: the CrewAI draft scored 7.25/10, no revision
  triggered, moved to `in_review`.
- **Not yet possible:** "historical performance" factor is neutral until
  Phase 10's playbook has real evidenced rules (now wired to check it).

## Phase 6 — Visual Agent
✅ Done (brief-only, by design)

- New note type: `Visuals/` + `_Templates/Visual-Brief-Note.md`
  (`provider: none`, `image_path: ""` — provider-independent by design).
- New skill: `.claude/skills/generate-visual/SKILL.md` (`/generate-visual
  [draft-id]`). Produces a detailed written brief (composition, exact
  labels, style, dimensions), never a rendered image.
- Validated for real: a real brief for the CrewAI draft,
  `Visuals/2026-09-16--crewai-crews-vs-flows-diagram.md`.
- **Not yet possible:** no actual image is ever produced — no
  image-generation provider is configured (explicit choice, no API key
  available). Wiring a real provider later shouldn't require schema
  changes.

## Phase 7 — Approval Manager
✅ Done

- New skill: `.claude/skills/review-drafts/SKILL.md` (`/review-drafts
  [draft-id]`). The only skill allowed to set `status: approved`.
  Implements all seven REQUIREMENTS.md §12 actions (Approve, Edit,
  Regenerate, Change Hook, Change Image, Change Time, Reject); only
  Approve/Reject end a draft's review cycle.
- Schema additions: `preferred_time`, `scheduled_id` on Draft Notes.
- Validated for real, with a genuine human decision (not simulated): the
  CrewAI draft was presented and the user chose **Approve** — it's now
  `status: approved`, the first real approved post in the system.
- **Not yet possible:** nothing downstream consumes `approved` drafts yet
  until Phase 8.

## Phase 8 — Scheduler Agent + Buffer integration
✅ Done — verified against a real, live Buffer account (2026-09-09)

- New skill: `.claude/skills/schedule-approved/SKILL.md`
  (`/schedule-approved [draft-id]`). Built against Buffer's **current
  GraphQL API** (`https://api.buffer.com`), verified directly from
  developers.buffer.com rather than assumed — the old REST v1 API is not
  what's live now. Implements `createPost`, the org/channel discovery
  queries, maintains the rolling 2-day-ahead buffer (§10), and never
  fabricates a `buffer_post_id` on failure.
- Sends `PushNotification`s on queue-depth drop and publish failure
  (Phase 11 wiring).
- **Real, live validation run (2026-09-09)**: with the user's explicit
  go-ahead, scheduled the real approved CrewAI draft
  (`Drafts/2026-09-16--crewai-crews-vs-flows.md`) via a genuine
  `createPost` call. First attempt failed with a real
  `GRAPHQL_VALIDATION_FAILED` error — the docs-derived mutation declared
  `channelId: String!`, but Buffer's live schema requires the custom
  scalar `channelId: ChannelId!`. Fixed based on that exact error message
  (not guessed) and retried once, which succeeded:
  `buffer_post_id: 6aa1026da821ff5ff7114840`, `dueAt: 2026-09-16T03:30:00Z`.
  `schedule-approved/SKILL.md` corrected to match. Full record in
  `Scheduled/2026-09-16--crewai-crews-vs-flows.md`. This is now the first
  genuinely working phase in this system that touches a real external
  service, not just a docs-verified design.
- Also surfaced (and logged, not silently fixed away): the draft's
  Reviewer Notes had claimed 1,451 characters; the actual text transmitted
  to Buffer measured 1,502. Recorded the real measured value on the
  Scheduled Note.
- Credentials were previously the documented blocker; they no longer are
  (`.env` now has real `BUFFER_ACCESS_TOKEN`/`BUFFER_CHANNEL_ID` values) —
  see DECISIONS.md for that correction.

## Phase 9 — Analytics Agent
🚧 Built, still never exercised against a live account

- New skill: `.claude/skills/pull-analytics/SKILL.md` (`/pull-analytics`).
  Queries Buffer's post-metrics API (verified: experimental, daily
  refresh, ~24h lag — a missing metric is reported as unavailable, never
  defaulted to 0). Appends append-only snapshots to Analytics/ records,
  moves genuinely-published posts from `Scheduled/` to `Published-Posts/`,
  flags real outperformance only against an actual baseline.
- Sends `PushNotification`s on publish failure and verified outperformance.
- **Not yet possible:** no per-channel follower-growth query built (only
  per-post metrics); nothing to actually pull yet since no post has been
  scheduled against a live account (same "never exercised live" gap as
  Phase 8 — credentials exist now, a real test just hasn't happened).

## Phase 10 — Growth Agent (Content Playbook)
✅ Done (logic complete; no real data to learn from yet)

- New skill: `.claude/skills/update-playbook/SKILL.md`
  (`/update-playbook`). Requires 3+ published posts per comparison before
  writing any rule; tags confidence by sample size; flags Topic Fatigue.
- Closed the loop: `plan-week`, `write-draft`, and `critique-draft` were
  all edited to check `Content-Learnings/playbook.md` for an applicable
  evidenced rule before falling back to their fixed defaults — otherwise
  this phase would just produce a document nothing reads.
- Validated the "refuse to invent" behavior for real:
  `Published-Posts/` is genuinely empty (0 posts), so no playbook update
  was made — correct behavior per its own hard rule, not a skipped test.
- **Not yet possible:** the playbook is still empty; it can't actually
  improve anything until Phase 8/9 produce real published posts with
  analytics.

## Phase 11 — Notifications
✅ Done

- Implemented as instrumentation inside existing skills (not a standalone
  skill, since every trigger is a side effect of a condition another
  skill already detects), using the real `PushNotification` tool:
  - `schedule-approved` → queue <2 days ahead, publish failure
  - `pull-analytics` → publish failure, verified outperformance
  - `critique-draft` → batched "N drafts ready for review"
  - `research-topic` → a genuinely high-trend (≥9) or time-sensitive topic
- Explicitly does *not* notify on routine/expected outcomes — matches the
  tool's own guidance that unnecessary notifications are costly in a way
  that accumulates.
- **Not yet possible:** nothing runs on a schedule, so these only fire
  when a human happens to run the relevant skill. True proactive
  monitoring needs a scheduled/automated trigger (out of scope so far —
  every phase has been manually invoked).

## Phase 12 — Cost/safety hardening
✅ Done (as an audit; some findings are design recommendations, not code)

- New doc: `COST-AND-SAFETY.md` — a traceability matrix mapping every
  REQUIREMENTS.md §21 safety rule to the actual skill(s) enforcing it
  (checked against the real files, not asserted), plus an honest list of
  known gaps.
- Real finding from the audit, fixed: §21's "clearly distinguish opinions
  from facts" wasn't enforced anywhere — `write-draft` now requires
  explicit subjective framing for opinion-format content.
- Cost-tiering (§20): documented as a design (route cheap sub-tasks like
  dedup/tagging to a smaller model via the `Agent` tool's model override)
  but **not implemented** — decided the orchestration overhead isn't
  worth it while everything is manually/interactively triggered. Revisit
  if a scheduled automation phase gets built.

## Phase 13+ — Multi-format expansion
⬜ Not started (future scope, see REQUIREMENTS.md §22)

---

## Post-Phase-2 revision — Pillar list expanded to 15, closed set
✅ Done

- REQUIREMENTS.md §2 now defines a fixed, closed set of 15 content pillars
  (user-specified): AI, Tech Career, Developer Tools, GenAI, Machine
  Learning, Deep Learning, Interview Prep, Data Analytics, Data
  Engineering, Maths Related to Data, Problem Solving, Algorithms,
  Research, Psychology + AI, AI in Healthcare — plus cross-cutting
  Resources (learning resources). Cheat sheets and do's/don'ts are content
  *formats* within a pillar, not pillars themselves.
- `Content-Research/` gained 5 new folders to match: `Deep-Learning`,
  `Data-Analytics`, `Data-Engineering`, `Problem-Solving`, `Algorithms`,
  `AI-Healthcare` (6 total, since Deep Learning/Algorithms/Problem Solving/
  Data Analytics/Data Engineering/AI in Healthcare had no prior folder).
- `research-topic/SKILL.md` updated: the pillar list is fixed (don't invent
  a 16th), but the *specific topic* within a pillar is still never
  hardcoded — every run still does a real-time search per pillar rather
  than reusing a topic list. `domain` argument narrows to one pillar;
  omitted (default) scans all 15 and lets trend strength pick which
  pillar(s) get covered this run.
- `_Templates/Research-Note.md` and `README.md`'s vault tree updated to
  list all 15 (+1) folders.
