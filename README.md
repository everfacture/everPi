# everpi

Reusable Pi package for agent workflows: engineering skills first, optional provider extensions alongside them.

## What It Includes

- **Skills** — reusable Pi skills for engineering discipline, architecture review, and GitHub hygiene.
- **Provider extension** — DashScope Coding Plan models exposed as Pi `/model` options.

## Install

```bash
pi install git:github.com/everfacture/everpi
/reload
```

For local development:

```bash
pi install /home/ibby/everpi
```

## Skills

Packaged skills live in `skills/`:

- `engineering-principles` — coding operating protocol for Pi agents.
- `improve-codebase-architecture` — architecture review and refactor-planning workflow.
- `github-hygiene` — commits, PRs, changelogs, releases, and repo cleanliness.

Each skill keeps long material in `references/` so Pi only loads detail when needed.

## DashScope Provider

The provider extension registers free Alibaba Bailian models via DashScope Coding Plan.

Setup:

```bash
export DASHSCOPE_API_KEY="your-key"
```

Add it to `~/.zprofile` or shell profile so Pi sees it in new sessions.

Models:

| Model | Context | Output | Inputs |
|-------|---------|--------|--------|
| qwen3.6-plus | 1M | 64K | text, image |
| kimi-k2.5 | 256K | 32K | text, image |
| glm-5 | 203K | 16K | text |
| MiniMax-M2.5 | 197K | 32K | text |

Endpoint: `coding-intl.dashscope.aliyuncs.com`.

## Repository Layout

```text
extensions/   Pi provider extensions
skills/       reusable Pi skills
AGENTS.md     repo operating guide
CHANGELOG.md  user-facing changes
```

## Development

```bash
node -e "JSON.parse(require('fs').readFileSync('package.json','utf8')); console.log('package.json ok')"
find skills -maxdepth 2 -name SKILL.md -print | sort
```
