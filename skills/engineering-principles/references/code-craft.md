# CODE CRAFT

_Guidebook for any agent coding in this environment. Read linearly on load. Apply immediately. Every word earns its place._

---

## QUICK REFERENCE

|Situation|Go to|
|---|---|
|Starting a new project|GEAR SELECTION → PRE-BUILD CHECKLIST|
|Joining an existing codebase|BEFORE YOU CODE → reading checklist|
|Before starting any task|HOW AGENTS FAIL → pre-task checklist|
|Something is broken|BUG FIX PROTOCOL|
|Brief feels wrong|AMBIGUITY HANDLING|
|Touching 5+ files|MULTI-FILE SEQUENCING|
|Setting up logging|LOGGING DISCIPLINE|
|Setting up config / env vars|ENVIRONMENT & CONFIGURATION|
|Building a tool agents will call|AGENTIC TOOL DESIGN|
|Handling errors across layers|ERROR HANDLING CONVENTIONS|
|Spawning a sub-agent|SUB-AGENT BRIEFING|
|Stuck after 3 attempts|FAILURE RECOVERY → escalation|
|Recognizing a known problem|PATTERN RECOGNITION|
|Shipping a CLI tool|GITHUB HYGIENE|

---

## GEAR SELECTION

Before any coding task, pick a gear. This resolves all contradictions in this document.

**SHIP** — MVPs, prototypes, quick fixes, validation, speed-critical work. Known stack only. SQLite over Postgres. OAuth over custom auth. Deploy before tests. Scope cuts mandatory when blocked.

**BUILD** — Production systems, refactors, complex bugs, architecture, team-shared code. Full reads of all relevant files. Tests required. Clean commits. Error handling mandatory.

**Default:** BUILD for existing codebases. SHIP for new projects or quick scripts.

The old mode names (SHOW, SCALE, VIBE) map to: SHOW → BUILD, SCALE → BUILD, VIBE → SHIP.

For agentic tools: define the interface contract first. CLI and MCP are both outputs of that contract, not a hierarchy.

---

## CONTEXT PRINCIPLES

**Context Poison.** Every token that doesn't change the output degrades it. Strip persona fluff, vague role descriptions, and restated instructions from sub-agent briefs. Real docs, concrete examples, actual file structure, history of what was tried — these are signal.

**AI Amplification.** AI does not fix weak structure — it multiplies it. Small inconsistencies in naming or conventions get amplified exponentially. 1,000 lines of well-structured code stays manageable. 1,000 lines of ambiguous structure becomes 10,000 lines of mess in a single session. Get naming, structure, and error handling right in the first 30 minutes before generating volume.

**Context Conservation.** Only load files directly relevant to the task. Use targeted search instead of reading entire files (except BUILD gear exploration, which requires full reads). Don't run unnecessary linters or validators in the same context as the main task. Include raw error output verbatim — never paraphrase.

**Context Staleness.** If more than 10 tool calls have passed since you read a file you're about to modify, re-read it before touching it. The cost is one tool call. The cost of not re-reading is a broken intermediate state you'll spend an hour debugging.

---

## AMBIGUITY HANDLING

The brief is not always right. Executing a wrong brief faster is not helpful.

**Reframe before building when:** the request describes a solution not a problem, two interpretations produce architecturally different outcomes, the ask duplicates something existing, or it will create obvious tech debt.

**Reframe test.** Before starting: _"The underlying problem this solves is ____."_ If you can't complete it, ask. If it reveals the request is solving the wrong thing, say so.

**When the brief is wrong, raise it explicitly:**

```
REFRAME: The request asks for X, but the underlying problem appears to be Y.
SUGGEST: Z would solve Y more directly and with less complexity.
PROCEED: If you want X anyway, I'll build it — but flagging this first.
```

Don't silently build the wrong thing. Don't refuse either. Raise it once, clearly, then execute the decision.

---

## BEFORE YOU CODE

**Understand before changing.** Never change code you haven't read.

- SHIP gear: scan key files, understand structure, then drill into specifics
- BUILD gear: read all relevant source files completely. Trace data flow, identify dependencies and side effects, understand test coverage

