---
name: google-workspace
description: Unified Google Workspace CLI — zero dependencies, direct REST API calls. 49 tools across Calendar, Gmail, Drive, Docs, Sheets, Contacts, Tasks. Auto-auth with browser OAuth. Use for ANY Google Workspace operation. Replaces gccli/gdcli/gmcli.
version: 1.0.0
---

# Google Workspace

One Python file. Zero dependencies. All Google Workspace APIs.

Adapted from [tolmachevmaxim/google-workspace-cli](https://github.com/tolmachevmaxim/google-workspace-cli) — a 905-line zero-dependency CLI that speaks directly to Google REST APIs via `urllib.request`. No `google-api-python-client`, no npm, no venv. Just Python 3.

## Quick Start

```bash
# 1. Check auth
python3 ~/.pi/agent/skills/google-workspace/scripts/gws.py auth check

# 2. If not authenticated, run auth (opens browser, catches callback on localhost:8000)
python3 ~/.pi/agent/skills/google-workspace/scripts/gws.py auth

# 3. Test — list next 10 calendar events
python3 ~/.pi/agent/skills/google-workspace/scripts/gws.py cal_events '{"time_min":"2026-05-17T00:00:00Z","max_results":10}'
```

## Auth

| Command | Purpose |
|---------|---------|
| `auth` | Run OAuth flow (opens browser, auto-catches callback) |
| `auth check` | Verify token validity (JSON output) |
| `auth revoke` | Revoke token with Google and delete local file |

**Credential file:** `~/.pi/agent/skills/google-workspace/client_secret.json` (your Desktop app OAuth JSON from Google Cloud Console)

**Token file:** `~/.pi/agent/skills/google-workspace/token.json` (auto-created on first auth)

## Calling Pattern

Every tool takes a single JSON argument:

```bash
python3 ~/.pi/agent/skills/google-workspace/scripts/gws.py <tool> '<json>'
```

Or pipe JSON via stdin:

```bash
python3 ~/.pi/agent/skills/google-workspace/scripts/gws.py <tool> - <<'ARGS'
{"key":"value"}
ARGS
```

## Calendar (8 tools)

```bash
gws.py cal_list '{}'
gws.py cal_events '{"calendar_id":"primary","time_min":"2026-05-01T00:00:00Z","time_max":"2026-05-31T23:59:59Z","max_results":50}'
gws.py cal_create '{"calendar_id":"primary","summary":"Standup","start":"2026-05-20T10:00:00Z","end":"2026-05-20T10:30:00Z","timezone":"UTC"}'
gws.py cal_update '{"calendar_id":"primary","event_id":"XXX","summary":"Updated"}'
gws.py cal_delete '{"calendar_id":"primary","event_id":"XXX"}'
gws.py cal_get '{"calendar_id":"primary","event_id":"XXX"}'
gws.py cal_quick_add '{"calendar_id":"primary","text":"Lunch with Sarah at 12pm tomorrow"}'
gws.py cal_freebusy '{"time_min":"2026-05-20T00:00:00Z","time_max":"2026-05-20T23:59:59Z","calendar_ids":["primary"]}'
```

## Gmail (9 tools)

```bash
gws.py gmail_search '{"query":"is:unread from:boss@company.com","max_results":10}'
gws.py gmail_get '{"message_id":"XXX"}'
gws.py gmail_send '{"to":"user@example.com","subject":"Hello","body":"Message","html":false}'
gws.py gmail_draft '{"to":"user@example.com","subject":"Draft","body":"Text"}'
gws.py gmail_labels '{}'
gws.py gmail_reply '{"message_id":"XXX","body":"Reply text"}'
gws.py gmail_modify '{"message_id":"XXX","add_labels":["Label_1"],"remove_labels":["UNREAD"]}'
gws.py gmail_delete '{"message_id":"XXX"}'
gws.py gmail_thread '{"thread_id":"XXX"}'
```

## Drive (9 tools)

```bash
gws.py drive_list '{"folder_id":"root","max_results":20}'
gws.py drive_search '{"query":"name contains \"report\"","max_results":10}'
gws.py drive_get '{"file_id":"XXX"}'
gws.py drive_create_folder '{"name":"New Folder","parent_id":"root"}'
gws.py drive_copy '{"file_id":"XXX","name":"Copy of file"}'
gws.py drive_delete '{"file_id":"XXX"}'
gws.py drive_move '{"file_id":"XXX","folder_id":"NEW_PARENT"}'
gws.py drive_share '{"file_id":"XXX","email":"user@example.com","role":"writer"}'
gws.py drive_get_meta '{"file_id":"XXX"}'
```

## Sheets (9 tools)

```bash
gws.py sheets_read '{"spreadsheet_id":"XXX","range":"Sheet1!A1:D10"}'
gws.py sheets_write '{"spreadsheet_id":"XXX","range":"Sheet1!A1","values":[["Name","Score"],["Alice","95"]]}'
gws.py sheets_append '{"spreadsheet_id":"XXX","range":"Sheet1!A:C","values":[["new","row","data"]]}'
gws.py sheets_info '{"spreadsheet_id":"XXX"}'
gws.py sheets_list '{"spreadsheet_id":"XXX"}'
gws.py sheets_create '{"title":"Budget"}'
gws.py sheets_add_sheet '{"spreadsheet_id":"XXX","title":"Q2"}'
gws.py sheets_delete_sheet '{"spreadsheet_id":"XXX","sheet_id":123}'
gws.py sheets_clear '{"spreadsheet_id":"XXX","range":"Sheet1!A1:D10"}'
gws.py sheets_batch_read '{"spreadsheet_id":"XXX","ranges":["Sheet1!A1:C3","Sheet2!A1:C3"]}'
gws.py sheets_format '{"spreadsheet_id":"XXX","requests":[{"repeatCell":{"range":{"sheetId":0,"startRowIndex":0,"endRowIndex":1},"cell":{"userEnteredFormat":{"textFormat":{"bold":true}}},"fields":"userEnteredFormat.textFormat.bold"}}]}'
```

## Docs (3 tools)

```bash
gws.py docs_get '{"document_id":"XXX"}'
gws.py docs_create '{"title":"Meeting Notes","body":"First paragraph..."}'
gws.py docs_append '{"document_id":"XXX","text":"Additional content"}'
```

## Contacts (3 tools)

```bash
gws.py contacts_list '{"max_results":50}'
gws.py contacts_search '{"query":"john"}'
gws.py contacts_create '{"names":[{"givenName":"John","familyName":"Doe"}],"emailAddresses":[{"value":"john@example.com"}]}'
```

## Tasks (6 tools)

```bash
gws.py tasks_lists '{}'
gws.py tasks_list '{"tasklist_id":"@default"}'
gws.py tasks_get '{"tasklist_id":"@default","task_id":"XXX"}'
gws.py tasks_create '{"tasklist_id":"@default","title":"Buy milk"}'
gws.py tasks_complete '{"tasklist_id":"@default","task_id":"XXX"}'
gws.py tasks_delete '{"tasklist_id":"@default","task_id":"XXX"}'
```

## Output Format

Every tool outputs JSON (or raw text for non-JSON responses). Pipe through `jq` or parse directly.

## When to Use

- Any Google Calendar, Gmail, Drive, Docs, Sheets, Contacts, or Tasks operation
- When gccli/gdcli/gmcli auth has expired or scopes are insufficient
- When you need a single tool covering all Workspace services
- When you want zero-dependency operation (no npm, no pip)

## Pitfalls

- **OAuth opens browser + localhost:8000 callback.** If you're in a headless environment, port-forward or use a machine with a browser. The script auto-opens `webbrowser.open()` and spins up `HTTPServer` on `localhost:8000` for 5 minutes.
- **Port 8000 must be free.** If something else is using it, kill it first or the auth will hang.
- **First auth needs all scopes.** Google shows a consent screen with 28 scopes. You only need to approve once.
- **Token auto-refreshes.** The token is refreshed automatically on each call if it's within 5 minutes of expiry.

## Verification

- `auth check` returns `{"authenticated": true}`
- `cal_events '{"max_results":1}'` returns events without errors
- `drive_list '{}'` returns files without errors
- `gmail_search '{"query":"is:unread","max_results":1}'` returns messages without errors

## Migration from gccli/gdcli/gmcli

This skill replaces the separate Node.js CLIs. Your existing tokens in `~/.gccli/`, `~/.gdcli/`, `~/.gmcli/` are left untouched — the old tools continue to work. The new tool uses its own token at `~/.pi/agent/skills/google-workspace/token.json`.

## Files

| File | Purpose |
|------|---------|
| `scripts/gws.py` | Main CLI (adapted from tolmachevmaxim/google-workspace-cli) |
| `client_secret.json` | OAuth Desktop app credentials (download from Google Cloud Console → APIs & Services → Credentials → Desktop app) |
| `token.json` | Auto-generated OAuth token with refresh |
