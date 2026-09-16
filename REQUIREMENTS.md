# AI-Powered LinkedIn Content Research & Growth Agent — Requirements

Status: **Draft — requirements captured, no implementation started.**
Owner: Priyanshu Arya
Last updated: 2026-09-17 (§27 added: Reading Third-Party Post Content)

---

## 1. Vision

A semi-autonomous LinkedIn growth agent that runs a continuous loop:

```
Research → Discover Ideas → Create Content → Generate Visual →
User Approval → Schedule → Publish → Analyze → Learn → Improve
```

The system does the repetitive work (research, drafting, scheduling, analysis).
Data drives decisions. **The user retains editorial control** — nothing is
scheduled or published without explicit approval, unless an autonomous mode is
explicitly enabled later. The system must get measurably better with every
publishing cycle.

---

## 2. Content Research

**No hardcoded topics, ever.** Every research cycle must start from a live,
real-time search — recent news, industry updates, major technology
announcements, new research/papers, company/product developments, market
trends, and active discussions — to determine what is genuinely trending,
important, and worth discussing *right now*. The specific topic for a post
is never chosen from a fixed/predefined list and is never reused
generic/stale content ("Top 10 Trends"-style filler).

**Topic domains** (the user's defined content pillars — closed set, but not
a menu of specific topics): AI, Tech Career, Developer Tools, GenAI, Machine
Learning, Deep Learning, Interview Prep, Data Analytics, Data Engineering,
Maths Related to Data, Problem Solving, Algorithms, Research, Psychology +
AI, AI in Healthcare. Every post must fall under one (or a clear combination)
of these — this bounds *what the account is about*, it does not supply the
topic itself. Within each pillar, the specific topic is still never
hardcoded: every research cycle starts from a live, real-time search —
recent news, industry updates, major technology announcements, new
research/papers, company/product developments, market trends, and active
discussions in that pillar — to determine what is genuinely trending,
important, and worth discussing *right now*. Never reuse generic/stale
content ("Top 10 Trends"-style filler) as a substitute for that research.
The default research mode scans across all pillars rather than being scoped
to one at a time, so trend strength (not the caller) decides which pillar(s)
get covered in a given run.

**Research pillar, specifically:** covers posts built from real, verified
research papers (arXiv, ACM/IEEE, company/lab publications, etc.) on trending
AI, Machine Learning, Deep Learning, Data Engineering, Algorithms, and
adjacent tech topics. A Research post must actually read the paper (not just
a press summary), then explain it as the author's own plain-language
take: what the paper found, why it matters, and a simple explanation with a
real-life example or practical usage — not an academic abstract restated.
Referencing/linking the source paper is optional per post (use it sometimes,
not every time); never fabricate a paper, finding, or citation — only
reference papers actually verified during research (per the Verification
rules above).

Maps to `Content-Research/` vault folders: AI, Career (= Tech Career),
Developer-Tools, GenAI, Machine-Learning, Deep-Learning,
Interview-Preparation, Data-Analytics, Data-Engineering, Mathematics (=
Maths Related to Data), Problem-Solving, Algorithms, Research-Papers (=
Research), Psychology-AI, AI-Healthcare, Resources (learning resources,
cross-cutting).

**Content types/formats to discover** (rotate, don't repeat the same shape
daily) — each applies within any of the pillars above, not as its own
domain:
- Educational: concept explanations, ELI5, deep-dives, tutorials, **cheat
  sheets**, interview prep, coding/system-design/ML/math concepts, roadmaps,
  curated **learning resources**.
- AI & tech: new tools, new model releases, trending GitHub projects, research
  breakdowns, use cases, prompting techniques, tool comparisons, workflows.
- Opinion/discussion: good vs bad AI use, tradeoffs, controversial takes, AI
  + psychology, AI augmenting vs replacing jobs, industry observations,
  **do's and don'ts** of current practice in a pillar.
- Career: interview questions, resume tips, job-search strategy, skills to
  learn, common mistakes, roadmaps.
