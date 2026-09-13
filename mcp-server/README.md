# linkedin-vault MCP server

Bridges this vault + the real Buffer scheduling API into Claude Desktop, so
you can schedule posts and pull stats from a normal Desktop chat instead of
Claude Code.

## What it exposes

- `list_notes`, `read_note`, `write_note` — generic vault file access.
- `buffer_check_credentials`, `buffer_discover_channels` — setup/diagnostics.
- `buffer_create_post` — real Buffer `createPost` mutation (schedules a live
  LinkedIn post).
- `buffer_get_post_metrics` — real Buffer post-metrics query.

Credentials (`BUFFER_ACCESS_TOKEN`, `BUFFER_CHANNEL_ID`) are read from this
vault's own `.env` at call time — they are not duplicated into the Desktop
config.

## Setup (already done once, kept here for reference)

```bash
cd mcp-server
npm install
```

Registered in `~/Library/Application Support/Claude/claude_desktop_config.json`
under `mcpServers.linkedin-vault`, pointing `VAULT_ROOT` at this vault's
absolute path. **Restart Claude Desktop** after any change to that file for
it to pick up the server.

## Using it

1. In Claude Desktop, create a Project for this vault.
2. Paste the contents of `DESKTOP-PROJECT-INSTRUCTIONS.md` into that
   Project's custom instructions.
3. Make sure the `linkedin-vault` MCP server is enabled for that
   conversation/Project (Desktop will prompt to allow tool calls the first
   time each tool is used).
4. Chat normally: "schedule this week's approved posts", "how did last
   week's posts perform", "what's still waiting in review", etc.

## Safety notes

- `buffer_create_post` makes a real, live scheduling call — same one
  `/schedule-approved` uses in Claude Code. There's no dry-run mode.
- All vault file access is sandboxed to this vault's folder (path traversal
  outside it is rejected).
- Nothing here auto-approves drafts — scheduling only ever acts on notes
  already `status: approved`.
