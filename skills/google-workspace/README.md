# Google Workspace Setup

Zero-dependency Python CLI for Google Calendar, Gmail, Drive, Docs, Sheets, Contacts, and Tasks.

## Prerequisites

- Python 3 (system or Homebrew)
- A Google Cloud project with the Google Workspace APIs enabled

## 1. Get OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create or select a project
3. Navigate to **APIs & Services > OAuth consent screen**
4. Choose **External** app type, fill in app name + user support email + developer contact email
5. Navigate to **APIs & Services > Credentials**
6. Click **Create Credentials > OAuth client ID**
7. Select **Desktop app** as Application type
8. Name it (e.g., "gws-cli")
9. Click **Create**, then **Download JSON**
10. Rename the downloaded file to `client_secret.json` and place it at:
    ```
    ~/.pi/agent/skills/google-workspace/client_secret.json
    ```

## 2. Enable APIs

In Google Cloud Console, go to **APIs & Services > Enabled APIs & services** and enable:

- Google Calendar API
- Gmail API
- Google Drive API
- Google Docs API
- Google Sheets API
- Google People API (for Contacts)
- Google Tasks API

## 3. Authenticate

```bash
python3 ~/.pi/agent/skills/google-workspace/scripts/gws.py auth
```

This opens your browser, shows Google's consent screen with all scopes, and auto-catches the callback on `localhost:8000`. A `token.json` is created automatically.

## 4. Test

```bash
# Check auth
python3 ~/.pi/agent/skills/google-workspace/scripts/gws.py auth check

# List next 10 calendar events
python3 ~/.pi/agent/skills/google-workspace/scripts/gws.py cal_events '{"time_min":"2026-05-18T00:00:00Z","max_results":10}'

# List Drive files
python3 ~/.pi/agent/skills/google-workspace/scripts/gws.py drive_list '{"max_results":10}'

# Search unread Gmail
python3 ~/.pi/agent/skills/google-workspace/scripts/gws.py gmail_search '{"query":"is:unread","max_results":5}'
```

## Security

- `client_secret.json` — your OAuth Desktop app credentials. **Never commit this.**
- `token.json` — your access and refresh tokens. **Never commit this.**

Both files are `.gitignore`d in this repo. If you clone this repo, you must provide your own `client_secret.json`.

## Credential Files Location

| File | Source | Created by |
|------|--------|------------|
| `scripts/gws.py` | This repo | — |
| `SKILL.md` | This repo | — |
| `client_secret.json` | Google Cloud Console download | You |
| `token.json` | Google OAuth response | `gws.py auth` |
