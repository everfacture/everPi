# everpi

Pi coding agent resources: extensions and skills. Install via `pi install` or copy manually.

## Extensions

### bailian-coding-plan

DashScope Coding Plan provider. Four zero-cost models registered as drop-in `/model` options.

| Model | Context | Output | Inputs |
|-------|---------|--------|--------|
| qwen3.6-plus | 1M | 64K | text, image |
| kimi-k2.5 | 256K | 32K | text, image |
| glm-5 | 203K | 16K | text |
| MiniMax-M2.5 | 197K | 32K | text |

**Requires:** `DASHSCOPE_API_KEY` env var.

[→ Extension details](extensions/README.md)

## Skills

| Skill | Description |
|-------|-------------|
| [engineering-principles](skills/engineering-principles/) | Operating protocol for coding work. SHIP vs BUILD gear, blast radius, verification. |
| [github-hygiene](skills/github-hygiene/) | GitHub workflow: commits, PRs, issues, releases, repo cleanliness. |
| [improve-codebase-architecture](skills/improve-codebase-architecture/) | Find deepening opportunities. Turn shallow modules into deep ones. |
| [google-workspace](skills/google-workspace/) | 49 Google Workspace tools via zero-dependency Python CLI. Calendar, Gmail, Drive, Docs, Sheets, Contacts, Tasks. |

## Install

```bash
# Extensions
pi install git:github.com/everfacture/everpi
npm install
/reload

# Skills — copy to ~/.pi/agent/skills/ or register via resources_discover hook
cp -r skills/<name> ~/.pi/agent/skills/
```

## License

MIT
