# Extensions

Drop into `~/.pi/agent/extensions/` or install via `pi install`.

## bailian-coding-plan

Registers provider `bailian-coding-plan` with the following models:

| Model | Context | Output | Inputs |
|-------|---------|--------|--------|
| qwen3.6-plus | 1,000,000 | 65,536 | text, image |
| kimi-k2.5 | 256,000 | 32,768 | text, image |
| glm-5 | 202,752 | 16,384 | text |
| MiniMax-M2.5 | 196,608 | 32,768 | text |

Endpoint: `https://coding-intl.dashscope.aliyuncs.com/v1`
All models at zero cost (DashScope Coding Plan subscription).

**Requires:** `DASHSCOPE_API_KEY` exported in your environment.

## evaluation-mode

Appends evaluation instructions to the system prompt for every turn.
The agent must produce verification evidence before claiming a task is done:
changed files, commands run, screenshots, repro steps, known limitations.

**Commands:**
- `/evaluation-mode` — toggle on/off (no args needed)
- `/evaluation-mode on|off|status` — explicit control

**How output is delivered:**
The agent includes the evaluation pack in its normal response — typically
as a `write` tool call that creates `evaluation-pack.html`. No separate
delivery mechanism; the agent decides how to present it.

**When to use:**
Turn on when doing task work (fixing bugs, building features). Turn off
for casual questions or exploration to avoid overhead.

Shows "Evaluation mode: ON" widget in the TUI. State persists across
forks and branches via session entries.

## protected-sensitive-files

Requires confirmation before:
- Writing or editing `.env`, `.env.*`, or `.gitignore`
- Running `rm -rf`, `find -delete`, or similar destructive bash commands

Non-interactive mode: blocks by default.

Derived from Pi's `examples/protected-paths.ts` (blocks writes to `.env`,
`.git/`, `node_modules/`). This version adds confirmation UI instead of
hard-block, and extends protection to destructive bash commands.

## everpi-yolo

Fine-grained permission system wrapping
[`@gotgenes/pi-permission-system`](https://github.com/gotgenes/pi-permission-system).
Pre-configured with YOLO defaults for productive development.

Default behavior:
- **Allow without asking:** read, write, edit, git, npm, node, python, pip, make, docker, curl, sudo, chmod, chown
- **Ask before running:** `rm -rf *`, external directory access

Config is in `config.json`. Edit `yoloMode` to false for full confirmation on everything.
The system supports per-surface permissions (bash, write, read, etc.) with
wildcard patterns.

**Credit:** Built on [`@gotgenes/pi-permission-system`](https://github.com/gotgenes/pi-permission-system) by [@gotgenes](https://github.com/gotgenes).
This package wraps it with a pre-configured YOLO `config.json`.
