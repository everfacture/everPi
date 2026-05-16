# everpi

My Pi customizations: providers and extensions.

## Install

```bash
pi install git:github.com/everfacture/everpi
```

Reload after install: `/reload`

## What's here

| Resource | What it does | Type |
|----------|-------------|------|
| [bailian-coding-plan](extensions/README.md#bailian-coding-plan) | DashScope/Coding Plan provider (qwen, kimi, glm, MiniMax) | Provider |
| [everpi-yolo](extensions/README.md#everpi-yolo) | Fine-grained permission system with YOLO defaults | Extension |

## Quick setup

1. Set `DASHSCOPE_API_KEY` in your shell profile
2. Install: `pi install git:github.com/everfacture/everpi`
3. Run `npm install` in the package root (for everpi-yolo)
4. Reload: `/reload` in Pi