**Reading an unfamiliar codebase — do this before touching anything:**

```
1. README          — what is this and why does it exist
2. AGENT.md        — how to work here specifically
3. Directory map   — where things live
4. Entry point     — trace how the system starts
5. Permission zones — what you can and can't touch
6. Tests           — what working looks like
7. Recent commits  — what's been changing and why
8. Only then: start
```

**Blast radius.** SHIP: quick estimate. BUILD: explicit file count + complexity (trivial/moderate/major). If > 5 files or major complexity, break into sequential steps. Small bombs ship faster and cleaner than one Fat Man. If scope expands mid-task: stop, reclassify, restart with smaller radius.

**Act without asking when:** within permission zone, blast radius small and reversible, enough context.
**Ask before acting when:** blast radius large or irreversible, restricted zone, two valid approaches with different architecture, brief feels wrong.

---

## PRE-BUILD CHECKLIST

Apply before starting any new project:

1. Interface contract — inputs, outputs, error states — define this first. CLI and MCP both derive from it.
2. Directory structure — `src/cli/`, `src/commands/`, `src/core/` — CLI project template
3. Shared utilities — error handling, logging, validation, config loading — write these first
4. Naming conventions — functions, files, types — written down, not implied
5. API boundaries — what talks to what, what's public, what's internal
6. AGENT.md — if another agent can't read cold in 60 seconds, rewrite it

For existing repos, use the reading checklist above instead.

---

## STACK DECISION TREE

Traverse this. Don't debate it in SHIP gear.

```
Need persistence?
├── < 1,000 records          → JSON file
├── < 100,000 records        → SQLite
└── > 100,000 / concurrent   → Postgres (BUILD gear only)

Need auth?
├── MVP                      → Magic links
├── Growth                   → OAuth (Google / GitHub)
└── Custom auth              → Prohibited. Always.

Need agent-facing interface?
├── Human + agent            → CLI with --json AND MCP server from same core
├── Agent only               → MCP server, skip CLI
└── Human only               → CLI

Need frontend?
├── Fastest                  → Vanilla HTML + JS
├── Known stack              → React / Vue (existing knowledge only)
└── New framework            → Prohibited in SHIP gear

Need to deploy?
├── Now                      → Vercel / Railway
├── Cost-sensitive           → VPS (Hetzner / DigitalOcean)
└── Complex infra            → Prohibited in SHIP gear

Repeating a task 3+ times?
└── Build a tool: watcher, generator, deploy script, review agent
```

Architecture emerges from real pain. Don't design it upfront.

---

## MULTI-FILE SEQUENCING

When a change spans 5+ files, the order matters. Broken intermediate states mislead you and make rollback harder.

**Default sequence:**

```
1. Interfaces and types first    — define the contract before the implementation
2. Core logic second             — implement against the contract
3. Adapters and integrations     — wire the core to the outside world
4. Entry points last             — CLI, API handlers, routes
5. Tests after each layer        — not at the end
```

If you break at step 2, the interface is still clean and rollback is surgical. Breaking at step 1 is cheap — nothing depends on it yet.

**Never:** touch entry points before core logic is verified. Never wire an integration before the thing it integrates with is tested in isolation.

If mid-sequence you discover the interface was wrong, stop. Fix the interface. Propagate forward. Don't patch implementations to compensate for a bad contract.

---

## CODE STANDARDS

### Naming

Names are the first documentation. If a name needs a comment to explain it, the name is wrong.

**Name by role, not type.** The type system already knows it's a list. Tell the reader what it _means_.

```ts
// ❌ type in the name — redundant
const employeeList = fetchEmployees();

// ✅ role suggests usage
const employees = fetchEmployees();
const ordersByCustomer = new Map();
```

**Name the concept, not the algorithm.** Callers don't care how you implement it.

```ts
// ❌ exposes implementation
users.linearSearchFor(userId);

// ✅ names the intent
users.includes(userId);
```

**Explaining variables.** When an expression is hard to read, assign it to a well-named variable.

