#!/usr/bin/env python3
"""
Validate every real note in the vault against its template's required
frontmatter fields. Stdlib only — no PyYAML dependency, so it runs on any
Python 3 install without a `pip install` step.

This is a deliberately narrow parser: it understands the specific YAML
subset these templates actually use (scalars, quoted strings, inline
`[...]` lists, and block `- item` / `- key: value` lists) — it is not a
general YAML parser and will not handle arbitrary frontmatter.

Usage:
    python3 scripts/validate_vault.py [--quiet]

Exit code 0 if no errors (warnings are still printed). Exit code 1 if any
note has an error-level problem.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PILLARS = {
    "AI", "Career", "Developer-Tools", "GenAI", "Machine-Learning",
    "Deep-Learning", "Interview-Preparation", "Data-Analytics",
    "Data-Engineering", "Mathematics", "Problem-Solving", "Algorithms",
    "Research-Papers", "Psychology-AI", "AI-Healthcare", "Resources",
}

# Single-value `platform` field, checked when a spec sets platform_key.
# (Idea Notes carry a plural `platforms: []` instead — not deeply validated
# here, since this parser doesn't parse inline YAML lists into items.)
PLATFORMS = {"linkedin", "x", "substack-article", "substack-note"}

# Single-value `engagement_goal` field (Draft Notes, Phase 17 Post Writer),
# checked when a spec sets engagement_goal_key — same optional-if-present
# pattern as PLATFORMS/platform_key below. Closed 5-value list per
# REQUIREMENTS.md §28; the field itself is optional (blank on drafts written
# before Phase 17), so this only fires when a value is actually present.
ENGAGEMENT_GOALS = {"likes", "comments", "shares", "saves", "profile-visits"}

# Single-value `source_type` field (Draft Notes, Phase 20 Repurposer),
# checked when a spec sets source_type_key — same optional-if-present pattern
# as ENGAGEMENT_GOALS/engagement_goal_key above. Closed 5-value list per
# REQUIREMENTS.md §31; the field itself is optional (blank/absent on every
# draft not produced by /repurpose-post), so this only fires when a value is
# actually present and non-empty. `none` is deliberately NOT a member of this
# set — a non-repurposed draft should simply leave the field blank rather
# than write the literal string "none" (both validate the same way here,
# since an empty check happens first, but the closed list itself only lists
# real source types).
SOURCE_TYPES = {"tweet", "thread", "youtube", "blog", "newsletter"}

ID_RE = re.compile(r"^\d{4}-\d{2}-\d{2}--[a-z0-9]+(-[a-z0-9]+)*$")


@dataclass
class NoteSpec:
    type_name: str
    folder: str  # relative to ROOT, non-recursive unless recursive=True
    recursive: bool
    required_keys: list[str]
    nonempty_scalar_keys: list[str]
    nonempty_list_keys: list[str]
    status_key: str | None
    status_enum: set[str] | None
    category_key: str | None  # checked against PILLARS if present
    platform_key: str | None = None  # checked against PLATFORMS if present
    # checked against ENGAGEMENT_GOALS if present (Phase 17 Post Writer);
    # None for every spec except "draft", since only Draft Notes carry this
    # field.
    engagement_goal_key: str | None = None
    # checked against SOURCE_TYPES if present (Phase 20 Repurposer); None for
    # every spec except "draft", since only Draft Notes carry this field.
    source_type_key: str | None = None
    # A pair of keys where exactly one must be non-empty (Phase 17 Post
    # Writer's idea-path-vs-spine-path split): None for every spec except
    # "draft", where it's ("idea_id", "spine_id") — an idea-drafted note
    # sets idea_id and leaves spine_id blank, a spine-drafted note is the
    # reverse, and a note setting both or neither is a real schema error,
    # not a valid state either drafting path can produce.
    exactly_one_of: tuple[str, str] | None = None
    # When True, and this spec shares a folder with other specs, a note in
    # that folder whose `type` matches none of the folder's registered
    # specs is silently left unvalidated instead of reported as an error.
    # Content-Learnings/ holds several living-doc types (`playbook`,
    # `voice-guide`) that have never had a NoteSpec of their own and were
    # never meant to be strictly validated — only specific opted-in types
    # (`story-bank`, `hook-formulas`) are. Folders like Drafts/ and
    # Published-Posts/ leave this False (the default): every real note
    # there is expected to match one of the folder's registered types, so
    # an unmatched type is a real error (e.g. a missing/typo'd `type`
    # field), not an intentionally-unvalidated file.
    permissive_folder: bool = False


SPECS = [
    NoteSpec(
        "research", "Content-Research", True,
        required_keys=["id", "type", "topic", "category", "date_discovered",
                        "status", "trend_score", "relevance_score",
                        "freshness_score", "authority_score",
                        "engagement_potential", "originality_score",
                        "educational_value", "sources"],
        nonempty_scalar_keys=["id", "type", "topic", "category",
                               "date_discovered", "status"],
        nonempty_list_keys=["sources"],
        status_key="status",
        status_enum={"new", "used", "placeholder"},
        category_key="category",
    ),
    NoteSpec(
        "idea", "Post-Ideas", False,
        required_keys=["id", "type", "topic", "angle", "why_it_matters",
                        "target_audience", "format", "hook", "category",
                        "content_type", "estimated_engagement",
                        "suggested_visual", "sources", "status",
                        "rank_score"],
        nonempty_scalar_keys=["id", "type", "topic", "angle",
                               "why_it_matters", "target_audience", "format",
                               "hook", "category", "content_type", "status"],
        nonempty_list_keys=["sources"],
        status_key="status",
        status_enum={"candidate", "selected", "drafted", "rejected",
                      "placeholder"},
        category_key="category",
    ),
    NoteSpec(
        "draft", "Drafts", False,
        required_keys=["id", "type", "idea_id", "category", "format",
                        "hook_style", "hashtags", "visual_ids", "sources",
                        "viral_score", "status", "history"],
        # `idea_id` stays in required_keys (the key must be present, even
        # if blank on a spine-drafted note) but is deliberately NOT in
        # nonempty_scalar_keys below — its own emptiness is checked, in
        # combination with `spine_id`, by exactly_one_of instead. A note
        # missing the key entirely is still a real schema error either way.
        nonempty_scalar_keys=["id", "type", "category", "format",
                               "hook_style", "status"],
        # `hashtags` deliberately excluded from nonempty_list_keys: it's a
        # required *field* (must be present) but its correct value is an
        # empty list for platform: x / substack-note (0-2 or no hashtags by
        # design, see voice-guide-x.md/voice-guide-substack.md) — only
        # LinkedIn's write-draft convention (3-5 tags) treats it as
        # never-empty, and that's enforced by that skill's own hard rules,
        # not a vault-wide schema requirement.
        #
        # `hook_formula`, `engagement_goal`, and `founders_angle` (Phase 17
        # Post Writer, REQUIREMENTS.md §28) are deliberately excluded from
        # required_keys/nonempty_scalar_keys entirely — they are optional
        # fields, blank by default, so every Draft Note written before this
        # field existed keeps validating with zero changes. `engagement_goal`
        # gets a closed-list check below (via engagement_goal_key) when it
        # *is* present; `hook_formula` and `founders_angle` reference rows in
        # living docs (hook-formulas.md/founders-angle-library.md) that this
        # parser doesn't cross-reference, so they're left unchecked beyond
        # existing as free-form optional strings. `spine_id` is handled by
        # exactly_one_of below, together with `idea_id`, instead of its own
        # nonempty check.
        #
        # `source_type` and `source_link` (Phase 20 Repurposer,
        # REQUIREMENTS.md §31) are the same kind of backward-compatible
        # optional addition — excluded from required_keys/
        # nonempty_scalar_keys so every Draft Note written before Phase 20
        # keeps validating unchanged. `source_type` gets a closed-list check
        # below (via source_type_key) when it *is* present and non-empty;
        # `source_link` is a free-form URL/blank string this parser doesn't
        # otherwise validate (no URL-shape check, same as other free-text
        # fields elsewhere in this schema).
        nonempty_list_keys=["sources", "history"],
        status_key="status",
        status_enum={"draft", "in_review", "approved", "rejected",
                      "placeholder"},
        category_key="category",
        platform_key="platform",
        engagement_goal_key="engagement_goal",
        source_type_key="source_type",
        exactly_one_of=("idea_id", "spine_id"),
    ),
    NoteSpec(
        "substack-article", "Drafts", False,
        required_keys=["id", "type", "platform", "idea_id", "category",
                        "title", "seo_description", "sources", "viral_score",
                        "status", "history"],
        nonempty_scalar_keys=["id", "type", "platform", "idea_id",
                               "category", "title", "status"],
        nonempty_list_keys=["sources", "history"],
        status_key="status",
        status_enum={"draft", "in_review", "approved", "rejected",
                      "placeholder"},
        category_key="category",
        platform_key="platform",
    ),
    NoteSpec(
        "visual", "Visuals", False,
        required_keys=["id", "type", "draft_id", "format", "provider",
                        "image_path", "status"],
        nonempty_scalar_keys=["id", "type", "draft_id", "format",
                               "provider", "status"],
        nonempty_list_keys=[],
        status_key="status",
        status_enum={"brief", "generated", "placeholder"},
        category_key=None,
        platform_key="platform",
    ),
    NoteSpec(
        "post", "Scheduled", False,
        required_keys=["id", "type", "draft_id", "final_text",
                        "buffer_post_id", "scheduled_date", "scheduled_time",
                        "publish_status", "category", "format", "length",
                        "hook_style", "hashtags", "sources"],
        nonempty_scalar_keys=["id", "type", "draft_id", "final_text",
                               "scheduled_date", "scheduled_time",
                               "publish_status", "category"],
        nonempty_list_keys=[],
        status_key="publish_status",
        status_enum={"scheduled", "published", "failed", "placeholder"},
        category_key="category",
        platform_key="platform",
    ),
    NoteSpec(
        "post", "Published-Posts", False,
        required_keys=["id", "type", "draft_id", "final_text",
                        "buffer_post_id", "scheduled_date", "scheduled_time",
                        "publish_status", "category", "format", "length",
                        "hook_style", "hashtags", "sources"],
        nonempty_scalar_keys=["id", "type", "draft_id", "final_text",
                               "scheduled_date", "scheduled_time",
                               "publish_status", "category",
                               "buffer_post_id"],
        nonempty_list_keys=[],
        status_key="publish_status",
        status_enum={"scheduled", "published", "failed", "placeholder"},
        category_key="category",
        platform_key="platform",
    ),
    NoteSpec(
        "substack-ready", "Substack-Ready", False,
        required_keys=["id", "type", "draft_id", "platform",
                        "publish_status", "category", "format", "sources"],
        nonempty_scalar_keys=["id", "type", "draft_id", "platform",
                               "publish_status", "category"],
        nonempty_list_keys=[],
        status_key="publish_status",
        status_enum={"ready_to_publish", "published", "placeholder"},
        category_key="category",
        platform_key="platform",
    ),
    NoteSpec(
        "substack-ready", "Published-Posts", False,
        required_keys=["id", "type", "draft_id", "platform",
                        "publish_status", "category", "format", "sources"],
        nonempty_scalar_keys=["id", "type", "draft_id", "platform",
                               "publish_status", "category",
                               "publish_confirmed_date"],
        nonempty_list_keys=[],
        status_key="publish_status",
        status_enum={"ready_to_publish", "published", "placeholder"},
        category_key="category",
        platform_key="platform",
    ),
    NoteSpec(
        "analytics", "Analytics", False,
        required_keys=["id", "type", "post_id", "status"],
        nonempty_scalar_keys=["id", "type", "post_id", "status"],
        nonempty_list_keys=[],
        status_key="status",
        status_enum={"active", "placeholder"},
        category_key=None,
        platform_key="platform",
    ),
    NoteSpec(
        "profile-optimization", "Profile-Optimization", False,
        required_keys=["id", "type", "source_pdf", "role_1_title",
                        "role_2_title", "primary_position", "current_score",
                        "projected_score", "status", "history"],
        nonempty_scalar_keys=["id", "type", "source_pdf", "role_1_title",
                               "role_2_title", "primary_position", "status"],
        nonempty_list_keys=["history"],
        status_key="status",
        status_enum={"draft", "delivered", "placeholder"},
        category_key=None,
    ),
    # Single living doc (same pattern as Content-Learnings/playbook.md,
    # REQUIREMENTS.md §13/§26) — no `status` field on this note type, so
    # status_key is None and every row-level placeholder-vs-real distinction
    # lives inside the note's own tables (a `status` column per row), not on
    # the note's frontmatter. Note: no NoteSpec previously existed for
    # playbook.md/voice-guide.md either — Content-Learnings/ wasn't
    # validated at all before this entry; this adds validation scoped only
    # to `type: story-bank`. `permissive_folder=True` because Content-
    # Learnings/ now (as of Phase 16) holds a second registered type
    # (`hook-formulas`) alongside several unregistered ones (`playbook`,
    # `voice-guide`) — those must stay silently unvalidated, not start
    # erroring, once this folder has more than one spec (see
    # `permissive_folder`'s definition on NoteSpec above).
    NoteSpec(
        "story-bank", "Content-Learnings", False,
        required_keys=["id", "type", "version", "last_updated"],
        nonempty_scalar_keys=["id", "type", "version", "last_updated"],
        nonempty_list_keys=[],
        status_key=None,
        status_enum=None,
        category_key=None,
        permissive_folder=True,
    ),
    # Added Phase 16 (Hook Extractor). Same single-living-doc shape as
    # story-bank.md above — see Content-Learnings/hook-formulas.md's own
    # header. This is the second registered spec for Content-Learnings/,
    # which is what makes that folder route by `type` instead of the old
    # single-spec-always-matches shortcut; permissive_folder=True for the
    # same reason as story-bank's entry above.
    NoteSpec(
        "hook-formulas", "Content-Learnings", False,
        required_keys=["id", "type", "version", "last_updated"],
        nonempty_scalar_keys=["id", "type", "version", "last_updated"],
        nonempty_list_keys=[],
        status_key=None,
        status_enum=None,
        category_key=None,
        permissive_folder=True,
    ),
    # Added Phase 18 (Humanizer). Same single-living-doc shape as
    # story-bank.md/hook-formulas.md above — see Content-Learnings/
    # humanizer-rules.md's own header. This is the third registered spec
    # for Content-Learnings/; permissive_folder=True for the same reason as
    # the two entries above (playbook.md/voice-guide.md and friends must
    # stay silently unvalidated, not start erroring, once the folder has
    # more than one spec).
    NoteSpec(
        "humanizer-rules", "Content-Learnings", False,
        required_keys=["id", "type", "version", "last_updated"],
        nonempty_scalar_keys=["id", "type", "version", "last_updated"],
        nonempty_list_keys=[],
        status_key=None,
        status_enum=None,
        category_key=None,
        permissive_folder=True,
    ),
    # Added Phase 19 (Post Audit). Same single-living-doc shape as
    # story-bank.md/hook-formulas.md/humanizer-rules.md above — see
    # Content-Learnings/algorithm-rules.md's own header. This is the fourth
    # registered spec for Content-Learnings/; permissive_folder=True for the
    # same reason as the three entries above (playbook.md/voice-guide.md and
    # friends must stay silently unvalidated, not start erroring, once the
    # folder has more than one spec).
    NoteSpec(
        "algorithm-rules", "Content-Learnings", False,
        required_keys=["id", "type", "version", "last_updated"],
        nonempty_scalar_keys=["id", "type", "version", "last_updated"],
        nonempty_list_keys=[],
        status_key=None,
        status_enum=None,
        category_key=None,
        permissive_folder=True,
    ),
]


def parse_frontmatter(text: str) -> tuple[dict | None, str]:
    """Minimal frontmatter parser for this repo's fixed template shapes."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return None, text

    fm_lines = lines[1:end]
    body = "\n".join(lines[end + 1:])
    data: dict[str, object] = {}
    i, n = 0, len(fm_lines)

    while i < n:
        raw = fm_lines[i]
        if not raw.strip() or raw.strip().startswith("#") or raw[0] in " \t":
            i += 1
            continue
        if ":" not in raw:
            i += 1
            continue

        key, _, rest = raw.partition(":")
        key = key.strip()
        value_part = strip_inline_comment(rest.strip())

        if value_part == "":
            # Possibly a block list on following indented lines.
            j = i + 1
            items: list[str] = []
            while j < n and fm_lines[j].strip() != "" and fm_lines[j][0] in " \t":
                items.append(fm_lines[j])
                j += 1
            data[key] = items if items else ""
            i = j
        else:
            val = value_part
            if len(val) >= 2 and val[0] == val[-1] and val[0] in ("'", '"'):
                val = val[1:-1]
            data[key] = val
            i += 1

    return data, body


