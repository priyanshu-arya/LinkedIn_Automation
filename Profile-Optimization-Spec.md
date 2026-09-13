**Product Requirements + Agent Workflow + Prompt Specification**

A single, implementation-ready specification for turning a current LinkedIn profile and two target roles into a recruiter-searchable, credible, human-convincing profile.

> **Core product promise**
> Do not merely "make the profile look good." Build a coherent professional identity that is discoverable by recruiters, clearly classified for the target market, rich in proof, and persuasive to hiring humans — without inventing facts or promising a guaranteed search rank.

| **Document status**                    | **Primary input**                                  | **Primary output**                                                    | **Optimization target**                               |
|-----------------------------------------|-----------------------------------------------------|--------------------------------------------------------------------------|-----------------------------------------------------------|
| Ready for product/agent implementation | 1 LinkedIn Profile PDF + 2 target job descriptions | Complete copy-ready LinkedIn profile + audit + keyword map + gap plan | Discovery + classification + credibility + conversion |

**Research basis.** This specification consolidates the user requirement and the supplied 2026 LinkedIn research document. The supplied research states that LinkedIn search is personalized, keyword stuffing is discouraged, standard job titles improve searchability, recruiter search can use skills/title/location/seniority and other filters, and profile optimization should combine discovery with evidence and conversion. *Source: supplied research document "Deep Research: How to Build a High-Performing, SEO-Friendly LinkedIn Technical & Management Profile."*

# Contents

1.  Product vision and non-negotiable principles
2.  Inputs and processing contract
3.  End-to-end agent workflow
4.  Target-role intelligence and keyword engine
5.  Evidence, credibility, and anti-hallucination system
6.  Complete LinkedIn section/field optimization framework
7.  Rewrite rules by profile section
8.  Technical / management / hybrid positioning logic
9.  Scoring and alignment model
10. Output package and copy-ready format
11. Agent system prompt
12. Structured output schema
13. QA and acceptance criteria
14. Common failure modes
15. 30–90 day maintenance loop
16. Research-derived evidence base

# 1. Product vision and non-negotiable principles

## 1.1 Product objective

The agent analyzes a user's existing LinkedIn profile against two target roles, determines the strongest market position, and produces a complete, ready-to-copy LinkedIn profile plus an audit explaining what changed and why.

## 1.2 The optimization model

DISCOVERY → CLASSIFICATION → CREDIBILITY → CONVERSION → ACTION

- Discovery: make the right recruiter able to find and filter for the profile using accurate role, skill, domain, location, seniority, and related terminology.
- Classification: make the professional identity immediately understandable — what role, specialty, domain, and level this person represents.
- Credibility: prove claims through outcomes, scale, architecture, teams, metrics, projects, publications, certifications, and social proof.
- Conversion: give a hiring manager enough clarity and evidence to want to speak with the candidate.
- Action: tell the user exactly what to change on LinkedIn, what evidence to add, and what to maintain over time.

> **Critical constraint**
> Never guarantee "top," "#1," or "always first" placement. The supplied research explicitly describes LinkedIn People Search as personalized and proprietary. The product can optimize relevance, discoverability, and conversion — not control the platform's ranking outcome.

## 1.3 Non-negotiable agent rules

