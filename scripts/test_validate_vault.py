#!/usr/bin/env python3
"""
Unit tests for scripts/validate_vault.py. Stdlib only (unittest), no
dependency on the real vault contents — every fixture is a temp file, so
this is safe to run anytime without touching real notes.

Usage:
    python3 scripts/test_validate_vault.py
"""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import validate_vault as vv  # noqa: E402


def spec_by(type_name: str, folder: str) -> vv.NoteSpec:
    for spec in vv.SPECS:
        if spec.type_name == type_name and spec.folder == folder:
            return spec
    raise AssertionError(f"no spec for type={type_name!r} folder={folder!r}")


DRAFT_SPEC = spec_by("draft", "Drafts")
SUBSTACK_ARTICLE_SPEC = spec_by("substack-article", "Drafts")


def write_note(tmp_dir: Path, stem: str, frontmatter: str, body: str = "content\n") -> Path:
    path = tmp_dir / f"{stem}.md"
    path.write_text(f"---\n{frontmatter}\n---\n\n{body}", encoding="utf-8")
    return path


class ParseFrontmatterTests(unittest.TestCase):
    def test_scalars_and_quoted_strings(self):
        data, body = vv.parse_frontmatter(
            '---\nid: 2026-01-01--x\ntitle: "Hello: World"\ncount: 3\n---\nBody text\n'
        )
        self.assertEqual(data["id"], "2026-01-01--x")
        self.assertEqual(data["title"], "Hello: World")
        self.assertEqual(data["count"], "3")
        self.assertEqual(body.strip(), "Body text")

    def test_inline_empty_list(self):
        data, _ = vv.parse_frontmatter("---\nhashtags: []\n---\n")
        self.assertTrue(vv.is_inline_empty_list(data["hashtags"]))

    def test_block_list(self):
        data, _ = vv.parse_frontmatter(
            "---\nsources:\n  - 2026-01-01--a\n  - 2026-01-02--b\n---\n"
        )
        self.assertEqual(vv.list_entry_count(data["sources"]), 2)

    def test_no_frontmatter_returns_none(self):
        data, _ = vv.parse_frontmatter("just a markdown file\n")
        self.assertIsNone(data)

    def test_inline_comment_stripped_but_not_inside_quotes(self):
        data, _ = vv.parse_frontmatter(
            '---\nformat: educational # a comment\ntitle: "value # not a comment"\n---\n'
        )
        self.assertEqual(data["format"], "educational")
        self.assertEqual(data["title"], "value # not a comment")


