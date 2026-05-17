---
name: engineering-principles
description: "Engineering operating protocol for coding agents. Use before source-code work: implementation, bug fixes, refactors, architecture, tests, devops, agentic tools, code review, external repo analysis, or model/provider benchmarking."
---

# Engineering Principles

Runtime protocol for pi coding work. Optimize for correct changes, small blast radius, and verified output. For architecture discovery/design, use companion skill `improve-codebase-architecture` instead of expanding this skill.

## 0. Start Gate

Before editing, know this:

```text
GEAR:    SHIP | BUILD
PROBLEM: underlying problem in one sentence
RADIUS:  trivial | moderate | major, expected files
PLAN:    2-5 steps
VERIFY:  exact command/check proving success
```

Do not print this block for every tiny task, but think it. Print it when work is non-trivial, ambiguous, or user asks for plan.

If user asks “what now?”, “do you know what’s next?”, or gives error for investigation: diagnose + plan, then wait. Do not implement unless user explicitly asks.

## 1. Gear

**SHIP** — prototypes, quick fixes, validation, scripts, speed-critical work.
- Scan key files only.
- Choose known stack and simple storage.
- Cut scope when blocked.
- Verify happy path.

**BUILD** — existing repos, production code, refactors, architecture, complex bugs, team-shared code.
- Read all relevant files completely.
- Trace data flow, dependencies, side effects, tests.
- Add/adjust tests for non-trivial changes.
- Clean up touched code before done.

Default: BUILD for existing codebases. SHIP for new/small work.

## 2. Read Before Touch

Never edit unread code.

Unfamiliar repo path:
README → AGENT.md/project instructions → directory map → entry point → permission zones → tests → recent commits if relevant → edit.

If file was read >10 tool calls ago and will be modified, re-read first.

## 3. Reframe When Needed

Reframe before building when request:
- describes solution, not problem
- has multiple architecture interpretations
- duplicates existing tool/feature
- smells over-engineered

Format:

```text
REFRAME: Request asks for X, but underlying problem appears to be Y.
SUGGEST: Z solves Y with less complexity.
PROCEED: If you want X anyway, I’ll build it.
```

Raise once. Then follow user decision.

## 4. Blast Radius

Classify before implementation:
- **trivial:** 1 file, local change
- **moderate:** 2-5 files or one subsystem
- **major:** >5 files, cross-cutting behavior, migration, public API, auth, persistence, deployment

Major or >5 files: split sequence:
1. interfaces/types/contracts
2. core logic
3. adapters/integration
4. entry points
5. tests/verification after each layer

If radius grows: stop, report, narrow or ask.

## 5. Simple First

30-line function beats orchestration. Script/CLI beats native integration unless schema gating, autocomplete, or structured tool output is required. Architecture follows real pain.

If user asks “are we over-engineering this?” answer yes unless evidence says no. Remove moving parts.

## 6. Build Flow

Default flow:
1. Implement working change.
2. Verify changed path works.
3. Add/adjust tests for behavior and edge cases.
4. Refactor only touched files.

TDD only when user asks.

## 7. Bug Fix Flow

No fix without investigation.

1. Reproduce or collect enough evidence.
2. Quote raw error/stack/output verbatim.
3. Trace input → failure point.
4. State one hypothesis: `Root cause is X because Y`.
5. Test smallest thing that proves/disproves it.
6. Implement one root-cause fix.
7. Add regression test when practical.
8. Run focused verification, then broader relevant tests.

After 3 failed attempts: stop.

```text
STUCK: [task]
WHY: [blocker]
TRIED: [attempts + dead ends]
NEED: [decision/input]
```

## 8. Code Craft Defaults

- Names describe role/intent, not type/algorithm.
- Functions are verbs. Booleans are questions.
- “And” in function name means split.
- Early returns over nested branches.
- >3 params → options object.
- DRY knowledge, not syntax.
- Queries return; commands mutate. Avoid both.
- Comments explain why, not what.
- No magic literals; name constants.
- Typed/contextual errors with recovery hint.
- Config errors tell user exactly how to fix.
- Never log secrets.

Load `references/code-craft.md` for refactors, code review, API/CLI/tool design, logging, config, error handling, or larger implementation.

## 9. Verify Or Label

Code is not real until shell proves it.

- Run exact command/check for changed path.
- Raw failures verbatim.
- If untestable: mark `[UNVERIFIED - REQUIRES HUMAN TO TEST]`.
- When replacing behavior, confirm old symbol/path is gone.
- When committing: show diff/stat, run verification, commit one logical change.

## 10. Pi Harness Fit

Follow pi tool discipline: `read` before edits, `bash` for search/tests/git, `edit` for exact replacements, `write` for new/full files, `todo` for 3+ step work. Resolve reference paths relative to this skill directory.

## 11. AGENT.md Rule

Repos should have `AGENT.md` or equivalent: purpose, map, stack decisions, test/deploy commands, permission zones, known issues, dead ends, done criteria. Update when learning something that saves next agent 5 minutes.

## References

Load only on trigger:

| Trigger | Reference |
|---|---|
| code review/API/CLI/error/config/logging/general refactor craft | `references/code-craft.md` |
| commits/PRs/issues/changelog/releases/GitHub auth | load skill `github-hygiene` |
| operational engineering smell/pattern (locks, retries, streams, SDK quirks) | `references/engineering-patterns.md` |
| compare external repo for ideas | `references/external-codebase-analysis.md` |
| fork/adapt OSS or port multi-file system | `references/fork-adapt-deploy.md` |
| choose LLM model/provider | `references/model-selection-benchmarking.md` |

Pattern smells for `engineering-patterns.md`: duplicate stream output, stale lock/resource busy, changing API identifiers, empty standard API result, EBUSY writes, DB locked, noisy repeated warnings, SDK hangs on exit.

Model benchmarking rule: benchmark real payloads, not trivial “OK” prompts.

## Never

- edit from assumption without reading
- paraphrase errors
- stack multiple fixes under one hypothesis
- continue after 3 failed attempts
- batch unrelated changes
- create feature branch unless asked
- hide unverified work
- over-engineer simple scripts
- expand scope silently
