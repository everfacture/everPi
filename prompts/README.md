# Prompt Templates

Invoke in Pi with `/prompt-name [args]`.

## html-slide-deck

```
/html-slide-deck analyze this codebase
```

Outputs findings as a single self-contained HTML slide deck with table of
contents, concrete findings, file paths, and recommended next steps.
Prefers sections, callouts, and short bullets over long prose.

## evaluation-pack-template

```
/evaluation-pack-template implement the auth middleware
```

Runs a task requiring verification evidence: changed files, commands run,
screenshots/GIFs for UI work, reproduction steps for bugs, known limitations,
presented as a self-contained HTML page.

## session-friction-review

```
/session-friction-review
```

Analyzes the current or specified session for wrong turns, repeated searches,
documentation gaps, noisy output, and context bloat. Outputs as HTML slide deck.
