# AGENTS.md

Project-level instructions, auto-loaded by Codex CLI/IDE at the start of every session in this repository. This mirrors [`CLAUDE.md`](CLAUDE.md) (Claude Code's equivalent auto-loaded file) — if you edit one, update the other.

## Mandatory: follow the documented workflow for every task

This repository's behavior is fully documented, stage by stage, in [`Documentation/Workflows/`](Documentation/Workflows/00-Overview.md). Before doing **any** task here — drafting a post, scheduling, pulling analytics, profile work, research, engagement replies, repurposing, anything — you must:

1. Read [`Documentation/Workflows/00-Overview.md`](Documentation/Workflows/00-Overview.md) if you haven't already this session. It indexes all 13 feature workflows and the shared building blocks (research/idea pool, human approval gate, visual briefs, Buffer integration, playbook feedback loop) so you don't have to re-derive them.
2. Identify which documented workflow matches the request — LinkedIn posting, X posting, profile optimization, LinkedIn/X analytics, content research, visual generation, Substack, story bank/hooks, quality/safety/originality tools, repurposing, engagement tools, or employee advocacy — and read that specific document before acting.
3. Execute the task by following that document's stage order and the exact skill named for each stage (`.claude/skills/<name>/SKILL.md`). Do not invent a shortcut, skip a documented stage (e.g. never skip `/audit-draft` or `/review-drafts` for content that's meant to go through them), or call a tool/API a stage doesn't document.
4. Carry forward every hard rule the documentation states, even if the user doesn't repeat it: never fabricate a Buffer post id or metric, never set `status: approved` outside the review/approval step, never mark Substack content `published` without explicit user confirmation that they posted it themselves, never write a playbook rule without ≥3 verified samples, never present an unverified web claim as fact.
5. If a request doesn't match any documented workflow, say so explicitly and ask how to proceed, rather than forcing it into the nearest workflow or inventing new behavior.

See [§4 of the workflow overview](Documentation/Workflows/00-Overview.md#4-known-gaps-inconsistencies--open-questions) for known gaps between the documented behavior and the current implementation — don't silently paper over those either; flag them the same way if they're relevant to a task.

## Codex-specific notes

- Codex doesn't have Claude Code's `.claude/skills/` slash-command auto-triggering. When a documented workflow stage calls for a skill, open and follow that skill's `SKILL.md` directly (you have filesystem access to the repo), or tell the user which file you're following (e.g. "following the steps in `.claude/skills/write-draft/SKILL.md`").
- If this session is connected only through the `linkedin-vault` MCP server's tools (`list_notes` / `read_note` / `write_note` / `buffer_create_post` / `buffer_get_post_metrics` / `buffer_discover_channels`, no direct filesystem skill access), follow [`mcp-server/DESKTOP-PROJECT-INSTRUCTIONS.md`](mcp-server/DESKTOP-PROJECT-INSTRUCTIONS.md) for the exact scheduling/analytics tool-call rules — it's already Claude-agnostic and written for exactly this case, so read it directly rather than re-deriving the same logic.
- Register the same MCP server Claude Desktop uses (`~/.codex/config.toml`, see the README's [Connecting to Codex](README.md#-connecting-to-codex-cli--ide) section) if this session needs real Buffer scheduling/metrics rather than just vault file access.
- Run Codex from inside this repository (or with this directory as the workspace root) so its sandboxed filesystem/shell access is scoped to the vault, matching how Claude Code's is scoped.

## Ground rules carried from the rest of the repo

- **Human-in-the-loop, always.** No draft is ever scheduled or published without an explicit human approval step. No autonomous mode exists in this repo — don't build a shortcut around this even if asked to "just post it."
- **The vault is the memory.** State lives in Markdown note frontmatter (`status` field, folder location), not in a database or in your own context. Read the actual note before acting on it — don't assume its state from an earlier turn.
- **Primary-source grounding.** Never state a fact, statistic, or quote that wasn't actually verified via a live fetch — see `REQUIREMENTS.md` and each skill's own `SKILL.md` for what counts as verified in that context.
- **Full spec:** [`REQUIREMENTS.md`](REQUIREMENTS.md). **Full architecture, skills matrix, and setup:** [`README.md`](README.md).
