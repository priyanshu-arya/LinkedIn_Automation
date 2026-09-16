# ⚡ LinkedIn Agentic AI
### *A Human-Approved, Evidence-Gated LinkedIn Content Pipeline*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Obsidian Native](https://img.shields.io/badge/Knowledge%20Base-Obsidian-purple.svg)](https://obsidian.md/)
[![Buffer API](https://img.shields.io/badge/Scheduling-Buffer%20GraphQL-24a159.svg)](https://buffer.com/)
[![Architecture](https://img.shields.io/badge/Architecture-Prompt--Driven%20Skills-orange.svg)](#-system-architecture)
[![Status](https://img.shields.io/badge/Status-Active%20Development-success.svg)](#)

---

**LinkedIn Agentic AI** is an open-source content pipeline that automates the heavy lifting of creator workflows across LinkedIn, X (Twitter), and Substack — continuous trend discovery, primary-source fact verification, viral-potential scoring, visual briefing, scheduling/publishing, and closed-loop analytics learning — while keeping a human in charge of every publishing decision.

**What it actually is, precisely:** a set of single-responsibility [Claude Code skills](.claude/skills/) (prompt-driven instruction files, not independent processes) that a human triggers manually via slash commands, in sequence, within one session (or bundled through a per-platform `generate-week*` orchestrator). One shared research/idea pool feeds three platform-specific pipelines — LinkedIn (the original, most-verified pipeline), X (posts and threads via Buffer), and Substack (long-form Articles and short-form Notes, published manually since Substack has no scheduling API) — so a trending topic can become a LinkedIn post, an X thread, and a Substack article without being re-researched three times. There is no scheduler or daemon running unattended yet (see the [roadmap](#️-project-roadmap), Phase 14) — every run happens because someone typed a command. What it *is* strong on: it enforces **strict human-in-the-loop editorial gates**, **primary-source fact validation**, **anti-hallucination guardrails** (verify-or-drop sourcing, no fabricated metrics, no playbook rule written without real supporting evidence), and **pure Markdown/Obsidian long-term memory** — no vendor lock-in database. It evolves over time, using real engagement metrics to update per-platform **Content Playbooks**, once there's enough published-post data to do so honestly for that platform.

---

## 📑 Table of Contents

- [⚡ System Architecture](#-system-architecture)
- [✨ Core Capabilities](#-core-capabilities)
- [🛡️ Quality, Safety & Anti-Hallucination Guardrails](#️-quality-safety--anti-hallucination-guardrails)
- [📂 Repository & Vault Structure](#-repository--vault-structure)
- [🤖 Multi-Agent Skills Matrix](#-multi-agent-skills-matrix)
- [🎯 Personalization & User Preferences](#-personalization--user-preferences)
- [🚀 Quickstart & Setup](#-quickstart--setup)
- [🖥️ Connecting to Claude Desktop](#️-connecting-to-claude-desktop)
- [🔄 End-to-End Workflow Walkthrough](#-end-to-end-workflow-walkthrough)
- [📝 Knowledge Base & Note Schemas](#-knowledge-base--note-schemas)
- [📊 Scoring Rubrics](#-scoring-rubrics)
- [⚙️ Configuration & Customization](#️-configuration--customization)
- [🗺️ Project Roadmap](#️-project-roadmap)
- [🤝 Contributing](#-contributing)
- [📄 License & Authors](#-license--authors)

---

## ⚡ System Architecture

The engine operates on a closed feedback loop across two distinct cycles:
1. **The Production Pipeline (Outer Loop):** Discovers trends, verifies primary sources, plans weekly editorial calendars, drafts posts according to human-like voice guides, scores viral potential, creates visual briefs, requires human approval, and schedules to Buffer.
2. **The Growth & Learning Loop (Inner Loop):** Ingests post-publishing analytics from Buffer, detects performance patterns, and updates a centralized `playbook.md` that guides future generations.

```mermaid
flowchart TD
    subgraph Research & Ideation
        A[🌐 Web & Trend Scout] -->|WebSearch & Primary Fetch| B[(Content-Research/)]
        B -->|Unused Research| C[💡 Idea Engine / Ranker]
        C -->|Rank & Filter| D[(Post-Ideas/)]
    end

    subgraph Strategy & Creation
        D -->|Flexible 3-Post/Week Cadence| E[📅 Content Strategist]
        E -->|Selected Candidate| F[✍️ LinkedIn Writer]
        F -->|Voice Guide & Research Grounding| G[(Drafts/)]
        G -->|Accurate & Engaging Check| H[🔍 Quality / Critic Agent]
        H -->|Viral Score >= 6.0| I[🎨 Visual Agent]
        I -->|Visual Brief| J[(Visuals/)]
    end

    subgraph Editorial & Distribution
        H & J --> K{👤 Human Approval Manager}
        K -->|Approve| L[(Scheduled/)]
        K -->|Edit / Regenerate / Reject| F
        L -->|Buffer GraphQL API| M[📡 Buffer Queue]
        M -->|Published to LinkedIn| N[(Published-Posts/)]
    end

    subgraph Feedback & Evolution
        N -->|Buffer Metrics Pull| O[📈 Analytics Agent]
        O -->|Performance Snapshots| P[(Analytics/)]
        P -->|Evidence-Based Learning| Q[🧠 Growth Agent]
        Q -->|Update Rules| R[📘 Content Playbook]
        R -.->|Informs Strategy & Voice| E & F & H
    end
```

---

## ✨ Core Capabilities

- **🕵️ Primary-Source Grounding:** Queries live sources, fetches documentation and repository data directly, and verifies claims before saving research. Hallucinated benchmarks, invented statistics, and unsourced quotes are explicitly rejected. Fetched web content is always treated as data to extract facts from, never as instructions to follow.
- **🧠 11 Single-Responsibility Skills:** Modularity through separate, manually-triggered prompt skills (Trend Scout, Research Agent, Idea Ranker, Content Strategist, LinkedIn Writer, Visual Designer, Quality Critic, Approval Manager, Scheduler, Growth Agent, plus the `generate-week` weekly orchestrator that chains the others through isolated per-post subagents) — not independent autonomous agents; one session runs them sequentially on command.
- **🗃️ Obsidian-Native Vault:** Stored entirely in clean, readable Markdown with structured YAML frontmatter and bi-directional `[[wikilinks]]`. No vendor lock-in database.
- **🛡️ 100% Human Editorial Control:** Zero automatic publishing. Every single draft must pass through an interactive terminal/IDE approval interface supporting 7 decision paths (*Approve, Edit, Regenerate, Change Hook, Change Image, Change Time, Reject*).
- **📈 Self-Improving Playbook:** Learns from real audience data. The system extracts winning hook formats, optimal word lengths, high-resonance topics, and posting times into a versioned playbook.
- **🚫 Anti-AI Slop Voice Engine:** Built-in negative constraints preventing common LLM clichés ("*In today's fast-paced world...*", "*Let's dive in!*", emoji bullet stuffing, and generic rhetorical questions).
- **📡 Modern Buffer GraphQL Integration:** Directly integrates with Buffer's current GraphQL endpoints to maintain a rolling 2-day scheduling queue.

---

## 🛡️ Quality, Safety & Anti-Hallucination Guardrails

| Requirement | Guardrail Mechanism | Enforced By |
| :--- | :--- | :--- |
| **No Hallucinated Data** | Compulsory `WebFetch` verification against primary sources (docs, repos, papers). Unverifiable claims are stripped. | `research-topic`, `critique-draft` |
| **No Unapproved Posts** | `status: approved` can *only* be set by the human approval skill. Downstream schedulers abort if unapproved. | `review-drafts`, `schedule-approved` |
| **Opinion vs. Fact Separation** | Subjective viewpoints and analyses are explicitly framed as opinions; technical specifications must cite sources. | `write-draft`, `COST-AND-SAFETY.md` |
| **Anti-Fatigue / Dedup** | Compares candidate ideas against all published and drafted notes across 90 days before generating new assets. | `generate-ideas`, `critique-draft` |
| **No Spurious Metrics** | Missing or lagging Buffer analytics are marked `null`/`unavailable`, never defaulted to 0 or estimated. | `pull-analytics` |
| **Evidence-Based Playbook** | Requires $\ge 3$ verified post samples before writing any performance rule to `playbook.md`. | `update-playbook` |

---

## 📂 Repository & Vault Structure

```text
LinkedIn_Automation/
├── .claude/
│   └── skills/                       # Executable Multi-Agent Skills
│       ├── research-topic/           # Trend discovery & deep verification (shared, all platforms)
│       ├── generate-ideas/           # Candidate generation & ranking (shared, all platforms)
│       ├── plan-week/                # LinkedIn: flexible, quality-gated weekly calendar
│       ├── write-draft/              # LinkedIn: human-like post drafting
│       ├── critique-draft/           # LinkedIn: fact check & 8-factor viral scoring
│       ├── generate-visual/          # Visual brief generator (LinkedIn/X/Substack Notes)
│       ├── review-drafts/            # Interactive approval CLI (shared, all platforms)
│       ├── schedule-approved/        # LinkedIn: Buffer GraphQL queue manager
│       ├── pull-analytics/           # LinkedIn: post metrics collector
│       ├── update-playbook/          # Self-improving playbook engine (platform-scoped)
│       ├── generate-week/            # LinkedIn weekly orchestrator (per-post subagents)
│       ├── plan-week-x/              # X: weekly calendar (~5/week, singles + threads)
│       ├── write-draft-x/            # X: post/thread drafting
│       ├── critique-draft-x/         # X: fact check & viral scoring
│       ├── schedule-approved-x/      # X: Buffer GraphQL queue manager
│       ├── pull-analytics-x/         # X: post metrics collector
│       ├── generate-week-x/          # X weekly orchestrator
│       ├── plan-week-substack-article/    # Substack Articles: weekly calendar (1/week)
│       ├── write-draft-substack-article/  # Substack: long-form article drafting
│       ├── critique-draft-substack-article/ # Substack: depth/structure/SEO scoring
│       ├── generate-visual-substack-article/ # Substack: multi-image brief generator
│       ├── plan-week-substack-note/       # Substack Notes: weekly calendar (~3/week)
│       ├── write-draft-substack-note/     # Substack: short-form Note drafting
│       ├── critique-draft-substack-note/  # Substack: fact check & viral scoring
│       ├── publish-substack/         # Substack: manual publish handoff (no API)
│       └── generate-week-substack/   # Substack weekly orchestrator (article + Notes)
│
├── Content-Research/                 # Long-Term Research Memory (15 pillars)
│   ├── AI/                           # Artificial Intelligence fundamentals
│   ├── GenAI/                        # LLMs, Diffusion, Prompting
│   ├── Machine-Learning/             # Classical ML
│   ├── Deep-Learning/                # Neural nets, architectures, training
│   ├── Mathematics/                  # Maths related to data (linear algebra, stats, calculus)
│   ├── Developer-Tools/              # Frameworks, SDKs, Dev productivity
│   ├── Data-Analytics/               # BI, analytics tooling, dashboards
│   ├── Data-Engineering/             # Pipelines, warehousing, streaming
│   ├── Problem-Solving/              # Problem-solving approaches & frameworks
│   ├── Algorithms/                   # DSA, complexity, algorithm design
│   ├── Psychology-AI/                # Human-AI interaction, cognition
│   ├── Research-Papers/              # ArXiv breakdowns & summaries
│   ├── Interview-Preparation/        # System design, coding, ML interviews
│   ├── Career/                       # Tech career growth, portfolio, leadership
│   ├── AI-Healthcare/                # AI applied to healthcare/medicine
│   └── Resources/                    # Curated lists, roadmaps, cheat sheets
│
├── Post-Ideas/                       # Scored & Ranked Idea Pipeline, all platforms  *(gitignored)*
├── Drafts/                           # Drafts awaiting critique/review — LinkedIn, X,
│                                      #   Substack Notes (Draft-Note), and Substack
│                                      #   Articles (Substack-Article-Note) share this
│                                      #   folder, routed by `type`               *(gitignored)*
├── Visuals/                          # High-context visual design briefs        *(gitignored)*
├── Scheduled/                        # Approved LinkedIn/X posts in Buffer queue *(gitignored)*
├── Substack-Ready/                   # Approved Substack items awaiting manual
│                                      #   publish — no Buffer, no API           *(gitignored)*
├── Published-Posts/                  # Live posts, all platforms                *(gitignored)*
├── Analytics/                        # Append-only engagement snapshots         *(gitignored)*
├── Content-Learnings/                # Living Strategy Vault, per platform
│   ├── playbook.md                   # LinkedIn: learned rules & audience insights
│   ├── playbook-x.md                 # X: learned rules (separate evidence trail)
│   ├── playbook-substack.md          # Substack: learned rules (Articles + Notes)
│   ├── voice-guide.md                # LinkedIn: writing tone, style & anti-patterns
│   ├── voice-guide-x.md              # X: terser, more opinionated voice
│   ├── voice-guide-substack.md       # Substack: essay-form (Articles) + casual (Notes)
│   └── content-index.md              # Fast dedup/fatigue index, all platforms *(gitignored)*
│
├── Profile-Optimization/             # Profile rewrite + audit reports (personal output) *(gitignored)*
│
├── _Templates/                       # Strict YAML frontmatter note templates
│   ├── Research-Note.md
│   ├── Idea-Note.md
│   ├── Draft-Note.md
│   ├── Visual-Brief-Note.md
│   ├── Scheduled-Published-Note.md
│   ├── Substack-Article-Note.md
│   ├── Substack-Ready-Note.md
│   ├── Analytics-Record.md
│   ├── Playbook-Note.md
│   └── Profile-Optimization-Note.md
│
├── REQUIREMENTS.md                   # Product specification & vision
├── Profile-Optimization-Spec.md      # Spec for the standalone Profile Optimization Agent
├── COST-AND-SAFETY.md                # Cost & safety hardening audit
├── LICENSE                           # MIT License
└── README.md                         # Project documentation
```

> **What's actually in git:** only code, skills, templates, and specs are tracked.
> Everything the pipeline *generates* at runtime (`Content-Research/`, `Post-Ideas/`,
> `Drafts/`, `Visuals/`, `Scheduled/`, `Substack-Ready/`, `Analytics/`,
> `Published-Posts/`, `Content-Learnings/content-index.md`,
> `Profile-Optimization/`) is real, working state on disk but is gitignored —
> it's personal content, not the codebase. Internal working logs
> (`DECISIONS.md`, `SKILLS.md`, `PROMPTS.md`) are likewise local-only and not
> part of the public repo.

---

## 🤖 Multi-Agent Skills Matrix

All skills are implemented as Claude Code / Antigravity Agent skills located in `.claude/skills/`:

| Command / Skill | Role | Description | Trigger |
| :--- | :--- | :--- | :--- |
| `/research-topic <domain> [count]` | **Trend Scout & Researcher** | Discovers trending tech, fetches primary sources, verifies claims, outputs scored research notes. | Manual / On Demand |
| `/generate-ideas [domain] [count]` | **Idea Engine** | Scans unused research, performs deduplication, generates structured angles and hooks, outputs ranked Idea Notes. | Weekly / On Demand |
| `/plan-week [YYYY-Www]` | **Content Strategist** | Assigns candidate ideas to specific days under a flexible, quality-gated cadence (default 3/week, Tue/Thu/Sat starting heuristic) — never pads the count to hit a quota. | Start of Week |
| `/generate-week [YYYY-Www] [count]` | **Weekly Orchestrator** | Runs the whole pipeline for the week in one invocation: plans angles, then generates each post through its own isolated subagent (independent research, draft, critique, visual prompt), checks each against the week's history, then one combined review + scheduling pass. | Weekly, one-shot |
| `/write-draft [idea-id]` | **LinkedIn Writer** | Converts selected ideas into high-engagement, scannable post copy grounded in research and adhering to `voice-guide.md`. | After Planning |
| `/critique-draft [draft-id]` | **Critic & Viral Gate** | Re-verifies facts, checks fatigue, scores 0–10 Viral Potential, auto-refines weak drafts, moves to `in_review`. | Post-Drafting |
| `/generate-visual [draft-id]` | **Visual Agent** | Formulates layout, color palette, visual hierarchy, and copy for accompanying diagram/infographic briefs. | Post-Critique |
| `/review-drafts [draft-id]` | **Approval Manager** | Presents draft + visual brief to the user for explicit decision (*Approve, Edit, Regenerate, Change Hook, Reject*). | User Review |
| `/schedule-approved [draft-id]` | **Scheduler Agent** | Verifies approval, validates date, pushes to Buffer via GraphQL API, manages rolling 2-day queue. | Post-Approval |
| `/pull-analytics` | **Analytics Agent** | Ingests impressions, reactions, comments, shares, and clicks from Buffer into append-only Markdown tables. | Daily / Weekly |
| `/update-playbook [platform]` | **Growth Agent** | Compares high vs. low performing posts, discovers statistical patterns, and updates the matching platform's playbook (`playbook.md` / `playbook-x.md` / `playbook-substack.md`; default `linkedin`). | Weekly / Monthly |

`/research-topic`, `/generate-ideas`, and `/review-drafts` are shared across
every platform below — one research/idea pool, one approval gate.

### X (Twitter) pipeline

| Command / Skill | Role | Description | Trigger |
| :--- | :--- | :--- | :--- |
| `/plan-week-x [YYYY-Www] [count]` | **Content Strategist (X)** | Assigns candidate ideas tagged for X to specific days, default ~5/week — quality gates the count, same as LinkedIn. | Start of Week |
| `/write-draft-x [idea-id]` | **X Writer** | Decides single-post vs. thread from the idea's depth, drafts in `voice-guide-x.md`'s terser voice. | After Planning |
| `/critique-draft-x [draft-id]` | **Critic & Viral Gate (X)** | Same rubric shape as LinkedIn's critic, plus a thread-cohesion factor for multi-tweet drafts. | Post-Drafting |
| `/schedule-approved-x [draft-id]` | **Scheduler Agent (X)** | Same proven Buffer GraphQL mutation, new X channel id; thread posting requires live schema confirmation before first use. | Post-Approval |
| `/pull-analytics-x` | **Analytics Agent (X)** | Same Buffer metrics pull, scoped to the X channel. | Daily / Weekly |
| `/generate-week-x [YYYY-Www] [count]` | **Weekly Orchestrator (X)** | Same per-post-subagent isolation pattern as `/generate-week`, ending in one shared review pass and `/schedule-approved-x`. | Weekly, one-shot |

### Substack pipeline (Articles + Notes)

Substack has no Buffer channel and no supported public posting API, so this
pipeline ends at a manual, human-confirmed publish step instead of an
automated schedule — see `/publish-substack` below.

| Command / Skill | Role | Description | Trigger |
| :--- | :--- | :--- | :--- |
| `/plan-week-substack-article [YYYY-Www]` | **Content Strategist (Articles)** | Picks at most one idea/week deep enough to earn full long-form treatment — an honest "nothing qualifies" is a valid outcome. | Start of Week |
| `/write-draft-substack-article [idea-id]` | **Substack Writer (Articles)** | Long-form writer: title/subtitle/sectioned body, no character ceiling, depth over hook-brevity, per `voice-guide-substack.md`. | After Planning |
| `/critique-draft-substack-article [draft-id]` | **Critic (Articles)** | Depth/structure/SEO-weighted rubric, not a scroll-stopping-hook gate. | Post-Drafting |
| `/generate-visual-substack-article [draft-id]` | **Visual Agent (Articles)** | Multi-image variant — one brief per `[IMAGE: ...]` marker in the article body. | Post-Critique |
| `/plan-week-substack-note [YYYY-Www] [count]` | **Content Strategist (Notes)** | Assigns candidate ideas tagged for Substack Notes, default ~3/week. | Start of Week |
| `/write-draft-substack-note [idea-id]` | **Substack Writer (Notes)** | Short-form, casual voice — reuses X's short-post shape, no hashtags. | After Planning |
| `/critique-draft-substack-note [draft-id]` | **Critic (Notes)** | Same rubric shape as `/critique-draft-x`, no thread concept. | Post-Drafting |
| `/publish-substack [note-id]` | **Manual Publish Handoff** | Produces a copy-ready `Substack-Ready/` note; only marks `published` once the user explicitly confirms they posted it themselves — never assumed. | Post-Approval |
| `/generate-week-substack [YYYY-Www]` | **Weekly Orchestrator (Substack)** | Plans + generates the week's article and Notes, one combined review pass, hands approved items to `/publish-substack`. | Weekly, one-shot |

### Profile Optimization Agent (separate module)

`/optimize-profile [pdf-path]` — not part of the posting pipeline above. Takes
a LinkedIn Profile PDF export plus **exactly two target job descriptions** and
produces a complete, evidence-only, keyword-optimized, copy-ready rewrite of
the entire profile (headline, About, experience, skills, projects, Featured,
etc.), plus a full audit (current vs. projected 100-point score,
role-alignment scores, keyword strategy, priority plan). The finished profile
leads the output note; the audit is a collapsed appendix underneath it, not
the headline deliverable. One-off/periodic trigger, not a recurring cadence.

Never silently drops an empty or thin section just because the PDF didn't
have anything for it — every gap and empty section is put to the user with a
real choice: supply the real content, ask the agent to draft 2-4 concrete
suggestions (clearly labeled unconfirmed until the user says they're actually
true), or explicitly skip it. Every resolution is logged in the note's Gap
Resolution Log, so nothing disappears quietly.

Full spec: [`Profile-Optimization-Spec.md`](Profile-Optimization-Spec.md).
Output written to `Profile-Optimization/` using
`_Templates/Profile-Optimization-Note.md`. Same anti-hallucination discipline
as the rest of this repo: every claim in the rewrite traces to an evidence
ledger built from the PDF, and a suggestion the agent drafts to fill a gap is
never treated as a fact until the user confirms it applies to them.

---

## 🎯 Personalization & User Preferences

Everything below is Priyanshu's own configuration of the pipeline — not generic defaults. Full detail always lives in the linked source file; this section is the one-stop summary so nothing has to be re-derived from `DECISIONS.md`.

### Weekly cadence

- **Default 3 posts/week**, not 5 — deliberately dropped from an earlier 5/week Mon–Fri plan. Rationale (user's own words, [DECISIONS.md](DECISIONS.md#phase-13-decisions)): a daily-feeling Mon–Fri cadence risks looking like content produced "just to post," which undermines the goal of genuinely valuable posts.
- **Starting-heuristic days: Tue / Thu / Sat.** This is a provisional default, not a fixed schedule — it's replaced automatically once `Content-Learnings/playbook.md` has real evidence (≥3 published posts) on which days actually perform. Saturday is in scope; **Sunday is excluded by default.**
- **Quality gates the count — a hard rule.** Never generate or schedule a post just to hit 3/week. If the week only supports 1–2 genuinely distinct, valuable angles, ship that many and say so plainly. A manufactured/padded post is never preferred over an honest gap.
- Content-type variety must span **≥2 distinct categories** across the week's chosen angles, checked against the Playbook's evidenced patterns first, this rule second — not pinned to specific calendar days.
- Full spec: [REQUIREMENTS.md §5](REQUIREMENTS.md#5-weekly-cadence).

### Posting-time defaults

Research-backed generic LinkedIn best-times (aggregated from Buffer's and Sprout Social's 2026 studies), used only until this account's own analytics override them. All times are local (IST) — no timezone conversion needed.

| Day | Default time | Notes |
| :--- | :--- | :--- |
| Monday | 13:00 | |
| Tuesday | 16:00 | strong window 11:00–17:00 |
| Wednesday | 16:00 | single strongest slot across all studies |
| Thursday | 17:00 | strong window 11:00, 13:00–17:00 |
| Friday | 15:00 | |
| Saturday | 09:00 | weekend engagement is weak platform-wide; morning outperforms evening |
| Sunday | — | excluded from default cadence |

For the default Tue/Thu/Sat cadence this collapses to **Tue 16:00 / Thu 17:00 / Sat 09:00**. This table is an unvalidated starting heuristic, not derived from real account performance — `/schedule-approved` says so rather than presenting it as optimized — and is superseded automatically once the Playbook has ≥3 published posts' worth of day+time evidence. Full spec: [REQUIREMENTS.md §11](REQUIREMENTS.md#11-posting-time-optimization).

### Content pillars (closed set of 15)

AI, Tech Career, Developer Tools, GenAI, Machine Learning, Deep Learning, Interview Prep, Data Analytics, Data Engineering, Maths Related to Data, Problem Solving, Algorithms, Research (papers), Psychology + AI, AI in Healthcare — plus a cross-cutting Resources folder. This bounds *what the account is about*; it never supplies the specific topic — every research cycle starts from a live, real-time scan within a pillar, never a hardcoded or "Top 10 Trends"-style topic. Default `/research-topic` mode scans **across all pillars** rather than one at a time, so trend strength decides coverage, not the caller.

**Research pillar, specifically:** built from real, verified papers (arXiv, ACM/IEEE, lab publications) — the paper must actually be read, not just its press summary, then explained as the author's own plain-language take (what it found, why it matters, a real-life example). Linking the source paper is optional per post, used sometimes not every time; a paper/finding/citation is never fabricated.

### Voice & writing rules

Condensed from [Content-Learnings/voice-guide.md](Content-Learnings/voice-guide.md) — the living source of truth, updated once real approved/edited posts exist to learn from (currently still the default, unseeded guide):

- **Hook:** a specific, concrete claim or tension, never a generic "Ever wondered how X works?" question. No throat-clearing — the first line stands alone.
- **Structure:** hook → useful content in short scannable paragraphs/tight lists → a discussion question only when the content genuinely raises one.
- **Length:** default ~1,200–1,500 characters, comfortably under LinkedIn's ~3,000 limit, unless the material genuinely needs more (e.g. a step-by-step tutorial).
- **Tone:** conversational and direct, like explaining to a smart peer — not a press release, not a motivational poster. Technically accurate over impressive-sounding; states uncertainty plainly rather than asserting confidently.
- **Banned AI-writing tells:** "In today's fast-paced world...", "Let's dive in", "Imagine a world where...", rhetorical-question hooks, emoji stacked as bullet substitutes, generic CTAs with no real question attached, em-dash overuse, hedging every sentence.
- **Hashtags:** 3–5 per post, directly tied to topic/category — never stuffed or generic filler.
- **Emoji:** sparing — fine as one occasional visual anchor, not a formatting crutch throughout.

### Generation & orchestration preferences

- **Per-post isolation via real subagents**, not a shared session — `/generate-week` spawns one fresh `Agent`-tool subagent per post, sequentially (not in parallel, so each post can see what earlier posts this week already covered), each following the real skill files directly rather than duplicated logic.
- **Duplicate detection is two-tier:** a *genuine* duplicate (same underlying story/example/hook/conclusion) auto-rejects before reaching human review; a stylistically-similar-but-substantively-distinct post only lowers the Originality sub-score, left for the human to weigh at `/review-drafts`. Retry cap of 2 re-angling attempts per slot before it's reported honestly unfillable.
- **Visuals stay prompt-only.** The deliverable is a finished ChatGPT-Images prompt, never a rendered file or a live image-generation API call — this is a deliberate, twice-confirmed choice, not a missing feature.
- **Scheduling stays text-only** — Buffer's mutation carries no media field; images are pasted in manually after being generated from the prompt.

### X and Substack cadence (multi-platform expansion, 2026-09-14)

- **One shared research/idea pool feeds all three platforms** — an Idea Note's `platforms: []` field marks which platforms it's eligible for; each platform drafts its own version independently (never a copy-paste of another platform's draft), and a `platform_schedule: []` field lets one idea carry a different assigned date per platform without disturbing LinkedIn's own `target_week`/`target_date` fields.
- **X: ~5/week**, mix of single posts and threads decided per-idea by `/write-draft-x` from the idea's actual depth — not a fixed singles/threads split. Same quality-gates-the-count hard rule as LinkedIn.
- **Substack: 1 Article/week + ~3 Notes/week.** Articles are long-form (title/subtitle/sectioned body, no character ceiling) and only get written for ideas that genuinely earn the depth — an empty Article slot in a given week is a correct, honest outcome, not a shortfall.
- **Substack publishing is manual by design, not a missing feature.** Buffer has no Substack channel and Substack has no supported public posting API — an unofficial, session-cookie-based API was explicitly considered and rejected for the ToS/reliability risk. `/publish-substack` produces a copy-ready `Substack-Ready/` note and only marks something `published` once the user explicitly confirms they posted it themselves.
- **X's Buffer thread-posting mutation shape is explicitly unverified** until the first real thread is scheduled — `/schedule-approved-x` is written to confirm it live against Buffer's actual schema/error responses rather than guess, the same discipline that caught the original LinkedIn scheduler's `channelId` type correction.
- **Each platform earns its own playbook and voice guide** (`playbook-x.md`/`voice-guide-x.md`, `playbook-substack.md`/`voice-guide-substack.md`) — a pattern proven on LinkedIn is never assumed to transfer to X or Substack's different audiences and formats.
- Full rationale and the four architecture questions resolved with the user before any of this was built: [DECISIONS.md — Multi-Platform Expansion (X + Substack) decisions](DECISIONS.md#multi-platform-expansion-x--substack-decisions).

### Profile Optimization preferences (separate module)

`/optimize-profile` evolved through two rounds of direct user feedback — both now baked into [`.claude/skills/optimize-profile/SKILL.md`](.claude/skills/optimize-profile/SKILL.md) and [Profile-Optimization-Spec.md](Profile-Optimization-Spec.md) as permanent defaults, not one-off requests:

- **Profile-first output, not a diagnostic report.** The finished, copy-ready profile leads the note immediately after frontmatter, followed by a ≤10-line summary. The full audit still exists in full, just collapsed under an "Appendix: Full Diagnostic Report" heading underneath.
- **Never silently drop a thin/empty section.** Every gap is put to the user as a real choice — supply the real content, ask the agent to draft 2–4 concrete labeled-unconfirmed suggestions, or explicitly skip it. Every resolution is logged in the note's Gap Resolution Log.
- **Seniority-calibrated language.** Compute years of experience from the evidence ledger and match scope/language to the correct rung — not a senior-profile ceiling applied to an early/mid-career profile.
- **Anti-clutter caps:** headline ≤3–4 segments, Skills led by ~10–20 core items, `[CONFIRM]`/`[ADD EVIDENCE]` brackets minimized in the copy-ready block (extended explanation moves to Gaps instead).
- **Coherence pass:** Headline → About → Experience → Skills → Projects must reinforce one identity/keyword set, not read as independently-optimized fragments.
- **SEO rule:** 2–3 natural mentions per primary keyword across assigned sections — precise, not vague "don't stuff" guidance.
- **Research current best practice live**, not solely the originally-supplied research document — e.g. LinkedIn's official 100-skills cap and field-truncation lengths were confirmed directly against LinkedIn's own Help pages, kept in a separate provenance-tracked section ([Profile-Optimization-Spec.md §16.1](Profile-Optimization-Spec.md)) from industry-aggregated (non-LinkedIn-confirmed) claims.
- Same anti-hallucination discipline as the rest of the repo applies here too: every claim traces to the evidence ledger, and any agent-drafted suggestion stays unconfirmed until the user says it's true.

---

## 🚀 Quickstart & Setup

### 1. Clone & Open Workspace
```bash
git clone https://github.com/priyanshu-arya/LinkedIn_Automation.git
cd LinkedIn_Automation
```

### 2. Environment Configuration
Create a `.env` file in the root directory:
```env
# Buffer GraphQL API Credentials
BUFFER_ACCESS_TOKEN=your_buffer_access_token_here
BUFFER_CHANNEL_ID=your_linkedin_channel_id_here

# Optional: Push Notification webhooks
NOTIFICATION_WEBHOOK_URL=https://your-webhook-endpoint.com
```

> **How to obtain Buffer credentials:**
> 1. Head to [Buffer Developer Portal](https://buffer.com/developers).
> 2. Create an Access Token.
> 3. Use `/schedule-approved` or Buffer's GraphQL Explorer (`query { account { organizations { channels { id name service } } } }`) to retrieve your target LinkedIn channel ID.

### 3. Open in Obsidian (Optional but Recommended)
Open the `LinkedIn_Automation` directory as an Obsidian Vault to enjoy graphical relationship visualizers, backlink panels, and Kanban-style pipeline tracking.

---

## 🖥️ Connecting to Claude Desktop

This project was built and is designed to run as a **Claude Code** project — the
skills lean on Claude Code's native `Bash`, `WebSearch`/`WebFetch`, and
whole-directory file read/write to operate on the vault, run
`scripts/validate_vault.py`, and call Buffer's GraphQL API. Claude Desktop
doesn't have those tools by default, so a couple of things need to be wired up
before the skills behave the same way there:

1. **Enable Skills.** In Claude Desktop, go to **Settings → Capabilities**
   and turn on **Skills**. Skills are uploaded as `.zip` files, one per skill —
   zip each folder under [`.claude/skills/`](.claude/skills/) (each one must
   contain its `SKILL.md` at the zip root) and add it via **Add skill**. This
   gives Desktop the same prompt-level instructions Claude Code loads
   automatically as slash commands.
2. **Give Desktop filesystem access to the vault.** Skills read and write
   Markdown notes across `Content-Research/`, `Post-Ideas/`, `Drafts/`, etc.
   Desktop has no native folder mount, so connect the official filesystem MCP
   server pointed at this repo's path (**Settings → Developer/Connectors →
   Add custom connector**, running
   `npx -y @modelcontextprotocol/server-filesystem "/path/to/LinkedIn_Automation"`).
   Without this, Desktop can *talk about* the skills but can't actually read
   or update your notes.
3. **Enable Web Search.** `/research-topic` and `/generate-visual` depend on
   live web search/fetch to verify primary sources. Turn on Desktop's built-in
   **Web search** capability in the same Settings page.
4. **Buffer scheduling stays Claude-Code-side.** `/schedule-approved` and
   `/pull-analytics` make authenticated calls to Buffer's GraphQL API using
   `BUFFER_ACCESS_TOKEN`. Desktop has no built-in HTTP/fetch tool for this —
   either keep running those two skills from Claude Code, or wrap Buffer's API
   in your own small MCP server and connect it the same way as step 2.

In short: Desktop can review/ideate against the vault once the filesystem MCP
server and web search are connected, but the full pipeline — including
scheduling — is exercised in Claude Code, where it was verified end-to-end
(see the [roadmap](#️-project-roadmap)). Menu names and the exact Skills upload
flow may shift as Anthropic ships Desktop updates — check **Settings →
Capabilities** for the current wording if a step above doesn't match what you
see.

---

## 🔄 End-to-End Workflow Walkthrough

Follow this standard weekly lifecycle:

```bash
# Step 1: Discover & verify 3 topics in Developer Tools
/research-topic Developer-Tools 3

# Step 2: Generate ranked content ideas from verified research
/generate-ideas Developer-Tools 5

# Step 3: Plan this week's slots (default 3/week: Tue/Thu/Sat starting heuristic)
/plan-week 2026-W38

# — or skip steps 1-3 (and most of 4-8) and run the whole week in one go:
# /generate-week 2026-W38

# Step 4: Write draft for a selected idea
/write-draft 2026-09-16--crewai-crews-vs-flows

# Step 5: Critique accuracy & evaluate viral potential score
/critique-draft 2026-09-16--crewai-crews-vs-flows

# Step 6: Generate supporting infographic / visual brief
/generate-visual 2026-09-16--crewai-crews-vs-flows

# Step 7: Review draft and approve
/review-drafts 2026-09-16--crewai-crews-vs-flows

# Step 8: Push approved post to Buffer queue
/schedule-approved 2026-09-16--crewai-crews-vs-flows

# Step 9: Pull performance analytics (run post-publishing)
/pull-analytics

# Step 10: Update the strategy playbook based on audience data
/update-playbook
```

---

## 📝 Knowledge Base & Note Schemas

Every asset in the vault follows a deterministic schema. All cross-note links use dual-indexing: plain string IDs in YAML for machine parsing, and `[[wikilinks]]` in the markdown body for Obsidian graphs.

### Example Note Types

```yaml
# 1. Research Note (Content-Research/.../*.md)
---
id: 2026-09-09--crewai-multi-agent-orchestration
type: research
category: Developer-Tools
trend_score: 8.5
status: used # new | used | archived
sources:
  - title: CrewAI Official Documentation
    url: https://docs.crewai.com
    type: official-docs
    confidence: high
---
```

```yaml
# 2. Idea Note (Post-Ideas/*.md)
---
id: 2026-09-09--crewai-crews-vs-flows
type: idea
category: Developer-Tools
rank_score: 8.0
status: drafted # candidate | selected | drafted | rejected
research_ids:
  - 2026-09-09--crewai-multi-agent-orchestration
---
```

```yaml
# 3. Draft Note (Drafts/*.md)
---
id: 2026-09-16--crewai-crews-vs-flows
type: draft
category: Developer-Tools
status: approved # drafted | in_review | approved | rejected
viral_potential_score: 7.25
char_count: 1451
target_date: 2026-09-16
preferred_time: "08:30"
---
```

---

## 📊 Scoring Rubrics

### Research Scoring (0–10 Rubric)
Every researched topic is evaluated on 7 weighted criteria:
1. **Trend Velocity:** Is search and discussion momentum accelerating?
2. **Relevance:** Does it directly impact engineers, data scientists, and technical leaders?
3. **Freshness:** Is there a recent release, milestone, or discovery?
4. **Authority:** Can assertions be verified with primary sources?
5. **Engagement Potential:** Does it spark professional discussion or debate?
6. **Originality:** Can we offer a novel angle rather than repeating common commentary?
7. **Educational Value:** Will the reader learn a concrete, actionable concept?

### Viral Potential Score (Pre-Publishing Quality Gate)
The `/critique-draft` agent scores drafts across 8 dimensions. Drafts scoring **< 6.0/10** are automatically refined before human presentation:
- **Hook Strength (0–10):** Stops the feed scroll in the first 2 lines; avoids throat-clearing.
- **Scannability (0–10):** Short paragraphs, white space, clean list formatting.
- **Novelty / Insight (0–10):** Delivers fresh insights beyond basic regurgitation.
- **Discussion Catalysis (0–10):** Compelling, non-generic CTA that invites practitioner thoughts.
- **Technical Accuracy (0–10):** Flawless consistency with linked primary research.
- **Emotional / Professional Resonance (0–10):** Addresses real workplace challenges and curiosity.
- **Visual Alignment (0–10):** Visual brief complements rather than duplicates the text.
- **Historical Playbook Alignment (0–10):** Complies with proven rules in `playbook.md`.

---

## ⚙️ Configuration & Customization

### Adapting Personal Voice
Edit [Content-Learnings/voice-guide.md](Content-Learnings/voice-guide.md) to customize:
- **Tone Boundaries:** Set preferred formality, technical depth, and cadence.
- **Banned Phrases:** Expand the anti-AI cliché list.
- **Formatting Rules:** Configure standard post length (e.g., 1,200–1,600 characters) and hashtag limits (3–5 tags).

### Modifying Topic Domains
Add or remove research categories by creating directories under `Content-Research/` and updating the domain list in `REQUIREMENTS.md`.

### Validating the Vault
Run `python3 scripts/validate_vault.py` to check every note in `Content-Research/`, `Post-Ideas/`, `Drafts/`, `Visuals/`, `Scheduled/`, `Substack-Ready/`, `Published-Posts/`, and `Analytics/` against its template's required frontmatter fields. `Drafts/` and `Published-Posts/` each hold more than one note shape (e.g. plain drafts vs. Substack Articles) and are routed by the note's own `type` field rather than assumed from the folder. Flags missing/empty required fields, malformed `id`/date formats, invalid `platform`/`category` values, and placeholder notes that leaked a real (non-`placeholder`) status. No dependencies beyond Python 3's standard library. Not wired into a git hook yet — run it manually after bulk edits or before trusting a large batch of new notes.

Run `python3 scripts/test_validate_vault.py` to unit-test the validator itself (frontmatter parsing, per-field checks, and the multi-spec folder routing) against temp-file fixtures — safe to run anytime, never touches real vault notes.

---

## 🗺️ Project Roadmap

- [x] **Phase 1:** Obsidian Knowledge Vault Schema & Templates
- [x] **Phase 2:** Trend Scout & Fact-Grounded Research Pipeline
- [x] **Phase 3:** Idea Generation & Multi-Factor Ranking Engine
- [x] **Phase 4:** Content Strategy Calendar & Voice-Grounded Post Writer
- [x] **Phase 5:** Critic Agent & Viral Potential Scoring Gate
- [x] **Phase 6:** Visual Design & Infographic Brief Generator
- [x] **Phase 7:** Interactive Human Approval CLI
- [x] **Phase 8:** Buffer GraphQL Scheduler & Queue Manager — *verified against a real, live Buffer account on 2026-09-09; one real API-shape correction made and documented*
- [~] **Phase 9:** Analytics Ingestion & Performance Tracking — *built against Buffer's documented API shape, not yet exercised against a live account*
- [x] **Phase 10:** Closed-Loop Growth Agent & Content Playbook Evolution
- [x] **Phase 11:** Proactive Event Notifications (Queue depth, viral posts)
- [x] **Phase 12:** Cost & Safety Hardening Audit (`COST-AND-SAFETY.md`)
- [~] **Phase 13:** Multi-Platform Derivative Content Engine — *X (Twitter) posts/threads and Substack Articles/Notes built 2026-09-14, sharing one research/idea pool with LinkedIn; X's Buffer scheduling and thread-mutation shape not yet exercised against a live account, Substack publishing is manual by design (no API). Carousels and PDF slidedecks still not started.*
- [ ] **Phase 14:** Automated Cron / Daemon Mode for Headless Research & Queue Monitoring

---

## 🤝 Contributing

Contributions are welcome — new research source providers (arXiv, GitHub Trending,
Hacker News), refined agent prompts, additional skills, or improvements to the
scoring/validation logic.

### Ground rules

- **Read [REQUIREMENTS.md](REQUIREMENTS.md) first.** It's the source of truth for
  intended behavior — architectural context that isn't obvious from the code alone.
- **No fabricated content, ever.** This project's core value is anti-hallucination
  guardrails (verify-or-drop sourcing, no invented metrics, no playbook rule
  without real supporting evidence). Any change that weakens those guardrails
  (in a skill prompt, a scoring rubric, or validation logic) will be rejected.
- **Skills are plain Markdown, not code you compile.** Each skill lives at
  `.claude/skills/<name>/SKILL.md`. Keep the frontmatter (`name`, `description`)
  accurate — the description is what the agent uses to decide when to trigger
  the skill, so vague descriptions cause misfires.
- **Never commit generated or personal content.** `Content-Research/`, `Drafts/`,
  `Post-Ideas/`, `Visuals/`, `Scheduled/`, `Analytics/`, `Published-Posts/`, and
  `Profile-Optimization/` are gitignored on purpose (see [Repository & Vault
  Structure](#-repository--vault-structure)) — don't force-add them, and don't
  commit real API tokens (`.env` is gitignored; use `.env.example`-style
  placeholders in docs).
- **Validate before you open a PR.** Run `python3 scripts/validate_vault.py`
  if your change touches note schemas/templates.

### Workflow

1. **Fork the repository.**
2. **Create a feature branch:** `git checkout -b feature/amazing-feature`
3. **Make focused commits** with clear messages (`feat: add arxiv research
   provider`, `fix: correct viral-score weighting`).
4. **Push to your branch:** `git push origin feature/amazing-feature`
5. **Open a pull request** describing *what* changed and *why*, and which
   skill(s)/section(s) it touches. Link any related issue.

### Reporting issues

Open a GitHub issue with: what you expected, what happened instead, and
(if relevant) which skill/command triggered it. For anything that could be a
security issue (credential handling, prompt injection via fetched web
content), please don't open a public issue — contact the maintainer directly.

### Code of conduct

Be respectful and constructive in issues, PRs, and reviews. Disagree on
substance, not people.

---

## 📄 License & Authors

Distributed under the **MIT License**. See [LICENSE](LICENSE) for more details.

**Author:** [Priyanshu Arya](https://github.com/priyanshu-arya)

*Crafted with precision for technical creators, engineers, and AI researchers.*