```ts
// ❌ dense
if (user.orders.filter(o => o.status === 'shipped').reduce((s, o) => s + o.total, 0) > 1000) {}

// ✅ each step named
const shippedOrders = user.orders.filter(o => o.status === 'shipped');
const totalSpent = shippedOrders.reduce((s, o) => s + o.total, 0);
if (totalSpent > 1000) {}
```

Functions are verbs. Booleans are questions (`isLoading`, `hasPermission`). Name contains "And" — doing two things — split it. Named constants over magic literals.

### Functions

```
Max 20 lines   — scrolling means splitting
Max 3 params   — beyond that, options object
Max 2 nesting  — early returns beat else blocks
```

One reason to change. If you need "and" to describe it, split it.

**Same level of abstraction.** A function should read like a table of contents.

```ts
// ❌ mixing levels
function processOrder(order) {
  validateOrder(order);
  const db = new DatabaseConnection('postgres://...');
  const query = `INSERT INTO orders ...`;
  db.exec(query);
  sendEmail(order.customerEmail, 'Order received');
}

// ✅ same level throughout
function processOrder(order) {
  validateOrder(order);
  saveOrderToDatabase(order);
  notifyCustomerOfReceipt(order);
}
```

**Fail fast.** Early returns beat nested if-blocks.

### DRY / CQS

Every piece of knowledge exists in exactly one place. DRY isn't about code — it's about knowledge.

**Queries ask; commands tell.** If a function returns a value, it shouldn't mutate. If it mutates, it shouldn't return.

```ts
// ✅ query — no side effects
function isValidUser(id: string): boolean { return db.users.exists(id); }

// ✅ command — clearly changes something
function recordUserCheck(id: string): void { db.users.update(id, { lastChecked: new Date() }); }
```

### Type Safety

```ts
// ✅ illegal states unrepresentable
type UserRole = 'admin' | 'editor' | 'viewer';
type UserId   = string & { readonly _brand: 'UserId' };
function createUser(role: UserRole, id: UserId) {}
```

Every `as` or `any` gets marked: `// TODO: remove cast when lib adds proper types`. Visible debt beats hidden debt.

**Replace conditionals with polymorphism.** Repeated `if`/`switch` on the same discriminator means adding a case edits existing code.

```ts
// ✅ adding Apple Pay? New class, nothing else changes.
interface PaymentMethod { charge(amount: Money): void; }
class CardPayment implements PaymentMethod { charge() { ... } }
class PayPalPayment implements PaymentMethod { charge() { ... } }
```

**Collection safety.** Never return a raw mutable collection from a getter — return a snapshot.

**Behavior over state.** Design the public interface first. What does this thing _do_? Internal representation can change later if hidden behind a clean API.

**Delegate, don't inherit.** Pass work to a collaborator, not subclassing. Keeps objects independently replaceable.

**Constructors create well-formed objects.** Never half-initialize. Pass all required dependencies upfront. If construction is complex, use a factory function.

**Encapsulate fields.** Access instance fields through methods — single place for validation, logging, lazy init, or change notification later.

**Other essentials:** equality/hash must match (same fields for both). Lazy initialization for expensive computations. Initialize all state at construction. Method objects for complex logic with shared temporaries. Abstraction ladder: 1 use → inline, 2 uses → consider helper, 3 uses → abstract.

**Comments are for why, not what.** If a comment restates what the code does, delete it.

### Error Handling

Never catch what you can't handle — let it bubble.

```ts
// ❌ silent killer
try { await doTheThing(); } catch (e) {}

// ✅ typed, named, contextual
class PaymentError extends Error {
  constructor(message: string, public readonly code: string) { super(message); this.name = 'PaymentError'; }
}
```

Always log with context: what was being attempted, what input caused it, what state the system was in.

**Configuration errors must guide, not crash.**

```ts
// ✅ guides the user
if (!apiKey) {
  throw new ConfigError('OPENAI_API_KEY not set', 'Add to .env or run: export OPENAI_API_KEY=...');
}
```

**Resource bracketing.** When two actions must always happen together, expose a single function that accepts a callback.

---

## ERROR HANDLING CONVENTIONS

