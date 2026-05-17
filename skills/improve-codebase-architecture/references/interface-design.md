# Interface Design

Use after user selects architecture candidate and wants interface options. Based on “design it twice”: first design is rarely best.

## Frame Constraints

Before designing, list:

```text
MODULE: [domain name]
SEAM: [where callers cross]
CALLERS: [current and likely]
BEHIND SEAM: [logic/data/effects hidden]
INVARIANTS: [facts interface must preserve]
ERRORS: [failure modes and recovery]
ADAPTERS: [real adapters now, not hypothetical]
TEST SURFACE: [what tests should exercise]
```

## Generate 3 Designs

Create three genuinely different options:

1. **Minimal interface** — 1-3 entry points, maximum leverage per call.
2. **Common-case interface** — default path trivial for most callers.
3. **Flexible interface** — extension points/adapters where variation is real.

Only add fourth design if needed: **ports/adapters interface** for external side effects or cross-seam dependencies.

For each design:

```text
DESIGN: [name]
INTERFACE: [methods/types plus invariants, order, errors]
USAGE: [short caller example]
HIDES: [implementation details behind seam]
ADAPTERS: [real adapters]
LEVERAGE: [what callers gain]
LOCALITY: [what changes concentrate]
TRADEOFFS: [cost/risk]
```

## Compare

Compare by:
- depth: behavior per interface concept
- locality: where future changes land
- seam placement: what caller no longer knows
- testability: what can be tested through public interface
- migration risk: how much public API/caller churn

End with opinionated recommendation. If hybrid is best, propose hybrid.
