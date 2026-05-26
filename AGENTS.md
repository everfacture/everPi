# Repository Guidelines

## Project Overview

Monorepo for Pi coding agent skills.

- **skills/** — Markdown SKILL.md files with procedural knowledge for Pi's skill system.

## Structure

```
everpi/
├── assets/                # Hero banner, images
├── skills/                # Pi skills (SKILL.md + optional references/)
│   ├── engineering-principles/
│   ├── github-hygiene/
│   ├── google-workspace/
│   └── improve-codebase-architecture/
├── AGENTS.md              # this file
├── CHANGELOG.md           # release history
├── CONTRIBUTING.md        # how to add skills
├── package.json           # pi package metadata
└── README.md              # monorepo front page
```

## Commands

- **install dependencies**: n/a
- **check**: `git status --short` — verify what's changing before committing
- **build**: n/a — no build step for skills (Markdown)
- **release**: bump version in package.json, edit CHANGELOG.md, then `git commit` + `git push`

## Style

- Skill directories should match their `name:` frontmatter field
- Reference files live in `references/` subdirectories alongside SKILL.md
- Conventional commit prefixes: `feat`, `fix`, `docs`, `chore`

## Agent Notes

- `skills/google-workspace/` contains a Python CLI (`scripts/gws.py`). Never commit credential files (`client_secret.json`, `token.json`). These are `.gitignore`d.
- This repo is the source of truth; the active Pi directory (`~/.pi/agent/`) is NOT git-tracked.