_Layered model for production failure handling._

Four levels — each adds context, none swallows it:
1. **Service** — API-specific (network, auth, rate limits)
2. **Orchestration** — unified handling across services
3. **Agent** — retry logic and recovery decisions
4. **Client** — structured error info passed back to callers

Errors get context as they bubble up. "Element not found. Did you run `peekaboo see` first?" — the top-level error tells the human exactly what went wrong and what to try next.

**Defensive defaults:** validate permissions before operations, timeout on every external call, graceful degradation with fallbacks, state validation before execution.

**Structured errors with recovery paths.** Throw typed errors with codes, context, and suggested fixes — never strings.

---

## LOGGING DISCIPLINE

**File-based by default. Never stdout in production.** Output to stdio disrupts clients (MCP, CLI parsers, agents).

**Structured logging (pino-style):** `{"level":30,"time":1713747200000,"msg":"Build completed","target":"cli","duration":1234}`

- Default file logger in `~/.logs/` or `/tmp/`, configurable via `[ProjectName]_LOG_FILE`
- Auto-creates missing parent directories, falls back to temp if primary path fails
- Flush before process exit — no lost messages

**Configurable verbosity without restarting:** `[ProjectName]_LOG_LEVEL` env var (any case), `[ProjectName]_CONSOLE_LOGGING=true`, `--verbose` or `--json` CLI flags.

**Category-specific capture for debugging.** Log by category, time window, or subsystem — don't capture the entire firehose.

**Never log secrets.** Redact API keys, tokens, passwords. Log the fact that auth happened, not the credentials.

---

## ENVIRONMENT & CONFIGURATION

**Sensible defaults — works out of the box.** Every environment variable has a reasonable default.

**Structured config loading.** One provider that reads, validates, and normalizes — not scattered `process.env` calls.

```ts
const config = Config.fromEnvironment();
const apiKey = config.getApiKey();     // throws ConfigError if missing
const timeout = config.getTimeout();   // defaults to 30s if not set
```

**Lenient parsing, strict advertising.** Accept variations (e.g. `path` for `project_path`, any case for log levels). Make it hard to use wrong, not impossible.

**`info` command pattern.** Every tool must offer an `info` subcommand: version (from package.json, never hardcoded), dependency status, config issues, missing env vars.

**Version injected at build time, never hardcoded.** Same version across TypeScript layer and native binaries.

**Custom path overrides for every external dependency.** `[ProjectName]_BINARY_PATH` — you can point any external binary anywhere.

---

## AGENTIC TOOL DESIGN

Tools that agents call have different requirements than tools humans run.

**Idempotency.** Agents retry. Every tool must be safe to call twice with the same inputs. Document whether each operation is idempotent.

**Error semantics.** Exit codes and stderr are human conventions. Agents need: is this permanent or transient? Is it retryable, after how long? What's the recovery path? Return structured error responses with code, retryable flag, retryAfterMs, and fix hint.

**Output budget.** Every token of tool output costs reasoning capacity. Return exactly what's needed, nothing more. Verbose logs and raw dumps are context poison. Default to minimal output, expand with `--verbose`.

**MCP vs CLI.** For agent-first tools, MCP is not a nice-to-have — typed inputs/outputs, schema descriptions, structured errors. For human-first tools that agents also use, ship both from shared core.

**Health check.** The `info` command is the CLI equivalent of a health endpoint. Agents should call it before starting work.

---

## IMPLEMENT THEN TEST

TDD wastes context on speculative test design. Instead:
1. Implement the change
2. Verify it works end-to-end
3. Write tests that cover the new behavior and edge cases
4. Refactor if needed
Exception: if explicitly requested, follow TDD.

**Tests are specifications.** Name them as such: `it('should reject payment when card is expired')`.

```
Unit         — pure logic, no I/O, fast
Integration  — real DB, fake network
E2E          — critical journeys only, slow, precious
```

A test needing 50 lines of mocking is testing the wrong thing. Refactor the code, not the test. BUILD gear: tests required. SHIP gear: tests expected for anything non-trivial.

---

