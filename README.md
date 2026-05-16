# everpi

My Pi customizations: providers, extensions, prompt templates, and skills.

## Install

```bash
pi install git:github.com/everfacture/everpi
```

Reload after install: `/reload`

## What's here

| Resource | What it does | Type |
|----------|-------------|------|
| [bailian-coding-plan](extensions/README.md#bailian-coding-plan) | DashScope/Coding Plan provider (qwen, kimi, glm, MiniMax) | Provider |
| [evaluation-pack](extensions/README.md#evaluation-pack) | Eval mode + structured task output with verification evidence | Extension |
| [protected-sensitive-files](extensions/README.md#protected-sensitive-files) | Confirms edits to .env/.gitignore; blocks destructive deletes | Extension |
| [everpi-yolo](extensions/README.md#everpi-yolo) | Fine-grained permission system with YOLO defaults | Extension |
| [tinyfish-search](skills/README.md) | Lightweight web search via API | Skill |
| [html-slide-deck](prompts/README.md#html-slide-deck) | Present findings as a browsable HTML slide deck | Prompt template |
| [evaluation-pack-template](prompts/README.md#evaluation-pack-template) | Run tasks requiring verification evidence → HTML page | Prompt template |
| [session-friction-review](prompts/README.md#session-friction-review) | Audit sessions for wasted agent motion → HTML deck | Prompt template |

## Quick setup

1. Set any required env vars in your shell profile
2. Install: `pi install git:github.com/everfacture/everpi`
3. Run `npm install` in the package root for everpi-yolo's dependency
4. Reload: `/reload` in Pi

Required env vars (only the ones you need):
- `DASHSCOPE_API_KEY` — for bailian-coding-plan
- `TINYFISH_API_KEY` — for tinyfish-search
