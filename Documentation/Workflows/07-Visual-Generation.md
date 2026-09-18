# Visual Generation — End-to-End Workflow

## 1. Overview

This document traces the complete visual/image-prompt generation workflow of
the LinkedIn Agentic AI system, used across LinkedIn, X, and Substack Notes
(single-image path) and Substack Articles (multi-image path).

**This system does not generate images.** No image-generation API or MCP
tool is configured or called anywhere in this pipeline. The deliverable of
every run documented here is a **finished, paste-ready text prompt** for the
human to run manually in ChatGPT Images (or an equivalent tool). Per the
[README's "Generation & orchestration preferences"](../../README.md):

> **Visuals stay prompt-only.** The deliverable is a finished ChatGPT-Images
> prompt, never a rendered file or a live image-generation API call — this
> is a deliberate, twice-confirmed choice, not a missing feature.

This is reinforced by [REQUIREMENTS.md §7 "Visuals"](../../REQUIREMENTS.md),
which requires the image-generation layer to be **provider-swappable**
(free/low-cost providers interchangeable) rather than hard-wired to one —
the schema is built so a real provider can be wired in later without any
change to the Draft Note or Visual Brief Note structure. Today, that
provider slot is simply empty (`provider: none`).

The work performed by the skills in this document is **prompt engineering**:
reading a post's actual content, deciding whether and what kind of visual
would genuinely add to it, researching what's currently working
visually/stylistically for that kind of content, and writing one complete,
specific, copy-paste-ready prompt block. The system stops there. A human
takes that prompt, runs it in ChatGPT Images themselves, and — separately,
at scheduling/publishing time — pastes the resulting image in manually.
Nothing downstream of the brief (scheduling, Buffer) ever touches an actual
image file; see §4 (Handoff/What happens after) below.

Two skills implement this:

- [`generate-visual`](../../.claude/skills/generate-visual/SKILL.md) — the
  single-image variant, shared across LinkedIn, X, and Substack Notes.
- [`generate-visual-substack-article`](../../.claude/skills/generate-visual-substack-article/SKILL.md)
  — the multi-image variant for long-form Substack Articles: one mandatory
  header/hero image plus one image per `[IMAGE: <label>]` marker the writer
  left in the article body.

Full documentation of the shared human-approval gate this feeds into
(including the "Change Image" decision path) lives in
[01-LinkedIn-Post-Creation-and-Scheduling.md](01-LinkedIn-Post-Creation-and-Scheduling.md);
this document covers only what's needed to understand that handoff.

---

## 2. Top-Line Flow Chain

### Single-image path (LinkedIn / X / Substack Notes)

```
Trigger (/generate-visual [draft-id], typically after /critique-draft
    moves a note to status: in_review)
  → Approved/Critiqued Draft Read (full post text, not just the idea's seed)
  → Visual-Need Determination (does this post actually benefit from a
      visual — support the point, not decorate, per REQUIREMENTS.md §7)
  → Visual Type Selection (diagram / infographic / quote-card / comparison /
      chart / framework-graphic / carousel / architecture-diagram / etc.,
      decided fresh from this post's content — never the last-used format
      by default)
  → Current Design-Trend Research (WebSearch for what's visually trending,
      skipped only when the concept is simple enough that it wouldn't
      change the outcome)
  → Design Prompt Formulation (composition, visual hierarchy, color
      direction, lighting/mood, exact in-image copy, aspect ratio)
  → Visual Brief Note Write (Visuals/YYYY-MM-DD--kebab-slug.md; draft's
      visual_ids[] updated)
  → [Human runs the finished prompt manually in ChatGPT Images]
  → [Human pastes the resulting image back in manually at
      scheduling/publishing time — Buffer's scheduling mutation carries
      no media field]
```

### Multi-image path (Substack Articles)

```
Trigger (/generate-visual-substack-article [draft-id])
  → Article Note Read (title, subtitle, full thesis — not just the opening
      paragraph)
  → Header/Hero Image Brief (mandatory, every article gets exactly one,
      regardless of body content — represents the piece as a whole)
  → Scan Article Body for [IMAGE: <label>] Markers (zero markers is a
      valid, unforced outcome — the header image alone still applies)
  → For each marker found:
      Read that section's actual content
        → decide what the image needs to show (varied per section, distinct
          from the header and from each other)
        → Design-Trend Research (same judgment-call gate as the single-image
          path)
        → Design Prompt Formulation (same full spec as single-image)
  → ONE Visual Brief Note Write covering the whole set (header block first,
      then one `## Section Image: <label>` block per marker; article's
      visual_ids[] gets this one id)
  → [Human runs each finished prompt manually in ChatGPT Images, one at a
      time]
  → [Human places the header image in Substack's header-image slot and
      each marker's image at that marker's spot in the body, manually,
      at publishing time]