- Never invent experience, metrics, company scope, technologies, certifications, degrees, awards, publications, responsibilities, leadership scope, or achievements.
- Never turn an unsupported inference into a factual claim. Mark it as "inferred," "recommended," or "needs user confirmation."
- Never keyword-stuff. Use natural semantic reinforcement across relevant sections.
- Prefer standard market job titles over creative titles when the standard title accurately represents the work.
- Optimize for one coherent primary market position, with secondary capabilities that support it.
- Preserve truth, chronology, seniority, and professional consistency across LinkedIn, resume, GitHub, portfolio, website, and publications when those sources are supplied.
- Use metrics whenever the source material supports them. When a metric is clearly valuable but missing, create a measurable-evidence request rather than inventing a number.
- Distinguish "search value" from "conversion value." Some sections primarily help discovery; others primarily prove credibility or convert profile visitors.
- Keep language human, specific, direct, and credible. Avoid buzzword clouds and generic claims.
- Never silently drop an empty or thin section. Every applicable section — populated, gap, or genuinely empty — gets resolved with the user per §5.5 before the rewrite is written: the user either supplies the real content, accepts an agent-drafted suggestion (explicitly confirming it's true of them before it becomes a fact), or explicitly says to skip it. "Not present in the PDF" is never itself a reason to omit a section from the conversation.
- A suggestion is not a fact. Content the agent drafts to help fill a gap (§5.5) stays labeled as a suggestion and must never appear in the copy-ready profile as a stated fact unless the user has explicitly confirmed it applies to them.

# 2. Inputs and processing contract

## 2.1 Required inputs

| **Input**                | **Required content**                                                   | **Agent use**                                                                                                              |
|---------------------------|---------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------|
| LinkedIn Profile PDF     | Current profile export or complete profile capture                     | Extract existing fields, dates, titles, skills, achievements, evidence, gaps, chronology, and current positioning.         |
| Target Job Role / JD #1  | Role title + responsibilities + requirements + skills; ideally full JD | Build role #1 target ontology, keyword priorities, capability requirements, seniority signals, and evidence expectations. |
| Target Job Role / JD #2  | Role title + responsibilities + requirements + skills; ideally full JD | Build role #2 target ontology and compare it against role #1 and the profile.                                            |

**Recommended optional inputs:** Resume/CV, GitHub, portfolio/website, job locations, target companies, target industries, preferred work model, achievements/metrics not captured in LinkedIn, publications, patents, certificates, and recruiter feedback.

## 2.2 Input normalization

PDF → profile fields → canonical facts → chronology → evidence ledger
JDs → role ontology → keyword taxonomy → must-have / preferred / negative signals
Profile × roles → gaps → positioning → rewrite → audit → QA

| **Normalized object** | **Examples**                                                 | **Required behavior**                                                              |
|-------------------------|----------------------------------------------------------------|---------------------------------------------------------------------------------------|
| Identity facts        | Name, location, current company                              | Treat as factual unless contradictory evidence exists.                             |
| Role facts             | Software Engineer, Engineering Manager, Director             | Prefer exact source wording; propose standardized alternatives only when accurate. |
| Technical facts       | Java, Python, AWS, Kafka, Kubernetes                         | Track skill + context + evidence.                                                  |
| Impact facts           | Latency reduction, cost reduction, scale, revenue, team size | Track numeric value, unit, period, scope, and source.                              |
| Leadership facts      | Hiring, mentoring, multi-team influence, organization size   | Map to seniority evidence.                                                         |
| Authority facts        | Patents, publications, talks, open source                    | Use as proof and authority; never overstate contribution.                          |
| Preferences            | Open to Work status, locations, job types                    | Recommend configuration; never silently change a user preference.                  |

# 3. End-to-end agent workflow

1. INGEST
2. EXTRACT
3. VERIFY
4. ANALYZE ROLE #1
5. ANALYZE ROLE #2
6. FIND OVERLAP / CONFLICTS
7. CHOOSE MARKET POSITION
8. BUILD KEYWORD MAP
9. SCORE CURRENT PROFILE
10. BUILD GAP MATRIX
11. REWRITE PROFILE
12. ADD EVIDENCE REQUESTS
13. SCORE PROJECTED PROFILE
14. RUN QA
15. GENERATE COPY-READY OUTPUT

## 3.1 Ingest
Accept the profile PDF and exactly two target roles. Confirm that the profile extraction includes all available LinkedIn sections and that the JDs are complete enough to analyze.

## 3.2 Extract
Parse name, headline, About, experience, education, skills, projects, Featured, credentials, recommendations, publications, patents, awards, languages, organizations, volunteer work, causes, services, career break, URL, contact details, location, industry, and any other fields visible in the input.

## 3.3 Verify
Create a fact ledger. Every rewritten claim must be traceable to a source fact or explicitly marked as user-confirmation-needed.

## 3.4 Analyze each role
Extract target title, seniority, technical skills, architecture concepts, domain, leadership requirements, business outcomes, tools, certifications, location/work model, and recruiter terminology.

## 3.5 Resolve overlap
Identify the shared skill/identity core across the two target roles. If the roles materially conflict, choose the most credible primary market position based on profile evidence and explain the trade-off.

## 3.6 Build keyword map
Score terms by role frequency, importance, evidence strength, placement suitability, and risk of sounding stuffed or irrelevant.

## 3.7 Audit current profile
Score discoverability, credibility, authority, leadership/business impact, conversion, and professionalism using the 100-point framework.

## 3.8 Rewrite
Rewrite every applicable field, prioritizing high-impact sections while also flagging sections that should remain unchanged or empty because adding them would not be truthful or useful.

## 3.9 Add evidence requests
For each missing high-value proof point, generate a concise prompt such as "What was the peak requests/second?" or "How many engineers did you mentor?"

## 3.10 Re-score
Estimate the projected score of the rewritten profile based only on evidence actually present or explicitly confirmed. Do not claim a score increase that depends on unverified additions.

## 3.11 QA
Check truthfulness, keyword stuffing, chronology, consistency, seniority fit, unsupported metrics, missing fields, duplicated skills, and copy-paste readiness.

## 3.12 Deliver
Produce: final profile, before/after changes, keyword strategy, job mapping, gaps, recommendations, scores, priorities, and maintenance actions.

# 4. Target-role intelligence and keyword engine

## 4.1 Role ontology

| **Bucket**          | **What to extract from each JD**                                                                                             |
|-----------------------|------------------------------------------------------------------------------------------------------------------------------|
| Role identity        | Target title, title variants, seniority, function, adjacent titles.                                                          |
| Core specialization  | Primary discipline and niche: backend, distributed systems, AI engineering, platform, engineering leadership, etc.           |
| Technical skills     | Languages, frameworks, cloud, databases, infrastructure, tooling.                                                            |
| Architecture          | System design, event-driven architecture, microservices, high availability, scalability, reliability, platform architecture. |
| Domain                | FinTech, SaaS, payments, AI infrastructure, security, healthcare, ecommerce, etc.                                            |
| Leadership             | Mentoring, hiring, team building, organizational design, stakeholder alignment, strategy.                                    |
| Business impact       | Revenue, cost, growth, delivery, product launch, reliability, customer outcomes.                                             |
| Credentials            | Degrees, certifications, patents, publications, security or cloud credentials.                                               |
| Operating model        | Location, remote/hybrid, workplace type, travel, working language.                                                           |
| Recruiter language    | Terms likely to appear in recruiter queries and structured filters.                                                          |

## 4.2 Keyword classes

| **Class**               | **Definition**                        | **Examples**                                          | **Placement approach**                                            |
|---------------------------|------------------------------------------|-----------------------------------------------------------|-------------------------------------------------------------------|
| Primary role keywords   | What the candidate should be found as | Staff Software Engineer, Principal Engineer           | Headline + current/recent Experience where truthful               |
| Specialization keywords | What the candidate is known for       | Distributed Systems, AI Infrastructure                | Headline + About + Experience + Skills                            |
| Technology keywords     | Technologies actually used            | Java, AWS, Kafka, Kubernetes                          | Experience + Skills; headline only for the strongest relevant set |
| Architecture keywords   | How the candidate builds              | System Design, Event-Driven Architecture, Scalability | About + Experience + Projects                                     |
| Domain keywords         | Business context                      | Payments, SaaS, FinTech                               | Experience + About + headline when central                        |
| Leadership keywords     | Scope and influence                   | Technical Strategy, Hiring, Mentoring                 | About + Experience + Skills                                       |
| Outcome keywords        | Value created                         | Latency, reliability, cost optimization, revenue      | Experience + project/case-study evidence                          |

## 4.2a Sourcing keywords beyond the two required JDs

The two target JDs (§2.1) remain the hard-required input for role analysis
and positioning — that contract doesn't change. But keyword *coverage* can
be strengthened cheaply: if the user has other real postings they're
targeting (even just a handful of links or pasted titles), ask if they want
to add them as supplementary keyword sources — extracting the terms that
recur across multiple real postings is stronger evidence of what recruiters
actually search than two JDs alone (§16.1). This is optional and never
blocks the run; it only widens the keyword map when offered.

A useful mix once the candidate keyword set is built: skew roughly 70%
specific/exact terms (the named technology, the named title) and 30%
broader category terms — specific terms convert better in search, broad
terms catch adjacent recruiter phrasing (§16.1).

## 4.3 Keyword priority score

```
keyword_score =
  0.30 * role_frequency
+ 0.25 * role_importance
+ 0.20 * candidate_evidence_strength
+ 0.15 * placement_fit
+ 0.10 * differentiation
- penalties_for_stuffing / irrelevance / ambiguity
```

This is an internal decision framework, not a claimed LinkedIn ranking formula. The supplied research explicitly warns that exact ranking weights are not publicly disclosed.

## 4.4 Placement logic

| **Section**     | **Primary purpose**             | **Keyword density** | **Proof density** | **Agent rule**                                                                                 |
|-------------------|------------------------------------|------------------------|----------------------|-----------------------------------------------------------------------------------------------|
| Headline         | Classification + positioning    | High, selective     | Medium             | Use target role + 2–4 core concepts + impact/domain phrase.                                    |
| Current title    | Recruiter matching              | High                 | High               | Use standard, truthful title; propose an externally understandable variant only when accurate. |
| Experience       | Search + evidence + credibility | High in context      | Very high           | Every major bullet should combine action + relevant capability + outcome/scale when supported. |
| Skills            | Capability map                  | High but curated     | Low                 | LinkedIn allows up to 100 (§16.1); stuffing toward that ceiling dilutes relevance. Curate 15–25 for early/mid-career, up to ~35 for senior technical profiles, always evidence-backed. Even a short curated list clears the practical bar — profiles listing 5+ relevant skills already see materially more recruiter contact (§16.1). |
| About             | Narrative + semantic context    | Medium-high          | High               | Use natural reinforcement, not repetition.                                                     |
| Projects          | Technical proof                 | Medium               | Very high           | Problem → solution → architecture → technology → scale → result → evidence.                    |
| Featured          | Conversion                      | Low for search       | Very high           | Use strongest proof artifacts; do not pretend Featured drives search discovery.                |
| Recommendations  | Social proof                    | Low                   | High                | Request specific evidence from varied credible relationships.                                  |

# 5. Evidence, credibility, and anti-hallucination system

## 5.1 Evidence ledger

| **Claim ID** | **Claim**               | **Source**                   | **Evidence type** | **Confidence** | **Allowed use**                                      |
|---------------|---------------------------|---------------------------------|----------------------|-------------------|--------------------------------------------------------|
| F-001        | Current title           | Profile PDF                  | Direct              | High             | May be rewritten without changing factual meaning    |
| F-002        | Technology used         | Experience description       | Direct              | High             | May be reused where relevant                          |
| M-001        | Metric missing          | Profile + JD                 | Gap                 | Low              | Ask user; do not invent                                |
| I-001        | Likely leadership scope | Career progression inference | Inference           | Medium           | Phrase as a hypothesis or confirmation request        |
| R-001        | Recommended keyword     | JD                            | Recommendation      | High             | May be used only when candidate evidence supports it  |

## 5.2 The evidence ladder

DIRECT FACT → CONTEXTUALIZED FACT → QUANTIFIED IMPACT → REPEATED / CROSS-SOURCE PROOF → AUTHORITY SIGNAL

- Direct fact: "Used AWS."
- Contextualized fact: "Designed AWS-based microservices."
- Quantified impact: "Reduced p95 latency by 42%."
- Repeated proof: the same specialization appears consistently in experience, projects, GitHub, and portfolio.
- Authority signal: publication, patent, conference talk, open source, research, or trusted recommendation.

## 5.3 Proof-density rule
Optimize for proof per sentence. Prefer specific descriptions that communicate ownership, technology/context, scale, and measurable result. Replace "experienced," "passionate," and similar low-evidence adjectives with concrete evidence.

## 5.4 Anti-hallucination checks

- Detect every new number and compare it against the source evidence ledger.
- Detect every new company, technology, title, credential, award, publication, or responsibility.
- Detect chronology changes or title inflation.
- Detect unsupported management claims such as "led a 50-person team" without a source.
- Detect "soft claims" that imply expertise without evidence, and downgrade them to neutral wording or a user-confirmation request.
- When evidence is missing but strategically important, output `[CONFIRM / ADD EVIDENCE]` rather than fabricate content.

## 5.5 Gap-resolution protocol (ask, don't silently omit)

The single most common way this product disappoints a user is not a fabricated
fact — it's a section that quietly disappears because the PDF didn't have
anything for it. A missing section is a decision point, not a reason to skip
straight to the rewrite. Before step 11 (rewrite), every gap logged in the
evidence ledger (`M-xxx`) and every applicable-but-entirely-empty section
(Certifications, Featured, Publications, Patents, Awards, Recommendations,
Projects, Languages, etc.) gets resolved with the user, one batched pass, not
scattered one-question-at-a-time interruptions.

For each open item, give the user exactly this choice:

1. **Provide it** — the user supplies the real information. It becomes a
   normal ledger fact (`F-xxx`) and flows into the rewrite like anything else
   from the PDF.
2. **Have the agent suggest options** — the agent proposes 2-4 concrete,
   realistic, role-relevant options (e.g., named certifications worth
   pursuing for the target role, a sample metric-shaped sentence with the
   number left blank for the user to fill in, a recommendation-request theme
   and who to ask, a project framing template). Every suggestion is labeled
   `[SUGGESTED — NOT YET TRUE]` inline and is a starting point for the user
   to accept as-is, edit, or reject — never a fact until the user confirms it.
3. **Skip it** — the user explicitly declines. This is different from the
   PDF simply not mentioning it: the user was asked and chose not to add it
   now. Log the decision either way.

A suggestion only becomes copy-ready content once the user confirms it's
literally true of them right now (already holds the certification, is
actually pursuing it, genuinely wants that project framing, etc.) — accepting
"good idea" is not the same as confirming truth. If a user says "yes, add
that certification as something I'm pursuing," write it as in-progress, not
as held. If the user just likes the idea for the future, it goes in the
maintenance plan (§15), not the copy-ready block.

Every resolution (real answer / agent-suggested-and-confirmed / explicitly
skipped) gets one line in the output note's Gap Resolution Log (§10.1a) —
this is what makes "nothing was silently ignored" independently checkable
without re-reading the whole diagnostic.

# 6. Complete LinkedIn section/field optimization framework

The agent should inspect every applicable field. The supplied research groups sections into Core, Recommended, and Additional areas and emphasizes that different fields have different strategic roles.

| **Field**                               | **Purpose**                      | **Search value**                    | **Rewrite logic**                                                                      | **Agent action**                                                                |
|--------------------------------------------|-------------------------------------|----------------------------------------|--------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Name                                     | Identity                         | Very low                             | Keep real name; no SEO keyword stuffing; preserve professional suffix only if genuine. | Rewrite only if extraction is incorrect or formatting can be improved.          |
| Name pronunciation                       | Accessibility / relationship     | Very low                             | Not an SEO field.                                                                        | Recommend recording when appropriate.                                           |
| Profile photo                            | Trust / first impression         | Very low                             | No meaningful keyword value.                                                              | Give visual recommendation, not fake textual optimization.                      |
| Banner / background                      | Brand positioning                | Low                                   | No strong evidence that banner text is a meaningful search ranking field.               | Recommend one clear professional concept; avoid billboard-style keyword walls.  |
| Headline                                 | Classification / positioning     | Very high                            | Target role + primary specialization + 2–4 core concepts + impact/domain.                | Provide 2–3 variants only when useful; default to one primary version.          |
| About                                     | Narrative / conversion           | High                                  | Use hook, identity, specialties, proof, impact, current focus, interests, CTA.          | Rewrite completely when weak or generic.                                        |
| Current position                          | Recruiter matching + evidence    | Very high                            | Use standard, truthful role terminology and relevant skills in context.                | Rewrite title/description without changing factual meaning.                     |
| Previous experience                       | Evidence / credibility           | Very high                            | Action + capability + scale + result.                                                    | Prioritize strongest recent/relevant roles; preserve chronology.                |
| Job titles                                | Searchability                    | Very high                            | Prefer standard market titles when accurate.                                            | Flag title mismatch and suggest an honest standard equivalent.                  |
| Skills                                    | Capability map                   | Very high                            | Curated, target-aligned skills; context beats random volume.                            | Rank into core / architecture / technology / domain / leadership clusters.      |
| Experience-associated skills              | Contextual proof                 | High                                  | Tie skills to specific roles where supported.                                           | Add only skills actually used in that role.                                     |
| Projects                                  | Technical proof                  | Medium-high                          | Problem → solution → architecture → tech → scale → result → evidence.                    | Recommend high-signal projects; quality over quantity for senior professionals. |
| Featured                                  | Conversion / proof               | Low for search; high for conversion  | Best work samples, not keyword stuffing.                                                 | Build 3–5 strongest proof items.                                                |
| Recommendations                           | Social proof                     | Medium                                | Specific evidence beats generic praise.                                                  | Recommend whom to request and what themes they should substantiate.             |
| Education                                 | Credibility / filters             | Medium                                | Degree, school, specialization; more detail for early career.                           | Include selective supporting evidence.                                          |
| Licenses & certifications                 | Credential proof                 | Medium                                | Only relevant, credible credentials.                                                     | Prioritize high-value credentials.                                              |
| Courses                                    | Supporting evidence              | Low-medium                            | Selective based on seniority and relevance.                                              | Do not pad the profile.                                                         |
| Publications                               | Authority                        | Role dependent                        | Title + context + venue + date + contribution + link.                                    | Highlight when strategically relevant.                                          |
| Patents                                    | Specialized authority            | Role dependent                        | Accurate inventor contribution.                                                           | Never overstate authorship.                                                     |
| Honors & awards                            | Credibility                      | Role dependent                        | Professional/technical distinction over low-value filler.                                | Prioritize meaningful recognition.                                              |
| Languages                                  | Recruiter filter                 | Role/location dependent               | Accurate proficiency.                                                                      | Include when relevant to target market.                                         |
| Volunteer experience                       | Leadership/context               | Role dependent                        | Leadership, mentoring, technical education, board/community service.                    | Add only when it strengthens the story.                                         |
| Organizations                              | Community / identity             | Low-medium                            | Professional communities that signal real identity.                                      | Avoid list dumping.                                                             |
| Causes                                      | Context                          | Low                                    | Use only when it contributes to authentic story.                                         | Never optimize for recruiter search.                                            |
| Services                                    | Discovery for service providers  | Role dependent                        | Clear service taxonomy.                                                                   | Optimize if consultant/freelancer/advisor/independent architect.                |
| Open to Work / career preferences          | Recruiter discovery              | High for job seekers                  | Target job types, locations, availability, and appropriate visibility.                  | Present the "Everyone" (public green frame) vs. "Recruiters only" trade-off explicitly and let the user choose — public visibility measurably increases recruiter InMail rates, but some hiring-manager perception research pushes the other way, and it's a personal risk call (current employer visibility) the agent shouldn't make silently (§16.1). |
| Career Break                                | Transparency                     | Low for SEO                           | Legitimate reason + professional narrative if useful.                                    | Prefer truthful career break over fictional employment.                         |
| Public profile URL                          | Identity / brand                 | Low-medium                            | Custom, recognizable URL.                                                                  | Recommend clean public URL.                                                     |
| Contact information                         | Conversion                       | Low for search                        | Professional contact paths.                                                                | Use only appropriate public contact information.                                |
| Industry / location                         | Recruiter filtering              | High                                    | Align with realistic target market and actual geography.                                 | Flag mismatch or missing information.                                           |
| Creator / professional profile elements     | Brand / activity                 | Role dependent                        | Support the chosen niche and authority strategy.                                          | Recommend only when aligned with the user's goals.                              |
| Activity / content                          | Authority / contextual discovery | Role dependent                        | Consistent niche and evidence-led content.                                                | Generate content strategy, not generic posting volume.                          |

# 7. Rewrite rules by profile section

## 7.1 Headline generator

`[TARGET ROLE] | [PRIMARY SPECIALIZATION] | [2–4 CORE SKILLS] | [DOMAIN / BUSINESS OR TECHNICAL IMPACT]`

- Start with the market-recognizable target role when truthful.
- Use 2–4 core capability anchors, not a long inventory.
- Include technologies only when they are genuinely differentiating and target-relevant.
- End with a value phrase that shows what the person builds, scales, leads, or changes.
- Avoid "passionate," "results-driven," "ninja," "guru," and similar empty descriptors unless the user specifically wants a personal-brand voice and the phrase adds real information.
- **Front-load for the ~70-character visible window.** LinkedIn allows up to
  220 characters, but only roughly the first 70 show in search results, the
  mobile preview, and next to comments — the exact target-role phrase and
  the strongest specialization keyword must land inside that window, not
  after the third pipe (§16.1).
- **Prefer the literal phrase a recruiter would type**, not just a related
  concept — search still weighs exact/near-exact phrase matches heavily, so
  "Data Engineer" outranks a synonym like "Data Pipeline Specialist" for a
  recruiter searching the literal title, when the literal title is truthful
  (§16.1).

## 7.1a "It's not on LinkedIn" is not a stopping point

For every generator in this section, if the source evidence for a slot is
missing (no headline history to anchor to, no clear domain phrase, no metric
for the value clause), that slot is a §5.5 gap-resolution item, not a reason
to leave the section thin or generic. Resolve it with the user before
finalizing the section.

## 7.2 About generator

```
HOOK
↓
WHO I AM
↓
WHAT I SPECIALIZE IN
↓
SELECTED PROOF
↓
TECHNICAL / BUSINESS IMPACT
↓
CURRENT FOCUS
↓
WHAT I WANT TO BE KNOWN FOR
↓
CTA
```

- **Front-load the first ~300 characters** (roughly the HOOK + WHO I AM
  beats). LinkedIn truncates About at ~300 characters on desktop and ~200 on
  mobile before "see more" — the primary role keyword and the single
  strongest proof point must appear before that cutoff, since most readers
  (and a fast recruiter scan) never click through (§16.1). The full section
  can use up to 2,600 characters; use the room, but don't bury the lede in
  it.

## 7.3 Experience bullet generator

`ACTION + TECHNOLOGY / METHOD + SYSTEM / SCOPE + SCALE + MEASURABLE RESULT`

- Technical IC: emphasize architecture, system design, reliability, scale, performance, developer productivity, and cross-team technical influence.
- Engineering Manager: emphasize hiring, team health, execution, architecture, coaching, stakeholder management, and measurable delivery/business outcomes.
- Director / VP: emphasize organizational scale, strategy, budgets, business outcomes, product impact, transformation, and executive influence.
- Principal / Staff: emphasize multi-team or company-level technical influence, architecture strategy, standards, major transformations, and business impact.

## 7.4 Project generator

`PROBLEM → SOLUTION → ARCHITECTURE → TECHNOLOGY → SCALE → RESULT → EVIDENCE LINK`

## 7.5 Recommendation-request generator

- Manager: architecture, ownership, execution, growth, leadership.
- Peer/architect: technical depth, design decisions, collaboration.
- Product partner: customer/business impact, prioritization, delivery.
- Direct report: coaching, team building, clarity, growth.
- Executive/client: strategic influence, outcomes, trust, transformation.

# 8. Technical / management / hybrid positioning logic

## 8.1 Technical IC

`DEPTH → ARCHITECTURE → SCALE → RELIABILITY → INFLUENCE → BUSINESS IMPACT`

Use technical specialization as the dominant identity. Projects, GitHub, architecture diagrams, research, and technical content carry extra weight.

## 8.2 Management

`PEOPLE → EXECUTION → TECHNICAL CREDIBILITY → STRATEGY → ORG SCALE → BUSINESS IMPACT`

Make team scope, hiring, organizational design, delivery, stakeholder alignment, and measurable business outcomes visible. Do not let the profile read like a junior developer portfolio.

## 8.3 Hybrid technical + management

```
ENGINEERING DEPTH
↓
ARCHITECTURE
↓
TECHNICAL LEADERSHIP
↓
TEAM / ORG IMPACT
↓
BUSINESS IMPACT
```

Use this for Staff+, Engineering Leads, senior managers, and leaders who must be legible to both technical recruiters and engineering leadership recruiters.

## 8.4 Seniority narrative

| **Level** | **Primary story**                 | **Evidence expected**                                                         |
|-------------|---------------------------------------|-------------------------------------------------------------------------------|
| Fresher    | Potential + skills + evidence     | Education, projects, internships, skills, GitHub, awards                      |
| Junior     | Skills + projects + execution     | Projects, production work, measurable contributions                           |
| Mid-level  | Experience + execution            | Ownership, delivery, technical scope                                          |
| Senior     | Ownership + impact                | Architecture, reliability, scale, mentoring, cross-team influence             |
| Staff      | Architecture + influence          | System + architecture + multiple teams + technical strategy + business impact |
| Principal  | Technical strategy + organization | Company-level architecture direction, standards, transformations              |
| Manager    | People + execution                | Hiring, team building, coaching, delivery, stakeholder management             |
| Director   | Organization + strategy           | Org scale, budgets, transformation, cross-functional/product impact           |
| VP         | Business + technology             | Growth, product launches, cost, organizational scale, strategy                |
| CTO        | Company + technology + market     | Technology strategy, product, business, innovation, organization, market      |

# 9. Scoring and alignment model

The supplied research proposes a 100-point profile audit. These are strategic diagnostic weights, not secret LinkedIn algorithm weights.

| **Dimension**                        | **Points** | **What the agent measures**                                                                                     |
|-----------------------------------------|--------------|-----------------------------------------------------------------------------------------------------------------|
| Discoverability                       | 25          | Target title, headline keywords, skills, experience keywords, location/industry, Open to Work/preferences.      |
| Credibility                            | 20          | Quantified achievements, experience quality, recommendations, certifications, awards/publications, consistency. |
| Technical / professional authority    | 20          | Projects, GitHub/portfolio, publications, Featured work, technical content, open source.                        |
| Leadership / business impact          | 15          | Ownership, team/cross-team impact, business metrics, strategy, cross-functional impact.                         |
| Conversion                             | 10          | About hook, narrative, Featured proof, CTA/contact, personal brand.                                             |
| Professionalism                        | 10          | Photo, banner, URL, education, certifications, formatting, current profile.                                     |

## 9.1 Score interpretation

| **Score** | **Diagnosis**                | **Agent response**                                                  |
|-------------|----------------------------------|-----------------------------------------------------------------------|
| 90–100     | Exceptional                   | Maintain; focus on role-specific refinement and authority.          |
| 80–89      | Strong                         | Fix high-impact gaps and improve proof density.                     |
| 70–79      | Good but improvable           | Prioritize headline, experience, skills, evidence, and positioning. |
| 60–69      | Average                        | Perform a substantial profile rebuild.                              |
| 50–59      | Weak positioning               | Rebuild core identity and evidence layer first.                     |
| <50        | Major optimization required   | Full repositioning and evidence-gathering workflow.                 |

## 9.2 Role-alignment score

```
ROLE ALIGNMENT (100) =
  30% must-have capability coverage
+ 20% target title / seniority fit
+ 15% technical skill evidence
+ 10% architecture / domain fit
+ 10% leadership / business fit
+ 10% proof / credibility
+ 5%  location / preference fit
```

The weights above are an agent design choice for comparative diagnosis, not a LinkedIn-published formula. The result must be labeled as an internal alignment score.

## 9.3 Two-role comparison

| **Output**              | **Role #1** | **Role #2** | **Shared core / decision**  |
|----------------------------|---------------|---------------|----------------------------------|
| Primary role fit          | [score]      | [score]      | [shared identity]               |
| Must-have coverage        | [x%]         | [y%]         | [overlap / conflict]            |
| Technical fit              | [score]      | [score]      | [common strengths]              |
| Leadership fit             | [score]      | [score]      | [common strengths]              |
| Evidence gap                | [top gap]    | [top gap]    | [shared missing proof]          |
| Recommended positioning   | [position]   | [position]   | [primary market position]       |

# 10. Output package and copy-ready format

## 10.0 Delivery shape: the profile leads, the report follows

The user's actual deliverable is a finished, recruiter-ready LinkedIn
profile — not an audit. Every output note is ordered so the complete
copy-ready profile is the first thing a reader sees after the frontmatter,
followed by a short (≤10 line) summary of what changed and why. Everything
else this section used to treat as equally prominent — both role analyses,
the evidence ledger, the keyword placement matrix, the priority plan, the
maintenance plan, the QA checklist — still gets produced in full (nothing
here is cut), but lives together under one collapsed **Appendix: Full
Diagnostic Report** heading at the bottom of the same note. The appendix is
reference material for someone who wants to audit the reasoning, not
something the user has to scroll past to reach their profile.

In chat, report back even leaner than the note: the file path, the chosen
primary position, the score delta in one line, and at most 3-5 items that
genuinely need the user's attention (unresolved gaps, a positioning
trade-off) — never restate the full diagnostic in the chat turn. See step 13.

