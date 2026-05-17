# Refactor Patterns

Generalized field-tested patterns. Load only when trigger matches.

## God Module Split

Signal: one file/module does 5+ unrelated jobs.

Process:
1. Identify cohesion groups by who imports/calls functions, not by proximity.
2. Create submodules by domain purpose.
3. Re-export public symbols from package/barrel to preserve caller imports when possible.
4. Fix internal cross-module calls explicitly.
5. Update importers if public path must change.
6. Verify import surface and main workflow.
7. Delete old file last.

Pitfalls:
- helpers that were same-file calls need imports after split
- tests often import old path
- splitting by line count creates worse architecture

## Shared Domain Rules Across Execution Contexts

Signal: same constants/conditions/calculations live in two contexts and drift.
Examples: live detector vs planner, API handler vs batch job, CLI query vs worker.

Process:
1. Audit duplicated constants/functions and note drift.
2. Choose source of truth using production behavior or documented decision.
3. Extract pure rules into shared module with no runtime-specific imports.
4. Keep context-specific adapters thin: state, I/O, orchestration stay outside shared rules.
5. Re-export old names for backwards compatibility when practical.
6. Add assertions/tests proving contexts use same values.

Do not unify when logic is intentionally different. Document divergence.

## SQL / Query Duplication

Signal: same where-clause/stage condition/count logic appears in multiple files.

Process:
1. Put stage/query definitions in one source-of-truth map or query builder.
2. Expose named functions like `countPending(stage, options)`.
3. Consumers import shared function, not embed SQL.
4. Test each stage/query against expected rows.

## Scattered Parsing Unification

Signal: several stages parse same LLM/API/user output differently: regexes, JSON extraction, fence stripping, marker lines.

Process:
1. Inventory parsing patterns and edge cases.
2. Add shared parser utilities near client/boundary layer.
3. Replace local parsers one consumer at a time.
4. Preserve output exactly; add fixtures from real responses.
5. Delete local parser copies.

## Thin Runner Inlining

Signal: orchestrator has many wrappers that only import one function, call it, catch error, return status.

Process:
1. Keep complex runners with real orchestration.
2. Replace pass-through runners with action table: `{name: (module, function)}`.
3. Add generic dispatcher with shared error handling.
4. Update sequential/concurrent paths to call dispatcher.
5. Verify each stage dispatches.

Deletion test: if wrapper body is import + call + return, it adds indirection without leverage.

## Pass-through Module Removal

Signal: module exists only to rename/re-export one thing, with no policy, validation, or behavior.

Choices:
- inline it if it has no domain meaning
- deepen it by moving real policy behind it
- keep it only if preserving public compatibility

## Test Surface Repair

Signal: tests reach into private helpers, mock many internals, or duplicate orchestration knowledge.

Process:
1. Define behavior callers care about.
2. Move hidden steps behind one interface.
3. Test through interface with real/fake adapters at real seams.
4. Delete tests that lock implementation shape.