def strip_inline_comment(value: str) -> str:
    """Strip a trailing ' # comment', respecting simple quoting."""
    quote = None
    for idx, ch in enumerate(value):
        if ch in ("'", '"'):
            if quote is None:
                quote = ch
            elif quote == ch:
                quote = None
        elif ch == "#" and quote is None and idx > 0 and value[idx - 1] == " ":
            return value[:idx - 1].rstrip()
    return value


def list_entry_count(raw_lines: list) -> int:
    if not isinstance(raw_lines, list):
        return 0
    return sum(1 for line in raw_lines if line.lstrip().startswith("- "))


def is_inline_empty_list(value: object) -> bool:
    return isinstance(value, str) and value.strip() in ("[]", "")


@dataclass
class Issue:
    level: str  # "ERROR" | "WARN"
    path: Path
    message: str


def validate_note(path: Path, spec: NoteSpec) -> list[Issue]:
    issues: list[Issue] = []
    text = path.read_text(encoding="utf-8", errors="replace")
    data, _body = parse_frontmatter(text)

    if data is None:
        return [Issue("ERROR", path, "No parseable YAML frontmatter block ('---' ... '---') found")]

    status_val = str(data.get(spec.status_key, "")) if spec.status_key else ""
    is_placeholder = status_val == "placeholder"

    for key in spec.required_keys:
        if key not in data:
            issues.append(Issue("ERROR", path, f"Missing required field: {key}"))

    if is_placeholder:
        # Placeholder notes are explicitly exempt from content-completeness
        # checks (that's the whole point of the status) — schema presence
        # above still applies, but skip empty/enum/pillar checks below.
        return issues

    for key in spec.nonempty_scalar_keys:
        if key in data:
            val = data[key]
            if isinstance(val, list) or (isinstance(val, str) and val.strip() == ""):
                issues.append(Issue("ERROR", path, f"Required field '{key}' is empty"))

    if spec.exactly_one_of is not None:
        key_a, key_b = spec.exactly_one_of
        val_a = str(data.get(key_a, "") or "").strip()
        val_b = str(data.get(key_b, "") or "").strip()
        # Phase 20 (Repurposer): a draft grounded in `source_type` (a
        # tweet/thread/video/article, not an Idea Note or Story Bank Post
        # Spine) legitimately has neither idea_id nor spine_id set. Treat a
        # real, non-"none" source_type as a third valid grounding for the
        # "neither is set" branch only — it does not exempt a note from the
        # "both idea_id and spine_id set" error above, which stays a real
        # schema conflict regardless of source_type.
        src_type_val = ""
        if spec.source_type_key:
            src_type_val = str(data.get(spec.source_type_key, "") or "").strip()
        has_source_grounding = bool(src_type_val) and src_type_val != "none"
        if val_a and val_b:
            issues.append(Issue(
                "ERROR", path,
                f"'{key_a}' and '{key_b}' are both set — a note must be "
                f"grounded in exactly one, never both",
            ))
        elif not val_a and not val_b and not has_source_grounding:
            issues.append(Issue(
                "ERROR", path,
                f"Neither '{key_a}' nor '{key_b}' is set — a note must be "
                f"grounded in exactly one (or, for a /repurpose-post draft, "
                f"a non-empty 'source_type')",
            ))

    for key in spec.nonempty_list_keys:
        if key in data:
            val = data[key]
            if isinstance(val, list):
                if list_entry_count(val) == 0:
                    issues.append(Issue("ERROR", path, f"Required list field '{key}' has no entries"))
            elif is_inline_empty_list(val):
                issues.append(Issue("ERROR", path, f"Required list field '{key}' is empty ([])"))

    if spec.status_enum is not None and spec.status_key in data:
        if status_val and status_val not in spec.status_enum:
            issues.append(Issue(
                "ERROR", path,
                f"'{spec.status_key}: {status_val}' is not one of {sorted(spec.status_enum)}",
            ))

    if spec.category_key and spec.category_key in data:
        cat = str(data[spec.category_key]).strip()
        if cat and cat not in PILLARS:
            issues.append(Issue(
                "ERROR", path,
                f"'{spec.category_key}: {cat}' is not one of the 16 fixed pillar folders",
            ))

    if spec.platform_key and spec.platform_key in data:
        plat = str(data[spec.platform_key]).strip()
        if plat and plat not in PLATFORMS:
            issues.append(Issue(
                "ERROR", path,
                f"'{spec.platform_key}: {plat}' is not one of {sorted(PLATFORMS)}",
            ))

    if spec.engagement_goal_key and spec.engagement_goal_key in data:
        goal = str(data[spec.engagement_goal_key]).strip()
        if goal and goal not in ENGAGEMENT_GOALS:
            issues.append(Issue(
                "ERROR", path,
                f"'{spec.engagement_goal_key}: {goal}' is not one of {sorted(ENGAGEMENT_GOALS)}",
            ))

    if spec.source_type_key and spec.source_type_key in data:
        src_type = str(data[spec.source_type_key]).strip()
        if src_type and src_type not in SOURCE_TYPES:
            issues.append(Issue(
                "ERROR", path,
                f"'{spec.source_type_key}: {src_type}' is not one of {sorted(SOURCE_TYPES)}",
            ))

    note_id = str(data.get("id", "")).strip()
    if note_id:
        if not ID_RE.match(note_id):
            issues.append(Issue("WARN", path, f"id '{note_id}' doesn't match YYYY-MM-DD--kebab-slug"))
        if note_id != path.stem:
            issues.append(Issue("ERROR", path, f"frontmatter id '{note_id}' != filename stem '{path.stem}'"))

    if "placeholder" in text.lower() and not is_placeholder:
        issues.append(Issue(
            "WARN", path,
            "Body/frontmatter mentions 'placeholder' but status isn't 'placeholder' — "
            "verify this isn't leaked example content",
        ))

    return issues


