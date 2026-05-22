---
name: improve-codebase-architecture
description: "Find architecture deepening opportunities in codebases. Use when improving architecture, refactoring modules, consolidating duplication, splitting god files, making code more testable, or making a repo easier for agents to navigate."
---

# Improve Codebase Architecture

Architecture review mode. Find friction first. Do not edit during discovery. Keep coding protocol details out of this skill; use this only for architecture discovery/design.

Goal: turn shallow modules into deeper modules: more behavior behind smaller, clearer interfaces. Optimize for testability, locality, leverage, and AI-navigability.

> **Origin:** Architecture vocabulary (module, interface, depth, seam, adapter, leverage, locality) adapted from [Matt Pocock's `improve-codebase-architecture` skill](https://github.com/mattpocock/skills/blob/main/skills/engineering/improve-codebase-architecture/SKILL.md). Extended with Start Gate, Explore, Domain Research Rule, Candidate/Grilling workflow, Execution Rules, and reference files.

## Start Gate

Before proposing changes, establish:

```text
SCOPE:   repo / subsystem / files
DOMAIN:  key project terms from CONTEXT.md, AGENT.md, README, docs/adr/
FRICTION: what is hard to understand, change, or test
OUTPUT:  candidates only | selected design | implementation
```

If user asks for “ideas”, “review”, “architecture”, or “what should improve”, output candidates only. No edits.

## Vocabulary

Use these terms in reports:

- **Module** — anything with interface + implementation: function, class, package, slice.
- **Interface** — everything caller must know: types, invariants, order, errors, config, performance. Not just signature.
- **Implementation** — code behind interface.
- **Depth** — leverage at interface. Deep = much behavior behind small interface. Shallow = interface nearly as complex as implementation.
- **Seam** — place where behavior can vary without editing caller.
- **Adapter** — concrete thing satisfying interface at seam.
- **Leverage** — capability callers get per interface learned.
- **Locality** — change, bugs, and knowledge concentrated in one place.

Tests:
- **Deletion test:** if deleting module removes complexity, it was pass-through. If complexity reappears across callers, module earns keep.
- **Interface is test surface:** if tests need to reach past interface, module shape may be wrong.
- **One adapter = hypothetical seam. Two adapters = real seam.**

Full vocabulary: `references/architecture-language.md`.

## Explore

Read first:
1. `CONTEXT.md` if present
2. `AGENT.md` or repo instructions
3. README
4. relevant `docs/adr/`
5. directory map and entry points
6. tests around target area

Use `rg`, `find`, and `read`. Explore directly with pi tools; do not assume separate subagent support.

Look for:
- understanding one concept requires bouncing across many small modules
- shallow pass-through modules
- duplicated domain rules or constants
- god modules doing 5+ unrelated jobs
- scattered parsing/validation/error logic
- pure functions extracted only for tests, while bugs live in orchestration
- tight coupling leaking through seams
- hard-to-test behavior because interface is wrong
- ADR decisions causing real current friction

Apply deletion test to suspected shallow modules.

## Domain Research Rule

For domain-specific systems, do not plan from generic architecture alone. Extract 3-5 questions and research how practitioners solve same problem. Then synthesize.

Examples:
- trading signal architecture
- CI/CD pipelines
- payment reconciliation
- LLM scoring/ranking systems
- scraping/job ingestion systems

Research calibrates scope. “Clean code” and “better domain result” may imply different refactors.

## Candidate Output

Present numbered candidates. Do not propose final interfaces yet.

```text
CANDIDATE 1: [name]
FILES: [files/modules]
FRICTION: [why current shape hurts]
DEEPENING: [plain-English change]
BENEFIT: [locality + leverage]
TEST IMPACT: [how testing gets easier]
RISK: [migration/API/behavior risk]
ADR: [none | conflicts ADR-xxxx because ...]
```

End with:

```text
ASK: Which candidate should we explore?
```

Use project domain terms from `CONTEXT.md`. If `CONTEXT.md` says “Order”, say “Order intake module”, not random implementation names.

## Grilling Selected Candidate

When user picks candidate, design with them before editing.

Cover:
- module name and domain concept
- seam placement
- interface facts callers must know
- adapters needed now vs hypothetical later
- what implementation hides
- migration sequence
- tests that survive
- rollback plan
- ADR conflicts or new ADR need

If naming creates new stable domain term, offer to add/update `CONTEXT.md`. If user rejects candidate for durable reason, offer ADR so future reviews avoid re-suggesting it.

For alternative interface designs, load `references/interface-design.md`.

## Execution Rules

Only execute after user approves candidate/design.

1. Map dependencies first: grep imports/callers before changes.
2. Write new code before deleting old.
3. Preserve public interface with re-exports/barrels/adapters when practical.
4. Test each step: imports, focused tests, relevant dry run.
5. Delete old code last.
6. Commit only when asked or repo workflow expects it; one logical step per commit.

If step breaks, revert that step only.

Detailed checklist: `references/refactor-execution.md`.

## Pattern Triggers

Load references when trigger matches:

| Trigger | Reference |
|---|---|
| deeper vocabulary needed | `references/architecture-language.md` |
| selected candidate needs interface options | `references/interface-design.md` |
| god module, duplication, scattered parsing, thin runners | `references/refactor-patterns.md` |
| implementing architecture refactor | `references/refactor-execution.md` |

## Never

- edit during discovery
- propose interfaces before user chooses candidate
- suggest seams with one adapter unless variation is real
- split modules by file size alone
- extract pass-through helpers and call it architecture
- ignore `CONTEXT.md` or ADRs
- relitigate ADRs without real friction
- batch large refactors without verification steps
