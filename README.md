<p align="center">
  <img src="assets/banner.svg" alt="everPi" width="100%"/>
</p>

<p align="center">
  Engineering-grade skills and provider extensions for Pi coding agent.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License"/>
  <img src="https://img.shields.io/badge/status-active-brightgreen" alt="Status: Active"/>
</p>

---

## What Is This

A curated pack of **skills** and **extensions** for [Pi](https://github.com/earendil-works/pi-coding-agent) — the terminal-based AI coding agent. Install them, and Pi ships with real engineering discipline instead of "vibe coding."

**What makes these different:**

- **Karpathy merge** — behavioral guidelines from [Andrej Karpathy](https://x.com/karpathy/status/2015883857489522876) baked into every skill: surface assumptions, don't pick silently, surgical changes only, per-step verification.
- **Anti-pattern examples** — each skill includes concrete wrong-vs-right code examples showing what LLMs do wrong and how to fix it.
- **Real-world patterns** — engineering patterns extracted from deep analysis of 10 production repos: streaming dedup, stale lock detection, atomic file writes, etc.
- **SHIP vs BUILD gear** — adapts rigor to context. Prototypes move fast. Production code gets read-first, test-required, verified discipline.

## Skills

| Skill | What It Does |
|-------|-------------|
| [engineering-principles](skills/engineering-principles/) | Operating protocol for all coding work. Start gate, blast radius, bug fix flow, code craft defaults, anti-pattern self-review. **Load this before any source-code task.** |
| [github-hygiene](skills/github-hygiene/) | GitHub workflow: commits, PRs, issues, releases, repo cleanliness. Conventional commits, changelog management, fork hygiene. |
| [improve-codebase-architecture](skills/improve-codebase-architecture/) | Find architecture deepening opportunities. Turn shallow modules into deep ones. Split god files, consolidate duplication, make code testable. |
| [google-workspace](skills/google-workspace/) | 49 Google Workspace tools via zero-dependency Python CLI. Calendar, Gmail, Drive, Docs, Sheets, Contacts, Tasks. Direct REST API, no SDK. |

## Extensions

### bailian-coding-plan

Registers a DashScope provider with Pi. Four models available via `/model` — zero cost with DashScope Coding Plan subscription.

| Model | Context | Output | Inputs |
|-------|---------|--------|--------|
| qwen3.6-plus | 1M | 64K | text, image |
| kimi-k2.5 | 256K | 32K | text, image |
| glm-5 | 203K | 16K | text |
| MiniMax-M2.5 | 197K | 32K | text |

**Requires:** `DASHSCOPE_API_KEY` env var.
[→ Extension details](extensions/README.md)

## Install

### Via Pi (recommended)

```bash
pi install git:github.com/everfacture/everpi
npm install
/reload
```

### Manual

```bash
# Skills — copy into Pi's skills directory
cp -r skills/<name> ~/.pi/agent/skills/

# Extensions — register in Pi config
# or copy extensions/*.ts to your Pi extensions directory
```

### Verify

After install, Pi should discover the skills automatically. Test with:

```
/load skill engineering-principles
```

## Structure

```
everpi/
├── assets/                 # Images and graphics
├── extensions/             # Pi TypeScript extensions
│   └── bailian-coding-plan.ts
├── skills/                 # Pi skills (SKILL.md + references/)
│   ├── engineering-principles/
│   ├── github-hygiene/
│   ├── google-workspace/
│   └── improve-codebase-architecture/
├── AGENTS.md               # Repo guidelines for agents
├── CHANGELOG.md            # Release history
├── CONTRIBUTING.md         # How to add skills and extensions
├── package.json            # Pi package metadata
└── README.md
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). TL;DR:

- **Add a skill:** Create `skills/<name>/SKILL.md` with frontmatter (`name`, `description`) and procedural content.
- **Add an extension:** Drop a `.ts` file in `extensions/`, register with Pi APIs, add to `package.json` `pi.extensions`.
- **Style:** Skill names match directory names. Extension filenames match primary command. Conventional commits.

## License

MIT
