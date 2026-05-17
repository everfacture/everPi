# Refactor Execution Checklist

Use after user approves architecture candidate/design.

## Before Editing

```text
TARGET: [module/subsystem]
PUBLIC SURFACE: [imports, commands, routes, classes, funcs]
CALLERS: [grep results]
TESTS: [focused + broad]
ROLLBACK: [how to revert step]
```

Commands:
- `rg "from old.path|import old.path|oldFunction" src tests`
- language-specific import/compile check
- focused test command
- relevant dry-run/status command

## Safe Sequence

1. **Map dependencies**
   - importers
   - callers
   - tests
   - config/routes/CLI references

2. **Create new shape without deletion**
   - new module/package
   - shared rules/core logic
   - adapters
   - re-export/barrel for compatibility

3. **Wire one caller/path**
   - smallest caller first
   - run import check
   - run focused test

4. **Migrate remaining callers**
   - one coherent group at time
   - verify after each group

5. **Delete old code last**
   - `rg` old symbols/paths
   - remove dead files/functions
   - run focused + broad relevant tests

6. **Document decision**
   - update `AGENT.md`, `CONTEXT.md`, or ADR if future agents need rationale

## Per-Step Verification

Use equivalent for stack:

```bash
# import/compile
python -c "import package.module"
python -m compileall path
npm test -- path

# focused tests
pytest tests/path/test_target.py

# behavior/dry run
python -m app --help
python -m app status
python -m app run --dry-run
```

Show raw failures. Do not batch many unverified changes.

## Compatibility Patterns

Python:
```python
# package/__init__.py
from .new_module import public_func, PublicClass
```

TypeScript:
```ts
// index.ts
export { publicFunc, PublicClass } from './new-module';
```

Keep aliases when callers use old names:
```python
old_name = new_name
```

## Stop Conditions

Stop and reassess when:
- caller count much larger than expected
- public API break appears
- tests require rewriting around implementation details
- one change reveals unrelated architectural issue
- third failed fix attempt occurs

Escalate:

```text
STUCK: [refactor step]
WHY: [new info]
TRIED: [attempts/dead ends]
OPTIONS: [narrow / redesign / stop]
``` 
