# Changelog

## Unreleased

### Added
- **skills/loop-engineering:** Added Pi-focused loop design protocol for recurring agent workflows, verifier gates, state, budgets, scheduling, and extension/MCP upgrade decisions.

### Removed
- **extensions/bailian-coding-plan:** Removed DashScope provider extension. Alibaba models are configured through `models.json` now.

## 1.1.0

### Added
- **skills/engineering-principles:** Karpathy behavioral guidelines merged into protocol — surface assumptions, don't pick silently, surgical changes, per-step verification.
- **skills/engineering-principles:** New `references/anti-patterns.md` — concrete wrong-vs-right code examples (hidden assumptions, over-abstraction, drive-by refactoring, style drift, vague goals).
- **CONTRIBUTING.md:** Guide for adding skills and extensions.
- **assets/banner.svg:** Hero banner for README.

### Changed
- **README.md:** Complete rewrite — hero image, one-liner, "what makes these different" section, improved install instructions, structure overview.
- **skills/engineering-principles/references/code-craft.md:** Removed duplicated pattern list → link to authoritative source. Trimmed "other essentials" dump to just abstraction ladder.
- **skills/engineering-principles/references/engineering-patterns.md:** Removed project-specific pattern (#14 Connection Consolidation for sayf) and dead stub (#16 Reserved). Now 12 clean, general-purpose patterns.

### Removed
- **skills/engineering-principles/references/model-selection-benchmarking.md:** Stale model matrix, protocol not durable enough for general reference.
- Partial pattern smell list from SKILL.md — replaced with reference to authoritative file.

## 1.0.0

### Added
- **skills/google-workspace**: Unified Google Workspace CLI — 49 tools across Calendar, Gmail, Drive, Docs, Sheets, Contacts, Tasks. Zero dependencies. See `skills/google-workspace/README.md` for setup.
- **skills/engineering-principles**: Operating protocol for coding work.
- **skills/github-hygiene**: GitHub workflow for commits, PRs, issues, releases.
- **skills/improve-codebase-architecture**: Architecture deepening opportunities.
- **extensions/bailian-coding-plan**: DashScope provider with 4 zero-cost models.
- **AGENTS.md**, **CHANGELOG.md**, **.gitignore**, **package.json**.
