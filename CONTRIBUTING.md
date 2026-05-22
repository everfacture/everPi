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

3. If the skill needs reference files (code examples, patterns, checklists), put them in `skills/<name>/references/`.

4. Test by copying to your local Pi: `cp -r skills/<name> ~/.pi/agent/skills/`

5. Update this README's Skills table.

### Skill Guidelines

- **One job per skill.** If it needs "and" in the description, split it.
- **Procedural, not theoretical.** "Do X, then Y, check Z" — not "consider the tradeoffs of X."
- **Self-contained.** A skill should be loadable without reading other skills.
- **Reference files are optional.** Only add them if code examples are needed.

## Adding an Extension

1. Create `extensions/<name>.ts`.
2. Register with Pi APIs (`pi.registerProvider`, `pi.registerCommand`, etc.).
3. The filename should match the primary registered command or provider name.
4. Add the extension path to `package.json` under `pi.extensions`.
5. Document in `extensions/README.md`.

### Extension Guidelines

- **Loaded by jiti.** No build step needed, but errors surface silently in Pi.
- **Zero dependencies preferred.** If you need external packages, note them in the extension README.
- **Graceful failure.** If an extension can't load (missing env var, etc.), fail with a clear message, not a crash.

## Commit Convention

Use conventional commit prefixes:

- `feat(skill): add google-workspace` — new skill
- `fix(skill): repair broken reference in engineering-principles`
- `docs: update README with new skill` — documentation
- `chore: update package.json` — maintenance

## Before You Push

```bash
git status --short
# Verify: only intended files changed
# Verify: no credential files (client_secret.json, token.json, etc.)
# Verify: AGENTS.md still accurate
```