```

---

## 3. Flowchart

```mermaid
flowchart TD
    A["/generate-visual [draft-id]<br/>(or /generate-visual-substack-article)"] --> B{"Platform?"}
    B -- "linkedin / x / substack-note" --> C["Read full draft text<br/>(status: in_review, typically post-critique)"]
    B -- "substack-article" --> SA["Read article title, subtitle,<br/>full thesis + body"]

    C --> D{"Does this post<br/>actually benefit from<br/>a visual? (support the<br/>point, not decorate)"}
    D -- "no — would add nothing<br/>beyond the text" --> D2["No visual generated<br/>for this draft"]
    D -- yes --> E["Select visual type fresh<br/>from this post's content<br/>(check content-index.md /<br/>recent Visuals/ to avoid<br/>repeating last format)"]

    E --> F{"Would trend research<br/>change the outcome?"}
    F -- "no — simple concept<br/>e.g. plain quote card" --> H["Skip WebSearch,<br/>note why in brief"]
    F -- yes --> G["WebSearch: current<br/>visual/design trends<br/>for this concept"]
    G --> H

    H --> I["Formulate finished prompt:<br/>subject, composition, hierarchy,<br/>lighting, mood, color, typography,<br/>aspect ratio (platform-mapped)"]
    I --> J["Write Visual-Brief-Note<br/>(Visuals/YYYY-MM-DD--slug.md)"]
    J --> K["Append id to Draft Note's<br/>visual_ids[]"]

    SA --> L["Header/hero image brief<br/>(mandatory — every article,<br/>regardless of body content)"]
    L --> M{"Any [IMAGE: label]<br/>markers in body?"}
    M -- "zero — valid outcome" --> P["One Visual-Brief-Note:<br/>header block only"]
    M -- "one or more" --> N["Per marker: read section<br/>content, decide image need,<br/>trend research gate, formulate<br/>prompt (distinct per section)"]
    N --> O["One Visual-Brief-Note:<br/>header block + one<br/>## Section Image block per marker"]
    O --> Q["Append single id to article's<br/>visual_ids[]"]
    P --> Q

    K --> R["Report back: full brief +<br/>finished prompt, clearly labeled<br/>'prompt, not image'"]
    Q --> R

    R --> S["/review-drafts (shared Approval<br/>Manager, status: in_review)"]
    S --> T{"Human decision"}
    T -- "Change Image" --> U["Re-run /generate-visual or<br/>/generate-visual-substack-article,<br/>replace visual_ids entry"]
    U --> S
    T -- Approve --> V["status: approved<br/>(brief unchanged, still prompt-only)"]

    V --> W["/schedule-approved(-x)<br/>Buffer GraphQL mutation —<br/>TEXT ONLY, no media field"]
    W --> X["[HUMAN STEP, outside this<br/>pipeline] Run the finished<br/>prompt in ChatGPT Images"]
    X --> Y["[HUMAN STEP] Paste the<br/>resulting image in manually<br/>at publish time (Buffer UI<br/>or Substack editor)"]

    D2 -.-> S
```

---

## 4. Stage-by-Stage Breakdown

### Stage: Visual-need determination and type selection

- **Trigger:** `/generate-visual [draft-id]` (or, with no `draft-id`, every
  `Drafts/` note with a non-empty `suggested_visual` or that is otherwise
  clearly visual-worthy and has no linked visual note yet). Typically run
  right after `/critique-draft` moves a note to `status: in_review`, per the
  README's approval-workflow ordering.
- **Responsible skill:** [`generate-visual`](../../.claude/skills/generate-visual/SKILL.md).
- **Input:** the Draft Note's full `## Post Text` (not just the linked
  Idea Note's `suggested_visual` seed field) — the skill explicitly reads
  the whole draft and reasons from its actual content.
