# External Codebase Analysis Pattern

## When to Use

User asks: "look at [external repo], see if anything is worth stealing for our codebase."

## Workflow

1. **Read own codebase first** — understand the current architecture, pain points, and existing patterns before looking at the external code. You can't compare against nothing.

2. **Read external codebase** — focus on:
   - Architecture diagram / file structure
   - Core pipeline / main execution loop
   - Key design decisions (what they do differently)
   - Tools/utilities that solve real problems
   - Prompt engineering patterns (if AI-driven)

3. **Compare and rank** — for each external pattern:
   - Does it solve a problem we have? (Impact)
   - How hard would it be to integrate? (Effort)
   - Does it conflict with our existing architecture? (Compatibility)
   - Rank: HIGH VALUE / MEDIUM / NICE TO HAVE / SKIP

4. **Write a plan doc** — save to `docs/PLAN_<TOPIC>.md` in the repo with:
   - What's worth stealing (ranked by impact)
   - What's NOT worth taking (and why)
   - Execution order with effort estimates
   - Bug fixes discovered during analysis

5. **Execute quick wins first** — same-day fixes that don't change architecture. Then tackle the bigger items.

## Principles

- **Steal patterns, not code.** The architecture decision is the value, not the implementation details.
- **Don't copy what already works better.** If our approach is superior, say so explicitly.
- **Respect the product context.** What works for a desktop agent may not work for a web app.
- **Plan before touching code.** Write the analysis doc, get alignment, then execute.

## Example Output Structure

```
# Plan: [External Repo] Improvements

## Phase 1: Quick Wins (same-day)
### 1.1 [Fix/Improvement]
### 1.2 [Fix/Improvement]

## Phase 2: Big Changes (multi-day)
### 2.1 [Architectural Change]

## Phase 3: Polish
### 3.1 [Nice-to-have]

## What We're NOT Stealing
| Feature | Skip Reason |

## Bug Fixes Found
| Bug | Root Cause | Fix |
```
