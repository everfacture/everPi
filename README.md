# everpi

My Pi customizations: providers, extensions, and skills.

## Install

```bash
pi install git:github.com/everfacture/everpi
```

Reload after install: `/reload`

## What's here

| Resource | What it does | Type |
|----------|-------------|------|
| [bailian-coding-plan](extensions/README.md#bailian-coding-plan) | DashScope/Coding Plan provider (qwen, kimi, glm, MiniMax) | Provider |
| [protected-sensitive-files](extensions/README.md#protected-sensitive-files) | Confirms edits to .env/.gitignore; blocks destructive deletes | Extension |
| [everpi-yolo](extensions/README.md#everpi-yolo) | Fine-grained permission system with YOLO defaults | Extension |
| [tinyfish-search](skills/README.md) | Lightweight web search via API | Skill |

## Quick setup

1. Set any required env vars in your shell profile
2. Install: `pi install git:github.com/everfacture/everpi`
3. Run `npm install` in the package root for everpi-yolo's dependency
4. Reload: `/reload` in Pi

Required env vars (only the ones you need):
- `DASHSCOPE_API_KEY` — for bailian-coding-plan
- `TINYFISH_API_KEY` — for tinyfish-search