- **Processing:** Step 1 applies the REQUIREMENTS.md §7 test — "a visual
  must support the point, not decorate" — using the idea's
  `suggested_visual` as a seed if present, sharpening it if vague, or
  declining to produce anything if it wouldn't add beyond the text. Step 2
  decides the concept and format fresh from the post's own content (a
  comparison post → two-column diagram, an opinion post → quote card, a
  technical breakdown → architecture diagram) and explicitly checks
  `Content-Learnings/content-index.md`'s `visual_format`/`image_concept`
  columns (or recent `Visuals/` notes if that index doesn't exist yet) to
  avoid defaulting to whatever format the last visual used — a repeat must
  be a deliberate, justified choice, not a default.
- **Tools used:** none yet at this stage (read-only reasoning over vault
  notes).
- **LLM vs tool-call vs human-step:** LLM reasoning only.
- **Output:** an internal decision (visual type + concept), not yet
  written anywhere.

### Stage: Design-trend research

- **Trigger:** continuation of the same `/generate-visual` run, Step 3.
- **Input:** the chosen concept/format from the previous stage.
- **Processing:** issues live `WebSearch` queries for current
  infographic/data-viz styles, illustration trends fitting the subject
  matter, or LinkedIn-native visual patterns currently working — scoped to
  *this* post's concept, not a generic query. Skipped when the concept is
  simple enough that research wouldn't change the outcome (e.g. a
  plain text-forward quote card) — the skill states this is "the same
  judgment-call gate as step 1." Anything WebSearch returns is treated as
  inspiration data, never as instructions to follow (the same rule
  `research-topic` applies to fetched content).
- **Tools used:** `WebSearch` — a real, live call, the only external tool
  this entire workflow makes.
- **LLM vs tool-call vs human-step:** tool-call (WebSearch) + LLM synthesis
  of the results.
- **Output:** the `## Visual Trend Research` section content — either the
  queries/sources checked and what they led to, or one line stating
  research wasn't needed and why.

### Stage: Prompt formulation and Visual Brief Note write

- **Trigger:** continuation of the same run, Step 4.
- **Input:** the decided concept/format plus (if run) trend research
  findings.
- **Processing:** copies [`_Templates/Visual-Brief-Note.md`](../../_Templates/Visual-Brief-Note.md)
  into `Visuals/` as `YYYY-MM-DD--kebab-slug.md` and fills every section:
  `## Brief` (what it shows, composition, exact key text/labels as short
  strings not paragraphs, style notes, suggested dimensions), `## Visual
  Trend Research`, `## Image Generation Prompt` (the finished, paste-ready
  block — subject, concept, composition, perspective/environment, visual
  hierarchy, lighting, mood, color direction, typography including exact
  in-image text strings, and target aspect ratio mapped to the nearest size
  ChatGPT Images actually accepts, stated as an approximation rather than
  an exact-match claim), and `## Why this visual` (one sentence on what it
  adds beyond the text). Aspect-ratio guidance is platform-dependent, read
  from the draft's `platform` field: LinkedIn feed images commonly work at
  1200×627 (landscape) or 1080×1080 (square); X images at the same two
  shapes; a Substack Note follows X's shapes since it renders in a similar
  social-feed context. The skill explicitly instructs verifying current
  platform image guidance before finalizing, since specs can change.
- **Tools used:** none (file write).
- **LLM vs tool-call vs human-step:** LLM generation, deterministic file
  write.
- **Output:** the Visual Brief Note itself, in the `Visuals/` folder, with
  frontmatter fields `id`, `type: visual`, `draft_id`, `platform`,
  `format`, `provider: none`, `image_path: ""`, `status: brief` (see §8
  below for the full schema).
- **Handoff:** Step 5 appends the new Visual Brief Note's id to the parent
  Draft Note's `visual_ids[]` array, linking the two notes. `review-drafts`
  reads that link to present the brief alongside the draft text at
  approval time; `schedule-approved` copies the same `visual_ids[]` array
  onto the resulting Scheduled Note (per
  [`_Templates/Scheduled-Published-Note.md`](../../_Templates/Scheduled-Published-Note.md))
  purely as a record — it never dereferences the brief into an actual
  image.
