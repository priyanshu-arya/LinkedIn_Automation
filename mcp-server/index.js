#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import fs from "node:fs/promises";
import path from "node:path";

const VAULT_ROOT = process.env.VAULT_ROOT;
if (!VAULT_ROOT) {
  console.error("VAULT_ROOT env var is required (path to the LinkedIn Agentic AI vault).");
  process.exit(1);
}

// Buffer credentials live in the vault's own .env, not in the Desktop config,
// so secrets aren't duplicated into a second file.
async function loadVaultEnv() {
  const envPath = path.join(VAULT_ROOT, ".env");
  const out = {};
  try {
    const raw = await fs.readFile(envPath, "utf8");
    for (const line of raw.split("\n")) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith("#")) continue;
      const eq = trimmed.indexOf("=");
      if (eq === -1) continue;
      out[trimmed.slice(0, eq).trim()] = trimmed.slice(eq + 1).trim();
    }
  } catch {
    // no .env file — treated as no credentials below
  }
  return out;
}

function looksPlaceholder(v) {
  if (!v) return true;
  const low = v.toLowerCase();
  return low.includes("your_") || low.includes("<") || low.includes("placeholder") || low === "changeme";
}

function resolveInVault(relPath) {
  const resolved = path.resolve(VAULT_ROOT, relPath);
  const rootResolved = path.resolve(VAULT_ROOT);
  if (resolved !== rootResolved && !resolved.startsWith(rootResolved + path.sep)) {
    throw new Error(`Path escapes the vault root: ${relPath}`);
  }
  return resolved;
}

function parseFrontmatter(content) {
  const match = content.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  const fm = {};
  if (match) {
    for (const line of match[1].split("\n")) {
      const m = line.match(/^([A-Za-z0-9_]+):\s*(.*)$/);
      if (m) fm[m[1]] = m[2].trim().replace(/^["']|["']$/g, "");
    }
  }
  return fm;
}

async function walk(dir, recursive) {
  const entries = await fs.readdir(dir, { withFileTypes: true });
  let files = [];
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (recursive) files = files.concat(await walk(full, recursive));
    } else if (entry.name.endsWith(".md")) {
      files.push(full);
    }
  }
  return files;
}

const server = new McpServer({
  name: "linkedin-vault",
  version: "1.0.0",
});

server.tool(
  "list_notes",
  "List markdown notes under a folder in the LinkedIn vault (path relative to vault root, e.g. 'Drafts' or 'Content-Research/AI'). Returns each note's path and parsed frontmatter fields. Optionally filter by a frontmatter 'status' value.",
  {
    folder: z.string().describe("Folder relative to the vault root, e.g. 'Drafts', 'Scheduled', 'Post-Ideas'."),
    status: z.string().optional().describe("If set, only return notes whose frontmatter 'status' field equals this value."),
    recursive: z.boolean().optional().default(true).describe("Recurse into subfolders (default true)."),
  },
  async ({ folder, status, recursive }) => {
    const dir = resolveInVault(folder);
    let files;
    try {
      files = await walk(dir, recursive ?? true);
    } catch (err) {
      return { content: [{ type: "text", text: `Error reading folder '${folder}': ${err.message}` }], isError: true };
    }
    const results = [];
    for (const file of files) {
      const content = await fs.readFile(file, "utf8");
      const fm = parseFrontmatter(content);
      if (status && fm.status !== status) continue;
      results.push({ path: path.relative(VAULT_ROOT, file), frontmatter: fm });
    }
    return { content: [{ type: "text", text: JSON.stringify(results, null, 2) }] };
  }
);

server.tool(
  "read_note",
  "Read the full raw content (frontmatter + body) of one note, path relative to the vault root.",
  { path: z.string() },
  async ({ path: relPath }) => {
    const full = resolveInVault(relPath);
    try {
      const content = await fs.readFile(full, "utf8");
      return { content: [{ type: "text", text: content }] };
    } catch (err) {
      return { content: [{ type: "text", text: `Error reading '${relPath}': ${err.message}` }], isError: true };
    }
  }
);

server.tool(
  "write_note",
  "Create or overwrite a note with the given full content (frontmatter + body), path relative to the vault root. Creates parent folders if needed. This overwrites the whole file — read the note first if you need to preserve existing content.",
  { path: z.string(), content: z.string() },
  async ({ path: relPath, content }) => {
    const full = resolveInVault(relPath);
    await fs.mkdir(path.dirname(full), { recursive: true });
    await fs.writeFile(full, content, "utf8");
    return { content: [{ type: "text", text: `Wrote ${relPath} (${content.length} bytes).` }] };
  }
);

