# Repository Guidelines

## Project Overview

Monorepo for Pi coding agent resources: extensions and skills.

- **extensions/** — TypeScript extensions registered with Pi via `pi.registerProvider()`, `pi.registerCommand()`, etc. Loaded by jiti at runtime.
- **skills/** — Markdown SKILL.md files with procedural knowledge for Pi's skill system.

## Structure

```
repo/
├── extensions/          # Pi extensions (.ts files)
│   ├── bailian-coding-plan.ts
│   └── README.md
├── skills/              # Pi skills (SKILL.md + optional references/)
│   ├── engineering-principles/
│   ├── github-hygiene/
│   ├── google-workspace/
│   ├── improve-codebase-architecture/
│   └── ...
├── AGENTS.md            # this file
├── CHANGELOG.md
├── README.md            # monorepo front page
├── .gitignore
└── package.json
```

## Commands

- **install dependencies**: `npm install` (only if editing TypeScript in extensions)
- **check**: `git status --short` — verify what's changing before committing
- **build**: n/a — no build step for skills (Markdown) or extensions (loaded by jiti)
- **release**: edit CHANGELOG.md Unreleased section, then `git commit` + `git push`

## Style

- Extension filenames should match their primary registered command name
- Skill directories should match their `name:` frontmatter field
- Reference files live in `references/` subdirectories alongside SKILL.md
- Conventional commit prefixes: `feat`, `fix`, `docs`, `chore`

## Agent Notes

- `skills/google-workspace/` contains a Python CLI (`scripts/gws.py`). Never commit credential files (`client_secret.json`, `token.json`). These are `.gitignore`d.
- Extensions loaded by jiti — no tsc compilation. Errors surface silently in Pi.
- This repo is the source of truth; the active Pi directory (`~/.pi/agent/`) is NOT git-tracked.
