# Fork-Adapt-Deploy Pattern

## When to Use

User asks you to fork an open-source project, adapt it to their needs (rename, reconfigure, add custom code), and deploy it as a standalone tool.

**Prerequisite:** `references/external-codebase-analysis.md` — analyze first, fork second.

## Workflow (4 passes)

### Pass 1: Fork + Rename + Install

```bash
# Private fork via gh CLI (assumes gh auth is set up)
gh repo fork <owner>/<repo> --clone --private --remote=false
mv <repo> <new-name> && cd <new-name>

# Rename package directory
mv src/<old-pkg> src/<new-pkg>

# Replace all imports
find . -type f -name '*.py' -exec sed -i 's/from <old-pkg>/from <new-pkg>/g' {} +
find . -type f -name '*.py' -exec sed -i 's/import <old-pkg>/import <new-pkg>/g' {} +

# Update pyproject.toml
sed -i 's/name = "<old-pkg>"/name = "<new-pkg>"/' pyproject.toml
sed -i 's/<old-pkg> = "<old-pkg>/<new-pkg> = "<new-pkg>/' pyproject.toml
# Fix packages directive if needed
sed -i 's/packages = \["src\/<old-pkg>"\]/packages = ["src\/<new-pkg>"]/' pyproject.toml

# Install
pip install -e .
```

**Order matters:** Rename BEFORE pip install. If you install first, import paths are baked into the installed package.

**Verify:**
```bash
python3 -c "from <new-pkg> import cli; print('OK')"
<new-pkg> --help
```

### Pass 1.5: Community Audit (Active Forks Only)

**Before** configuring data or modifying code, if the original repo has >100 stars or >10 forks, run a community audit:

```bash
# Check top forks by stars — these contain fixes not yet merged upstream
curl -s "https://api.github.com/repos/<owner>/<repo>/forks?per_page=5&sort=stargazers" | \
  python3 -c "import sys,json; [print(f['full_name'], f['stargazers_count'], '★') for f in json.load(sys.stdin)]"

# Check open issues sorted by comments (most discussed = most impactful)
curl -s "https://api.github.com/repos/<owner>/<repo>/issues?state=open&per_page=20&sort=comments&direction=desc" | \
  python3 -c "import sys,json; [print(f'#{i[\"number\"]} {i[\"title\"]} ({i[\"comments\"]} comments)') for i in json.load(sys.stdin)]"

# Check closed issues with real-world field reports (issue #22 pattern — large body = field report)
curl -s "https://api.github.com/repos/<owner>/<repo>/issues?state=closed&per_page=20&sort=comments&direction=desc" | \
  python3 -c "import sys,json; [print(f'#{i[\"number\"]} {i[\"title\"][:80]}') for i in json.load(sys.stdin) if len(i.get('body','')) > 2000]"
```

**What to look for:**

