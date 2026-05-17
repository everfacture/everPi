# Repository Guidelines

## Project Overview

everpi is a reusable Pi package. It bundles:
- reusable Pi skills under `skills/`
- DashScope Coding Plan provider extension for Pi

Pi package loading is declared in `package.json` under `pi.extensions` and `pi.skills`.

## Structure

- `extensions/` — Pi extension TypeScript files.
- `skills/` — Pi skills, each as `skills/<name>/SKILL.md` plus optional `references/`.
- `docs/` — future detailed docs.
- `README.md` — package overview and install path.
- `CHANGELOG.md` — user-facing changes, `Unreleased` first.

## Commands

- Install deps: `npm install`
- Validate package metadata: `node -e "JSON.parse(require('fs').readFileSync('package.json','utf8')); console.log('package.json ok')"`
- List skill files: `find skills -maxdepth 2 -name SKILL.md -print | sort`
- Local install test: `pi install /home/ibby/everpi`

## Skill Rules

- Keep `SKILL.md` terse and operational.
- Put long detail in `references/` and load only on trigger.
- Frontmatter requires `name` and `description`.
- Names use lowercase letters, numbers, hyphens.
- Avoid project-specific memories in general skills.

## Extension Rules

- Keep provider/model docs in `extensions/README.md` and root README.
- Do not hardcode secrets. `DASHSCOPE_API_KEY` comes from environment.
- Update README model table when model definitions change.

## Release

Before release or push:
1. update `CHANGELOG.md`
2. verify package JSON parses
3. verify skills are discoverable
4. test local install if Pi behavior changed

## Agent Notes

- Work on current branch unless user asks otherwise.
- Do not create feature branches unless requested.
- Do not edit `.git/` internals or lockfiles unless required by npm install/update.
- Keep repo clean: README = overview, AGENTS = operating map, skill references = detail.
