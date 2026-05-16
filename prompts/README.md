# Prompt Templates

Prompt templates expand into full instructions when invoked. All three
output a single self-contained HTML file — open it in a browser.

Invoke with `/prompt-name [optional-arg]`.

## html-slide-deck

**Use when:** you want findings presented as a browsable deck, not terminal
wall-of-text.

```
/html-slide-deck analyze this codebase
```

Produces one HTML file with:
- Left-side table of contents
- Concrete findings with file paths
- Compact code snippets
- Recommended next steps

## evaluation-pack-template

**Use when:** you want the agent to prove its work before claiming "done."

```
/evaluation-pack-template implement the auth middleware
```

The agent must complete the task AND produce an evaluation pack:
- What changed and why
- Exact files changed
- Commands run with outcomes
- Verification evidence (screenshots for UI, repro steps for bugs)
- Known limitations
- Delivered as a self-contained HTML page

See also the `evaluation-pack` extension (`/evaluation-mode on`) for
persistent mode across a whole session.

## session-friction-review

**Use when:** audit a session to find wasted agent motion and improve repo
affordances for next time.

```
/session-friction-review                           # review current session
/session-friction-review ./logs/session.jsonl      # review specific file
```

The `argument-hint: "[session/context]"` in the template is optional.
Pass a path to review a specific session, omit it for the current one.
The template uses shell expansion (`${ARGUMENTS:+: $@}`) — if you pass an
argument it becomes `": ./logs/session.jsonl"`, otherwise nothing.

Analyzes:
- Wrong turns before finding the right path
- Repeated searches, file reads, or tool calls
- Documentation gaps or stale instructions
- Noisy output that likely distracted the agent
- Context bloat that should have been branched sooner

Output is an HTML slide deck with friction points, root causes, and
highest-priority fixes.