def iter_notes(folder: str, recursive: bool) -> list[Path]:
    base = ROOT / folder
    if not base.exists():
        return []
    pattern = "**/*.md" if recursive else "*.md"
    return sorted(p for p in base.glob(pattern) if p.is_file())


def group_specs_by_folder(specs: list[NoteSpec]) -> dict[str, list[NoteSpec]]:
    by_folder: dict[str, list[NoteSpec]] = {}
    for spec in specs:
        by_folder.setdefault(spec.folder, []).append(spec)
    return by_folder


def route_note_spec(data: dict | None, specs: list[NoteSpec]) -> NoteSpec | None:
    """Pick which of a folder's specs a note belongs to, by its `type`
    field. A folder with exactly one spec always matches it, regardless of
    `type` content (preserves pre-multi-spec behavior for single-shape
    folders). A folder with several specs (e.g. Drafts/ holding both plain
    `draft` and `substack-article` notes) requires `type` to name one of
    them; returns None if it doesn't (caller reports that as an error)."""
    if len(specs) == 1:
        return specs[0]
    note_type = str(data.get("type", "")).strip() if data else ""
    return next((s for s in specs if s.type_name == note_type), None)


def is_permissive_folder(specs: list[NoteSpec]) -> bool:
    """True if an unmatched `type` in this folder should be silently
    skipped rather than reported as an error (see `permissive_folder` on
    NoteSpec). Any spec in the folder opting in is enough — the folder is
    the real unit here, all specs sharing one folder are expected to agree."""
    return any(s.permissive_folder for s in specs)