- High-engagement/viral formats: "I tested X", lessons learned, mistakes to
  avoid, X vs Y, top resources, frameworks, checklists, myth vs reality,
  before/after, mini case studies, poll-worthy questions. Prefer formats
  proven to travel well on LinkedIn for the pillar's audience over safe,
  generic phrasing — see §14 (Virality/Quality Gate).

**Scoring per topic** (weights TBD, tunable):
Trend, Relevance, Freshness, Authority, Engagement Potential, Originality,
Educational Value.

**Verification rules**: prefer primary sources; cross-check important claims;
never invent statistics, findings, benchmarks, or quotes.

---

## 3. Knowledge Base (Obsidian)

All research persists as the system's long-term memory, in the user's
Obsidian vault under `Content-Research/`:

```
AI/  GenAI/  Machine-Learning/  Mathematics/  Psychology-AI/
Developer-Tools/  Research-Papers/  Interview-Preparation/  Career/
Resources/  Post-Ideas/  Published-Posts/  Analytics/  Content-Learnings/
```

Each research note: topic, summary, key findings, sources/URLs, date
discovered, category, trend score, content ideas, potential hooks, related
topics, "content already created from this?" flag.

---

## 4. Idea Engine

Generate ~10–20 candidate ideas per cycle (not just the final 5). Each idea
carries: topic, angle, why it matters, target audience, format, hook,
estimated engagement potential, sources, suggested visual, category. Rank and
select for strongest + most diverse set.

---

## 5. Weekly Cadence

- **Default target: 3 posts/week**, not a fixed 5. Starting-heuristic days:
  **Tue / Thu / Sat** — a provisional default (same status as §11's generic
  posting-time default), to be replaced once `Content-Learnings/
  playbook.md` has real evidence (≥3 published posts) on which days
  actually perform for this account. Sunday stays excluded by default;
  Saturday is in scope by default (previously excluded unless requested —
  reversed because forcing every post into Mon–Fri artificially compressed
  a lower-frequency cadence back toward a daily-feeling one).
- **Quality gates the count — this is a hard rule, not a target to hit.**
  Never generate or schedule a post just to reach 3/week. If the week's
  research only supports 1 or 2 genuinely distinct, valuable angles, ship
  that many and say so plainly. An honest gap is always preferred over a
  manufactured or padded post.
- Avoid same-topic repetition across the week. Content-type variety is
  **not** bound to specific calendar days (a fixed Mon=X/Tue=Y table doesn't
  fit a flexible 3-slot week) — instead, the week's chosen angles must span
  at least 2 distinct categories/content-types, checked against the
  Playbook's evidenced patterns first, falling back to this variety rule
  otherwise. Mix should evolve based on analytics, not stay fixed.

---

## 6. Post Generation

Human-sounding, conversational, educational, scannable, technically accurate,
non-generic, free of obvious AI-writing tells, consistent personal voice.
Strong hook → useful body → natural discussion CTA when appropriate. No
gratuitous clickbait. Stay comfortably under LinkedIn's character limit unless
length is genuinely justified.

**Style learning**: analyze the user's past posts, posts approved unedited vs.
heavily edited, preferred hooks/formatting/emoji usage/technical depth/CTA
style/vocabulary/length. Approved + edited posts feed back as few-shot
examples so future drafts increasingly sound like the user.

**Hashtags**: recommended from topic/audience/trends/historical performance/
niche relevance; strategy evolves from real performance data, not stuffing.

---

## 7. Visuals

Auto-propose/generate visuals when they aid understanding: infographics,
cheat sheets, diagrams, concept illustrations, comparisons, framework
graphics, AI illustrations, quote cards, slides, mini carousels, architecture
diagrams. Visual must support the point, not decorate. Image-generation layer
must be provider-swappable (free/low-cost providers interchangeable).

---

## 8. Approval Workflow (hard requirement)

```
Generated → Research Verified → Post Created → Visual Created →
Preview → Awaiting Approval
```

