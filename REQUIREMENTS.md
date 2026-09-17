# AI-Powered LinkedIn Content Research & Growth Agent — Requirements

Status: **Draft — requirements captured, no implementation started.**
Owner: Priyanshu Arya
Last updated: 2026-09-17 (§29 added: Humanizer)

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

---

## 29. Humanizer (Style De-AI-ification)

Added 2026-09-17 (Phase 18). `/humanize-draft` scores and rewrites a
draft's **surface style** against a real, numeric 2026 AI-writing-tell
rule set in `Content-Learnings/humanizer-rules.md`, and documents — never
claims to close — the disagreement between AI-detection services. It is a
shared step two later builds (Post Audit, Repurposer) call, not just a
standalone skill, so its input/output contract matters as much as its own
behavior.

**Scoring dimensions**, all defined with real numbers (not invented
thresholds) in `Content-Learnings/humanizer-rules.md`:
- **AI vocabulary markers** — durable 2026 markers (e.g. leverage, robust,
  landscape, nuanced) scored per paragraph; decaying 2023-24 terms (delve,
  tapestry, realm, journey, paradigm) flagged for scrutiny but noted as
  "now mostly harmless." Density threshold: 3+ markers in one paragraph
  triggers a rewrite of that paragraph; a single marker alone does not.
