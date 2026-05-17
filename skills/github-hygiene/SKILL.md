---
name: github-hygiene
description: GitHub and repository workflow for coding agents. Use for commits, PRs, issues, changelogs, releases, forks, publishing, repo hygiene, or checking GitHub auth/remotes.
---

# GitHub Hygiene

Use when task involves git commits, GitHub, PRs, issues, releases, forks, publishing, or repo workflow. Do not load for normal code edits unless committing/publishing is in scope.

Style target: clean repos that are operationally obvious. Another agent should land a safe change after reading README + AGENTS + CHANGELOG in 3 minutes.

## Start Gate

Before repository actions:

```text
REPO:    [path + remote]
BRANCH:  [current branch]
STATUS:  [clean/dirty summary]
ACTION:  commit | PR | issue | release | fork | push | inspect
VERIFY:  [test/build/check before action]
```

Run:

```bash
git status --short
git branch --show-current
git remote -v
gh auth status
```

## GitHub Access

GitHub does not provide shell SSH. SSH auth only supports git operations.

Use:
- `gh` CLI for GitHub API/PR/issues/releases/forks
- `git` for clone/fetch/pull/push

Check auth:

```bash
gh auth status
ssh -T git@github.com -o BatchMode=yes
```

If SSH says authenticated but no shell, that is normal.

## Branching

Default: work on current branch. Do not create feature branches unless user asks or repo workflow requires it.

Scoping is safety mechanism: small changes, atomic commits, verification.

## Commits

Commit only when asked or repo workflow clearly expects it.

Before commit:
1. Show `git diff --stat` or relevant diff.
2. Run verification command and show output.
3. Confirm old code/symbols removed when replacing behavior.
4. `git status --short` to show staged/untracked scope.

Atomic commit rule: one logical change per commit. If subject needs “and”, split commit.

Conventional subjects:

```text
feat(auth): add PKCE flow
fix(api): handle missing user profile
refactor(db): extract query builder
test(auth): cover expired token refresh
docs(readme): update setup
chore(deps): bump typescript
perf(images): lazy load thumbnails
fun(ui): add success confetti
```

Body explains why and evidence:

```text
fix(auth): handle expired JWT during refresh

Root cause: refresh endpoint decoded expired token before expiry fallback ran.
Regression test: test_expired_token_triggers_refresh
Verification: pytest tests/auth/test_refresh.py
```

## PRs

PR description answers:
1. What changed?
2. Why changed?
3. How verified?

Include:
- screenshots for UI changes
- test output for logic changes
- breaking changes
- migration notes
- known follow-ups

Useful commands:

```bash
gh pr create --fill
gh pr view --web
gh pr checks
gh pr diff
```

## Issues and Proposals

Issues are decision logs, not vague reminders.

Issue format:

```text
Problem:
Reproduce:
Expected:
Actual:
Tried:
Decision/Next:
```

Proposal format for bigger features:

```text
Summary: [2 sentences]
Motivation:
Tradeoffs:
Alternatives:
Open questions:
Owner/decision:
```

## Changelog and Releases

Changelog required for releases. Include what changed, why, and what may break.

```markdown
## v1.2.0 — 2026-04-22
- feat: added `--verbose` flag to config command
- fix: crash when config file has empty providers array
- BREAKING: `config set` now requires `--provider`
```

Beta-first when publishing packages or risky releases:
1. publish beta/pre-release
2. install/test as user would
3. verify CLI/API/version
4. promote stable

Never hardcode version in multiple places. Use package metadata/build injection.

## Forks

For forks/adapted OSS, prefer `engineering-principles/references/fork-adapt-deploy.md` for full process.

Private fork via CLI:

```bash
gh repo fork OWNER/REPO --clone --private
```

Audit upstream before deep adaptation:
- recent commits
- open/closed issues with high comments
- active forks
- license
- release cadence

## Repo Cleanliness Standard

Clean repo answers fast:
1. What is this?
2. How do I install/run it?
3. How do I develop/test it?
4. How do I release it?
5. What must agents not break?

Expected shape:

```text
repo/
├── README.md              # product page: what/why/install/quickstart
├── AGENTS.md              # exact repo operating instructions
├── CHANGELOG.md           # user-facing changes, Unreleased first
├── LICENSE
├── docs/                  # detailed topic docs, not README dump
├── scripts/               # canonical workflows: check/build/release/smoke
├── src/                   # implementation
└── tests/                 # verification
```

Prefer `AGENTS.md`. If repo already uses `AGENT.md`, follow existing convention.

## README Standard

README is product front page, not manual.

Order:
1. name + one-line value prop
2. screenshot/badge only if useful
3. why/use cases
4. install
5. quickstart with 3 commands max
6. key features
7. links to detailed docs
8. license

Avoid:
- dumping every flag into README
- stale architecture essays
- huge troubleshooting sections
- install paths that are not tested

Move detail to `docs/`.

## AGENTS.md Standard

`AGENTS.md` is repo-specific operating map. No generic advice.

Include:

```text
# Repository Guidelines

## Project Overview
[what this repo is, stack, runtime]

## Structure
[src/tests/docs/scripts/generated files]

## Commands
- install:
- check:
- test:
- build:
- run/restart:
- release:

## Style
[formatter/linter/naming/framework rules]

## Testing
[what to run for common changes]

## Release
[script/docs/version/changelog rules]

## Agent Notes
[real footguns: generated files, stale binaries, multiple checkouts, secrets]
```

Good AGENTS notes are concrete:
- “Use `pnpm check`, not raw test command.”
- “Generated GraphQL files live under X; do not edit.”
- “If UI doesn’t match code, verify running binary path.”
- “Multiple agents work here; ignore unknown dirty files and list them.”

Bad AGENTS notes are generic principles copied from elsewhere.

## Changelog Standard

Changelog is user-facing decision log.

Rules:
- top section: `Unreleased`
- group by `Added`, `Changed`, `Fixed`, `Removed`, `Security` when useful
- one bullet per user-visible change
- thank contributors when merging external PRs
- do not scatter multiple bullets for same feature/fix
- update for user-visible behavior before release

Example:

```markdown
# Changelog

## Unreleased

### Fixed
- CLI: keep stale daemon status checks from replacing newer token warnings.

## 1.2.0 — 2026-04-22

### Added
- CLI: add `doctor --providers` for provider readiness checks.
```

## Scripts Standard

Scripts are repo muscle memory. Prefer one command per workflow:

```text
scripts/check        # format/lint/test gate
scripts/build        # build/package
scripts/release      # release flow
scripts/smoke        # install/user-path smoke
```

Use package-manager equivalents when idiomatic:
- `pnpm check`
- `npm test`
- `make check`
- `swift test`

Do not invent new tooling when repo already has scripts.

## Docs Standard

Docs carry detail README should not.

Good docs:
- `docs/install.md`
- `docs/configuration.md`
- `docs/cli.md`
- `docs/releasing.md`
- `docs/troubleshooting.md`
- `docs/architecture.md`

If docs folder grows large, add `docs/index.md` or front matter summaries/read_when where repo tooling supports it.

## Repository Shape For CLI/Tools

For CLI/tool repos, prefer:

```text
repo/
├── README.md
├── CHANGELOG.md
├── LICENSE
├── package.json           # version source when Node project
├── AGENTS.md
├── docs/commands/         # one doc per command if CLI is large
├── src/cli/               # entry point, parsing, dispatch
├── src/commands/          # command implementations
├── src/core/              # business logic, decoupled from CLI
├── tests/
└── scripts/
```

Command docs: flags/defaults, examples, gotchas, expected `--json` output.

## Standard CLI Checks

For CLI repos, verify:

```bash
project --help
project --version
project info
project command --json
```

Standard `info` output should expose config/dependency health without leaking secrets.

## Never

- commit unverified work without marking it unverified
- batch unrelated changes
- create branch unless asked/workflow requires
- rewrite history without explicit permission
- touch `.git/` internals manually
- commit credentials, tokens, `.env`, or secrets
- publish stable before testing install path