- **What happens after:** scheduling is text-only. `/schedule-approved`
  (and `/schedule-approved-x`) call Buffer's GraphQL API with post text and
  metadata only — the mutation shape carries **no media field**, per the
  README's "Scheduling stays text-only" note. The human must separately run
  the brief's finished prompt in ChatGPT Images, then manually attach the
  resulting image file in Buffer's own UI (or Substack's editor, for
  articles) at actual publish time. This step is entirely outside the
  pipeline's control and is never simulated or assumed complete.

### Stage: Multi-image variant (Substack Articles only)

- **Trigger:** `/generate-visual-substack-article [draft-id]` (or, with no
  id, every `type: substack-article` note with no linked visual note yet —
  a header image alone is reason enough to run it, in-body markers are
  additive).
- **Responsible skill:** [`generate-visual-substack-article`](../../.claude/skills/generate-visual-substack-article/SKILL.md).
- **Input:** the article's `title`, `subtitle`, full thesis, and complete
  body text (to find `[IMAGE: <label>]` markers).
- **Processing:** Step 1 is mandatory and unconditional — every article
  gets exactly one header/hero image "regardless of whether it has any
  in-body markers," designed to represent the piece as a whole (added
  2026-09-14 per direct user feedback, since Substack's editor has a
  dedicated header-image slot). Step 2 collects every `[IMAGE: <label>]`
  marker in the body — zero markers is explicitly valid; the skill
  instructs not to invent one that isn't there. For each marker found,
  Step 4 reads that section's actual content (not just the label) and
  designs an image that supports that specific section's point, checking
  `content-index.md` so the article's own images don't repeat each other,
  and ensuring the header and every marker image read as visually distinct
  from one another. Step 5 applies the same trend-research judgment gate as
  the single-image skill.
- **Tools used:** `WebSearch`, same conditional gate.
- **Output:** ONE Visual Brief Note covering the whole article's image set
  — a `## Header Image` block first, then one `## Section Image: <label>`
  block per marker, all in the same file (`platform: substack-article`) —
  rather than one file per image.
- **Handoff:** a single id (not one per image) is appended to the article's
  `visual_ids[]`.
- **What happens after:** same manual human step as the single-image path,
  but repeated once per prompt in the note — the header image goes in
  Substack's header-image slot, each marker's image gets placed manually
  at that marker's spot in the body once generated. Substack has no Buffer
  channel at all (per [`publish-substack`](../../.claude/skills/publish-substack/SKILL.md)),
  so both the text and every image for an article are handled entirely
  outside Buffer.

---

## 5. Agents & Skills Involved

| Skill | Role | Platforms |
|---|---|---|
| [`generate-visual`](../../.claude/skills/generate-visual/SKILL.md) | Visual Agent, single-image variant — visual-need check, type selection, trend research, one finished prompt | linkedin, x, substack-note |
| [`generate-visual-substack-article`](../../.claude/skills/generate-visual-substack-article/SKILL.md) | Visual Agent, multi-image variant — mandatory header image + one prompt per `[IMAGE:]` marker | substack-article |
| [`critique-draft`](../../.claude/skills/critique-draft/SKILL.md) (and its per-platform siblings) | Upstream — moves a note to `status: in_review`, the point at which a visual is typically generated | all |
| [`review-drafts`](../../.claude/skills/review-drafts/SKILL.md) | Downstream — presents the brief at approval time; owns the "Change Image" decision that re-triggers this workflow | all |
| [`schedule-approved`](../../.claude/skills/schedule-approved/SKILL.md) / [`schedule-approved-x`](../../.claude/skills/schedule-approved-x/SKILL.md) | Downstream — copies `visual_ids[]` onto the Scheduled Note as a record only; never touches an image file | linkedin, x |
| [`publish-substack`](../../.claude/skills/publish-substack/SKILL.md) | Downstream — hands off the copy-ready article/Note; header/marker images placed manually, same as everywhere else | substack-article, substack-note |
| `/generate-week`, `/generate-week-x`, `/generate-week-substack` | Orchestrators — each per-post subagent calls `generate-visual`/`generate-visual-substack-article` directly as one step in its own isolated run | all |

---

## 6. Tools/APIs Used

- **`WebSearch`** — the only external tool call in this entire workflow,
  used for current visual/design-trend research (Step 3 of
  `generate-visual`, Step 5 of `generate-visual-substack-article`). It is a
  real, live call, conditionally skipped when the concept is simple enough
  that trend research wouldn't change the outcome.