## ZERO-TRUST EXECUTION

Code is not real until the shell proves it.

1. Never guess endpoints. Check official docs before writing the code.
2. Never guess execution. If you write a script, bash wrapper, or API call, exec it immediately.
3. If you cannot test it, you cannot ship it. State explicitly: `[UNVERIFIED — REQUIRES HUMAN TO TEST]`.

An LLM generates plausible text. An engineer executes and verifies. Be the engineer.

---

## PATTERN RECOGNITION

When you notice one of these smells, apply the matching pattern. The smell is the trigger.

1. **Output repeats mid-stream** → Streaming Dedup with Overlap Heuristics. Check tail of existing vs head of new chunk. Append only non-overlapping suffix.
2. **Queue, everything urgent, nothing gets done** → Exponential Priority Decay. Score by recency (exp decay × half-life) × focus ratio. Not FIFO.
3. **"Resource busy" but nothing holds it** → Stale Lock Detection with Heartbeats. Check if lock's PID is alive, if heartbeat is fresh. Dead processes leave live locks.
4. **API identifiers worked yesterday, 404 today** → Dynamic API Hash Resolution. Scrape the client (JS bundle, HTML) that generates identifiers. Parse webpack maps. Cache.
5. **Standard API returns empty for some inputs** → Multi-Strategy Child Discovery. Try alternative attributes, fallback selectors, different traversal methods.
6. **EBUSY/ENOTEMPTY on writes (esp. Windows)** → Atomic File Write with Retry. Write to temp file, rename with exponential backoff.
7. **Same try/retry/fallback copied 3×** → Variadic AutoCall with Generics. Extract into generic wrapper across different return signatures.
8. **Config "doesn't work" but does on your machine** → Multi-Source Config Aggregation. Load from all known locations, merge with first-write-wins.
9. **"Database is locked" but connection released** → DB Snapshot. Copy DB (including WAL) to temp, read from snapshot, delete after.
10. **Permission check says no, operation succeeds** → Permission Probing via Operation. Trust the result, not the gatekeeper.
11. **Tree traversal hangs on finite graph** → Cycle Detection with Hashing. Hash visited nodes. Guard with visited set + depth limit.
12. **Error output too noisy** → Warning Aggregation with Dedup. Compact repeated warnings. Cap to top 3. Show the pattern.
13. **Hardcoded upstream identifier broke after deploy** → Dynamic API Discovery from Client Bundles. Download JS bundle, parse module maps, extract identifiers. Cache. Never hardcode upstream values.
14. **SDK hangs on exit, cleanup never fires** → Monkey-Patch SDK Prototypes with WeakMaps. Patch upstream prototype to fix cleanup bugs. Track child processes with WeakMap.

---

## BUG FIX PROTOCOL

**The Iron Law: No fix without investigation.**

1. Reproduce the failure consistently
2. Trace the data flow from input to the broken point
3. Form a hypothesis about root cause
4. Test the hypothesis (add logging, isolate the component)
5. Only then implement the fix
6. After 3 failed attempts: STOP. Escalate. Reassess.

**Phase 1 — Root Cause Investigation (before any fix):**
- Read error messages completely — stack traces, line numbers, error codes. Don't skip past warnings.
- Reproduce consistently — if not reproducible, gather more data, don't guess.
- Check recent changes — git diff, last 10 commits, new dependencies, config changes.
- For multi-component systems: add diagnostic instrumentation at each component boundary. Log what enters, what exits, verify config propagation, check state at each layer. Run once to find WHERE it breaks, THEN investigate that component.
- Trace data flow upstream: where does the bad value originate? What called this with the bad value? Fix at the source, not the symptom.

**Phase 2 — Pattern Analysis (before fixing):**
- Find working examples in the same codebase. What works that's similar?
- If implementing a known pattern, read the reference COMPLETELY — don't skim.
- List every difference between working and broken, however small. Don't assume "that can't matter."
- Understand all dependencies: config, environment, assumptions.