## 10.1 Required final output

Ordering matters as much as content — see §10.0. Produced in full every run:

1. Complete rewritten LinkedIn profile, ready to copy/paste (leads the note).
2. Short summary: primary position, score delta, what changed, in ≤10 lines.
3. Gap Resolution Log (§10.1a) — every gap/empty section and how it was
   resolved with the user.
4. *(Appendix, collapsed together)* Executive diagnosis; Role #1 analysis;
   Role #2 analysis; two-role overlap/conflict report; current 100-point
   profile score with rationale; role-alignment score for each target role;
   evidence ledger; before vs. after for every relevant section; keyword
   strategy (primary/secondary/supporting/avoid) and placement matrix;
   recruiter-search configuration recommendations; personal-brand/Featured
   recommendations; Critical/High/Medium/Low action plan; 30-90 day
   maintenance plan; QA checklist.

## 10.1a Gap Resolution Log

One row per item raised in the §5.5 gap-resolution pass — the audit trail
that proves nothing was silently dropped, without requiring anyone to read
the full appendix to check it.

| Section / gap | Resolution | What was used |
|---|---|---|
| e.g. Certifications (empty) | User chose: agent-suggested, then confirmed | "Pursuing AWS Certified Solutions Architect – Associate" (user confirmed in-progress) |
| e.g. M-003 quantified metric | User declined to provide | Left out of copy-ready block; noted in maintenance plan as a 30-day action |

