# Extensions

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