| Signal | What It Means |
|--------|---------------|
| Top fork added new feature | Community voted with their stars — consider adding it |
| Most-discussed open issue | The biggest pain point — you'll hit it too |
| Closed field report (#22 style) | Real user ran 3,000+ jobs — their improvements are proven |
| Multiple forks fixing same thing | The original has a design flaw — fix it early |
| 80% of apply errors = X | The #1 failure mode — plan a mitigation or accept the constraint |

**Audit findings go in the plan doc** (`docs/PLAN_<TOPIC>.md`) before execution. This surfaces community fixes before you spend time reinventing them.

### Pass 2: Configure Data Files First

This is the most important principle: **configure data files before touching code.** Understanding the data model (YAML, JSON, env) reveals how the code works without modifying it.

**Research first, copy second.** Before copying config values from the spec (URLs, site names, employer entries), verify they are current:
- Search for "top [region] job boards 2025 2026" to validate each proposed board
- Spot-check URLs by fetching them or verifying they resolve to real job sites
- Cross-reference against the original repo's template format — does your new entry match the existing pattern exactly?
- Prune boards that no longer exist and add ones the spec missed

| What | Where | Why |
|------|-------|-----|
| Profile/identity | `profiles/<user>.json` or similar | Truth anchor for the entire system |
| Search/config queries | `<pkg>/config/<queries>.yaml` | Defines what the tool searches/processes |
| Site/endpoint lists | `<pkg>/config/<sites>.yaml` | Defines external targets |
| Employer/organization maps | `<pkg>/config/<employers>.yaml` | Defines structured targets |
| Env vars | `~/.<pkg>/.env` | API keys, tokens, IDs |

**Common pitfalls:**
- Profile fields like `password`, `email`, `phone` may contain placeholders — flag these to the user, don't block on them
- Some fields (salary_expectation, work_authorization) affect scoring/filtering — use the actual values from the user's existing profile files
- Resume text (.txt or .md) must be a real import — training generators use it as the truth anchor

### Pass 3: Code Changes (minimal, targeted)

After data is configured, make only the code changes the spec explicitly requires:

| Change Type | Typical Scope | Example |
|-------------|--------------|---------|
| Path/config | 1 line | `APP_DIR = ~/.newdir` |
| New module | ~100-200 lines | Notification hook, reporting |
| CLI flag | ~5 lines | `--notify`, `--profile` |
| Pipeline hook | ~10 lines | Post-completion callout |
| Config reader | ~5 lines | Load profile from new path |

**Files you DON'T touch (typically 95%+ of codebase):**
- Core pipeline/execution loop
- Database layer
- API clients (with one exception: URL endpoints)
- Domain logic (scoring, enrichment, discovery)

**Exception to the rule:** If the fork requires connecting to a different API or service, the URL/base-path change goes in config, not code.

### Pass 4: Environment + Scheduling

```bash
# Create .env
cat > ~/.<pkg>/.env << 'EOF'
API_KEY=<placeholder>
BOT_TOKEN=<placeholder>
EOF

# Cron (discovery/crawl runs offset from scoring/publishing)
# Example: discover every 6h, score+notify 1h offset
0 */6 * * * cd ~/<pkg> && <pkg> run discover >> logs/cron.log 2>&1
0 1,7,13,19 * * * cd ~/<pkg> && <pkg> run score notify >> logs/cron.log 2>&1
```

## Pitfalls

1. **Don't auto-apply on constrained hardware.** A VPS with 8GB/no-swap can run HTTP scraping + LLM scoring but will OOM on Chrome workers (500MB-1GB each). Push browser-heavy stages to the MacBook or accept the constraint.
2. **Private fork needs `gh auth` working.** If the user wants private, don't use the GitHub web UI fork — use `gh repo fork --private`.
3. **There is no god-mode "init" command.** Many tools have `init` commands that create config files interactively. Read the source to understand if config files go in the repo or in `~/.<pkg>/`. Don't assume either.
4. **Profile.json is the truth anchor.** Scoring, tailoring, and application all draw from it. `resume_facts.preserved_companies`, `.preserved_projects`, and `.real_metrics` are fed to a fabrication validator — the system explicitly forbids the LLM from inventing facts not in these lists. Fill the profile completely.
5. **Gemini free tier limits are real.** 15 RPM, 1M tokens/day. For 200+ job scorings, expect ~15-20 minutes with built-in retry/backoff. Flag this as expected behavior, not a bug.
6. **Bot tokens fail silently.** If no BOT_TOKEN is set, the notify flag exits without error. Mention this in the plan so the user knows notifications won't work until the token is set.
7. **Safe rename order.** Rename `src/<old>/` → `src/<new>/` and run sed replacements BEFORE `pip install -e .`. Installing first bakes the old import paths into the installed package.
8. **Template fidelity.** When adding entries to a forked project's config files (sites.yaml, employers.yaml, any YAML/JSON config), match the original's exact format, not a general YAML style. Check: comment markers (`# ── Section ──` vs plain `#`), placeholder variable names (`{query_encoded}` vs `{query}` or `{q}`), field keys (`type: search` vs `type: jobboard`), indentation style, and entry ordering. Deviating from the template introduces bugs in downstream parsers that key on exact field names.
9. **CLI flag import trap.** When adding a new `--flag` to a Typer/Click command, check whether `import os` is already at the top of the file. Setting `os.environ["VAR"] = "1"` from the flag handler needs `os` imported. This is easy to miss because Typer option blocks don't use `os` directly.
10. **Telegram notification pattern (env var → CLI flag → pipeline hook).** Common pattern for forked tools that need status delivery:
    - `notify.py`: module with `_send_telegram()` function reading `BOT_TOKEN`, `CHAT_ID`, `MESSAGE_THREAD_ID` from env
    - Pipeline hook: after completion, check `if os.environ.get("JOBOP_NOTIFY", "") in ("1", "true", "yes"):` → import and call notifier
    - CLI flag: `notify: bool = typer.Option(False, "--notify")` → sets env var before calling pipeline
    - Group topic support: pass `message_thread_id` parameter to Telegram Bot API's `sendMessage` for Forum/Topics groups
    - Silent fallback: if no BOT_TOKEN is set, notification functions return False without error

## Verification Sequence

```bash
# Pass 1 verify
python3 -c "from <new-pkg> import cli; print('Import OK')"

# Pass 2 verify
<pkg> doctor  # if exists — shows config readiness

# Pass 3 verify
<pkg> run <stage> --dry-run  # if exists — dry-run without side effects

# Pass 4 verify
crontab -l  # shows expected entries
```
