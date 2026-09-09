# AI-Powered LinkedIn Content Research & Growth Agent — Requirements

Status: **Draft — requirements captured, no implementation started.**
Owner: Priyanshu Arya
Last updated: 2026-09-09

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