## 10.2 Copy-ready profile output structure

```
PROFILE READY TO COPY

NAME
[exact name]

HEADLINE
[final headline]

ABOUT
[final About]

EXPERIENCE
[Company]
[Standard title]
[Dates]
• ...
• ...

PROJECTS
[Project]
Description...

SKILLS
1. ...
2. ...

FEATURED
1. ...
2. ...

EDUCATION
...

CERTIFICATIONS
...

PUBLICATIONS / PATENTS / AWARDS
...

LANGUAGES
...

VOLUNTEER / ORGANIZATIONS / CAUSES
...

OPEN TO WORK / PREFERENCES
...

CONTACT / URL
...
```

## 10.3 Before vs after table

| **Section** | **Current state**  | **Problem**                       | **Final version**     | **Why this change**                       |
|---------------|-----------------------|---------------------------------------|---------------------------|------------------------------------------------|
| Headline     | [current]            | [generic / weak / not targeted]   | [final]                 | Improves classification and positioning.  |
| About         | [current]            | [empty / narrative gap]           | [final]                 | Improves conversion and semantic context. |
| Experience    | [current bullet]     | [responsibility only]              | [impact bullet]         | Adds ownership, context and proof.        |
| Skills         | [current list]       | [too broad / missing]             | [curated list]          | Improves target relevance.                |
| Featured      | [items]               | [weak proof]                       | [recommended stack]     | Improves conversion.                      |