def main() -> int:
    quiet = "--quiet" in sys.argv
    all_issues: list[Issue] = []
    checked = 0

    # Group specs by folder — a folder with >1 spec (e.g. Drafts/ holding
    # both plain `draft` and `substack-article` notes) routes each note by
    # its own `type` field rather than assuming one schema per folder.
    specs_by_folder = group_specs_by_folder(SPECS)

    for folder, specs in specs_by_folder.items():
        recursive = any(s.recursive for s in specs)
        for path in iter_notes(folder, recursive):
            checked += 1
            data = None
            if len(specs) > 1:
                text = path.read_text(encoding="utf-8", errors="replace")
                data, _ = parse_frontmatter(text)
            match = route_note_spec(data, specs)
            if match is None:
                if is_permissive_folder(specs):
                    # Intentionally unvalidated file type in this folder
                    # (e.g. Content-Learnings/playbook.md) — not an error.
                    continue
                all_issues.append(Issue(
                    "ERROR", path,
                    f"Unrecognized or missing 'type' for a note in {folder}/ "
                    f"(expected one of {sorted(s.type_name for s in specs)})",
                ))
                continue
            all_issues.extend(validate_note(path, match))

    errors = [i for i in all_issues if i.level == "ERROR"]
    warnings = [i for i in all_issues if i.level == "WARN"]

    if not quiet:
        for issue in all_issues:
            rel = issue.path.relative_to(ROOT)
            print(f"[{issue.level}] {rel}: {issue.message}")

    print(f"\nChecked {checked} notes — {len(errors)} error(s), {len(warnings)} warning(s).")
    if errors:
        print("FAIL")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