- **Em-dash cap** — see below.
- **Reveal bridges** — four specific phrases ("The result?", "It's not X,
  it's Y", "Stop X, start Y", "Here's what/how"), each with a measured
  real reach-impact percentage; every hit is flagged, no free allowance.
- **Staccato fragment stacks** — five patterns banned outright (pseudo-
  question fragments, "No X. No Y. Just Z.", "All the X. None of the Y.",
  adjective stacks, one-word paragraphs), plus a document-wide cap of 2
  standalone fragments for any other legitimate use.
- **Stacked triads** — one natural rule-of-three allowed per post
  (matching the ~26% of top-performing posts that contain one); anything
  beyond that is scrubbed.
- **Performed sincerity** — phrases like "Let me be honest" or "Unpopular
  opinion:" preceding a widely-held claim, plus inserted hedges
  ("perhaps," "I might be wrong") flagged as a related tell.
- **Readability** — Flesch reading ease target > 55.
- **Odd-precision numbers** — only counted as a genuine human fingerprint
  when a named referent (who/what/when/cost) is attached; a bare precise
  number is not automatically a positive signal, and is never rewritten
  since doing so would change a claim.

**Em-dash cap, specifically.** Capped at **~1 per 100 words** — a cap, not
a ban. Zero em dashes is itself a tell ("trying too hard to look human").
For reference, GPT-5.4-era text emits ~1.43 em dashes per 1,000 words,
well below the ~3.23-per-1,000 human baseline, so this cap is deliberately
generous, not restrictive. Excess dashes convert to commas, colons, or
parentheses — never periods, since that changes rhythm too much to count
as a same-meaning style fix.

**Never claims to beat or guarantee evasion of any AI-detection service.**
The multi-detector spread-check (GPTZero, Originality.ai, ZeroGPT,
Sapling, Copyleaks) is manual-only — no API keys are held for any of the
five services, and none of their APIs are ever called or their web UIs
scraped, permanently, not just "for now." This is the same manual-fallback
precedent as §7 (visuals: no image-generation provider configured, so the
deliverable is a paste-ready prompt) and §25.3 (Substack publishing: no
supported API, so the deliverable is a copy-ready note and a human
publishes it). Here, the skill hands back the finished revised draft plus
an instruction block asking the user to paste it into each of the five
services themselves and report back the scores; if they do, those scores
are logged verbatim and the spread is reported as a range ("scores ranged
X–Y across services; treat none as ground truth, never average them into
a single verdict") — never fabricated, never averaged into a single
pass/fail verdict.

**Input/output contract** (the stable interface Post Audit and
Repurposer, two later builds, will call this skill through — see
`.claude/skills/humanize-draft/SKILL.md`'s own "Input / Output Contract"
section for the full, authoritative version):
- **Input:** `text`, `platform` (linkedin | x | substack-note |
  substack-article), optional `draft_id` (if given and a real Draft Note
  with that id exists, a `history` entry is logged on it).
- **Output:** `revised_text`; a `score_report` (one entry per scoring
  dimension above); a `detector_spread` object that starts `{status:
  "not_run"}` and only becomes `{status: "manual_results_provided",
  results: [...]}` once the user actually supplies real detector scores;
  a `changes_made` list (`{rule, before, after}` per change); and a
  `caveats` string that is always present, every call, stating plainly
  that no detector-proof or guaranteed-undetectable claim is being made.

**Style/surface only — never touches facts.** This skill never changes a
claim, source, or number in a draft; that discipline stays
`/critique-draft`'s job (§14/§21). Humanizer rewrites how something is
said, never what is claimed.

---

## 30. Pre-Publish Algorithm & Authenticity Audit (Post Audit)

Added 2026-09-17 (Phase 19). `/audit-draft` runs on a Draft Note that has
already been through `/critique-draft` and sits at `status: in_review` —
after the accuracy/originality/viral-score pass, before `/review-drafts`
presents the note for human approval. It checks the draft against current
LinkedIn platform-mechanics behavior and screens it for AI-writing tells,
then **annotates the note with a `## Post Audit Notes` section**. It never
changes `status` itself — the same non-gating role for this dimension that
`/critique-draft`'s viral-score check already plays for originality (§14):
a finding here is information for the human reviewer, not an automatic
block.

**Pipeline position:** `/write-draft` → `/critique-draft` (`draft →
in_review`) → `/audit-draft` (this skill — annotation only) →
`/review-drafts` (`in_review → approved`, the only skill allowed to make
that transition) → `/schedule-approved`.

**Three-tier confidence structure.** Every finding `/audit-draft` cites
from `Content-Learnings/algorithm-rules.md` carries one of three tiers,
and they are never blended or presented with equal weight:
- **Sourced Findings** — each names its real source (e.g. the 360Brew
  paper, AuthoredUp's 2026 reach data, Van der Blom's algorithm-insights
  analysis, a named LinkedIn VP Product statement).
- **Verified Numeric Thresholds** — hard numbers checked directly against
  the draft (length sweet spot, hook-truncation cutoffs, hashtag count,
  external-link-in-body penalty, closing-question lift, posting-window
  fit).
- **Unconfirmed / Third-Party Claims** — explicitly low-confidence
  (pod-detection accuracy, comment-pod penalties, link-in-first-comment
  lift, save-to-like weighting, and similar reported-but-unofficial
  figures). These are always cited as "reported, unconfirmed" — per §21
  (never present an unconfirmed claim with the same confidence as a
  verified one), `/audit-draft` never lets one of these fail a check or
  read as settled fact.

**90-day self-refresh policy.** `Content-Learnings/algorithm-rules.md`
carries a `last_updated` date and is treated as stale after 90 days (or if
the file doesn't exist yet). `/audit-draft` checks this on every run — if
stale, it re-researches via `WebSearch` against official LinkedIn
engineering/creator statements and reputable aggregators (Buffer,
Hootsuite, Social Insider, AuthoredUp — the same sourcing bar as §11's
posting-time research) before applying the audit, then rewrites the file
with fresh findings, preserving the three-tier structure. This is the same
lazy "self-refresh on use" pattern `/generate-visual` already applies to
live visual-trend research (§7) — there is no separate cron/scheduled job
keeping this file current.

**AI-detection is delegated, never duplicated.** `/audit-draft` does not
re-implement any of Humanizer's vocabulary/em-dash/pattern-density
detection logic. It calls `/humanize-draft`'s own documented Input/Output
Contract (§29; `.claude/skills/humanize-draft/SKILL.md`) directly — `text`
= the draft body, `platform` = the draft's platform — and surfaces the
returned `score_report` and `caveats` verbatim in its own output. If
Humanizer also returns a suggested rewrite, `/audit-draft` reports it but
does not apply it; applying an edit stays `/critique-draft`'s,
`/humanize-draft`'s (run directly with intent to revise), or a manual
edit's job.

**Annotation only — hard rules.** `/audit-draft` never changes `status`,
never auto-schedules or auto-publishes, never fabricates an algorithm rule
without a cited, tiered source, and never auto-revises the draft text
itself. Its output is a `## Post Audit Notes` section on the Draft Note
(algorithm findings tagged by confidence tier, Humanizer's full output,
and the rules file's freshness status) plus a `history` entry — nothing
more.

*Reference material for `Content-Learnings/algorithm-rules.md`'s seed data
adapted (not copied verbatim) from the MIT-licensed
`sergebulaev/linkedin-skills` project — see that file's own header for the
full attribution.*

---

## 31. Repurposing (Cross-Platform → LinkedIn)

Added 2026-09-17 (Phase 20). `/repurpose-post` (Repurposer) is the first
skill in this repo that goes the direction every existing multi-platform
skill doesn't: **other platform's content → LinkedIn**, rather than
LinkedIn-pipeline idea → another platform (§25's `write-draft-x`,
`write-draft-substack-article`/`-note` all go outward from this system's own
idea pool). It turns a tweet/thread, YouTube video, blog post, or newsletter
into a native LinkedIn post, writing a normal `status: draft` Draft Note
that flows through the exact same `/critique-draft` → `/audit-draft` →
`/review-drafts` → `/schedule-approved` pipeline as any other draft — this
skill adds a new *input* path, never a new approval path.

**Source types and input handling.** Four source types, each with its own
judgment call layered on top of §27's shared "reading third-party post
content" convention (pasted text is primary and reliable; a URL is
best-effort metadata only; no skill in this repo scrapes or bypasses
login/ToS) — Repurposer cross-references §27 rather than restating it:
- **Tweet/thread:** pasted text is primary, per §27. A URL may be attempted
  via WebFetch as a best-effort convenience, but X/Twitter typically
  requires login for full content server-side, so any fetch result is
  treated as unverified — the user must confirm it matches what they
  actually see, or paste the text directly, before it's used.
- **YouTube video:** a **mandatory manual-paste case**, permanently. No
  transcript-fetching capability exists anywhere in this repo, and
  WebFetch on a YouTube URL returns only the page shell, never the
  transcript. Repurposer always asks for a pasted transcript excerpt or
  written summary of the key point(s), and never claims to have "watched"
  or reliably retrieved a video's content.
- **Blog/newsletter:** WebFetch is genuinely plausible (ordinary HTML
  renders fine) and is attempted as the primary path, falling back to a
  pasted-text request only if the fetch fails or returns unusable content
  (paywall, JS-rendered body, mostly boilerplate).

If no usable source content is obtained through any of the above, the skill
stops and asks for a manual paste rather than proceeding on a guess — the
same never-fabricate discipline as everywhere else in this spec (§21).

**Re-hook and expansion, citing §30's real thresholds (not new numbers).**
The source's own opening line was written for a different platform's
fold/audience assumptions, so Repurposer writes a genuinely new first 1-2
sentences against the **210-character (desktop) / 140-character (mobile)
hook-truncation cutoffs** (§30, Verified Numeric Threshold) — a rewrite of
the opening, not a trim of the source's. The body is then expanded into
the **900–1,300 character length sweet spot** (§30, Verified Numeric
Threshold) via framing/elaboration only: a concrete example or analogy
consistent with the source, unpacking an implication the source stated
tersely, or adding the personal-take framing LinkedIn favors. Expansion
never introduces a new factual claim, statistic, or quote beyond what the
source actually said.

**Links move to a first comment, never the body.** Per §30's documented
40-60% external-link-in-body reach-suppression threshold (Verified Numeric
Threshold — the same one `/audit-draft` flags an in-body link against), any
link worth preserving from the source is stored in the Draft Note's new
`source_link` field instead of the post body. Posting it as the actual
first LinkedIn comment is a **manual step** the user performs after the
post itself goes live — this repo has no mechanism to auto-post a follow-up
comment, the same deliberate-manual precedent as visuals (§7) and Substack
publishing (§25.3).

**Mandatory Humanizer pass.** Before finalizing, Repurposer calls
`/humanize-draft`'s documented Input/Output Contract (§29;
`.claude/skills/humanize-draft/SKILL.md`) with `text` = the drafted body and
`platform: linkedin`, and uses the returned `revised_text` as the final
copy — it does not re-implement any of Humanizer's own pattern-matching
logic, and surfaces the returned `caveats` string verbatim in its report,
the same delegation discipline `/audit-draft` already applies to the same
contract.

**Dedup check against `content-index.md`.** Before finalizing, Repurposer
checks `Content-Learnings/content-index.md` for topic/hook/argument overlap
with existing drafts or published posts — the same duplicate/fatigue
discipline `/write-draft`'s pipeline and `/generate-ideas` already apply
(§15/§25.4) — and flags rather than silently drafts a near-duplicate
repurposed angle.

**Draft Note schema.** `_Templates/Draft-Note.md` gains two more optional
frontmatter fields, all empty-string by default so every previously written
draft keeps validating unchanged: `source_type` (tweet | thread | youtube |
blog | newsletter | none) and `source_link` (the URL to post as a first
comment, blank if none).

**Never auto-publishes.** Output is always `status: draft`, entering the
existing approval pipeline unchanged — this skill never marks anything
`approved`, `scheduled`, or `published`, and never auto-posts the first
comment itself.

---

## 32. Weekly Calendar View & Comment Targets (Content Planner)

Added 2026-09-17 (Phase 21). **This section is additive to §5, not a
replacement** — the count/quality-gating rule in §5 is unchanged word for
word: default ~3 posts/week, never padded to hit a count, quality gates the
count as a hard rule rather than a target to hit. This section only adds a
full-week visibility format and two new per-slot fields to `/plan-week`
(Content Planner). It does not change which ideas get selected, how many
slots get filled, or the Tue/Thu/Sat starting heuristic and content-type
variety rule §5 already defines.

**Mon-Sun calendar view.** `/plan-week` now renders its report as a full
seven-day table (Monday through Sunday), not a list of only the days it
filled. Days §5's quality gate didn't clear are shown as explicit rows with
`status: empty` and the same one-line reason the skill already produces for
an unfilled slot (e.g. "no Career-category ideas in the pool") — an empty
day is visible and explained, never silently omitted and never padded with
a weak idea just to have something to show in every row. Sunday remains
excluded from the *fillable* cadence by default (§5) but still appears in
the view as an empty row, consistent with the rest of the week.

**Hook-formula assignment (filled slots only).** For each slot that gets
filled, `/plan-week` reads `Content-Learnings/hook-formulas.md` fresh and
assigns one `status: canonical` formula whose `engagement_goals` value fits
the idea's likely engagement goal (or a general-purpose formula carrying no
goal tag) and whose mechanic fits the idea's category/content_type. Two
anti-repetition checks apply, both required: (1) the same `formula_id`
never appears on two slots within the same week's plan, and (2) the recent
history in `Content-Learnings/content-index.md`'s `hook_gist` column
(§15/§25.4) is checked so a formula's mechanic isn't repeated from the last
few weeks' published/scheduled posts either, not just within this week's
own picks. This assigns a *formula suggestion* only, never the finished
hook text — `/write-draft` (§28) still does the actual drafting later, reads
`hook-formulas.md` fresh itself at that time, and may pick a different
formula if circumstances have changed by then (e.g. a `proposed` formula
was promoted to `canonical` in the meantime, or new playbook evidence
shifted the goal-fit). Nothing here overrides `/write-draft`'s own
hook-selection step. Only `canonical` formulas are eligible, same rule as
`/write-draft` — a `proposed` row is never assigned at planning time either.

**Time assignment (filled slots only).** For each filled slot,
`/plan-week` attaches the posting time §11 already specifies for whichever
day the slot landed on (Tue 16:00 / Thu 17:00 / Sat 09:00, etc.), unless
`Content-Learnings/playbook.md` has ≥3 published posts' worth of evidence
for a better day+time+content-type combination, in which case that
evidenced combination is used instead — exactly the override §11 already
defines. This is pure surfacing of §11's existing rule at planning time
instead of leaving the time unset until `/schedule-approved`; it introduces
no new time logic, no new default table, and no change to §11 itself.

**Comment targets (new concept, filled slots only).** For each filled
slot, `/plan-week` attaches 2-3 specific external accounts/posts to
proactively comment on that day. This is a genuinely new concept, not
previously defined anywhere else in this spec, sourced in priority order:

1. `Content-Learnings/comment-targets.md` — a new, **user-maintained**
   plain list (name, profile URL/handle, why, added date) of accounts and
   thought-leaders the user wants ongoing engagement with. Unlike every
   other `Content-Learnings/` living doc in this spec (`playbook.md`,
   `hook-formulas.md`, `humanizer-rules.md`, `algorithm-rules.md`,
   `story-bank.md`), this file is never system-populated or
   system-appended — it starts empty and only grows by the user's own
   edits.
2. **Fallback**, used only when (1) is absent or too thin to fill a slot:
   accounts/authors/publications that came up as sources or citations in
   that week's `/research-topic` runs, specifically the research actually
   backing that slot's idea.
3. **Neither source yields anything:** the field is left explicitly empty
   in the report with a one-line stated reason (e.g. "no
   comment-targets.md entries and no research-cited accounts this week").
   Never invented — a fabricated account or post here would look like a
   real recommendation and is exactly the kind of unverifiable claim §21
   already prohibits, so this file starts with zero example rows rather
   than the placeholder-row pattern `story-bank.md`/`hook-formulas.md` use
   for their schema.

**Hard rule (equal weight to §5's count-padding rule).** Hook formulas and
comment targets are attached only to filled slots. Never invent either for
a day that stays empty, and never let hook-formula or comment-target
scarcity itself become a reason to fill a slot that otherwise wouldn't
clear §5's quality bar. Scarcity in a supporting field is never license to
lower the bar on the underlying selection decision.

**Vault schema.** `Content-Learnings/comment-targets.md` is a fifth
registered `Content-Learnings/` NoteSpec in `scripts/validate_vault.py`
(`type: comment-targets`), validated with the same minimal
`id`/`type`/`version`/`last_updated` shape and `permissive_folder=True`
pattern as the four existing entries (`story-bank`, `hook-formulas`,
`humanizer-rules`, `algorithm-rules`) — the user-maintained `## Targets`
table itself is not schema-validated, the same way none of those four
files' body tables are.

---

## 33. Comment Drafting (Comment Drafter)

Added 2026-09-17 (Phase 22). `/draft-comment` drafts a comment on someone
else's LinkedIn post, in the user's own voice — a lightweight, mostly
ephemeral utility, not a new stage of the Research → Draft → Approve →
Schedule pipeline.

**Input** follows §27's shared convention exactly — pasted post text is
the primary, reliable input; a URL alone is optional metadata and a
WebFetch attempt on it is best-effort convenience only, never ground truth
without the user's explicit confirmation. Nothing here adds to or narrows
§27 — this is one of the four skills (alongside `/extract-hook`,
`/draft-reply`, and `/monitor-engagement`, §35) that cross-reference it
rather than restating it.

**Output is always ephemeral copy-paste text.** No vault artifact is
created: no Draft Note, no `Drafts/` entry, no `status: draft`/`in_review`
lifecycle, no entry in the approval pipeline (§8) or the Content Planner's
calendar (§32). This is the key difference from every other drafting skill
in this repo — a LinkedIn/X/Substack post draft is a vault-tracked object
because it eventually gets approved and scheduled; a comment on someone
else's post never does, so it never needs the schema that exists to
support that lifecycle.

**No comment-posting API exists anywhere in this repo.** Buffer covers
only the user's own scheduling/publishing/analytics (§9), never posting a
comment onto a third party's content. Same limitation class as §27's "no
read API for arbitrary third-party posts" — the output here is always
handed to the user to paste in manually; this skill never claims to have
posted anything.

---

## 34. Reply Drafting (Reply Handler)

Added 2026-09-17 (Phase 23). `/draft-reply` drafts replies to comments on
a LinkedIn post — single-reply mode for one pasted comment, or a sweep
mode for a full pasted thread export — the same lightweight, mostly
ephemeral shape as Comment Drafter (§33), not a new stage of the
Research → Draft → Approve → Schedule pipeline.

**Input** follows §27's shared convention exactly — pasted comment/thread
text is the primary, reliable input; a post URL alone is optional
metadata and a WebFetch attempt on it is best-effort convenience only.
This is the second of the three skills named in §27 (alongside
`/draft-comment` and `/monitor-engagement`, §35) that cross-reference it
rather than restating it.

**2-level-flattening attribution rule.** LinkedIn nests replies only one
level deep, flattening a reply-to-a-reply into the same top-level-reply
list with an auto-inserted "@Name" prefix marking its true target. Sweep
mode parses each top-level comment's replies into `{author, text,
replied_to}`, inferring `replied_to` from a leading "@Name" mention and
defaulting to the top-level comment's author when absent. Every drafted
reply is labeled with its explicit addressee ("Reply to [Author]
(responding to [X])") so nothing is misattributed when replies are
copy-pasted back individually.

**Low-value filter (sweep mode only)** — skipped, and reported as skipped
with a reason, rather than silently dropped: pure emoji/reaction-only
comments; generic praise with no specific reference to the post; off-topic
self-promotion/spam; a near-duplicate of a comment already answered
earlier in the thread; a tag/mention with no added content. Single-reply
mode always drafts what's asked — the filter never applies there.

**Output is always ephemeral copy-paste text.** No vault artifact is
created — no Draft Note, no `Drafts/` entry, no approval-pipeline
lifecycle (§8), same class of limitation as §33: no comment/reply-posting
API exists anywhere in this repo, so output always goes to the user to
paste in manually.

---

## 35. Engagement Monitoring (Comment Threads and Audience ICP)

Added 2026-09-17 (Phase 24). `/monitor-engagement` is the third and last
of the three skills named in §27's shared third-party-content-reading
convention (alongside Comment Drafter, §33, and Reply Handler, §34) — the
"not-yet-built Engagement Monitor" those two sections referenced is now
built, and their cross-references have been updated accordingly.

**State this plainly: both of this skill's workflows are manual-input
only.** Confirmed against `pull-analytics/SKILL.md` (§9): Buffer's API
returns metrics only for the user's own scheduled/published posts — it
has no visibility into third-party post/comment activity at all. There is
no live data source anywhere in this repo for (a) detecting when someone
replies to the user's comment on someone else's post, or (b) pulling a
likers/commenters list for an arbitrary post. Neither gap is closeable
without scraping or an unofficial/session-cookie API, which this repo
already rejected on the publishing side (§25.3) and that rejection
extends here to reading third-party engagement data — no live polling or
scraping capability is ever added for this skill.

**Workflow 1 — thread watch (`/monitor-engagement threads`).** Tracks the
user's own comment threads on other people's posts for author replies.
There is no notification/polling mechanism for third-party reply activity
anywhere in this repo, so every run is a manual snapshot: the user pastes
the post URL, the thread's current visible text, and (on first run) their
own comment's timestamp. Storage is a new top-level `Engagement/` folder,
one file per tracked thread: `Engagement/<post-slug>--thread.md`, created
from a new `_Templates/Engagement-Thread-Note.md` (frontmatter `id`,
`type: engagement-thread`, `post_url`, `my_comment_text`,
`my_comment_time` — user-supplied, since no API confirms it —
`status: watching|closed`; body a `## Logged Replies` table of
`author | text_snippet | seen_date`). Each run diffs the freshly pasted
thread text against the note's logged table; entries not already logged
are "new," and each new reply is bucketed by elapsed time from
`my_comment_time` to the diff run's own date (an approximation, not a
guaranteed reply-time measurement — stated as such in every report):
under 6h logs the reply and defers drafting; 6-24h delegates to
`/draft-reply`'s single-reply mode for an immediate follow-up draft;
over 24h still delegates to `/draft-reply` but flags the window as
"likely passed, lower priority." **This workflow never reimplements reply
drafting — it always calls `/draft-reply`,** which itself never
auto-posts. The updated `## Logged Replies` table is written back after
every run so the next diff only reports genuinely new activity.