## 10.4 Priority system

| **Priority** | **Definition**                                         | **Examples**                                                                                            |
|----------------|------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|
| CRITICAL      | Directly blocks target-role discovery or credibility   | Wrong target title, severe positioning conflict, missing core experience keyword, unsupported headline. |
| HIGH           | Meaningfully improves recruiter matching or conversion | Headline, About, recent Experience, Skills, Open to Work, key evidence.                                 |
| MEDIUM        | Strengthens authority / polish                          | Projects, Featured, recommendations, relevant certifications, portfolio links.                          |
| LOW             | Optional context / brand refinement                    | Causes, low-value courses, nonessential formatting polish.                                              |

# 11. Agent system prompt

Use the following as the core system instruction for the AI agent. It is intentionally strict about truthfulness and evidence.

```
You are an expert LinkedIn Profile Optimization Agent for Technical, Engineering, Product, Management, and Leadership professionals.

INPUTS
- One LinkedIn Profile PDF representing the user's current profile.
- Exactly two target job roles / job descriptions.

MISSION
Transform the current profile into a recruiter-searchable, human-convincing, evidence-heavy LinkedIn profile aligned to the strongest credible market position supported by the user's actual background and the two target roles.

FIRST: ANALYZE, THEN WRITE
Do not rewrite immediately. First extract facts, chronology, existing positioning, target-role requirements, overlaps, conflicts, evidence, and gaps.

TRUTHFULNESS
Never invent achievements, metrics, company scope, titles, responsibilities, technologies, certifications, education, publications, awards, team sizes, revenue, latency, scale, or leadership responsibilities.
Every factual claim in the final profile must be supported by the profile or other supplied evidence.
When valuable evidence is missing, write [CONFIRM] or [ADD EVIDENCE] in the diagnostic section rather than fabricating content.

POSITIONING
Choose one primary market position. Do not attempt to optimize one LinkedIn profile as if it were simultaneously a Backend Engineer, AI Engineer, Product Manager, Engineering Manager, Cloud Architect, and CTO.
Use secondary capabilities to support the primary identity.
If the two target roles conflict, explain the trade-off and choose the position best supported by the user's evidence.

SEARCH OPTIMIZATION
Optimize for recruiter understanding and relevance, not keyword repetition.
Use standard market job titles when truthful.
Use important role-specific terminology naturally across headline, About, Experience, Skills, Projects, and other relevant sections.
Never keyword-stuff.
Do not claim exact LinkedIn ranking weights or guarantee a top search position.

WRITING
Make the profile sound like a strong real professional, not a resume parser.
Maximize proof density: ownership + context + technology/method + scope/scale + measurable result where supported.
Match wording and evidence to career level.
Technical ICs should emphasize architecture, systems, scale, reliability, and influence.
Managers should emphasize people, execution, architecture, hiring, coaching, stakeholder management, and outcomes.
Director/VP/CTO profiles should increasingly emphasize organizational scale, strategy, business impact, transformation, and market context.

SECTION COVERAGE
Review every applicable LinkedIn field: Name, pronunciation, photo, banner, headline, About, current position, previous Experience, skills, experience-associated skills, education, certifications, projects, Featured, recommendations, publications, patents, awards, courses, languages, volunteer experience, organizations, causes, services, Open to Work / preferences, career break, public URL, contact information, location, industry, creator/professional profile elements, and activity/content.
For fields that cannot or should not be changed, say so and give a recommendation.

OUTPUT
Return:
1) Executive diagnosis
2) Primary market position
3) Role #1 analysis
4) Role #2 analysis
5) Two-role overlap/conflict report
6) Current 100-point score
7) Role alignment scores
8) Complete rewritten profile ready to copy/paste
9) Before vs after for every applicable section
10) Keyword strategy and placement map
11) Gaps and missing evidence
12) Recommended additions
13) Recruiter-search recommendations
14) Personal-brand / Featured strategy
15) Priority action list: Critical / High / Medium / Low
16) Maintenance plan

QUALITY BAR
A recruiter should be able to answer quickly:
- Who is this person?
- What are they unusually good at?
- What have they actually accomplished?
- Why should we talk to them for this role?

The final result must be coherent, specific, credible, machine-readable, human-readable, and ready to implement on LinkedIn.
```

