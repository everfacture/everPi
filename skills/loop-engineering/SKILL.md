---
name: loop-engineering
description: "Design safe Pi agent loops: recurring runs, CI/issue triage, evaluators, MCP/extension workflows, schedules, persistence, budgets, and human gates."
---

# Loop Engineering

Use when designing a Pi workflow that should run more than once: scheduled agent runs, CI/issue/PR triage, repo-health checks, evaluator loops, prompt/model hill-climbs, MCP-backed automations, or Pi extensions that enforce loop policy.

Do **not** use for one-off coding/debugging/refactoring. Use `engineering-principles` for normal code work. A loop is justified only when work recurs, state matters, verification can fail the run, or a scheduler/event source will re-trigger it.

Core doctrine:
- Loop replaces human re-prompting, not human judgment.
- Hard part is not making agent run. Hard part is adding something that can say **no**.
- Prefer smallest deterministic verifier before clever autonomy.
- Persist state outside chat. Context is cache, not memory.
- Human gates stay mandatory for irreversible or sensitive side effects.

## 0. Start Gate

Before proposing or building a loop, answer:

```text
LOOP:       [name]
VALUE:      [recurring outcome]
SOURCE:     [CI/issues/logs/inbox/API/etc]
ARTIFACT:   [skill | extension | MCP | script | cron | Actions | worktree]
VERIFY:     [checks/evaluator that can fail]
STATE:      [file/issue/DB/log where memory persists]
SCHEDULE:   [manual/cron/webhook/CI/cloud]
BUDGET:     [time/retries/tokens/files changed]
GATE:       [human approval points]
STOP:       [done/no-progress/escalation condition]
```

If any line is unknown, name gap before implementation.

## 1. Should This Be a Loop?

| Question | Good sign | Bad sign |
|---|---|---|
| Recurs? | CI, logs, issues, metrics, inbox, or data drift repeat | one bug, one file, one fix |
| Source? | real input source with IDs/timestamps | vague desire to "improve" |
| Action? | outputs scoped task/report/PR | endless generic advice |
| Verification? | tests, lint, smoke, evaluator, human gate | same agent self-grades |
| State? | needs run history, queue, seen IDs, decisions | answer can be stateless |
| Risk bounded? | sandbox/worktree/branch/budget/gate | can deploy/delete/pay/trade blindly |

Three or more bad signs: do direct work, not loop engineering.

## 2. Pick Smallest Artifact

| Need | Build |
|---|---|
| reusable procedure/rubric/checklist | **Skill** |
| enforce/block/confirm tool calls, inject context, save traces, add commands/UI | **Pi extension** |
| call external systems: GitHub, Slack, Linear, DB, cloud, browser | **MCP/tool connector** |
| local recurring run | script + cron/systemd/Pi command |
| repo-only unattended run | GitHub Actions/cloud runner |
| parallel code edits | git worktrees/branches |

Default: skill first. Upgrade only when runtime enforcement, external access, or scheduling proves necessary.

## 3. System Type Sets Shape

| Type | Loop shape | Rule |
|---|---|---|
| Clear | checklist/script + deterministic gate | automate directly |
| Complicated | inspect → isolate → patch/report → review/test | use maker/checker |
| Complex | small experiments + measurement | optimize by evidence |
| Chaotic | stabilize, preserve logs, stop damage | do not schedule chaos |

## 4. Five Moves Per Turn

Every loop turn needs:

1. **Discovery** — read work source: CI, issues, PRs, logs, metrics, queue, API.
2. **Handoff** — convert one finding into one isolated task: branch/worktree/job/subagent.
3. **Verification** — independent check can fail: tests, smoke, evaluator, reviewer, human.
4. **Persistence** — write result/state outside context: PR, issue, board, state file, DB, log.
5. **Scheduling** — define next trigger: manual command, cron, webhook, CI schedule, cloud job.

Missing move = harness, not loop. Call it out.

## 5. Verification Stack

Never let generator be final judge.

Prefer in order:
1. **Deterministic checks** — tests, typecheck, lint, schema, static/security scan.
2. **Behavior checks** — API/app run, Playwright path, screenshot/DOM, smoke test.
3. **Independent evaluator** — fresh context, skeptical rubric, quotes evidence.
4. **Human gate** — required for sensitive judgment or side effects.

Evaluator prompt shape:

```text
Assume output is broken until evidence proves otherwise.
Judge behavior, not intent.
Quote exact failing evidence.
PASS only if every requirement has evidence.
If uncertain, FAIL with missing evidence.
```

If no deterministic check exists, create smallest useful verifier before adding autonomy.

## 6. Isolation Rules

- One finding = one task.
- Multiple agents editing code = separate worktrees/branches/temp dirs.
- Do not let parallel workers share one dirty worktree.
- Broad refactor, migration, deploy, release, or public comms requires human gate.
- Loop may prepare PR/report; human decides merge/deploy/send.

## 7. Persistence

State must survive context loss. Put it where operator will look:

- repo-owned loop: `docs/agent-loop-state.md` or issue/PR labels/comments
- ops loop: dashboard/state file in durable ops workspace
- research/eval loop: result log + decisions file
- external queue: DB/board/ticket system with stable IDs

Minimum state file:

```markdown
# [Loop] State

## Objective
[recurring outcome]

## Last Run
- time:
- trigger:
- inputs read:
- outputs produced:
- checks passed:
- checks failed:
- cost/time:

## Queue
| id | source | task | status | owner/worktree | next step | gate |
|---|---|---|---|---|---|---|

## Decisions
- YYYY-MM-DD: [decision + reason]

## Failure Modes
- [failure] → [guard]
```

Never store secrets. Record that secret/config exists; do not copy values.

## 8. Scheduling + Budgets

Schedule only after manual run + verification pass.

| Need | Scheduler |
|---|---|
| local files/dev server | local cron/systemd/manual Pi command |
| repo-only/nightly | GitHub Actions/cloud runner |
| external event | webhook/MCP/serverless |
| human-curated queue | issue label/comment/Slack command |

Set caps before background execution:

```text
MAX_RUNS_PER_DAY=
MAX_RETRIES_PER_ITEM=
MAX_WALL_TIME_PER_RUN=
MAX_FILES_CHANGED_PER_TASK=
MAX_PARALLEL_TASKS=
MAX_TOKENS_OR_COST_PER_DAY=
```

Cap hit = stop and escalate. Retrying without new evidence is loop rot.

## 9. Human Gates

Require explicit approval for:

- merge, deploy, release, publish
- money, payments, orders, trading
- DB writes, migrations, deletes, destructive filesystem ops
- credentials, auth, security policy
- public/customer/client communications
- broad refactors or high-blast-radius changes
- evaluator uncertainty

Loop prepares decision-quality evidence. Human owns decision.

## 10. Hill-Climb After Runs

After 3-5 runs, review traces/state. Improve in this order:

1. discovery filters and context assembly
2. deterministic checks
3. skill/rubric wording
4. connector/tool reliability
5. evaluator strictness
6. schedule/budget caps
7. model choice last

Record each harness change in state decisions.

## 11. Pi Extension Upgrade Triggers

Move from skill/script to Pi extension when loop must:

- block/confirm sensitive `bash`, `write`, `edit`, or MCP calls
- inject loop state/rubric before agent start
- append run evidence after tool results or agent end
- register `/loop-*` commands or custom tools
- show queue/status/review UI
- enforce budgets or path allowlists at runtime

Keep policy in skill. Put enforcement in extension.

## 12. Anti-Patterns

Stop these:

- prompt wall in cron instead of named skill/procedure
- vague objective: "improve repo" / "make better"
- no persistent state; chat memory only
- same agent writes and self-approves
- PR spam without failing/passing gate
- auto-merge/deploy/release without gate
- parallel agents in same worktree
- retry loops without diagnosis
- hiding/skipping tests to get green
- no-change notifications every run
- no budget/retry caps
- local scheduler for work that must run while laptop is off

## 13. Output Format

When asked to design a loop, answer:

```text
RECOMMEND: [skill/extension/MCP/script/scheduler]
WHY: [short reason]
LOOP CONTRACT:
  objective:
  discovery:
  handoff/isolation:
  verification:
  persistence:
  schedule:
  budget caps:
  human gates:
  stop/escalation:
IMPLEMENTATION PLAN:
  1. [step] → verify: [check]
  2. [step] → verify: [check]
  3. [step] → verify: [check]
RISKS:
  - [risk] → [guard]
```

When reporting loop work, include status, loop shape, changed files/commands, evidence, remaining gates, and next loop turn.
