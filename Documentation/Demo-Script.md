# Demo Video — Shot List & Script

A ready-to-record script for a 2-3 minute walkthrough of this repo, for embedding in `README.md`. Nothing here is automated — an AI agent working inside this repo cannot capture screen video; this is written so a human can record it in one take with QuickTime (macOS, built in: `Cmd+Shift+5`), Loom, or `asciinema` for a terminal-only cut.

## Before recording

- Use a **disposable or test topic** for the drafting steps below — whatever gets drafted will be a real note written into your vault (`Content-Research/`, `Post-Ideas/`, `Drafts/`).
- **Stop before `/schedule-approved`.** That command makes a real, live Buffer API call — the one thing in this whole pipeline that reaches an external service and can't be undone by closing the recording. Show the approval screen and narrate what happens next instead of actually running it, unless you're deliberately demoing against a disposable test Buffer channel.
- Record at your terminal/IDE's default font size — viewers will be reading code and file trees, not squinting at a dense 10pt terminal.
- Have `Documentation/Workflows/00-Overview.md` open in a second tab/pane so you can flash it during the narration beat that explains `CLAUDE.md`'s mandatory-workflow rule.

## Shot list

**Scene 1 — Open (0:00–0:15)**
- Show the repo open in Claude Code (or the IDE extension), file tree visible.
- Narration: *"This is LinkedIn Agentic AI — a human-approved content pipeline for LinkedIn, X, and Substack, built entirely as Claude Code skills. Nothing here posts anything without you explicitly approving it first."*

**Scene 2 — The mandatory workflow rule (0:15–0:35)**
- Briefly show `CLAUDE.md` at the repo root, scroll to the "Mandatory" section.
- Cut to `Documentation/Workflows/00-Overview.md` — scroll past the document index table.
- Narration: *"Every task this agent does is grounded in a documented workflow — one file per feature, each one read directly from the real skill files, not summarized from memory. `CLAUDE.md` makes following these mandatory, on any machine this repo is opened on."*

**Scene 3 — Kick off a real request (0:35–1:10)**
- Type a real prompt in the chat: `Research and draft a LinkedIn post about <your disposable test topic>.`
- Let the agent actually run `/research-topic` and narrate over the tool calls as they stream: *"It's doing a live web search and fetching primary sources right now — it won't write a claim it can't verify."*
- Cut/speed up through `/generate-ideas` → `/write-draft` → `/critique-draft` if the real run takes a while; a sped-up montage with the file tree updating (`Content-Research/`, `Post-Ideas/`, `Drafts/` each gaining a new note) reads well on video.

**Scene 4 — The viral gate and visual brief (1:10–1:30)**
- Show the critique note's `viral_score` field and the pass/fail line.
- Show `/generate-visual`'s output — the finished ChatGPT-Images prompt in the Visual-Brief-Note.
- Narration: *"This scores itself against an 8-factor rubric before it's even shown to you, and any visual is a finished prompt for you to run yourself — nothing here calls an image API."*

**Scene 5 — Human approval (1:30–2:00)**
- Run `/review-drafts`, show the 7-way decision prompt (Approve / Edit / Regenerate / Change Hook / Change Image / Change Time / Reject).
- Narration: *"Every single post stops here. No draft reaches Buffer without an explicit human decision — that's a hard rule, not a default that can be switched off."*
- **Stop the demo here** (per the warning above) rather than actually approving/scheduling, unless recording against a disposable Buffer channel — or show the Approve action landing and cut away before `/schedule-approved` actually fires.

**Scene 6 — Close (2:00–2:20)**
- Cut back to the file tree / `README.md`.
- Narration: *"Full setup for Claude Desktop and Codex, the complete skills matrix, and every workflow documented end-to-end — all in the README and `Documentation/Workflows/`."*
- End card: repo URL.

## After recording

1. Export as an MP4 (or GIF for a shorter loop of just Scenes 3-5).
2. Either:
   - Upload the MP4 directly into a GitHub issue/PR comment on this repo (GitHub hosts it and gives you a stable `https://github.com/.../assets/...` URL) and use that URL in the README embed, or
   - Host it externally (YouTube, Loom) and link out.
3. Replace the placeholder in `README.md`'s `## 🎬 Demo` section with the real embed/link.
