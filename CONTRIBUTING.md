# Contributing

## Adding a Skill

1. Create `skills/<name>/SKILL.md` with frontmatter:

```yaml
---
name: my-skill
description: One-line summary of when to use this skill.
---
```

2. Write the skill body using structured sections:
   - `## When to Use` — trigger conditions
   - `## Procedure` — ordered steps
   - `## Pitfalls` — common mistakes
   - `## Verification` — checks that prove success

3. If the skill needs reference files, put them in `skills/<name>/references/`.

4. Run the repo check:

```bash
python3 scripts/check_repo.py
```

5. Test locally by copying to Pi:

```bash
cp -r skills/<name> ~/.pi/agent/skills/
```

6. Update the README Skills table and CHANGELOG if the change is public-facing.

## Skill Guidelines

- **One job per skill.** If the description needs “and”, split it.
- **Procedural, not theoretical.** “Do X, then Y, check Z” — not “consider the tradeoffs of X.”
- **Self-contained.** A skill should be loadable without reading other skills.
- **Reference files are optional.** Only add them if examples, checklists, or longer context shorten future work.
- **No private operational sludge.** Public skills should not mention local secrets, private paths, raw customer names, or stale incident details unless generalized.

## Versioning

This repo uses repo-level semantic versioning for the installable skill pack.

- **Patch** — docs, typo fixes, validation, attribution, non-behavioural cleanup.
- **Minor** — new skill, new workflow, or meaningful new capability.
- **Major** — removed/renamed skills, breaking install layout, or changed invocation contract.

Individual skills do not need separate versions unless they become separately installable packages.

## Commit Convention

Use conventional commit prefixes:

- `feat(skill): add google-workspace` — new skill
- `fix(skill): repair broken reference in engineering-principles`
- `docs: update README with new skill` — documentation
- `chore: update package metadata` — maintenance

## Before You Push

```bash
git status --short
python3 scripts/check_repo.py
```

Verify:

- only intended files changed
- no credential files (`client_secret.json`, `token.json`, `.env`, etc.)
- README and CHANGELOG match package version when releasing
- AGENTS.md still reflects the repo shape
