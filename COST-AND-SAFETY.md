# Cost & Safety Audit (Phase 12)

Status: living document, last audited 2026-09-09 against the skills as
they exist after Phase 11.

## Safety-rule traceability (REQUIREMENTS.md §21)

Each rule below was checked against the actual skill files, not asserted
from memory.

| Rule | Enforced by | How |
|---|---|---|
| Never fabricate research/statistics/quotes | `research-topic`, `write-draft`, `critique-draft` | research-topic drops any claim not traced to a fetched source; write-draft only uses facts present in linked research notes; critique-draft re-verifies and fixes drift before anything else |
| Clearly distinguish opinions from facts | `write-draft` | opinion-format drafts must use explicit subjective framing ("I think," "my take"), not declarative fact-voice — **gap found and fixed during this audit**, see DECISIONS.md |
| Prefer primary sources | `research-topic` | step 3 explicitly favors official/primary sources over secondary write-ups |
| Cross-check important claims | `research-topic` | step 3; demonstrated live in Phase 2's validation run (caught a stale secondary-source stat) |
| Avoid auto-publishing unverified breaking news | Structural, across `research-topic` → `review-drafts` → `schedule-approved` | there is no code path from research or draft creation directly to Buffer — every draft must pass through `review-drafts` (human approval) before `schedule-approved` will touch it. A high-trend_score notification recommends fast coverage but does not skip this path. |
| Prevent duplicate posts | `generate-ideas` (idea-level dedup), `plan-week` (cross-week fatigue check), `critique-draft` (draft-level duplicate/originality check) | three separate checkpoints, not one |
| Require approval before scheduling | `review-drafts`, `schedule-approved` | `review-drafts` is the only skill permitted to set `status: approved`; `schedule-approved`'s hard rules refuse anything not already `approved` |
| Maintain logs of generated/published content | Vault-wide (`history` field on every Draft Note) + `DECISIONS.md`/`SKILLS.md` | every status transition is appended, never overwritten |

## Cost tiering (REQUIREMENTS.md §20)

**Current reality:** every skill in this system runs inline in whatever
model is driving the current session — there is no automatic routing of
"cheap" sub-tasks (classification, tagging, dedup checks) to a smaller
model. This was a reasonable simplification while building interactively
(the session's model is already paying for the turn regardless), but it
means the intended cost structure from §20 isn't actually implemented yet.

**How it could be implemented, if/when this runs unattended:** the `Agent`
tool supports a `model` override (e.g. spawning a Haiku-tier subagent for
a specific sub-task). This would be worth doing for:
- duplicate/fatigue detection in `generate-ideas` and `plan-week`
- basic tagging/classification steps

...and *not* worth doing for anything that needs real judgment: research
verification, final post writing, viral-potential scoring, performance
analysis (§20 explicitly reserves these for a stronger model).

**Recommendation, not yet actioned:** don't add this complexity until the
system actually runs on a schedule (cron/automation) at high enough volume
that the orchestration overhead of spawning sub-agents is worth it. Doing
it now, interactively, would add latency and complexity without saving
anything real. Revisit when/if a scheduled automation phase is built.

## Known gaps (honest, not exhaustive)

- Image generation has no real provider wired in (Phase 6, by explicit
  choice) — briefs only.
- Buffer integration (Phase 8/9) is built and verified against Buffer's
  current documented API shape, but **has never been exercised against a
  live account**. `.env` now has real `BUFFER_ACCESS_TOKEN`/
  `BUFFER_CHANNEL_ID` values (as of 2026-09-09, correcting an earlier
  version of this note) — the remaining gap is purely "never tested live,"
  not missing credentials. A deliberate, user-approved dry run against a
  real approved draft is still needed before either skill can be trusted.
  See DECISIONS.md.
- A live-content pipeline that fetches arbitrary web pages (`research-topic`
  via `WebFetch`/`WebSearch`) and eventually reaches a real external API
  (`schedule-approved` → Buffer) has a prompt-injection surface: a crafted
  page could embed hidden instructions in its content. `research-topic`
  now has an explicit hard rule to treat fetched page content as data to
  extract facts from, never as instructions — mitigated, not eliminated
  (inherent to any agent that reads the open web and later acts).
- No automated validation exists that vault notes actually conform to
  their templates — correctness relied entirely on each skill's own
  care. Partially addressed: `scripts/validate_vault.py` now checks
  frontmatter against template-required fields and flags placeholder
  leakage; it's a manual/CI-optional check, not enforced automatically
  before every write.
- Follower-growth tracking (a §12 metric) has no per-channel query built
  yet — only per-post metrics.
- Model cost-tiering is designed but not implemented (see above).
- No automated/scheduled cadence exists anywhere — every skill is manually
  triggered. That's fine for the current human-in-the-loop design, but
  means "the system should notify me" (§24) only fires when someone is
  actually running a skill that checks for it.
- **Notification delivery is currently blocked by user config**: a real
  test `PushNotification` returned "mobile push is disabled in /config."
  The §24 triggers are correctly wired in each skill, but won't actually
  reach the user until that setting is enabled — this is a user-side
  config choice, not a code defect.