No auto-publish of newly generated content, ever, unless the user explicitly
enables an autonomous mode later. User actions on a draft: **Approve, Edit,
Regenerate, Change Hook, Change Image, Change Time, Reject**. Only Approved
items enter the scheduling queue.

---

## 9. Buffer Integration

Approved posts go to Buffer. System tracks: post text, media, scheduled
date/time, status, Buffer post ID, publish status. Prefer Buffer's official
API/integration over browser automation.

---

## 10. Rolling Schedule

Maintain **≥2 days of approved, scheduled content ahead** at all times. If the
buffer drops below 2 days, notify the user and prepare new drafts for
approval. At the start of each week, can prepare all 5 posts at once.

---

## 11. Posting-Time Optimization

Start from research-backed generic LinkedIn best-times. Once enough posts are
published, the user's own analytics take priority — learn best
day+time+content-type combos (e.g., tutorials Wed afternoon, career posts Tue
evening, breaking AI news ASAP rather than waiting for a slot). Scheduling
becomes personalized over time.

**Generic starting default (research-backed, as of 2026-09):** aggregated
from Buffer's and Sprout Social's 2026 LinkedIn studies (multi-million-post
datasets). All times are the user's local time (IST) — LinkedIn best-time
research treats "X pm" as local to the poster/audience, no timezone
conversion needed.

| Day | Default time | Notes |
|---|---|---|
| Monday | 13:00 | |
| Tuesday | 16:00 | strong window 11:00–17:00 |
| Wednesday | 16:00 | single strongest slot across all studies |
| Thursday | 17:00 | strong window 11:00, 13:00–17:00 |
| Friday | 15:00 | |
| Saturday | 09:00 | weekend engagement is weak platform-wide; morning outperforms evening if Saturday must be used |
| Sunday | — | avoid; excluded from default cadence (§5) |

For the project's default Tue/Thu/Sat cadence (§5) this means **Tue 16:00 /
Thu 17:00 / Sat 09:00** local time until playbook evidence overrides it.
This table is itself an unvalidated starting heuristic, not derived from
this account's real performance data — `/schedule-approved` should say so,
not present it as optimized. It is superseded automatically once
`Content-Learnings/playbook.md` has ≥3 published posts' worth of
day+time evidence (§13).

---

## 12. Analytics

Pull from Buffer periodically: impressions, reach, reactions, comments,
shares, clicks, engagement rate, follower growth, plus post metadata (time,
category, format, length, hook style, hashtags, visual type). Each published
post keeps a performance history.

---

## 13. Performance Analysis & Learning Loop