**Phase 3 — Hypothesis (scientific method):**
- Form a SINGLE hypothesis. State clearly: "I think X is the root cause because Y." Write it down.
- Test minimally — smallest change, one variable at a time. Don't fix multiple things.
- If it doesn't work: form a NEW hypothesis. Don't add more fixes on top.
- When you don't know: say "I don't understand X." Ask the user. Research more. Don't pretend to know.

**Phase 4 — Implementation:**
- Create failing regression test BEFORE fixing. The test proves it and prevents recurrence.
- Implement single fix addressing the root cause. ONE change. No "while I'm here" improvements.
- Verify: specific test passes, full suite still passes.

**The Rule of Three — when fixes fail:**
- If < 3: return to Phase 1, re-analyze with new information.
- If ≥ 3: STOP. Question the architecture, don't try fix #4.

**Questioning architecture — pattern indicators:**
- Each fix reveals new shared state/coupling in a different place
- Fixes require "massive refactoring" to implement
- Each fix creates new symptoms elsewhere
This is NOT a failed hypothesis — this is a wrong architecture. Discuss with the user before more fixes.

Every bug fix gets:
1. Atomic commit (one fix = one commit)
2. Regression test that would have caught it
3. Commit message explaining root cause, not symptom

```
fix(auth): handle expired JWT during token refresh

Root cause: refresh endpoint assumed token was valid when
checking expiry, but expired tokens threw before the check.

Regression test: test_expired_token_triggers_refresh
```

**Dead end documentation.** Record failed approaches before moving on:
```
DEAD END: tried X because Y. Failed because Z. Do not retry.
```
Undocumented dead ends get re-attempted by the next agent. Record them.

**Red flags — STOP and return to Phase 1:**
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Add multiple changes, run tests"
- "Skip the test, I'll manually verify"
- "I don't fully understand but this might work"
- "One more fix attempt" (after 2+ failures)
- Each fix reveals a new problem in a different place

## VERIFICATION & COMMIT

**Safe modification before touching anything significant:**
READ → STATUS (git check, stash if needed) → BACKUP (timestamp if high-risk) → APPLY → VALIDATE → TEST → LOG.

**20% refactor cycle.** Ship first, then clean. One focused pass on files already modified — improving only what you now understand. Don't expand scope. Leave codebase cleaner than found, not perfect.

**Permission zones:**
- **Move freely** — memory, docs, tools, skills, scripts
- **Move with tests** — CLI, adapters, implementations
- **Explicit permission** — Gateway, sandbox, core config
- **Never touch** — `.git/`, `node_modules/`, `*.lock`, credentials

---

## SUB-AGENT BRIEFING

**Destination not route.** "Refactor the payment module to use the repository pattern" outperforms a 10-step specification. The sub-agent has capability — use it.

**Real context only.** Open with the actual situation: the file, the constraint, what was tried, success criteria. Apply context poison rules. No role declarations.

**Task brief:**
```
GEAR:       [ship / build]
GOAL:       [one sentence — what done looks like]
RADIUS:     [small / controlled / large]
CONTEXT:    [files, changes, constraints]
TRIED:      [what failed and why]
DEAD ENDS:  [approaches confirmed not to work]
MUST NOT:   [explicit off-limits]
CHECKPOINT: [when to stop and report back]
```

**Completion report — success:**
```
SHIPPED:    [what works now]
COMMITS:    [list]
TESTS:      [pass / fail / none — and why]
CLI:        [--help ok, --version ok, --json valid]
DOCS:       [AGENT.md/CHANGELOG/docs updated]
DEBT:       [any tech debt introduced]
DEAD ENDS:  [approaches confirmed dead]
NEXT:       [suggested follow-up]
```

**Completion report — blocked:**
```
STUCK:      [what task]
COMPLETED:  [what was finished before hitting block]
WHY:        [what's blocking]
TRIED:      [approaches attempted]
DEAD ENDS:  [what definitely doesn't work]
NEED:       [exactly what's needed from human]
ROLLBACK:   [yes/no — state left clean?]
```

A completion report that omits dead ends is incomplete.

---

## FAILURE RECOVERY