class ValidateNoteDraftTests(unittest.TestCase):
    """Covers the bug fixed 2026-09-14: hashtags: [] must be accepted for
    platform: x / substack-note, not just present-but-nonempty as LinkedIn
    drafts require by convention (enforced by write-draft, not the vault
    schema)."""

    def _minimal_draft_frontmatter(self, platform: str, hashtags: str) -> str:
        return (
            "id: 2026-01-01--example\n"
            "type: draft\n"
            "idea_id: 2026-01-01--idea\n"
            f"platform: {platform}\n"
            "category: AI\n"
            "format: ai-tech\n"
            "hook_style: test\n"
            f"hashtags: {hashtags}\n"
            "visual_ids: []\n"
            "sources:\n"
            "  - 2026-01-01--research\n"
            "viral_score: 7.0\n"
            "status: in_review\n"
            "history:\n"
            "  - action: created\n"
        )

    def test_x_draft_with_empty_hashtags_is_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(
                Path(tmp), "2026-01-01--example",
                self._minimal_draft_frontmatter("x", "[]"),
            )
            issues = vv.validate_note(path, DRAFT_SPEC)
            errors = [i for i in issues if i.level == "ERROR"]
            self.assertEqual(errors, [], f"unexpected errors: {errors}")

    def test_substack_note_draft_with_empty_hashtags_is_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(
                Path(tmp), "2026-01-01--example",
                self._minimal_draft_frontmatter("substack-note", "[]"),
            )
            issues = vv.validate_note(path, DRAFT_SPEC)
            errors = [i for i in issues if i.level == "ERROR"]
            self.assertEqual(errors, [], f"unexpected errors: {errors}")

    def test_linkedin_draft_with_hashtags_still_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(
                Path(tmp), "2026-01-01--example",
                self._minimal_draft_frontmatter("linkedin", '["#AI", "#ML"]'),
            )
            issues = vv.validate_note(path, DRAFT_SPEC)
            errors = [i for i in issues if i.level == "ERROR"]
            self.assertEqual(errors, [], f"unexpected errors: {errors}")

    def test_linkedin_draft_with_empty_hashtags_no_longer_errors(self):
        # Documents the deliberate post-fix behavior: the vault schema no
        # longer enforces "hashtags must be non-empty" for any platform —
        # that convention now lives in write-draft's own hard rules.
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(
                Path(tmp), "2026-01-01--example",
                self._minimal_draft_frontmatter("linkedin", "[]"),
            )
            issues = vv.validate_note(path, DRAFT_SPEC)
            errors = [i for i in issues if i.level == "ERROR"]
            self.assertEqual(errors, [], f"unexpected errors: {errors}")

    def test_empty_sources_still_errors(self):
        # Regression check: the fix only touched `hashtags`, not the other
        # nonempty_list_keys.
        fm = self._minimal_draft_frontmatter("x", "[]").replace(
            "sources:\n  - 2026-01-01--research\n", "sources: []\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(Path(tmp), "2026-01-01--example", fm)
            issues = vv.validate_note(path, DRAFT_SPEC)
            messages = [i.message for i in issues if i.level == "ERROR"]
            self.assertTrue(
                any("sources" in m for m in messages),
                f"expected a 'sources' error, got: {messages}",
            )

    def test_missing_required_field_errors(self):
        fm = self._minimal_draft_frontmatter("x", "[]").replace("category: AI\n", "")
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(Path(tmp), "2026-01-01--example", fm)
            issues = vv.validate_note(path, DRAFT_SPEC)
            messages = [i.message for i in issues if i.level == "ERROR"]
            self.assertTrue(any("category" in m for m in messages), messages)

    def test_invalid_platform_value_errors(self):
        fm = self._minimal_draft_frontmatter("bluesky", "[]")
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(Path(tmp), "2026-01-01--example", fm)
            issues = vv.validate_note(path, DRAFT_SPEC)
            messages = [i.message for i in issues if i.level == "ERROR"]
            self.assertTrue(any("platform" in m for m in messages), messages)

    def test_invalid_category_errors(self):
        fm = self._minimal_draft_frontmatter("x", "[]").replace(
            "category: AI\n", "category: NotAPillar\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(Path(tmp), "2026-01-01--example", fm)
            issues = vv.validate_note(path, DRAFT_SPEC)
            messages = [i.message for i in issues if i.level == "ERROR"]
            self.assertTrue(any("pillar" in m for m in messages), messages)

    def test_placeholder_status_skips_content_checks(self):
        # A placeholder with an invalid platform/empty sources should only
        # be flagged for missing required *keys*, never content emptiness.
        fm = self._minimal_draft_frontmatter("x", "[]").replace(
            "sources:\n  - 2026-01-01--research\n", "sources: []\n"
        ).replace("status: in_review\n", "status: placeholder\n")
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(Path(tmp), "2026-01-01--example", fm)
            issues = vv.validate_note(path, DRAFT_SPEC)
            errors = [i for i in issues if i.level == "ERROR"]
            self.assertEqual(errors, [], f"unexpected errors: {errors}")

    def test_id_mismatch_with_filename_errors(self):
        fm = self._minimal_draft_frontmatter("x", "[]").replace(
            "id: 2026-01-01--example\n", "id: 2026-01-01--different\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(Path(tmp), "2026-01-01--example", fm)
            issues = vv.validate_note(path, DRAFT_SPEC)
            messages = [i.message for i in issues if i.level == "ERROR"]
            self.assertTrue(any("filename stem" in m for m in messages), messages)


class ValidateNoteDraftPhase17Tests(unittest.TestCase):
    """Covers the Phase 17 (Post Writer) Draft Note additions: the four new
    optional frontmatter fields (hook_formula, engagement_goal,
    founders_angle, spine_id). All must stay backward-compatible with every
    draft written before Phase 17, which has none of these keys at all."""

    def _minimal_draft_frontmatter(self, extra: str = "", idea_id: str = "2026-01-01--idea") -> str:
        return (
            "id: 2026-01-01--example\n"
            "type: draft\n"
            f'idea_id: "{idea_id}"\n'
            "platform: linkedin\n"
            "category: AI\n"
            "format: ai-tech\n"
            "hook_style: test\n"
            f"{extra}"
            'hashtags: ["#AI"]\n'
            "visual_ids: []\n"
            "sources:\n"
            "  - 2026-01-01--research\n"
            "viral_score: 7.0\n"
            "status: in_review\n"
            "history:\n"
            "  - action: created\n"
        )

    def test_pre_phase17_draft_with_no_new_fields_is_still_valid(self):
        # No hook_formula/engagement_goal/founders_angle/spine_id keys at
        # all — exactly what every draft written before this phase looks
        # like. Must not error.
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(
                Path(tmp), "2026-01-01--example", self._minimal_draft_frontmatter(),
            )
            issues = vv.validate_note(path, DRAFT_SPEC)
            errors = [i for i in issues if i.level == "ERROR"]
            self.assertEqual(errors, [], f"unexpected errors: {errors}")

    def test_new_fields_present_but_empty_is_valid(self):
        extra = (
            'hook_formula: ""\n'
            'engagement_goal: ""\n'
            'founders_angle: ""\n'
            'spine_id: ""\n'
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(
                Path(tmp), "2026-01-01--example",
                self._minimal_draft_frontmatter(extra),
            )
            issues = vv.validate_note(path, DRAFT_SPEC)
            errors = [i for i in issues if i.level == "ERROR"]
            self.assertEqual(errors, [], f"unexpected errors: {errors}")

    def test_new_fields_present_with_valid_values_is_valid(self):
        # idea-path draft: idea_id set, spine_id absent — the ordinary case.
        extra = (
            "hook_formula: F10\n"
            "engagement_goal: comments\n"
            "founders_angle: A5\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(
                Path(tmp), "2026-01-01--example",
                self._minimal_draft_frontmatter(extra),
            )
            issues = vv.validate_note(path, DRAFT_SPEC)
            errors = [i for i in issues if i.level == "ERROR"]
            self.assertEqual(errors, [], f"unexpected errors: {errors}")

    def test_spine_path_draft_with_empty_idea_id_is_valid(self):
        # spine-path draft (Phase 17 --spine): idea_id blank, spine_id set —
        # must NOT trip the old idea_id-required assumption.
        extra = (
            "hook_formula: F10\n"
            "engagement_goal: comments\n"
            "spine_id: 2026-01-01--spine\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(
                Path(tmp), "2026-01-01--example",
                self._minimal_draft_frontmatter(extra, idea_id=""),
            )
            issues = vv.validate_note(path, DRAFT_SPEC)
            errors = [i for i in issues if i.level == "ERROR"]
            self.assertEqual(errors, [], f"unexpected errors: {errors}")

    def test_both_idea_id_and_spine_id_set_errors(self):
        extra = "spine_id: 2026-01-01--spine\n"
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(
                Path(tmp), "2026-01-01--example",
                self._minimal_draft_frontmatter(extra, idea_id="2026-01-01--idea"),
            )
            issues = vv.validate_note(path, DRAFT_SPEC)
            messages = [i.message for i in issues if i.level == "ERROR"]
            self.assertTrue(any("both set" in m for m in messages), messages)

    def test_neither_idea_id_nor_spine_id_set_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(
                Path(tmp), "2026-01-01--example",
                self._minimal_draft_frontmatter(idea_id=""),
            )
            issues = vv.validate_note(path, DRAFT_SPEC)
            messages = [i.message for i in issues if i.level == "ERROR"]
            self.assertTrue(any("Neither" in m for m in messages), messages)

    def test_invalid_engagement_goal_errors(self):
        extra = "engagement_goal: virality\n"
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(
                Path(tmp), "2026-01-01--example",
                self._minimal_draft_frontmatter(extra),
            )
            issues = vv.validate_note(path, DRAFT_SPEC)
            messages = [i.message for i in issues if i.level == "ERROR"]
            self.assertTrue(any("engagement_goal" in m for m in messages), messages)

    def test_each_closed_list_engagement_goal_value_is_valid(self):
        for goal in sorted(vv.ENGAGEMENT_GOALS):
            with tempfile.TemporaryDirectory() as tmp:
                path = write_note(
                    Path(tmp), "2026-01-01--example",
                    self._minimal_draft_frontmatter(f"engagement_goal: {goal}\n"),
                )
                issues = vv.validate_note(path, DRAFT_SPEC)
                errors = [i for i in issues if i.level == "ERROR"]
                self.assertEqual(errors, [], f"goal={goal!r} unexpected errors: {errors}")


class ValidateNoteDraftPhase20Tests(unittest.TestCase):
    """Covers the Phase 20 (Repurposer) Draft Note additions: the two new
    optional frontmatter fields (source_type, source_link). Same
    backward-compatible pattern as Phase 17's four fields above — every
    draft written before Phase 20, which has neither key at all, must keep
    validating unchanged."""

    def _minimal_draft_frontmatter(self, extra: str = "") -> str:
        return (
            "id: 2026-01-01--example\n"
            "type: draft\n"
            'idea_id: "2026-01-01--idea"\n'
            "platform: linkedin\n"
            "category: AI\n"
            "format: ai-tech\n"
            "hook_style: test\n"
            f"{extra}"
            'hashtags: ["#AI"]\n'
            "visual_ids: []\n"
            "sources:\n"
            "  - 2026-01-01--research\n"
            "viral_score: 7.0\n"
            "status: in_review\n"
            "history:\n"
            "  - action: created\n"
        )

    def test_pre_phase20_draft_with_no_new_fields_is_still_valid(self):
        # No source_type/source_link keys at all — exactly what every draft
        # written before this phase (including Phase 17 drafts) looks like.
        # Must not error.
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(
                Path(tmp), "2026-01-01--example", self._minimal_draft_frontmatter(),
            )
            issues = vv.validate_note(path, DRAFT_SPEC)
            errors = [i for i in issues if i.level == "ERROR"]
            self.assertEqual(errors, [], f"unexpected errors: {errors}")

    def test_new_fields_present_but_empty_is_valid(self):
        extra = (
            'source_type: ""\n'
            'source_link: ""\n'
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(
                Path(tmp), "2026-01-01--example",
                self._minimal_draft_frontmatter(extra),
            )
            issues = vv.validate_note(path, DRAFT_SPEC)
            errors = [i for i in issues if i.level == "ERROR"]
            self.assertEqual(errors, [], f"unexpected errors: {errors}")

    def test_new_fields_present_with_valid_values_is_valid(self):
        extra = (
            "source_type: tweet\n"
            'source_link: "https://x.com/example/status/1"\n'
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(
                Path(tmp), "2026-01-01--example",
                self._minimal_draft_frontmatter(extra),
            )
            issues = vv.validate_note(path, DRAFT_SPEC)
            errors = [i for i in issues if i.level == "ERROR"]
            self.assertEqual(errors, [], f"unexpected errors: {errors}")

    def test_invalid_source_type_errors(self):
        extra = "source_type: podcast\n"
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(
                Path(tmp), "2026-01-01--example",
                self._minimal_draft_frontmatter(extra),
            )
            issues = vv.validate_note(path, DRAFT_SPEC)
            messages = [i.message for i in issues if i.level == "ERROR"]
            self.assertTrue(any("source_type" in m for m in messages), messages)

    def test_each_closed_list_source_type_value_is_valid(self):
        for src_type in sorted(vv.SOURCE_TYPES):
            with tempfile.TemporaryDirectory() as tmp:
                path = write_note(
                    Path(tmp), "2026-01-01--example",
                    self._minimal_draft_frontmatter(f"source_type: {src_type}\n"),
                )
                issues = vv.validate_note(path, DRAFT_SPEC)
                errors = [i for i in issues if i.level == "ERROR"]
                self.assertEqual(errors, [], f"source_type={src_type!r} unexpected errors: {errors}")

    def test_repurposed_draft_with_no_idea_id_or_spine_id_is_valid(self):
        # A /repurpose-post draft has neither an Idea Note nor a Story Bank
        # Post Spine behind it — its grounding is the source content itself,
        # recorded via source_type/source_link. This must NOT trip the
        # exactly_one_of(idea_id, spine_id) "neither is set" check.
        fm = (
            "id: 2026-01-01--example\n"
            "type: draft\n"
            'idea_id: ""\n'
            "platform: linkedin\n"
            "category: AI\n"
            "format: ai-tech\n"
            "hook_style: test\n"
            "source_type: tweet\n"
            'source_link: "https://x.com/example/status/1"\n'
            'hashtags: ["#AI"]\n'
            "visual_ids: []\n"
            "sources:\n"
            '  - "https://x.com/example/status/1"\n'
            "viral_score: 0\n"
            "status: draft\n"
            "history:\n"
            "  - action: created\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(Path(tmp), "2026-01-01--example", fm)
            issues = vv.validate_note(path, DRAFT_SPEC)
            errors = [i for i in issues if i.level == "ERROR"]
            self.assertEqual(errors, [], f"unexpected errors: {errors}")

    def test_no_idea_id_spine_id_or_source_type_still_errors(self):
        # Regression guard: a plain, non-repurposed draft still needs
        # exactly one of idea_id/spine_id — an empty source_type must not
        # silently exempt it.
        with tempfile.TemporaryDirectory() as tmp:
            fm = self._minimal_draft_frontmatter().replace(
                'idea_id: "2026-01-01--idea"\n', 'idea_id: ""\n'
            )
            path = write_note(Path(tmp), "2026-01-01--example", fm)
            issues = vv.validate_note(path, DRAFT_SPEC)
            messages = [i.message for i in issues if i.level == "ERROR"]
            self.assertTrue(any("Neither" in m for m in messages), messages)


STORY_BANK_SPEC = spec_by("story-bank", "Content-Learnings")
HOOK_FORMULAS_SPEC = spec_by("hook-formulas", "Content-Learnings")


class ValidateNoteStoryBankTests(unittest.TestCase):
    """Covers the Phase 15 (Interviewer) story-bank NoteSpec: a single
    living doc (same pattern as playbook.md) with no `status` field on the
    note itself, so is_placeholder is always False for this type — content
    checks always apply, unlike every other note type which can opt out via
    `status: placeholder`."""

    def _minimal_story_bank_frontmatter(self, last_updated: str = "2026-09-16") -> str:
        return (
            "id: story-bank\n"
            "type: story-bank\n"
            "version: 1\n"
            f"last_updated: {last_updated}\n"
        )

    def test_valid_story_bank_note_has_no_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(
                Path(tmp), "story-bank", self._minimal_story_bank_frontmatter(),
            )
            issues = vv.validate_note(path, STORY_BANK_SPEC)
            errors = [i for i in issues if i.level == "ERROR"]
            self.assertEqual(errors, [], f"unexpected errors: {errors}")

    def test_missing_last_updated_field_errors(self):
        fm = self._minimal_story_bank_frontmatter().replace(
            "last_updated: 2026-09-16\n", ""
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(Path(tmp), "story-bank", fm)
            issues = vv.validate_note(path, STORY_BANK_SPEC)
            messages = [i.message for i in issues if i.level == "ERROR"]
            self.assertTrue(any("last_updated" in m for m in messages), messages)

    def test_empty_last_updated_value_errors(self):
        # The template's own placeholder value (`last_updated: ""`) is
        # correct for an unpopulated template, but a real note (this note
        # type has no `placeholder` status to exempt it) must have it
        # filled in once it actually exists in the vault.
        fm = self._minimal_story_bank_frontmatter(last_updated='""')
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(Path(tmp), "story-bank", fm)
            issues = vv.validate_note(path, STORY_BANK_SPEC)
            messages = [i.message for i in issues if i.level == "ERROR"]
            self.assertTrue(any("last_updated" in m for m in messages), messages)

    def test_id_mismatch_with_filename_errors(self):
        fm = self._minimal_story_bank_frontmatter().replace(
            "id: story-bank\n", "id: story-bank-wrong\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(Path(tmp), "story-bank", fm)
            issues = vv.validate_note(path, STORY_BANK_SPEC)
            messages = [i.message for i in issues if i.level == "ERROR"]
            self.assertTrue(any("filename stem" in m for m in messages), messages)


class ValidateNoteHookFormulasTests(unittest.TestCase):
    """Covers the Phase 16 (Hook Extractor) hook-formulas NoteSpec: the
    second registered spec for Content-Learnings/, added alongside
    story-bank — same single-living-doc shape, no `status` field."""

    def _minimal_hook_formulas_frontmatter(self, last_updated: str = "2026-09-17") -> str:
        return (
            "id: hook-formulas\n"
            "type: hook-formulas\n"
            "version: 1\n"
            f"last_updated: {last_updated}\n"
        )

    def test_valid_hook_formulas_note_has_no_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(
                Path(tmp), "hook-formulas",
                self._minimal_hook_formulas_frontmatter(),
            )
            issues = vv.validate_note(path, HOOK_FORMULAS_SPEC)
            errors = [i for i in issues if i.level == "ERROR"]
            self.assertEqual(errors, [], f"unexpected errors: {errors}")

    def test_missing_last_updated_field_errors(self):
        fm = self._minimal_hook_formulas_frontmatter().replace(
            "last_updated: 2026-09-17\n", ""
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(Path(tmp), "hook-formulas", fm)
            issues = vv.validate_note(path, HOOK_FORMULAS_SPEC)
            messages = [i.message for i in issues if i.level == "ERROR"]
            self.assertTrue(any("last_updated" in m for m in messages), messages)

    def test_id_mismatch_with_filename_errors(self):
        fm = self._minimal_hook_formulas_frontmatter().replace(
            "id: hook-formulas\n", "id: hook-formulas-wrong\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(Path(tmp), "hook-formulas", fm)
            issues = vv.validate_note(path, HOOK_FORMULAS_SPEC)
            messages = [i.message for i in issues if i.level == "ERROR"]
            self.assertTrue(any("filename stem" in m for m in messages), messages)


HUMANIZER_RULES_SPEC = spec_by("humanizer-rules", "Content-Learnings")


class ValidateNoteHumanizerRulesTests(unittest.TestCase):
    """Covers the Phase 18 (Humanizer) humanizer-rules NoteSpec: the third
    registered spec for Content-Learnings/, added alongside story-bank and
    hook-formulas — same single-living-doc shape, no `status` field."""

    def _minimal_humanizer_rules_frontmatter(self, last_updated: str = "2026-09-17") -> str:
        return (
            "id: humanizer-rules\n"
            "type: humanizer-rules\n"
            "version: 1\n"
            f"last_updated: {last_updated}\n"
        )

    def test_valid_humanizer_rules_note_has_no_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(
                Path(tmp), "humanizer-rules",
                self._minimal_humanizer_rules_frontmatter(),
            )
            issues = vv.validate_note(path, HUMANIZER_RULES_SPEC)
            errors = [i for i in issues if i.level == "ERROR"]
            self.assertEqual(errors, [], f"unexpected errors: {errors}")

    def test_missing_last_updated_field_errors(self):
        fm = self._minimal_humanizer_rules_frontmatter().replace(
            "last_updated: 2026-09-17\n", ""
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(Path(tmp), "humanizer-rules", fm)
            issues = vv.validate_note(path, HUMANIZER_RULES_SPEC)
            messages = [i.message for i in issues if i.level == "ERROR"]
            self.assertTrue(any("last_updated" in m for m in messages), messages)

    def test_id_mismatch_with_filename_errors(self):
        fm = self._minimal_humanizer_rules_frontmatter().replace(
            "id: humanizer-rules\n", "id: humanizer-rules-wrong\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(Path(tmp), "humanizer-rules", fm)
            issues = vv.validate_note(path, HUMANIZER_RULES_SPEC)
            messages = [i.message for i in issues if i.level == "ERROR"]
            self.assertTrue(any("filename stem" in m for m in messages), messages)


ALGORITHM_RULES_SPEC = spec_by("algorithm-rules", "Content-Learnings")


class ValidateNoteAlgorithmRulesTests(unittest.TestCase):
    """Covers the Phase 19 (Post Audit) algorithm-rules NoteSpec: the
    fourth registered spec for Content-Learnings/, added alongside
    story-bank, hook-formulas, and humanizer-rules — same single-living-doc
    shape, no `status` field."""

    def _minimal_algorithm_rules_frontmatter(self, last_updated: str = "2026-09-17") -> str:
        return (
            "id: algorithm-rules\n"
            "type: algorithm-rules\n"
            "version: 1\n"
            f"last_updated: {last_updated}\n"
        )

    def test_valid_algorithm_rules_note_has_no_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(
                Path(tmp), "algorithm-rules",
                self._minimal_algorithm_rules_frontmatter(),
            )
            issues = vv.validate_note(path, ALGORITHM_RULES_SPEC)
            errors = [i for i in issues if i.level == "ERROR"]
            self.assertEqual(errors, [], f"unexpected errors: {errors}")

    def test_missing_last_updated_field_errors(self):
        fm = self._minimal_algorithm_rules_frontmatter().replace(
            "last_updated: 2026-09-17\n", ""
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(Path(tmp), "algorithm-rules", fm)
            issues = vv.validate_note(path, ALGORITHM_RULES_SPEC)
            messages = [i.message for i in issues if i.level == "ERROR"]
            self.assertTrue(any("last_updated" in m for m in messages), messages)

    def test_id_mismatch_with_filename_errors(self):
        fm = self._minimal_algorithm_rules_frontmatter().replace(
            "id: algorithm-rules\n", "id: algorithm-rules-wrong\n"
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = write_note(Path(tmp), "algorithm-rules", fm)
            issues = vv.validate_note(path, ALGORITHM_RULES_SPEC)
            messages = [i.message for i in issues if i.level == "ERROR"]
            self.assertTrue(any("filename stem" in m for m in messages), messages)


class RouteNoteSpecTests(unittest.TestCase):
    """Covers the multi-spec-per-folder routing added alongside the
    Substack expansion (Drafts/ now holds both `draft` and
    `substack-article` notes)."""

    def test_single_spec_folder_ignores_type_content(self):
        # A folder with exactly one spec (e.g. Post-Ideas/) must keep
        # matching regardless of what `type` says — this is the
        # pre-existing behavior for every non-Drafts/non-Published-Posts
        # folder and must not regress.
        idea_spec = spec_by("idea", "Post-Ideas")
        match = vv.route_note_spec({"type": "something-else"}, [idea_spec])
        self.assertIs(match, idea_spec)

    def test_routes_draft_type_to_draft_spec(self):
        match = vv.route_note_spec(
            {"type": "draft"}, [DRAFT_SPEC, SUBSTACK_ARTICLE_SPEC]
        )
        self.assertIs(match, DRAFT_SPEC)

    def test_routes_substack_article_type_to_its_spec(self):
        match = vv.route_note_spec(
            {"type": "substack-article"}, [DRAFT_SPEC, SUBSTACK_ARTICLE_SPEC]
        )
        self.assertIs(match, SUBSTACK_ARTICLE_SPEC)

    def test_unrecognized_type_returns_none(self):
        match = vv.route_note_spec(
            {"type": "carousel"}, [DRAFT_SPEC, SUBSTACK_ARTICLE_SPEC]
        )
        self.assertIsNone(match)

    def test_missing_type_returns_none_in_multi_spec_folder(self):
        match = vv.route_note_spec({}, [DRAFT_SPEC, SUBSTACK_ARTICLE_SPEC])
        self.assertIsNone(match)

    def test_routes_story_bank_type_to_story_bank_spec(self):
        # Content-Learnings/ became multi-spec in Phase 16 (hook-formulas
        # added alongside story-bank) — same by-type routing must apply.
        match = vv.route_note_spec(
            {"type": "story-bank"}, [STORY_BANK_SPEC, HOOK_FORMULAS_SPEC]
        )
        self.assertIs(match, STORY_BANK_SPEC)

    def test_routes_hook_formulas_type_to_hook_formulas_spec(self):
        match = vv.route_note_spec(
            {"type": "hook-formulas"}, [STORY_BANK_SPEC, HOOK_FORMULAS_SPEC]
        )
        self.assertIs(match, HOOK_FORMULAS_SPEC)

    def test_routes_humanizer_rules_type_to_humanizer_rules_spec(self):
        match = vv.route_note_spec(
            {"type": "humanizer-rules"},
            [STORY_BANK_SPEC, HOOK_FORMULAS_SPEC, HUMANIZER_RULES_SPEC],
        )
        self.assertIs(match, HUMANIZER_RULES_SPEC)

    def test_routes_algorithm_rules_type_to_algorithm_rules_spec(self):
        match = vv.route_note_spec(
            {"type": "algorithm-rules"},
            [STORY_BANK_SPEC, HOOK_FORMULAS_SPEC, HUMANIZER_RULES_SPEC,
             ALGORITHM_RULES_SPEC],
        )
        self.assertIs(match, ALGORITHM_RULES_SPEC)

    def test_unmatched_type_in_content_learnings_returns_none(self):
        # playbook.md / voice-guide.md carry `type: playbook` / `type:
        # voice-guide` — neither matches any registered spec.
        match = vv.route_note_spec(
            {"type": "playbook"},
            [STORY_BANK_SPEC, HOOK_FORMULAS_SPEC, HUMANIZER_RULES_SPEC,
             ALGORITHM_RULES_SPEC],
        )
        self.assertIsNone(match)


class PermissiveFolderTests(unittest.TestCase):
    """Covers the fix for the regression Phase 15's report flagged: once
    Content-Learnings/ gained a second registered spec (hook-formulas,
    Phase 16), the pre-existing single-spec-per-folder shortcut no longer
    protects files like playbook.md/voice-guide.md, which carry a `type`
    that matches neither registered spec. `permissive_folder` makes an
    unmatched type in such a folder a silent skip, not a new error,
    while Drafts/-style folders (where every real note is expected to
    match a registered type) keep erroring on an unmatched type."""

    def test_content_learnings_specs_are_permissive(self):
        self.assertTrue(vv.is_permissive_folder([STORY_BANK_SPEC, HOOK_FORMULAS_SPEC]))

    def test_drafts_specs_are_not_permissive(self):
        self.assertFalse(vv.is_permissive_folder([DRAFT_SPEC, SUBSTACK_ARTICLE_SPEC]))

    def test_single_spec_folder_permissiveness_is_irrelevant(self):
        # Doesn't matter either way for single-spec folders, since
        # route_note_spec never returns None for them in the first place —
        # documented here so the invariant is explicit, not assumed.
        idea_spec = spec_by("idea", "Post-Ideas")
        match = vv.route_note_spec({"type": "anything"}, [idea_spec])
        self.assertIsNotNone(match)

    def test_unmatched_type_in_permissive_folder_is_not_an_error(self):
        # End-to-end: playbook.md-shaped note in a Content-Learnings-shaped
        # multi-spec folder must route to None *and* be treated as a skip,
        # not surfaced as an "unrecognized type" error.
        specs = [STORY_BANK_SPEC, HOOK_FORMULAS_SPEC]
        data = {"type": "playbook"}
        match = vv.route_note_spec(data, specs)
        self.assertIsNone(match)
        self.assertTrue(vv.is_permissive_folder(specs))

    def test_unmatched_type_in_non_permissive_folder_stays_an_error(self):
        specs = [DRAFT_SPEC, SUBSTACK_ARTICLE_SPEC]
        data = {"type": "carousel"}
        match = vv.route_note_spec(data, specs)
        self.assertIsNone(match)
        self.assertFalse(vv.is_permissive_folder(specs))


class GroupSpecsByFolderTests(unittest.TestCase):
    def test_drafts_folder_has_two_specs(self):
        by_folder = vv.group_specs_by_folder(vv.SPECS)
        self.assertEqual(len(by_folder["Drafts"]), 2)
        type_names = {s.type_name for s in by_folder["Drafts"]}
        self.assertEqual(type_names, {"draft", "substack-article"})

    def test_published_posts_folder_has_two_specs(self):
        by_folder = vv.group_specs_by_folder(vv.SPECS)
        self.assertEqual(len(by_folder["Published-Posts"]), 2)
        type_names = {s.type_name for s in by_folder["Published-Posts"]}
        self.assertEqual(type_names, {"post", "substack-ready"})

    def test_content_learnings_folder_has_four_specs(self):
        # Was single-spec through Phase 15; Phase 16 (Hook Extractor) adds
        # hook-formulas alongside story-bank; Phase 18 (Humanizer) adds
        # humanizer-rules alongside both; Phase 19 (Post Audit) adds
        # algorithm-rules alongside all three.
        by_folder = vv.group_specs_by_folder(vv.SPECS)
        self.assertEqual(len(by_folder["Content-Learnings"]), 4)
        type_names = {s.type_name for s in by_folder["Content-Learnings"]}
        self.assertEqual(
            type_names,
            {"story-bank", "hook-formulas", "humanizer-rules",
             "algorithm-rules"},
        )


if __name__ == "__main__":
    unittest.main()