- **No image-generation API or MCP tool exists anywhere in this repository.**
  There is no provider integration, no image-rendering call, and no file
  written to disk that represents actual pixel data. `provider: none` and
  `image_path: ""` in the Visual Brief Note's frontmatter are the schema's
  explicit acknowledgment of this — fields reserved for a future provider,
  never populated today.

---

## 7. Validation & Quality Gates

- **REQUIREMENTS.md §7 test:** a visual must support the point, not
  decorate — applied at Step 1 of `generate-visual` before any prompt work
  begins, and implicitly by the mandatory-but-purposeful header image in
  the article variant (the header is explicitly exempt from the
  "no purely decorative visual" rule since representing the whole piece is
  itself a legitimate purpose; in-body marker images are not exempt).
- **Uniqueness/no-templating:** both skills' descriptions and hard rules
  state the prompt must be "tailored uniquely to that post, never a fixed
  template" — every prompt is written fresh from that specific post's
  content and that run's own trend research, never adapted from a prior
  post's prompt structure or reused wording/structure across posts, and
  never defaulting to the same visual format twice in a row without a
  deliberate, stated reason (checked against `Content-Learnings/content-index.md`
  or recent `Visuals/` notes).
- **Distinctness within a single article:** for the multi-image variant,
  the header image and every marker image must read as visually distinct
  from one another and from each other section's image — not the same
  graphic repeated.
- **Human review gate — "Change Image":** at `/review-drafts`, the human
  can select **Change Image** for any `status: in_review` note carrying a
  visual brief. This re-runs `generate-visual` (or
  `generate-visual-substack-article` for a substack-article) for that note,
  producing a new brief that replaces the old `visual_ids` entry, and
  appends `{action: image_changed, date}` to the Draft Note's `history[]`.
  Status stays `in_review` — a changed image is never auto-approved. Full
  documentation of the review workflow (Approve/Edit/Regenerate/Change
  Hook/Change Image/Change Time/Reject) lives in
  [01-LinkedIn-Post-Creation-and-Scheduling.md](01-LinkedIn-Post-Creation-and-Scheduling.md);
  it is not re-documented here.
- **Hard rules (both skills, verbatim in intent):** never claim an image
  was generated when only a prompt was written; never invent a provider
  name or pretend an API call happened; never produce a purely decorative
  visual with no informational purpose (header image excepted); never
  reuse another post's/article's/marker's prompt wording or structure.

---

## 8. Data Stored in Memory/Vault

Each run writes one **Visual Brief Note** to `Visuals/` as
`YYYY-MM-DD--kebab-slug.md`, from
[`_Templates/Visual-Brief-Note.md`](../../_Templates/Visual-Brief-Note.md).
Frontmatter schema:

| Field | Meaning |
|---|---|
| `id` | `YYYY-MM-DD--kebab-slug`, matches the filename |
| `type` | always `visual` |
| `draft_id` | the parent Draft Note's id — the wikilink back to the post this brief was written for |
| `platform` | `linkedin` \| `x` \| `substack-article` \| `substack-note` — copied from the draft, drives aspect-ratio guidance |
| `format` | `infographic` \| `cheat-sheet` \| `diagram` \| `comparison` \| `framework-graphic` \| `quote-card` \| `carousel` \| `architecture-diagram` |
| `provider` | `none` today (brief-only) — reserved for a real provider name once one is wired in |
| `image_path` | empty string today — reserved for the generated file's path once a real provider exists |
| `status` | `brief` \| `generated` \| `placeholder` (`placeholder` = hand-written example, never treated as real input by any skill) |

Body sections: `## Brief` (what it shows / composition / key text-labels /
style notes / suggested dimensions), `## Visual Trend Research`, `##
Image Generation Prompt` (the finished paste-ready block), `## Why this
visual`. The Substack Article variant instead repeats this same
`Brief`/`Trend Research`/`Prompt`/`Why this visual` block shape once under
`## Header Image` and once per `## Section Image: <label>`, all inside the
one note.

