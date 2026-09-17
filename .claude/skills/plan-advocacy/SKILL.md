---
name: plan-advocacy
description: Use when the user wants to plan or launch a team LinkedIn employee-advocacy program, define a 14-day launch plan/posting cadence/brand governance for a team, or explicitly invokes /plan-advocacy. Produces a program plan (launch schedule, per-person cadence suggestions, brand dos/don'ts, approval chain) plus a self-reported metrics template for team members to fill in -- this repo's Buffer access is scoped to the user's own channel only (REQUIREMENTS.md §12), so it cannot pull or automate analytics for any other team member's account. This is a separate module from the content-posting pipeline (research/draft/schedule skills) -- a one-off/periodic program plan and quarterly review cadence, not a recurring daily posting pipeline.
---

# Plan Advocacy (Employee Advocacy Agent)

This is the most standalone skill in this repo: it plans a program for a
**team of other people**, most of whom aren't using this tool themselves.
Same framing precedent as `optimize-profile` — this is a separate module
from the content-posting pipeline (research/draft/schedule skills), a
one-off/periodic program plan with a quarterly review cadence, not a
recurring daily posting pipeline.

Full requirement: `REQUIREMENTS.md` §36. Read it if anything below is
ambiguous.

## Hard input contract

Same discipline as `optimize-profile`'s "exactly two JDs": **stop and ask
rather than guessing** if these are missing.

**Required:**
- **Company/team name.**
- **Roster** — name + role + LinkedIn profile URL per person. Used only
  to populate the plan document. Never fetched or scraped — per
  REQUIREMENTS.md §27's discipline against unofficial access to a
  third-party profile, which applies to a team member's profile exactly
  as it applies to any other person's.
- **Program goal** — exactly one of: `brand-awareness` / `hiring` /
  `thought-leadership` / `sales-pipeline`. Don't accept a blended goal —
  ask which one is primary if the user names more than one.

**Optional:**
- **Existing brand voice/guidelines doc** (path or pasted text). If
  absent, draft a minimal one from scratch and flag every item
  `[DRAFTED — CONFIRM WITH LEGAL/COMMS]`.
- **Target content pillars.** Default: offer REQUIREMENTS.md §2's 15
  content pillars as a starting menu the team can narrow, rather than
  inventing a new pillar set for this program.
- **Launch date.** If absent, ask, or default to "TBD — confirm before
  distributing."

Do not proceed past intake with a missing company name or roster —
everything downstream (the launch plan, the metrics log) depends on
having real people and a real program identity to plan around.

## Deliverable format and storage

New top-level `Employee-Advocacy/` folder (same precedent as
`Profile-Optimization/` — a periodic, re-runnable artifact accumulating
history across runs, not part of the recurring content pipeline).

Two files per program run:

1. `Employee-Advocacy/YYYY-MM-DD--<company-slug>-program.md` — the
   program plan itself, from `_Templates/Employee-Advocacy-Note.md`.
2. `Employee-Advocacy/YYYY-MM-DD--<company-slug>-metrics-log.md` — one
   **shared** log for the whole team (never per-person files), from
   `_Templates/Advocacy-Metrics-Log.md`, that team members fill in
   periodically. Its `program_id` field cross-references the program
   note's `id`.

On a re-run for a company/team that already has a program note, treat it
as an update to the existing pair (new `history` entry on the program
note; the metrics log keeps accumulating rather than being replaced) —
don't create a duplicate set of files for the same program unless the
user explicitly wants a fresh relaunch.

## Process

### 1. Intake
Per the hard input contract above. Stop and ask if company name or
roster is missing. Confirm the single program goal. Ask once whether a
brand-voice/guidelines doc exists; if not, say plainly that dos/don'ts
will be drafted from scratch and flagged for legal/comms sign-off.

### 2. Draft or import brand dos-and-don'ts
Every item sourced from the intake doc if one was supplied; every item
without a real source is labeled `[DRAFTED — CONFIRM WITH LEGAL/COMMS]`.
Cover, at minimum:
- **Confidentiality** — no unannounced product/financial information.
- **Tone alignment** — with the company's public voice.
- **Disclosure** — mention affiliation when discussing the employer.
- **No engaging with trolls/negative press** — personally, on the
  company's behalf.
- **No political/controversial takes** under the company's halo.

### 3. Build the 14-day launch plan
Day-by-day onboarding + first-post prompts per person. Content-angle
suggestions are drawn from the pillar menu (step 1's confirmed list, or
the §2 default) — never fabricate specifics about what any real named
person will actually post; these are prompts/angles for them to use, not
claims about content that exists.

### 4. Define ongoing cadence
State a recommendation (e.g. 1-2 posts/week/person) framed **explicitly
as a suggestion** — this tool has no mechanism to enforce or schedule
anything for anyone but the primary user's own channel.

### 5. Define the approval chain and escalation path
This tool cannot access or approve other people's drafts, so the
realistic default is a **spot-check pattern**: advocates share drafts in
a shared channel/doc during the first 14 days, tapering to self-serve
after. Escalation: a named point-of-contact (comms/manager) plus a
2-step process for anything off-brand that goes live — (1) private flag,
(2) takedown request. State plainly that this skill cannot itself detect
or monitor that happening — there is no access anywhere in this repo to
any team member's feed. Escalation is human-triggered only, always.

### 6. Aggregate the metrics log (re-run only)
On a run against an existing program, read whatever rows already exist
in the metrics log and compute a simple rollup:
- **Most-active contributor** — most self-reported entries.
- **Most-engaged post** — highest self-reported numbers.
- **Participation rate** — (# of roster members with at least one entry)
  / roster size.

Never invent a number for someone who didn't submit one, and never call
participation rate an "engagement" or "performance" metric in the
report — it's a completion-rate statistic about who submitted a report,
nothing about how any individual post actually performed. On a first run
(no existing metrics log), skip this step — the Rollup section ships
saying "no entries yet."

### 7. Write both files and report back
File paths for both notes, plus **3-5 open decisions** that genuinely
need the user's or comms team's sign-off (e.g. an unconfirmed
`[DRAFTED — CONFIRM WITH LEGAL/COMMS]` item, the launch date, the named
escalation point-of-contact). Don't restate the full plan in chat — point
at the files.

## Hard rules

- **Never claims automated tracking of any team member's individual
  account performance.** State the Buffer-scoping limitation
  (REQUIREMENTS.md §12) plainly, every time this comes up — it is a
  **permanent architectural constraint**, not a gap to be fixed later.
- **Never fabricates a self-reported metric on someone's behalf.** Every
  row in the metrics log comes from what a team member actually
  submitted.
- **Never treats a missing self-report as zero** — same null-handling
  discipline as `pull-analytics`. Absent means absent, not
  zero-performance.
- **Brand-guidance items not sourced from a real company doc are always
  labeled `[DRAFTED — CONFIRM]`** (in practice, the fuller
  `[DRAFTED — CONFIRM WITH LEGAL/COMMS]`) — never presented as settled
  policy.
- **Never stores team members' personal contact info** beyond name,
  role, and profile URL already given by the user.
- **Never posts, schedules, or accesses any team member's LinkedIn
  account.** Output is a planning document only — same "produces the
  deliverable, human executes it" precedent as image generation
  (REQUIREMENTS.md §7) and Substack publishing (§25.3).
- **Never fetches or scrapes a roster member's profile.** The URL is
  stored as given; it is never the basis for pulling that person's real
  content or activity.

## Report back

Always end with: the two file paths, the confirmed program goal, and the
3-5 open decisions needing sign-off from the user or comms team. Make
explicit that this is a planning document — the program still needs a
human (the user, comms, or a manager) to actually distribute it, collect
sign-off, and run the 14-day launch with the real team.