# 12. Structured output schema

```json
{
  "candidate": {
    "name": "",
    "current_title": "",
    "location": "",
    "industry": ""
  },
  "positioning": {
    "primary_market_position": "",
    "secondary_capabilities": [],
    "domain": [],
    "recommended_niche": ""
  },
  "roles": {
    "role_1": {
      "title": "",
      "alignment_score": 0,
      "must_have": [],
      "matches": [],
      "gaps": [],
      "keywords": []
    },
    "role_2": {
      "title": "",
      "alignment_score": 0,
      "must_have": [],
      "matches": [],
      "gaps": [],
      "keywords": []
    }
  },
  "profile_audit": {
    "current_score": 0,
    "discoverability": 0,
    "credibility": 0,
    "authority": 0,
    "leadership_business_impact": 0,
    "conversion": 0,
    "professionalism": 0
  },
  "rewritten_profile": {
    "name": "",
    "headline": "",
    "about": "",
    "experience": [],
    "skills": [],
    "projects": [],
    "featured": [],
    "education": [],
    "certifications": [],
    "publications": [],
    "patents": [],
    "awards": [],
    "courses": [],
    "languages": [],
    "volunteer": [],
    "organizations": [],
    "causes": [],
    "services": [],
    "open_to_work": {},
    "career_break": {},
    "public_url": "",
    "contact": {}
  },
  "keywords": {
    "primary": [],
    "secondary": [],
    "supporting": [],
    "avoid_or_low_priority": [],
    "placement": {}
  },
  "evidence_requests": [],
  "before_after": [],
  "priorities": {
    "critical": [],
    "high": [],
    "medium": [],
    "low": []
  },
  "maintenance": {
    "days_30_90": []
  }
}
```

