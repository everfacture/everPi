# everpi

Ibby's Pi package: DashScope Coding Plan provider plus reusable Pi skills.

## What It Includes

- **DashScope Coding Plan provider** — free Alibaba Bailian models as Pi `/model` options.
- **Engineering skills** — coding, architecture, and GitHub hygiene workflows for Pi agents.

## Install

```bash
pi install git:github.com/everfacture/everpi
npm install
/reload
```

For local development:

```bash
pi install /home/ibby/everpi
```

## Provider Setup

```bash
export DASHSCOPE_API_KEY="your-key"
```

Add it to `~/.zprofile` or shell profile so Pi sees it in new sessions.

## Models

All four are free under the [DashScope Coding Plan](https://bailian.console.aliyun.com/):

| Model | Context | Output | Inputs |
|-------|---------|--------|--------|
| qwen3.6-plus | 1M | 64K | text, image |
| kimi-k2.5 | 256K | 32K | text, image |
| glm-5 | 203K | 16K | text |
| MiniMax-M2.5 | 197K | 32K | text |

Endpoint: `coding-intl.dashscope.aliyuncs.com` (Alibaba Cloud international route).

## Skills

Packaged skills live in `skills/`:

- `engineering-principles` — coding operating protocol for Pi agents.
- `improve-codebase-architecture` — architecture review and refactor-planning workflow.
- `github-hygiene` — commits, PRs, changelogs, releases, and repo cleanliness.

Each skill keeps long material in `references/` so Pi only loads detail when needed.

## Repository Layout

```text
extensions/   Pi provider extension
skills/       reusable Pi skills
AGENTS.md     repo operating guide
CHANGELOG.md  user-facing changes
```

## Development

```bash
npm install
node -e "JSON.parse(require('fs').readFileSync('package.json','utf8')); console.log('package.json ok')"
find skills -maxdepth 2 -name SKILL.md -print | sort
```