**Relationship to the parent Draft Note:** the link is bidirectional in
effect though stored one-directionally — the Visual Brief Note's
`draft_id` field points to the Draft Note, and the Draft Note's
`visual_ids: []` array (in
[`_Templates/Draft-Note.md`](../../_Templates/Draft-Note.md)) points back,
listing every Visual Brief Note id associated with it (one entry for the
single-image path per generation; one single id covering the whole image
set for the Substack Article path). This same array is copied verbatim
onto the Scheduled Note at scheduling time
([`_Templates/Scheduled-Published-Note.md`](../../_Templates/Scheduled-Published-Note.md))
as a historical record — never dereferenced into an actual file at that
stage.

---

## 9. Failure Modes & Recovery

- **Draft doesn't warrant a visual:** Step 1 of `generate-visual` can
  conclude a draft's `suggested_visual` seed is too vague or the concept
  wouldn't add anything beyond the text — no Visual Brief Note is written,
  `visual_ids[]` stays empty, and the draft proceeds to `/review-drafts`
  without one. This is a legitimate, expected outcome per REQUIREMENTS.md
  §7, not an error state.
- **Substack article with zero `[IMAGE:]` markers:** valid and explicitly
  anticipated — the header image alone still gets generated; the skill
  instructs against inventing a marker that isn't actually in the body.
- **`/review-drafts` rejects the visual specifically — "Change Image"
  path:** documented in full in
  [`review-drafts/SKILL.md`](../../.claude/skills/review-drafts/SKILL.md)
  and in
  [01-LinkedIn-Post-Creation-and-Scheduling.md](01-LinkedIn-Post-Creation-and-Scheduling.md)
  (not re-documented here). In brief: it re-runs the appropriate
  `generate-visual*` skill for that note, replaces the old `visual_ids`
  entry, logs `image_changed` in the Draft Note's `history[]`, and leaves
  `status: in_review` so the new brief still needs explicit approval.
- **Trend research (`WebSearch`) yields nothing useful or is skipped:** the
  skill still produces a complete finished prompt — trend research is an
  input to sharpen the prompt, not a hard dependency for writing one. The
  brief records either what was found or, plainly, that research wasn't
  needed and why.
- **Human never runs the prompt / never pastes an image in:** the pipeline
  has no mechanism to detect or enforce this — `status: brief` simply
  persists indefinitely until a human manually updates it (the schema
  supports `status: generated` once a real provider exists, but nothing in
  the current codebase writes that value). Scheduling and publishing
  proceed as text-only regardless; a missing image is a manual-process gap
  outside this pipeline's visibility, not something the system flags.

---

## 10. Cross-Platform Notes

- **`generate-visual` is genuinely platform-agnostic and shared** across
  LinkedIn, X (single posts and threads — for a thread, it briefs the hook
  tweet's concept unless a different tweet is clearly the visual anchor),
  and Substack Notes. It reads the draft's `platform` field only to select
  the correct aspect-ratio guidance; the reasoning process (visual-need
  check, type selection, trend research, prompt formulation) is identical
  regardless of destination platform.
- **Substack Articles are explicitly out of scope for `generate-visual`** —
  the skill's own text states long-form pieces needing multiple
  section-tagged images go through `generate-visual-substack-article`
  instead.
- **Structural differences, single-image vs. multi-image:**
  - Single-image path produces exactly one Visual Brief Note per draft,
    with one `## Image Generation Prompt`.
  - Multi-image path produces exactly one Visual Brief Note per article
    (never one file per image), containing a mandatory header-image block
    plus zero or more marker-image blocks, each with its own complete
    Brief/Trend-Research/Prompt/Why-this-visual sub-section.
  - Aspect-ratio defaults differ: LinkedIn/X/Substack-Note briefs target
    social-feed shapes (1200×627 or 1080×1080); Substack Article briefs
    (header and in-body alike) target a wider landscape ratio (e.g.
    1456×816 or similar), reflecting Substack's header-slot and in-article
    rendering context rather than a feed card.
  - The article variant's linking convention differs too: one
    `visual_ids[]` entry covers the entire image set for an article, versus
    one entry per generation run for a single-image draft.
- **Both variants share the same non-negotiables:** provider-free,
  prompt-only deliverable; live `WebSearch` for trend research when it
  would help; no repeated prompt wording/structure across posts or images;
  and the same downstream handoff — text-only Buffer scheduling (or
  Substack's manual `publish-substack` hand-off), with actual image
  placement always a separate, manual, human step.