# 13. QA and acceptance criteria

| **Check**             | **Pass condition**                                                                                                 | **Fail example**                                                                |
|--------------------------|------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------|
| Truthfulness           | Every factual statement maps to supplied evidence or is explicitly marked for confirmation.                       | Invented "50M events/day" metric.                                               |
| Role relevance         | Most important profile content directly supports the selected target market position.                             | Headline targets a different career.                                            |
| Searchability           | Target titles, relevant skills and domains appear naturally in appropriate sections.                              | Important target skill exists only in a random skills dump.                     |
| No stuffing             | No repetitive keyword strings or unnatural repetition.                                                              | Java \| Java Developer \| Java Engineer \| Java Backend \| Java Programming.    |
| Seniority fit           | Nature of impact matches career level.                                                                              | Principal profile written like an entry-level implementation log.               |
| Proof density           | Major experience claims include concrete scope/result when supported.                                             | "Responsible for APIs."                                                         |
| Consistency             | Dates, titles, companies and specialties are consistent across supplied sources.                                  | LinkedIn says Manager while resume says IC for same period with no explanation. |
| Completeness            | All applicable LinkedIn sections are reviewed and either rewritten, recommended, or intentionally left unchanged. | Only headline/About/Skills are optimized.                                       |
| Copy readiness          | Final profile is clean prose with no internal tokens, analysis notes, or tool markup.                             | Profile contains [SOURCE LINE 123] artifacts.                                   |
| Ranking claim safety   | No unsupported "#1" or guaranteed ranking promises.                                                               | "This will always appear at the top."                                           |

## 13.1 Final recruiter simulation

```
SIMULATE RECRUITER SEARCH
1. Search by target title
2. Filter by key skills
3. Filter by seniority/location
4. Read headline
5. Read About
6. Scan recent Experience
7. Look for proof
8. Check Featured / Projects
9. Check social proof
10. Decide: message / shortlist / pass
```

The agent should explain what a recruiter would learn at each stage and identify the first point at which the candidate may lose relevance or trust.

# 14. Common failure modes

| **Failure**                    | **Why it hurts**                                 | **Agent prevention**                                          |
|-----------------------------------|------------------------------------------------------|-----------------------------------------------------------------|
| Generic headline                | Low classification value                          | Use explicit target role and core specialization.             |
| Keyword stuffing                | Can reduce readability and may hurt visibility    | Natural semantic reinforcement.                                |
| Resume dumping                   | LinkedIn needs more readable narrative and proof  | Convert duties into outcomes and context.                     |
| Responsibility-only bullets     | Weak proof                                          | Use action + context + scale + result.                        |
| Too many technologies           | Dilutes specialization and credibility            | Prioritize target-relevant technologies.                      |
| Empty About                      | Missed conversion opportunity                     | Use structured narrative.                                     |
| No proof                          | Candidate looks unverified                        | Projects, recommendations, Featured, GitHub, research, talks. |
| Buzzword overload                | Feels generic or inflated                          | Replace adjectives with evidence.                              |
| Wrong seniority narrative        | Level mismatch reduces fit                        | Use level-specific evidence model.                             |
| Trying to target everything     | No coherent market identity                       | Choose one primary market position.                            |
| Inventing metrics                 | Severe trust failure                               | Evidence ledger + confirmation requests.                       |
| Treating Featured as SEO         | Wrong optimization objective                       | Use Featured for conversion/proof.                             |

# 15. 30–90 day maintenance loop

Profile optimization is not a one-time rewrite. The supplied research recommends revisiting the profile every 30–90 days as roles, technologies, achievements, and target markets change.

| **Period**                    | **Focus**          | **Actions**                                                                                                             |
|----------------------------------|------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| Every 30 days                   | Signal freshness    | Add recent achievement; verify current title; update current focus; review profile views/search context.               |
| Every 60 days                   | Target alignment    | Review current target JDs; refresh top keywords; remove obsolete or low-value technologies.                            |
| Every 90 days                   | Authority / proof   | Refresh Featured; add a case study/project; request recommendations; review portfolio/GitHub consistency.               |
| When targeting a new market    | Repositioning        | Re-run the two-role analysis; recalculate overlap and alignment; update market position only when evidence supports it. |

## 15.1 Content / thought-leadership layer

```
DAYS 1–30
40% educational
30% technical experience
20% architecture
10% career / leadership

DAYS 31–60
architecture breakdowns + case studies + research summaries + trade-offs

DAYS 61–90
original frameworks + deep dives + research analysis + architecture patterns + case studies + open source
```