**Workflow 2 — audience pull (`/monitor-engagement audience
<post-url-or-id>`).** Pulls a post's likers/commenters — pasted by the
user, per §27, never fetched live — and classifies each by ICP fit using
a three-way rubric, applied to whatever job title/headline text the user
actually pasted and always offered as a suggestion the user can correct,
never asserted as settled fact:
- **Peer** — an individual-contributor/similar-seniority title in
  AI/ML/data/engineering, doing comparable work.
- **Aspirational** — a senior/leadership title (Director, VP, Head of,
  Principal, Founder) or a recognizable figure the user doesn't already
  have a peer relationship with.
- **Prospect** — a title with hiring/buying power relevant to the user
  (recruiter, hiring/engineering manager, founder hiring).

Before finalizing a classification, `Content-Learnings/icp-map.md` is
checked for that name; an existing mapping is reused rather than
re-guessed (surfaced to the user rather than silently trusted forever), and
any new or ambiguous name is confirmed with the user before being written.
Confirmed classifications are appended into `icp-map.md`'s `## Mappings`
table (`name | category | last_confirmed_date`) — a living doc, same
accumulation pattern as `hook-formulas.md`/`humanizer-rules.md`/
`algorithm-rules.md`/`comment-targets.md` — so a repeat account isn't
re-classified from scratch every time it shows up in a new post's list.
It ships empty and accumulates only from real `/monitor-engagement
audience` runs, never seeded with invented names. The full snapshot (all
names, not just newly classified ones) is also written into a new
`Engagement/<post-slug>--audience.md` note, created from a new
`_Templates/Engagement-Audience-Note.md` (frontmatter `id`,
`type: engagement-audience`, `post_url`, `captured_date`; body: one table
per ICP category — Peer / Aspirational / Prospect — with columns
`name | title_or_headline | notes`).

**Vault schema.** `scripts/validate_vault.py` gains a sixth
`Content-Learnings/` NoteSpec (`icp-map`, `permissive_folder=True`, same
minimal `id`/`type`/`version`/`last_updated` shape as the other five) and
two new NoteSpecs for the new `Engagement/` folder: `engagement-thread`
(required `id`/`type`/`post_url`/`my_comment_time`/`status`, status enum
`{watching, closed, placeholder}`) and `engagement-audience` (required
`id`/`type`/`post_url`/`captured_date`). `Engagement/` is
`permissive_folder=True` from day one, since — like `Content-Learnings/`
— it holds two note types sharing one folder from the start, and each
spec must let the other's `type` pass through unvalidated rather than
erroring on it.

**Hard rules.** Never fabricate a reply, liker, or commenter beyond what
the user actually pasted; never claim "no new replies" beyond what was
pasted this run; never auto-post anything — Workflow 1's drafting is
always delegated to `/draft-reply`, itself non-posting, and this skill
never posts a follow-up, a comment, or anything else itself; ICP labels
are always suggestions pending the user's confirmation, never settled
fact; no scraping, no session-cookie/unofficial API access, ever, per
§27.
