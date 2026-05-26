<p align="center">
  <img src="assets/banner.svg" alt="everPi" width="100%"/>
</p>

<p align="center">
  Engineering-grade skills for Pi coding agent.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License"/>
  <img src="https://img.shields.io/badge/status-active-brightgreen" alt="Status: Active"/>
</p>

---

## What Is This

A curated pack of **skills** for [Pi](https://github.com/earendil-works/pi-coding-agent) — the terminal-based AI coding agent. Install them, and Pi ships with real engineering discipline instead of "vibe coding."

**What makes these different:**

- **Karpathy merge** — behavioral guidelines from [Andrej Karpathy](https://x.com/karpathy/status/2015883857489522876) baked into every skill: surface assumptions, don't pick silently, surgical changes only, per-step verification.
- **Anti-pattern examples** — each skill includes concrete wrong-vs-right code examples showing what LLMs do wrong and how to fix it.
- **Real-world patterns** — engineering patterns extracted from deep analysis of 10 production repos: streaming dedup, stale lock detection, atomic file writes, etc.
- **SHIP vs BUILD gear** — adapts rigor to context. Prototypes move fast. Production code gets read-first, test-required, verified discipline.

## Skills

| Skill | What It Does |
|-------|-------------|
| [engineering-principles](skills/engineering-principles/) | Operating protocol for all coding work. Karpathy behavioral guidelines merged in. Code standards shaped by Pieter Levels' shipping ethos and Peter Steinberger's systems discipline. Start gate, blast radius, bug fix flow, anti-pattern self-review. **Load before any source-code task.** |
| [github-hygiene](skills/github-hygiene/) | GitHub workflow: commits, PRs, issues, releases, repo cleanliness. Conventional commits, changelog management, fork hygiene. |
| [improve-codebase-architecture](skills/improve-codebase-architecture/) | Architecture review and deepening. Vocabulary adapted from [Matt Pocock](https://github.com/mattpocock/skills); extended with Start Gate, Explore, Candidate/Grilling workflow, and execution rules. |
| [google-workspace](skills/google-workspace/) | 49 Google Workspace tools via zero-dependency Python CLI. Calendar, Gmail, Drive, Docs, Sheets, Contacts, Tasks. Direct REST API, no SDK. Original source unattributed — adapted from an internal Pi community CLI.

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
├── skills/                 # Pi skills (SKILL.md + references/)
│   ├── engineering-principles/
│   ├── github-hygiene/
│   ├── google-workspace/
│   └── improve-codebase-architecture/
├── AGENTS.md               # Repo guidelines for agents
├── CHANGELOG.md            # Release history
├── CONTRIBUTING.md         # How to add skills
├── package.json            # Pi package metadata
└── README.md
```

## Credits

Skills and references build on work from the open-source community:

- **improve-codebase-architecture** — vocabulary (module, interface, depth, seam, adapter, leverage, locality) adapted from [Matt Pocock's skill](https://github.com/mattpocock/skills/blob/main/skills/engineering/improve-codebase-architecture/SKILL.md), extended with workflow and execution rules.
- **engineering-principles / code-craft** — code standards and SHIP/BUILD philosophy shaped by the shipping ethos of [Pieter Levels](https://levels.io/) and the systems discipline of [Peter Steinberger](https://steipete.com/) (@steipete).
- **engineering-patterns** — 12 implementation patterns extracted from deep analysis of [Peter Steinberger's](https://github.com/steipete) production repos.
- **Karpathy guidelines** — behavioral guidelines merged into engineering-principles from [Andrej Karpathy](https://x.com/karpathy/status/2015883857489522876)'s observations on LLM coding pitfalls.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). TL;DR:

- **Add a skill:** Create `skills/<name>/SKILL.md` with frontmatter (`name`, `description`) and procedural content.
- **Style:** Skill names match directory names. Conventional commits.

## License

MIT