Derive *why* posts perform (e.g., "tool tutorials get 1.8x engagement",
"<1500 chars performs better", "cheat-sheet images drive saves", "Wednesday
posts get more impressions", "question hooks drive comments"). These become
structured rules in a persistent **Content Playbook**: best topics, hooks,
length, times, visual formats, CTAs, categories; and anti-patterns (poor
performers, topics going stale). Full cycle:

```
Research → Create → Approve → Publish → Measure → Analyze → Learn →
Update Strategy → Create Better Content
```

---

## 14. Virality / Quality Gate

A pre-publish **Viral Potential Score** from: hook strength, topic freshness,
audience relevance, emotional resonance, educational value, shareability,
discussion potential, originality, credibility, visual usefulness, historical
performance of similar posts. Low-scoring drafts get auto-improved before
being shown for approval. (Framed as reach probability, never a guarantee.)

---

## 15. Duplicate / Fatigue Detection

Before generating, check prior research + published content for same topic,
hook, examples, resources, arguments, or images. If too similar, pick another
topic or a substantially different angle.

---

## 16. Evergreen vs. Trending Balance

Mix trending (new releases, papers, news, tools) with evergreen (interview
prep, ML concepts, math, career advice, cheat sheets, tutorials) so the
account isn't purely news-cycle-dependent.

---

## 17. Source & Citation Management

Every post retains, internally, its Research Sources (primary + supporting),
publication date, and confidence level — visible to the user for verification
even when not included in the LinkedIn post text itself.

---

## 18. Content Calendar / Dashboard

Views: Research (trending ideas discovered), Drafts (awaiting review),
Approval Queue, Scheduled (approved, in Buffer), Published, Analytics,
Learnings.

---

## 19. Notifications

Notify on: weekly posts ready, approval needed, scheduled queue <2 days, a
post failed to publish, a post significantly outperforms baseline, an
important trending topic appears, a time-sensitive AI announcement needs fast
coverage.

---

## 20. Cost Optimization

Cheap/fast models for: topic classification, summarization, tagging,
duplicate detection, simple transforms. Stronger models reserved for: deep
research, fact verification, final post writing, complex reasoning,
performance analysis. Image generation and LLM providers must both be
swappable without an application rewrite (provider abstraction layer).

---

## 21. Safety Controls

Never fabricate research, statistics, quotes; clearly separate opinion from
fact; prefer primary sources; cross-check important claims; do not
auto-publish unverified breaking news; prevent duplicate posts; require
approval before scheduling; keep logs of everything generated and published.

---

## 22. Future Expansion (not in initial scope)

LinkedIn carousels, LinkedIn articles, polls, X/Twitter, Instagram, Threads,
blog posts, newsletters, YouTube scripts, short-form video scripts. One
research item → many derivative content pieces (post → carousel → blog →
thread → newsletter → video script). Architecture should not preclude this,
but it is not required for v1.

---

## 23. Proposed Agent/Module Decomposition

1. **Trend Scout** — surfaces trending/emerging topics.
2. **Research Agent** — deep research + verification.
3. **Idea Ranker** — scores and ranks candidate ideas.
4. **Content Strategist** — decides weekly mix, what/when to post.
5. **LinkedIn Writer** — drafts the final post text.
6. **Visual Agent** — generates supporting images/diagrams/carousels.
7. **Quality/Critic Agent** — checks accuracy, readability, originality, hook
   strength, viral potential score.
8. **Approval Manager** — presents drafts, collects user decisions.
9. **Scheduler Agent** — pushes approved posts to Buffer, manages rolling
   2-day-ahead buffer.
10. **Analytics Agent** — pulls performance data from Buffer.
11. **Growth Agent** — turns analytics into Content Playbook updates.
12. **Knowledge Manager** — reads/writes the Obsidian vault (research,
    content, sources, analytics, learnings).

---

## 24. Open Questions (need user input before/while planning)

- Obsidian vault location on disk, and whether it's already in use for other
  notes (namespace collisions to avoid).
- Buffer plan/API access level (which endpoints are available on the user's
  plan) and target LinkedIn page/profile.
- LLM provider(s) available (API keys) for cheap-tier vs. strong-tier models.
- Image-generation provider(s) available/preferred to start with.
- Where the user wants to review/approve drafts day-to-day (CLI, Obsidian
  itself, a small web dashboard, Slack/email digest, etc.).
- Hosting/runtime for the "always-on" parts (research cadence, queue
  monitoring, notifications) — local machine on a schedule, or a server?
- Definition of "significantly outperforms normal" for the notification
  trigger (needs a baseline once there's post history).

---

## 25. Multi-Platform Expansion: X (Twitter) and Substack

Added 2026-09-14, once the LinkedIn pipeline above was working end to end.
Extends the same research → idea → draft → critique → visual → approval →
publish → analyze → learn loop to X and Substack, reusing whatever is
genuinely platform-agnostic and building fresh only where a platform's
format or publishing mechanism actually differs. Full architecture
rationale: [DECISIONS.md — Multi-Platform Expansion (X + Substack)
decisions](DECISIONS.md#multi-platform-expansion-x--substack-decisions).

### 25.1 Shared research and idea pool

**No separate research pipeline per platform.** §2's live, real-time,
never-hardcoded research discipline stays exactly as specified — it simply
now feeds three platforms instead of one. An Idea Note (§4) gains a
`platforms: []` field naming which platform(s) it's eligible for; each
platform's own writer produces its own draft from the idea independently —
never a copy-pasted adaptation of another platform's draft. Because one
idea can carry different assigned dates on different platforms, ideas also
gain a `platform_schedule: []` field for every platform except LinkedIn,
which keeps using the original `target_week`/`target_date` fields
unchanged.

### 25.2 X (Twitter)

- **Cadence:** ~5/week by default, mix of single posts and threads decided
  per-idea by the writer from the idea's actual depth — never a fixed
  singles/threads split, and never padded to hit the number (same hard
  rule as §5).
- **Format:** a single post stays well under X's per-post character limit;
  a thread is written as an ordered sequence where the first tweet must
  stand alone as a hook. Hashtags: 0–2 (much lighter than LinkedIn's 3–5),
  omitted by default rather than forced.
- **Posting-time heuristic:** sourced live from current X best-time
  research the first time weekly planning runs for this platform — not
  assumed to match LinkedIn's IST/Tue-Thu-Sat table, since audience
  behavior differs. Same "unvalidated starting point until real evidence
  exists" framing as §11.
- **Scheduling:** via the same Buffer account already used for LinkedIn,
  a separate connected channel. Single-post scheduling reuses the proven
  `createPost` mutation. **Thread-posting's mutation shape is not assumed**
  — it must be confirmed against Buffer's live GraphQL schema/error
  responses before the first real thread is scheduled, the same discipline
  that caught the original LinkedIn scheduler's `channelId` type
  correction (§9/Phase 8).
- **Analytics & playbook:** same Buffer metrics pull as LinkedIn, scoped to
  the X channel, feeding a separate `playbook-x.md` — a pattern proven on
  LinkedIn is not assumed to transfer to X.

### 25.3 Substack (Articles and Notes)

Two distinct formats under one platform:

- **Articles:** long-form (title, subtitle, sectioned body), no character
  ceiling — length is governed by the material, not a target. Default
  cadence 1/week, and only for ideas that genuinely earn full-length
  treatment; an empty slot in a given week is a correct, honest outcome.
  Critiqued on structure/depth/SEO fit rather than a scroll-stopping hook
  (§14's Viral Potential Score framing still applies, just reweighted for
  the format). Visuals may be multiple per piece, one per section that
  genuinely needs one, unlike the single-image LinkedIn/X norm.
- **Notes:** short-form, casual, conversational — closer to X's brevity
  than LinkedIn's polish, no hashtag convention. Default cadence ~3/week.

**Publishing is manual by design, not a missing feature.** Buffer has no
Substack channel, and Substack has no supported public posting API. An
unofficial, session-cookie-based API was explicitly considered and rejected
(ToS risk, undocumented, could break silently) in favor of the same
deliberate-manual precedent this pipeline already uses for image generation
(§7): the system produces a finished, copy-ready deliverable, and a human
performs the actual publish action. The system never marks something
`published` without the user's explicit confirmation that run — no
assuming publication happened just because time passed.

**Analytics** have no automated pull (no API) — §12's metrics get entered
manually from the user's own Substack dashboard when available, same
never-fabricate discipline as everywhere else in this spec (§21): a number
not actually obtained is left blank, never estimated. Playbook evidence
(§13) accumulates in `playbook-substack.md`, tracking Articles and Notes as
separate populations rather than averaging a 2,000-word piece against a
one-line Note.

### 25.4 Guardrails unchanged

§8 (no auto-publish without human approval), §15 (duplicate/fatigue
detection), §17 (source/citation retention), and §21 (never fabricate,
opinion/fact separation) all apply identically per platform. The
`content-index.md` fast-lookup table (§13/§15 machinery) gains a `platform`
column so cross-platform dedup and fatigue checks share one index instead
of three, while the underlying per-platform playbooks and voice guides stay
separate — evidence and voice do not transfer across platforms by
assumption.

---

## 26. Story Bank (Interviewer)

Added 2026-09-16. Every content-generation skill so far (`/write-draft` and
its X/Substack variants, `/plan-week`, `/generate-week`) has assumed either
a research note or a prior post archive to ground itself in. Neither exists
for a user who hasn't posted yet, and even for an established account,
research notes don't carry the specific personal material — a real number,
a war story, a position the user would actually defend — that separates a
generic post from one only this person could have written. The **Story
Bank** is where that material lives.

**What it stores, and why.** Six categories, direct from the user's own
mouth only: **Roles** (what they've actually done), **Receipts** (real
numbers with a named referent — never a rounded or invented one),
**Turning Points** (beliefs abandoned, and the cost), **Scars** (hard
lessons from a reversal or failure), **Defensible Positions** (contrarian
views the user would actually defend, distinguished from stated fact per
§21's opinion/fact discipline), and **Told-Out-Loud Stories** (narratives
already pre-tested by being told verbally, not written for the first time
during a draft). None of this is ever inferred, estimated, or generated —
it is recorded only from a direct interview (`/interviewer`), the same
never-fabricate discipline as §21 applied to a new kind of source: the
user themselves, not a web search.

**Single living document.** All of it lives in one file,
`Content-Learnings/story-bank.md`, using the same single-versioned-doc
pattern as `playbook.md` (§13) rather than one note per item — rows
accumulate under a stable `id` per row (never referenced by position) as
repeated interviews add to it. Corrections to an existing row are explicit,
logged, user-requested edits, never a silent overwrite.

**Read by every content-generation skill, not just this one.** Rather than
a drafting skill prompting the user mid-draft for "a real example" or "a
number that backs this up," it should read `story-bank.md` first and pull
an existing Receipt/Scar/Position/Story that fits, citing it by `id`. This
skill (`/interviewer`) only ever writes the Story Bank — it never drafts,
critiques, schedules, or publishes; wiring individual reading skills (e.g.
`/write-draft --spine`) to actually consume it is separate, incremental
work tracked per-skill, not a requirement that this skill itself implement.

**The only skill that works with zero post archive.** Every other
content-generation skill needs either research notes or prior posts to
ground a draft. `/interviewer`'s onboarding mode (Mode A) needs neither —
it draws directly on the user's career history through a guided interview,
which is why it is the correct starting point for a brand-new account with
no archive at all.

**Mode B: Post Spines.** A focused, single-topic interview
(`/interviewer <topic>`) doesn't run the full six-category onboarding
round — it asks a handful of targeted questions and assembles a **Post
Spine** (hook angle, story beat, cross-referenced receipt/position, a
suggested close). This is stored as its own entry, in the same
`story-bank.md` file under a `## Post Spines` section — not a separate
scratch file — so spines accumulate and stay queryable by `id` alongside
the material they cite.

---

## 27. Reading Third-Party Post Content (Shared Convention)

Added 2026-09-17. Four skills across this repo need to read the content of
a post someone else published — `/extract-hook` (Phase 16, reverse-
engineering a viral post's hook) and three later builds: Comment Drafter,
Reply Handler, and Engagement Monitor. Rather than each one re-deriving
its own rule for how that reading happens, the rule is stated once, here,
and every skill that needs it cross-references this section instead of
restating it.

**No official API exists anywhere in this repo for reading an arbitrary
third-party post's content from just a URL** — on LinkedIn or any other
platform. Buffer, this system's only platform integration, covers the
user's own scheduling/publishing/analytics, never someone else's content.

**WebFetch on a gated post URL is unreliable.** It may be attempted as a
best-effort convenience, but it typically returns a login wall or a
stripped/partial page rather than the full text. Its result must never be
treated as ground truth without the user explicitly confirming it matches
what they actually see when they view the post themselves.

**The primary, reliable input is the user pasting the text directly.** A
URL is optional metadata only — useful for filing, reference, or dedup —
never the sole data source a skill drafts, classifies, or replies from.

**No skill in this repo scrapes, uses session cookies, or otherwise
bypasses login/ToS to read third-party content** — the same precedent as
§25.3's rejection of an unofficial, session-cookie-based Substack API for
this system's own publishing. If it wasn't acceptable to bypass ToS to
*publish* the user's own content, it isn't acceptable to bypass it to
*read* someone else's.

**Every skill following this convention says so explicitly in its own
SKILL.md** — a one-line cross-reference to this section — rather than
re-stating the full rule inline.

---

## 28. Viral Hook Formulas, Founders Angles & Post Spines (Post Writer)

Added 2026-09-17 (Phase 17). `/write-draft` (Post Writer) is reworked to
pick a hook formula for every draft, optionally shape a draft around a
founders angle, and — new alternative entry path — draft directly from a
Story Bank Post Spine instead of an Idea Note. The existing idea-based flow
remains the primary, default path; none of this weakens its
research-grounding or no-fabrication rules.

**Engagement goal — closed 5-value list.** Every draft is written toward
exactly one engagement goal: **likes, comments, shares, saves,
profile-visits**. No sixth value is ever introduced. Precedence for
determining it: an explicit `--goal` argument > the idea's own goal field
if set (idea path only) > a `playbook.md`-evidenced pattern for that
category, if one exists > default `comments`.

**Hook formula selection.** `/write-draft` reads `Content-Learnings/
hook-formulas.md` (§ established at Phase 16) fresh on every run and
selects a `status: canonical` row tagged for the chosen engagement goal (a
row with no `engagement_goals` value is general-purpose, eligible for any
goal). A `proposed` row is never selected for drafting — only human
promotion to `canonical` makes a formula trustworthy for this purpose. The
skill prefers a formula not used in the last ~5 drafts, checked via the
Draft Note's new `hook_formula` frontmatter field, to avoid visibly
repetitive openings — but goal-fit still wins over novelty when every
eligible formula was recently used.

**Founders angle — optional, fallback is to drop it, never fabricate.**
`Content-Learnings/founders-angle-library.md` (new, Phase 17) is a second
shared living doc in the same canonical/proposed pattern as
`hook-formulas.md`, seeded with 10 angles adapted from
`sergebulaev/linkedin-skills` (MIT). A founders angle reshapes a draft's
*entire structure* (not just its opening line, unlike a hook formula) and
is only ever considered for the Career / Interview Prep categories, or when
the user explicitly asks for one. It is used only when a `canonical` angle's
bracketed template slots can be filled from an actual, real
`Content-Learnings/story-bank.md` row (a Receipt, Turning Point, Scar, or
Defensible Position) that genuinely matches the topic — every bracket
filled with a real value, cited by that row's `id`. If no real match
exists, the angle is dropped for that draft entirely, and the skill says so
explicitly when reporting back — never filled with an invented
number/anecdote that merely looks real. This is the Story Bank's (§26)
never-fabricate discipline extended to angle *selection*, not just
fact-checking within a chosen angle.

**New `--spine` entry path (alternative to an Idea Note).** `/write-draft
--spine <spine_id>` drafts directly from a Post Spine row in
`Content-Learnings/story-bank.md`'s `## Post Spines` table (§26), produced
by `/interviewer`'s Mode B. The spine's `receipt_id`/`position_id`
cross-references, when set, are this path's grounding, held to the exact
same rigor as an idea's linked research notes — every claim traces back to
the spine's own fields or the Story Bank rows it cites, and a spine that
cross-references nothing may not have anything invented in its place. A
draft from this path has no `idea_id` (so no idea `status` to flip to
`drafted` afterward) — instead its Draft Note records `spine_id`, and its
`sources` list cites the Story Bank row(s) actually used rather than a
research note.

**Draft Note schema.** `_Templates/Draft-Note.md` gains four new optional
frontmatter fields, all empty-string by default so every previously
written draft keeps validating unchanged: `hook_formula`,
`engagement_goal`, `founders_angle`, `spine_id`.