The supplied research recommends choosing one recognizable niche rather than posting across unrelated professional identities. High-authority content examples include architecture diagrams, production case studies, original research, open-source projects, technical tutorials, research summaries, and system design.

# 16. Research-derived evidence base

**The following statements are directly derived from the supplied research document:**

- LinkedIn People Search is described as personalized; there is no universal profile ranking position.
- LinkedIn explicitly warns that more keywords do not automatically mean better visibility and discourages keyword stuffing.
- Standard job titles are recommended over creative titles for searchability.
- Recruiter search can use job titles, skills, location, company, school, industry, languages, seniority, workplace type, Open to Work, and keywords; the supplied research also describes AI-assisted recruiter search.
- The research separates Discovery, Classification, and Conversion and emphasizes that skills help discovery while proof helps conversion.
- Experience is treated as a core evidence layer; bullets should favor action + technology/method + scale + result.
- Projects are framed as proof-of-work and should communicate problem, solution, architecture, technology, scale, result, and evidence.
- Featured is treated primarily as a conversion/work-sample layer rather than a search-discovery layer.
- Skills should be curated rather than blindly filled to the maximum allowed count.
- Contextual skills matter because evidence of how a skill was used is more informative than a bare skill label.
- Technical + management profiles should connect engineering depth to architecture, technical leadership, organizational impact, and business impact.
- The research recommends one primary market position rather than simultaneously targeting many unrelated identities.
- A 100-point diagnostic can be used across discoverability, credibility, authority, leadership/business impact, conversion, and professionalism.
- Maintenance every 30–90 days is recommended.

> **Source reference**
> Supplied research document: "Deep Research: How to Build a High-Performing, SEO-Friendly LinkedIn Technical & Management Profile." It cites LinkedIn Help, LinkedIn Recruiter Help, LinkedIn Talent Solutions, and supporting industry sources. This specification treats the uploaded research as the source basis requested by the user; it does not silently upgrade its claims into additional independently verified findings.

## Selected URLs cited in the supplied research

> https://www.linkedin.com/help/linkedin/answer/a524188
>
> https://www.linkedin.com/help/linkedin/answer/a521944
>
> https://www.linkedin.com/help/recruiter/answer/a414428
>
> https://www.linkedin.com/help/recruiter/answer/a415295
>
> https://www.linkedin.com/help/recruiter/answer/a596630
>
> https://www.linkedin.com/help/recruiter/answer/a723067
>
> https://www.linkedin.com/help/recruiter/answer/a1676527
>
> https://www.linkedin.com/help/linkedin/answer/a552452
>
> https://www.linkedin.com/help/linkedin/answer/a507508
>
> https://www.linkedin.com/help/linkedin/answer/a518980
>
> https://www.linkedin.com/help/linkedin/answer/a540837

## 16.1 2026-09-13 research refresh

The original supplied research document above (§16) is preserved verbatim as
the historical source basis. This subsection adds a second, independently
verified pass — live web research done specifically to check whether the
platform mechanics behind that guidance had changed, and to ground the
keyword/placement rules in specific, current numbers rather than general
advice. Confirmed against LinkedIn's own Help pages where a hard platform
limit is claimed; industry-aggregated for softer behavioral claims (labeled
accordingly below — these are widely-repeated practitioner findings, not
LinkedIn-disclosed ranking weights, consistent with this spec's existing
posture in §4.3 and §9).

**Confirmed directly from LinkedIn Help:**
- Members can add up to 100 skills to a profile (LinkedIn Help, "Add and
  remove skills on your profile"). This doesn't change the agent's curation
  guidance (§4.4, §6) — quality over volume still holds — it just corrects
  the platform ceiling itself.
- Headline: 220-character field limit; only roughly the first 70 characters
  render in search results, the mobile app, and next to comments — this is
  why front-loading the target role and top keyword matters mechanically,
  not just stylistically (§7.1).
- About: 2,600-character field limit; truncates for the reader at roughly
  300 characters on desktop and 200 on mobile before a "see more" click
  (§7.2).

**Industry-aggregated (not LinkedIn-disclosed, treat as directional):**
- Recruiter/People Search appears to weigh exact or near-exact phrase
  matches in the headline and current-title fields heavily, on top of
  broader semantic/contextual matching — reinforces "use the literal target
  title when truthful" (§1.3) over a paraphrase.
- Profiles that list at least ~5 clearly relevant skills report
  substantially higher recruiter contact rates than profiles with few or no
  skills listed — supports asking the user to fill a thin Skills section
  rather than leaving it sparse, even before it reaches the curated 15-35
  range (§4.4).
- Recent, visible activity appears to influence how a profile surfaces in
  search results, not just static field content — relevant context for the
  existing Activity/content row in §6, not a reason to change this module's
  scope (content strategy is the separate posting pipeline, not this
  one-off rewrite module).
- The public "Open to Work" photo frame correlates with materially higher
  recruiter InMail rates, but some hiring-manager sentiment pushes the other
  direction (perceived as broadcasting availability rather than targeted
  interest); "Recruiters only" visibility is a commonly recommended
  middle path. Treated as a user choice to present, not a default the agent
  picks (§6, Open to Work row).
- A practical way to source keywords beyond a single JD: extract terms that
  recur across multiple real postings for the target role (5-15 postings in
  the fuller version of this technique), then skew roughly 70% specific/
  exact-match terms to 30% broader category terms (§4.2a).

**Sources consulted (2026-09-13):**
- https://www.linkedin.com/help/linkedin/answer/a549047 (LinkedIn Help — Add and remove skills on your profile; confirms the 100-skill limit)
- https://blog.theinterviewguys.com/linkedin-seo/
- https://blog.theinterviewguys.com/linkedin-keywords/
- https://blog.theinterviewguys.com/linkedin-open-to-work-guide/
- https://blog.theinterviewguys.com/linkedins-hidden-open-to-work-settings-that-actually-work/
- https://linkedinrank.com/blogs/linkedin-search-algorithm-explained
- https://connectsafely.ai/articles/how-to-use-keywords-on-linkedin-profile-seo-2026
- https://authoredup.com/blog/linkedin-character-limit

None of these industry-aggregated sources are LinkedIn-official ranking
disclosures — treated the same way this spec already treats the original
supplied research's keyword-score formula (§4.3): an internal decision
framework informed by the best available evidence, never claimed as the
platform's actual algorithm.

> **Final product principle**
> The agent should produce a profile that is machine-readable, recruiter-searchable, human-convincing, evidence-heavy, narrowly positioned, and continuously maintained — while remaining completely faithful to the candidate's actual experience.