**Detection → Response:** syntax error → stop and fix. Test failure → stop, assess scope. Merge conflict → stop, resolve manually. Tool unavailable → log, retry once, escalate. 30 min without progress → escalate.

**Rollback protocol:** STOP → ASSESS (last known good commit) → STASH → REVERT → VERIFY → LOG → RESUME (smaller blast radius).

**Escalation format:**
```
STUCK: [what task]
WHY:   [what's blocking]
TRIED: [approaches attempted]
NEED:  [what is needed from human to unblock]
```

Escalate after: 3 failed attempts, blast radius expanding, unclear permission zone, or something feels wrong.

---

## QUALITY GATES

Binary. Either it passes or it doesn't.

**SHIP gear:**
- [ ] Runs locally
- [ ] `--help` and `--version` correct
- [ ] `info` subcommand accurate
- [ ] Deployable in one command
- [ ] README reflects current state
- [ ] CHANGELOG.md updated
- [ ] Committed — atomic, typed, reasoning in body

**BUILD gear:**
- [ ] Tests pass
- [ ] No agent file conflicts
- [ ] 20% refactor pass done — only files already touched
- [ ] AGENT.md updated
- [ ] CHANGELOG.md updated
- [ ] No dead code
- [ ] `--json` output valid for all commands

**DONE — universal, every task:**
- [ ] Another agent reading cold understands in 60 seconds
- [ ] 3am error tells the engineer what went wrong
- [ ] Regression test exists
- [ ] Dead ends documented
- [ ] Codebase cleaner than when you arrived

---

## AGENT.MD

Every repo must have one. It's part of the product.

Contents:
- Project purpose (2 sentences)
- Directory map
- CLI command reference
- Active gear and why
- Stack decisions already made and reasoning
- Test command, deploy command
- Permission zones specific to this repo
- Known issues — what's broken and why
- Dead ends — what was tried and failed
- What "done" looks like here

Update AGENT.md whenever you learn something that saves the next agent 5 minutes.

---

## HOW AGENTS FAIL

Specific failure modes with detection signals and corrections. Each has caused real damage in real sessions.

| # | Failure Mode | Signal | Correction |
|---|---|---|---|
| 1 | **Confidence without verification** | "Should work" without running it | Execute it or mark `[UNVERIFIED]` explicitly |
| 2 | **Brief acceptance** | Coding within 2 calls, no reframe test done | Complete: "The underlying problem is ___" before writing |
| 2b | **Directional misinterpretation** | Coding after "what's next?" / "do you know what to do?" | These mean CONFIRM DIRECTION. State the plan. Wait for go-ahead. User frustration response like "I didn't say go on a mad one" = you did this. |
| 3 | **Context drift** | Modifying file read >10 calls ago | Re-read before touching. No exceptions. |
| 3 | **Context drift** | Modifying file read >10 calls ago | Re-read before touching. No exceptions. |
| 4 | **Premature convergence** | 3+ calls into implementation without considering alternatives | Spend one call asking: what would a senior engineer choose? |
| 5 | **Blast radius creep** | Modifying a file outside initial estimate | Stop. Note as follow-up task. Finish original scope first. |
| 6 | **Sycophantic correction** | Changing answer after pushback with no new information | Hold position, explain reasoning once more. Don't collapse. |
| 7 | **Completion bias** | 3 failed attempts, framing as "almost there" | Escalate. Surface the block, don't bury it. |
| 8 | **Partial read confidence** | Decisions based on partial read of >100 line file | Read it completely. In BUILD gear this is mandatory. |
| 9 | **Error paraphrasing** | "The error says something about..." instead of quoting | Include full raw error output verbatim. It's data. |
| 10 | **Silent assumption** | 5+ calls into an implementation based on unstated assumption | State assumptions explicitly before acting. "Assuming X — flag me if wrong." |

**Pre-task checklist — run before starting:**
```
[ ] Reframe test complete — underlying problem identified
[ ] Blast radius estimated — files to touch known
[ ] Context current — files read recently (<10 calls ago)
[ ] Approach considered — alternatives weighed
[ ] Assumptions named — ambiguities stated explicitly
[ ] Verification plan — how I will prove this works
```

