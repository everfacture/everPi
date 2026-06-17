# Repository Guidelines

## Project Overview

Monorepo for Pi coding agent skills.

- **skills/** — Markdown SKILL.md files with procedural knowledge for Pi's skill system.
- **scripts/check_repo.py** — no-dependency repo validation used locally and in CI.

## Structure

```text
everPi/
├── .github/workflows/      # CI checks
├── assets/                 # Hero banner, images
├── scripts/                # Repo validation scripts
├── skills/                 # Pi skills (SKILL.md + optional references/)
│   ├── engineering-principles/
│   ├── github-hygiene/
│   ├── google-workspace/
│   ├── improve-codebase-architecture/
│   └── loop-engineering/
├── AGENTS.md               # this file
├── CHANGELOG.md            # release history
├── CONTRIBUTING.md         # how to add skills
├── LICENSE                 # MIT license
├── package.json            # pi package metadata
└── README.md               # monorepo front page
```

## Commands

- **install dependencies**: n/a
- **check**: `python3 scripts/check_repo.py`
- **package check**: `npm run check`
- **build**: n/a — no build step for Markdown skills
- **release**: bump `package.json`, edit `CHANGELOG.md`, run checks, commit, tag `vX.Y.Z`, push with tags

## Style

- Skill directories must match their `name:` frontmatter field.
- Reference files live in `references/` subdirectories alongside `SKILL.md`.
- Conventional commit prefixes: `feat`, `fix`, `docs`, `chore`.
- Public copy should be direct and useful. Avoid borrowed-credibility padding and private/local operational details.

## Agent Notes

- `skills/google-workspace/` contains a Python CLI (`scripts/gws.py`). Never commit credential files (`client_secret.json`, `token.json`, `.env`). These are `.gitignore`d and checked by `scripts/check_repo.py`.
- This repo is the source of truth; the active Pi directory (`~/.pi/agent/`) is NOT git-tracked.
- GitHub repo metadata should stay aligned with README: public description, topics, license, and release tags.