server.tool(
  "buffer_check_credentials",
  "Check whether Buffer API credentials are present and non-placeholder in the vault's .env. Never returns the actual secret values.",
  {},
  async () => {
    const env = await loadVaultEnv();
    const token = env.BUFFER_ACCESS_TOKEN;
    const channelId = env.BUFFER_CHANNEL_ID;
    const result = {
      tokenPresent: Boolean(token) && !looksPlaceholder(token),
      channelIdPresent: Boolean(channelId) && !looksPlaceholder(channelId),
    };
    return { content: [{ type: "text", text: JSON.stringify(result, null, 2) }] };
  }
);

async function bufferGraphQL(query, variables) {
  const env = await loadVaultEnv();
  const token = env.BUFFER_ACCESS_TOKEN;
  if (!token || looksPlaceholder(token)) {
    throw new Error("BUFFER_ACCESS_TOKEN is missing or a placeholder in the vault's .env.");
  }
  const res = await fetch("https://api.buffer.com", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ query, variables }),
  });
  const json = await res.json();
  if (json.errors) {
    throw new Error(`Buffer GraphQL error: ${JSON.stringify(json.errors)}`);
  }
  return json.data;
}

server.tool(
  "buffer_discover_channels",
  "One-time setup helper: lists Buffer organizations and their connected channels, to find the LinkedIn channel id. Only needed if BUFFER_CHANNEL_ID is not yet known.",
  {},
  async () => {
    try {
      const orgData = await bufferGraphQL(
        `query GetOrganizations { account { organizations { id } } }`,
        {}
      );
      const orgId = orgData?.account?.organizations?.[0]?.id;
      if (!orgId) {
        return { content: [{ type: "text", text: "No organization found on this Buffer account." }], isError: true };
      }
      const chData = await bufferGraphQL(
        `query GetChannels($organizationId: OrganizationId!) { channels(input: { organizationId: $organizationId }) { id name displayName service } }`,
        { organizationId: orgId }
      );
      return { content: [{ type: "text", text: JSON.stringify(chData.channels, null, 2) }] };
    } catch (err) {
      return { content: [{ type: "text", text: err.message }], isError: true };
    }
  }
);

server.tool(
  "buffer_create_post",
  "Schedule a real LinkedIn post via Buffer's createPost mutation. This makes a real, live scheduling call — only use it for a draft that is actually status:approved. Returns the real Buffer post id and due time on success, or the exact error on failure. Never fabricate a post id yourself if this errors.",
  {
    text: z.string().describe("Final post text to schedule."),
    dueAt: z.string().describe("ISO 8601 datetime for when the post should go out, e.g. '2026-09-16T09:00:00Z'."),
  },
  async ({ text, dueAt }) => {
    const env = await loadVaultEnv();
    const channelId = env.BUFFER_CHANNEL_ID;
    if (!channelId || looksPlaceholder(channelId)) {
      return {
        content: [{ type: "text", text: "BUFFER_CHANNEL_ID is missing or a placeholder in the vault's .env. Run buffer_discover_channels first." }],
        isError: true,
      };
    }
    const mutation = `mutation CreatePost($text: String!, $channelId: ChannelId!, $dueAt: DateTime!) {
      createPost(input: {
        text: $text
        channelId: $channelId
        schedulingType: automatic
        mode: customScheduled
        dueAt: $dueAt
      }) {
        ... on PostActionSuccess { post { id text dueAt } }
        ... on MutationError { message }
      }
    }`;
    try {
      const data = await bufferGraphQL(mutation, { text, channelId, dueAt });
      const result = data.createPost;
      if (result.message) {
        return { content: [{ type: "text", text: `Buffer rejected the post: ${result.message}` }], isError: true };
      }
      return { content: [{ type: "text", text: JSON.stringify(result.post, null, 2) }] };
    } catch (err) {
      return { content: [{ type: "text", text: err.message }], isError: true };
    }
  }
);

server.tool(
  "buffer_get_post_metrics",
  "Query real performance metrics for a post already scheduled via Buffer. Metrics refresh once daily and can be null for up to ~24h after scheduling — report null as 'not yet available', never as zero.",
  { postId: z.string().describe("The real Buffer post id (from buffer_create_post's result, or an existing note's buffer_post_id field).") },
  async ({ postId }) => {
    const query = `query GetPostMetrics($id: PostId!) { post(input: { id: $id }) { id metrics { type name value unit } } }`;
    try {
      const data = await bufferGraphQL(query, { id: postId });
      return { content: [{ type: "text", text: JSON.stringify(data.post, null, 2) }] };
    } catch (err) {
      return { content: [{ type: "text", text: err.message }], isError: true };
    }
  }
);

const transport = new StdioServerTransport();
await server.connect(transport);
