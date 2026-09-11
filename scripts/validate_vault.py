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
        nonempty_scalar_keys=["id", "type", "idea_id", "category", "format",
                               "hook_style", "status"],
        nonempty_list_keys=["hashtags", "sources", "history"],
        status_key="status",
        status_enum={"draft", "in_review", "approved", "rejected",
                      "placeholder"},
        category_key="category",
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
    ),
    NoteSpec(
        "analytics", "Analytics", False,
        required_keys=["id", "type", "post_id", "status"],
        nonempty_scalar_keys=["id", "type", "post_id", "status"],
        nonempty_list_keys=[],
        status_key="status",
        status_enum={"active", "placeholder"},
        category_key=None,
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


def iter_notes(spec: NoteSpec) -> list[Path]:
    base = ROOT / spec.folder
    if not base.exists():
        return []
    pattern = "**/*.md" if spec.recursive else "*.md"
    return sorted(p for p in base.glob(pattern) if p.is_file())


def main() -> int:
    quiet = "--quiet" in sys.argv
    all_issues: list[Issue] = []
    checked = 0

    for spec in SPECS:
        for path in iter_notes(spec):
            checked += 1
            all_issues.extend(validate_note(path, spec))

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
