#!/usr/bin/env python3
"""gws — Unified Google Workspace CLI for Pi.
Direct REST API calls. Zero external dependencies.

Usage:
    gws.py <tool> '{"email":"you@gmail.com", ...}'
    gws.py auth [email]
    gws.py --help

Auth:
  OAuth client credentials in ~/.pi/agent/skills/google-workspace/client_secret.json
  Tokens saved to ~/.pi/agent/skills/google-workspace/token.json
  Auto-refresh. Re-auth: gws.py auth [email]
"""
import base64
import hashlib
import json
import os
import platform
import secrets
import sys
import webbrowser
from datetime import datetime, timezone, timedelta
from email.mime.text import MIMEText
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlencode, urlparse, parse_qs, quote
import urllib.error
import urllib.request

# ━━ Config ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
CLIENT_SECRET_PATH = os.path.join(SKILL_DIR, "client_secret.json")
TOKEN_PATH = os.path.join(SKILL_DIR, "token.json")
REDIRECT_URI = "http://localhost:8000/oauth2callback"
TOKEN_URL = "https://oauth2.googleapis.com/token"
REFRESH_BUFFER = 300  # refresh 5 min before expiry

DEFAULT_EMAIL = ""  # user must provide via --email or JSON arg
DEFAULT_TIMEZONE = "UTC"

SCOPES = " ".join([
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/calendar",
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.labels",
    "https://www.googleapis.com/auth/gmail.settings.basic",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/documents.readonly",
    "https://www.googleapis.com/auth/presentations",
    "https://www.googleapis.com/auth/presentations.readonly",
    "https://www.googleapis.com/auth/contacts",
    "https://www.googleapis.com/auth/contacts.readonly",
    "https://www.googleapis.com/auth/tasks",
    "https://www.googleapis.com/auth/tasks.readonly",
    "https://www.googleapis.com/auth/forms.body",
    "https://www.googleapis.com/auth/forms.body.readonly",
    "https://www.googleapis.com/auth/forms.responses.readonly",
])


# ━━ Errors ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class ApiError(Exception):
    def __init__(self, code, body):
        self.code = code
        self.body = body
        super().__init__(f"HTTP {code}: {body[:500]}")


# ━━ Auth ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def get_default_email():
    return DEFAULT_EMAIL


def get_default_tz():
    return DEFAULT_TIMEZONE


def get_client_creds():
    """Read client_id and client_secret from the Desktop app JSON."""
    if not os.path.exists(CLIENT_SECRET_PATH):
        fail(f"Missing client secret. Expected at: {CLIENT_SECRET_PATH}\n"
             f"Download from Google Cloud Console (OAuth 2.0 Desktop app) and save there.")
    with open(CLIENT_SECRET_PATH) as f:
        data = json.load(f)
    # Support both raw client_secret format and full OAuth JSON
    if "installed" in data:
        data = data["installed"]
    elif "web" in data:
        data = data["web"]
    cid = data.get("client_id", "")
    cs = data.get("client_secret", "")
    if not cid or not cs:
        fail(f"Could not extract client_id/client_secret from {CLIENT_SECRET_PATH}")
    return cid, cs


def load_token():
    if not os.path.exists(TOKEN_PATH):
        return None
    with open(TOKEN_PATH) as f:
        return json.load(f)


def save_token(creds):
    os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
    with open(TOKEN_PATH, "w") as f:
        json.dump(creds, f, indent=2)
    try:
        os.chmod(TOKEN_PATH, 0o600)
    except OSError:
        pass


def is_expired(creds):
    expiry = creds.get("expiry", "")
    if not expiry:
        return True
    try:
        exp_dt = datetime.fromisoformat(expiry)
        if exp_dt.tzinfo is None:
            exp_dt = exp_dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return True
    return datetime.now(timezone.utc) >= exp_dt - timedelta(seconds=REFRESH_BUFFER)


def do_refresh(creds):
    """Refresh access token using refresh_token. Returns updated creds or None."""
    rt = creds.get("refresh_token")
    if not rt:
        return None
    cid, cs = get_client_creds()
    data = urlencode({
        "grant_type": "refresh_token",
        "refresh_token": rt,
        "client_id": cid,
        "client_secret": cs,
    }).encode()
    req = urllib.request.Request(TOKEN_URL, data=data,
                                headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        resp = urllib.request.urlopen(req)
        tokens = json.loads(resp.read())
        creds["token"] = tokens["access_token"]
        creds["expiry"] = (datetime.now(timezone.utc) +
                           timedelta(seconds=tokens.get("expires_in", 3600))).isoformat()
        if "refresh_token" in tokens:
            creds["refresh_token"] = tokens["refresh_token"]
        save_token(creds)
        return creds
    except urllib.error.HTTPError:
        return None


def oauth_flow():
    """Full OAuth: open browser, catch callback, exchange code, save token."""
    cid, cs = get_client_creds()
    verifier = secrets.token_urlsafe(64)[:128]
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode()).digest()
    ).rstrip(b"=").decode()

    auth_url = "https://accounts.google.com/o/oauth2/auth?" + urlencode({
        "response_type": "code",
        "client_id": cid,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES,
        "state": secrets.token_hex(16),
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "access_type": "offline",
        "prompt": "consent",
    })

    print(f"Opening browser for Google auth...", file=sys.stderr)
    webbrowser.open(auth_url)
    print("Waiting for callback on localhost:8000...", file=sys.stderr)

    code = [None]

    class H(BaseHTTPRequestHandler):
        def do_GET(self):
            p = parse_qs(urlparse(self.path).query)
            if "code" in p:
                code[0] = p["code"][0]
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(b"<h1>Done! Close this tab.</h1>")
            else:
                self.send_response(400)
                self.end_headers()
        def log_message(self, *a):
            pass

    srv = HTTPServer(("localhost", 8000), H)
    srv.timeout = 300
    while code[0] is None:
        srv.handle_request()
    srv.server_close()

    if not code[0]:
        fail("No authorization code received")

    data = urlencode({
        "code": code[0],
        "client_id": cid,
        "client_secret": cs,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code",
        "code_verifier": verifier,
    }).encode()
    req = urllib.request.Request(TOKEN_URL, data=data,
                                headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        resp = urllib.request.urlopen(req)
        tokens = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        fail(f"Token exchange failed: {e.code} {e.read().decode()}")

    creds = {
        "token": tokens["access_token"],
        "refresh_token": tokens.get("refresh_token", ""),
        "token_uri": TOKEN_URL,
        "client_id": cid,
        "client_secret": cs,
        "scopes": SCOPES.split(),
        "expiry": (datetime.now(timezone.utc) +
                   timedelta(seconds=tokens.get("expires_in", 3600))).isoformat(),
    }
    save_token(creds)
    print(f"Authorized ({len(creds['scopes'])} scopes)", file=sys.stderr)
    return creds


def ensure_token():
    """Get valid access token. Auto-refreshes or re-auths as needed."""
    creds = load_token()
    if creds and not is_expired(creds):
        return creds["token"]
    if creds:
        refreshed = do_refresh(creds)
        if refreshed:
            return refreshed["token"]
    creds = oauth_flow()
    return creds["token"]


# ━━ HTTP ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def api(method, url, token, data=None):
    headers = {"Authorization": f"Bearer {token}"}
    body = None
    if data is not None:
        body = json.dumps(data).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        resp = urllib.request.urlopen(req)
        raw = resp.read()
        if not raw:
            return {}
        ct = resp.headers.get("Content-Type", "")
        if "json" in ct:
            return json.loads(raw)
        return raw.decode(errors="replace")
    except urllib.error.HTTPError as e:
        raise ApiError(e.code, e.read().decode(errors="replace"))


def fail(msg):
    print(json.dumps({"error": msg}), file=sys.stdout)
    sys.exit(1)


# ━━ Calendar ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CAL = "https://www.googleapis.com/calendar/v3"


def cal_list(token, a):
    return api("GET", f"{CAL}/users/me/calendarList", token)


def cal_events(token, a):
    cid = a.get("calendar_id", "primary")
    p = {"singleEvents": "true", "orderBy": "startTime",
         "maxResults": a.get("max_results", 50)}
    if "time_min" in a:
        p["timeMin"] = a["time_min"]
    if "time_max" in a:
        p["timeMax"] = a["time_max"]
    if "q" in a:
        p["q"] = a["q"]
    return api("GET", f"{CAL}/calendars/{quote(cid, safe='')}/events?{urlencode(p)}", token)


def cal_create(token, a):
    cid = a.get("calendar_id", "primary")
    tz = a.get("timezone", get_default_tz())
    event = {
        "summary": a["summary"],
        "start": {"dateTime": a["start_time"], "timeZone": tz},
        "end": {"dateTime": a["end_time"], "timeZone": tz},
    }
    for k in ("description", "location"):
        if k in a:
            event[k] = a[k]
    if "attendees" in a:
        event["attendees"] = [{"email": e} if isinstance(e, str) else e for e in a["attendees"]]
    return api("POST", f"{CAL}/calendars/{quote(cid, safe='')}/events", token, event)


def cal_update(token, a):
    cid = a.get("calendar_id", "primary")
    eid = a["event_id"]
    tz = a.get("timezone", get_default_tz())
    patch = {}
    for k in ("summary", "description", "location"):
        if k in a:
            patch[k] = a[k]
    if "start_time" in a:
        patch["start"] = {"dateTime": a["start_time"], "timeZone": tz}
    if "end_time" in a:
        patch["end"] = {"dateTime": a["end_time"], "timeZone": tz}
    return api("PATCH", f"{CAL}/calendars/{quote(cid, safe='')}/events/{eid}", token, patch)


def cal_delete(token, a):
    cid = a.get("calendar_id", "primary")
    eid = a["event_id"]
    api("DELETE", f"{CAL}/calendars/{quote(cid, safe='')}/events/{eid}", token)
    return {"deleted": eid}


def cal_get(token, a):
    """Get single event by ID."""
    cid = a.get("calendar_id", "primary")
    eid = a["event_id"]
    return api("GET", f"{CAL}/calendars/{quote(cid, safe='')}/events/{eid}", token)


def cal_quick_add(token, a):
    """Create event from natural language text."""
    cid = a.get("calendar_id", "primary")
    return api("POST", f"{CAL}/calendars/{quote(cid, safe='')}/events/quickAdd?text={quote(a['text'], safe='')}", token)


def cal_freebusy(token, a):
    """Check free/busy status for calendars in a time range."""
    body = {
        "timeMin": a["time_min"],
        "timeMax": a["time_max"],
        "items": [{"id": cid} for cid in a.get("calendar_ids", ["primary"])],
    }
    return api("POST", f"{CAL}/freeBusy", token, body)


# ━━ Sheets ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SH = "https://sheets.googleapis.com/v4/spreadsheets"


def sheets_read(token, a):
    sid = a["spreadsheet_id"]
    rng = a["range"]
    return api("GET", f"{SH}/{sid}/values/{quote(rng, safe='')}", token)


def sheets_write(token, a):
    sid = a["spreadsheet_id"]
    rng = a["range"]
    opt = a.get("input_option", "USER_ENTERED")
    body = {"range": rng, "majorDimension": "ROWS", "values": a["values"]}
    return api("PUT", f"{SH}/{sid}/values/{quote(rng, safe='')}?valueInputOption={opt}", token, body)


def sheets_append(token, a):
    sid = a["spreadsheet_id"]
    rng = a["range"]
    opt = a.get("input_option", "USER_ENTERED")
    body = {"range": rng, "majorDimension": "ROWS", "values": a["values"]}
    return api("POST", f"{SH}/{sid}/values/{quote(rng, safe='')}:append?valueInputOption={opt}&insertDataOption=INSERT_ROWS", token, body)


def sheets_info(token, a):
    sid = a["spreadsheet_id"]
    return api("GET", f"{SH}/{sid}?fields=properties,sheets.properties", token)


def sheets_list(token, a):
    q = quote("mimeType='application/vnd.google-apps.spreadsheet'", safe="")
    n = a.get("max_results", 20)
    return api("GET", f"https://www.googleapis.com/drive/v3/files?q={q}&pageSize={n}&fields=files(id,name,modifiedTime)", token)


def sheets_create(token, a):
    """Create new spreadsheet."""
    body = {"properties": {"title": a["title"]}}
    if "sheets" in a:
        body["sheets"] = [{"properties": {"title": s}} for s in a["sheets"]]
    return api("POST", SH, token, body)


def sheets_add_sheet(token, a):
    """Add a new sheet/tab to existing spreadsheet."""
    sid = a["spreadsheet_id"]
    body = {"requests": [{"addSheet": {"properties": {"title": a["title"]}}}]}
    return api("POST", f"{SH}/{sid}:batchUpdate", token, body)


def sheets_delete_sheet(token, a):
    """Delete a sheet/tab by sheet ID (not name)."""
    sid = a["spreadsheet_id"]
    body = {"requests": [{"deleteSheet": {"sheetId": a["sheet_id"]}}]}
    return api("POST", f"{SH}/{sid}:batchUpdate", token, body)


def sheets_clear(token, a):
    """Clear values in a range."""
    sid = a["spreadsheet_id"]
    rng = a["range"]
    return api("POST", f"{SH}/{sid}/values/{quote(rng, safe='')}:clear", token, {})


def sheets_batch_read(token, a):
    """Read multiple ranges at once."""
    sid = a["spreadsheet_id"]
    ranges = "&".join(f"ranges={quote(r, safe='')}" for r in a["ranges"])
    return api("GET", f"{SH}/{sid}/values:batchGet?{ranges}", token)


def sheets_format(token, a):
    """Format cells (bold, colors, etc.) via batchUpdate requests."""
    sid = a["spreadsheet_id"]
    body = {"requests": a["requests"]}
    return api("POST", f"{SH}/{sid}:batchUpdate", token, body)


# ━━ Drive ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DR = "https://www.googleapis.com/drive/v3"

EXPORT_MAP = {
    "application/vnd.google-apps.document": "text/plain",
    "application/vnd.google-apps.spreadsheet": "text/csv",
    "application/vnd.google-apps.presentation": "text/plain",
}


def drive_list(token, a):
    p = {"pageSize": a.get("max_results", 20),
         "fields": "files(id,name,mimeType,modifiedTime,size)",
         "orderBy": "modifiedTime desc"}
    if "query" in a:
        p["q"] = a["query"]
    return api("GET", f"{DR}/files?{urlencode(p)}", token)


def drive_search(token, a):
    p = {"q": a["query"],
         "pageSize": a.get("max_results", 20),
         "fields": "files(id,name,mimeType,modifiedTime,size)"}
    return api("GET", f"{DR}/files?{urlencode(p)}", token)


def drive_get(token, a):
    fid = a["file_id"]
    meta = api("GET", f"{DR}/files/{fid}?fields=id,name,mimeType,size", token)
    mime = meta.get("mimeType", "")
    export_as = a.get("export_as") or EXPORT_MAP.get(mime)
    if export_as:
        content = api("GET", f"{DR}/files/{fid}/export?mimeType={quote(export_as, safe='')}", token)
    else:
        content = api("GET", f"{DR}/files/{fid}?alt=media", token)
    return {"metadata": meta, "content": content if isinstance(content, str) else "(binary data)"}


def drive_create_folder(token, a):
    """Create a folder in Drive."""
    body = {"name": a["name"], "mimeType": "application/vnd.google-apps.folder"}
    if "parent_id" in a:
        body["parents"] = [a["parent_id"]]
    return api("POST", f"{DR}/files", token, body)


def drive_copy(token, a):
    """Copy a file."""
    body = {}
    if "name" in a:
        body["name"] = a["name"]
    if "parent_id" in a:
        body["parents"] = [a["parent_id"]]
    return api("POST", f"{DR}/files/{a['file_id']}/copy", token, body)


def drive_delete(token, a):
    """Move file to trash."""
    api("PATCH", f"{DR}/files/{a['file_id']}", token, {"trashed": True})
    return {"trashed": a["file_id"]}


def drive_move(token, a):
    """Move file to another folder."""
    fid = a["file_id"]
    meta = api("GET", f"{DR}/files/{fid}?fields=parents", token)
    old_parents = ",".join(meta.get("parents", []))
    return api("PATCH", f"{DR}/files/{fid}?addParents={a['parent_id']}&removeParents={old_parents}", token, {})


def drive_share(token, a):
    """Share file with someone."""
    fid = a["file_id"]
    perm = {"type": a.get("type", "user"), "role": a.get("role", "reader")}
    if "email" in a:
        perm["emailAddress"] = a["email"]
    p = {}
    if perm["type"] in ("user", "group"):
        p["sendNotificationEmail"] = str(a.get("notify", True)).lower()
    return api("POST", f"{DR}/files/{fid}/permissions?{urlencode(p)}", token, perm)


def drive_get_meta(token, a):
    """Get file metadata without downloading content."""
    fid = a["file_id"]
    fields = a.get("fields", "id,name,mimeType,size,modifiedTime,parents,webViewLink,permissions")
    return api("GET", f"{DR}/files/{fid}?fields={quote(fields, safe='')}", token)


# ━━ Gmail ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GM = "https://www.googleapis.com/gmail/v1/users/me"


def _gmail_body(payload):
    """Extract text body from nested Gmail payload."""
    if payload.get("body", {}).get("data"):
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode(errors="replace")
    for part in payload.get("parts", []):
        if part.get("mimeType") == "text/plain" and part.get("body", {}).get("data"):
            return base64.urlsafe_b64decode(part["body"]["data"]).decode(errors="replace")
    for part in payload.get("parts", []):
        r = _gmail_body(part)
        if r:
            return r
    return ""


def gmail_search(token, a):
    p = {"q": a["query"], "maxResults": a.get("max_results", 10)}
    result = api("GET", f"{GM}/messages?{urlencode(p)}", token)
    msgs = result.get("messages", [])
    out = []
    for m in msgs:
        d = api("GET", f"{GM}/messages/{m['id']}?format=metadata"
                "&metadataHeaders=From&metadataHeaders=To"
                "&metadataHeaders=Subject&metadataHeaders=Date", token)
        hdrs = {h["name"]: h["value"] for h in d.get("payload", {}).get("headers", [])}
        out.append({
            "id": m["id"], "threadId": m.get("threadId"),
            "from": hdrs.get("From", ""), "to": hdrs.get("To", ""),
            "subject": hdrs.get("Subject", ""), "date": hdrs.get("Date", ""),
            "snippet": d.get("snippet", ""),
        })
    return {"messages": out, "total": result.get("resultSizeEstimate", 0)}


def gmail_get(token, a):
    mid = a["message_id"]
    msg = api("GET", f"{GM}/messages/{mid}?format=full", token)
    hdrs = {h["name"]: h["value"] for h in msg.get("payload", {}).get("headers", [])}
    return {
        "id": msg["id"], "threadId": msg.get("threadId"),
        "from": hdrs.get("From", ""), "to": hdrs.get("To", ""),
        "subject": hdrs.get("Subject", ""), "date": hdrs.get("Date", ""),
        "body": _gmail_body(msg.get("payload", {})),
        "labels": msg.get("labelIds", []),
    }


def gmail_send(token, a):
    msg = MIMEText(a["body"])
    msg["To"] = a["to"]
    msg["Subject"] = a["subject"]
    if "from" in a:
        msg["From"] = a["from"]
    if "cc" in a:
        msg["Cc"] = a["cc"]
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    return api("POST", f"{GM}/messages/send", token, {"raw": raw})


def gmail_draft(token, a):
    msg = MIMEText(a["body"])
    msg["To"] = a["to"]
    msg["Subject"] = a["subject"]
    if "from" in a:
        msg["From"] = a["from"]
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    return api("POST", f"{GM}/drafts", token, {"message": {"raw": raw}})


def gmail_labels(token, a):
    """List all Gmail labels."""
    return api("GET", f"{GM}/labels", token)


def gmail_reply(token, a):
    """Reply to a message (adds In-Reply-To and References headers)."""
    orig = api("GET", f"{GM}/messages/{a['message_id']}?format=metadata"
               "&metadataHeaders=Message-ID&metadataHeaders=Subject"
               "&metadataHeaders=From&metadataHeaders=To", token)
    hdrs = {h["name"]: h["value"] for h in orig.get("payload", {}).get("headers", [])}
    msg_id_hdr = hdrs.get("Message-ID", "")
    subject = hdrs.get("Subject", "")
    if not subject.lower().startswith("re:"):
        subject = f"Re: {subject}"
    to = a.get("to", hdrs.get("From", ""))
    msg = MIMEText(a["body"])
    msg["To"] = to
    msg["Subject"] = subject
    if msg_id_hdr:
        msg["In-Reply-To"] = msg_id_hdr
        msg["References"] = msg_id_hdr
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    return api("POST", f"{GM}/messages/send", token, {
        "raw": raw, "threadId": orig.get("threadId", "")
    })


def gmail_modify(token, a):
    """Modify message labels (mark read/unread, archive, star, etc.)."""
    mid = a["message_id"]
    body = {}
    if "add_labels" in a:
        body["addLabelIds"] = a["add_labels"]
    if "remove_labels" in a:
        body["removeLabelIds"] = a["remove_labels"]
    return api("POST", f"{GM}/messages/{mid}/modify", token, body)


def gmail_delete(token, a):
    """Trash a message (recoverable)."""
    mid = a["message_id"]
    return api("POST", f"{GM}/messages/{mid}/trash", token)


def gmail_thread(token, a):
    """Get all messages in a thread."""
    tid = a["thread_id"]
    thread = api("GET", f"{GM}/threads/{tid}?format=full", token)
    msgs = []
    for m in thread.get("messages", []):
        hdrs = {h["name"]: h["value"] for h in m.get("payload", {}).get("headers", [])}
        msgs.append({
            "id": m["id"],
            "from": hdrs.get("From", ""), "to": hdrs.get("To", ""),
            "subject": hdrs.get("Subject", ""), "date": hdrs.get("Date", ""),
            "body": _gmail_body(m.get("payload", {})),
            "labels": m.get("labelIds", []),
        })
    return {"threadId": tid, "messages": msgs}


# ━━ Docs ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DOC = "https://docs.googleapis.com/v1/documents"


def docs_get(token, a):
    """Get Google Doc content as structured JSON."""
    did = a["document_id"]
    return api("GET", f"{DOC}/{did}", token)


def docs_create(token, a):
    """Create a new Google Doc."""
    body = {"title": a["title"]}
    return api("POST", DOC, token, body)


def docs_append(token, a):
    """Append text to end of a Google Doc."""
    did = a["document_id"]
    doc = api("GET", f"{DOC}/{did}", token)
    end_idx = doc.get("body", {}).get("content", [{}])[-1].get("endIndex", 1) - 1
    if end_idx < 1:
        end_idx = 1
    body = {"requests": [{"insertText": {"location": {"index": end_idx}, "text": a["text"]}}]}
    return api("POST", f"{DOC}/{did}:batchUpdate", token, body)


# ━━ Contacts (People API) ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PEOPLE = "https://people.googleapis.com/v1"


def contacts_list(token, a):
    """List contacts."""
    n = a.get("max_results", 100)
    fields = a.get("fields", "names,emailAddresses,phoneNumbers")
    return api("GET", f"{PEOPLE}/people/me/connections?pageSize={n}&personFields={quote(fields, safe='')}", token)


def contacts_search(token, a):
    """Search contacts by name, email, or phone."""
    q = a["query"]
    fields = a.get("fields", "names,emailAddresses,phoneNumbers")
    return api("GET", f"{PEOPLE}/people:searchContacts?query={quote(q, safe='')}&readMask={quote(fields, safe='')}&pageSize=30", token)


def contacts_create(token, a):
    """Create a contact."""
    person = {}
    if "name" in a:
        person["names"] = [{"givenName": a["name"]}]
    if "first_name" in a or "last_name" in a:
        person["names"] = [{"givenName": a.get("first_name", ""), "familyName": a.get("last_name", "")}]
    if "email" in a:
        person["emailAddresses"] = [{"value": a["email"]}]
    if "phone" in a:
        person["phoneNumbers"] = [{"value": a["phone"]}]
    return api("POST", f"{PEOPLE}/people:createContact", token, person)


# ━━ Tasks ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TASKS_URL = "https://tasks.googleapis.com/tasks/v1"


def tasks_lists(token, a):
    """List all task lists."""
    return api("GET", f"{TASKS_URL}/users/@me/lists", token)


def tasks_list(token, a):
    """List tasks in a task list."""
    lid = a.get("list_id", "@default")
    p = {"maxResults": a.get("max_results", 100)}
    if "show_completed" in a:
        p["showCompleted"] = str(a["show_completed"]).lower()
    if "show_hidden" in a:
        p["showHidden"] = str(a["show_hidden"]).lower()
    return api("GET", f"{TASKS_URL}/lists/{lid}/tasks?{urlencode(p)}", token)


def tasks_get(token, a):
    """Get a single task."""
    lid = a.get("list_id", "@default")
    return api("GET", f"{TASKS_URL}/lists/{lid}/tasks/{a['task_id']}", token)


def tasks_create(token, a):
    """Create a task."""
    lid = a.get("list_id", "@default")
    body = {"title": a["title"]}
    if "notes" in a:
        body["notes"] = a["notes"]
    if "due" in a:
        body["due"] = a["due"]
    return api("POST", f"{TASKS_URL}/lists/{lid}/tasks", token, body)


def tasks_complete(token, a):
    """Mark a task as completed."""
    lid = a.get("list_id", "@default")
    return api("PATCH", f"{TASKS_URL}/lists/{lid}/tasks/{a['task_id']}", token, {"status": "completed"})


def tasks_delete(token, a):
    """Delete a task."""
    lid = a.get("list_id", "@default")
    api("DELETE", f"{TASKS_URL}/lists/{lid}/tasks/{a['task_id']}", token)
    return {"deleted": a["task_id"]}


# ━━ CLI ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TOOLS = {
    "cal_list": cal_list, "cal_events": cal_events, "cal_create": cal_create,
    "cal_update": cal_update, "cal_delete": cal_delete, "cal_get": cal_get,
    "cal_quick_add": cal_quick_add, "cal_freebusy": cal_freebusy,
    "sheets_read": sheets_read, "sheets_write": sheets_write, "sheets_append": sheets_append,
    "sheets_info": sheets_info, "sheets_list": sheets_list, "sheets_create": sheets_create,
    "sheets_add_sheet": sheets_add_sheet, "sheets_delete_sheet": sheets_delete_sheet,
    "sheets_clear": sheets_clear, "sheets_batch_read": sheets_batch_read, "sheets_format": sheets_format,
    "drive_list": drive_list, "drive_search": drive_search, "drive_get": drive_get,
    "drive_create_folder": drive_create_folder, "drive_copy": drive_copy,
    "drive_delete": drive_delete, "drive_move": drive_move, "drive_share": drive_share,
    "drive_get_meta": drive_get_meta,
    "gmail_search": gmail_search, "gmail_get": gmail_get, "gmail_send": gmail_send,
    "gmail_draft": gmail_draft, "gmail_labels": gmail_labels, "gmail_reply": gmail_reply,
    "gmail_modify": gmail_modify, "gmail_delete": gmail_delete, "gmail_thread": gmail_thread,
    "docs_get": docs_get, "docs_create": docs_create, "docs_append": docs_append,
    "contacts_list": contacts_list, "contacts_search": contacts_search, "contacts_create": contacts_create,
    "tasks_lists": tasks_lists, "tasks_list": tasks_list, "tasks_get": tasks_get,
    "tasks_create": tasks_create, "tasks_complete": tasks_complete, "tasks_delete": tasks_delete,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] == "--help":
        print("Google Workspace CLI\n")
        print("Usage: gws.py <tool> '{json}' | gws.py <tool> - <<'ARGS'")
        print("       gws.py auth")
        print("       gws.py auth check")
        print("       gws.py auth revoke\n")
        print(f"Tools ({len(TOOLS)}):")
        for name, fn in TOOLS.items():
            print(f"  {name:24s} {fn.__doc__ or ''}")
        return

    tool = sys.argv[1]

    if tool == "auth":
        if len(sys.argv) >= 3 and sys.argv[2] == "check":
            creds = load_token()
            if not creds:
                fail("Not authenticated. Run: gws.py auth")
            if is_expired(creds):
                refreshed = do_refresh(creds)
                if refreshed:
                    print(json.dumps({"authenticated": True, "refreshed": True}))
                    return
                fail("Token expired. Run: gws.py auth")
            print(json.dumps({"authenticated": True}))
            return
        if len(sys.argv) >= 3 and sys.argv[2] == "revoke":
            creds = load_token()
            if not creds:
                print(json.dumps({"status": "no_token"}))
                return
            token = creds.get("token", "")
            if token:
                try:
                    req = urllib.request.Request(
                        f"https://oauth2.googleapis.com/revoke?token={token}",
                        method="POST",
                        headers={"Content-Type": "application/x-www-form-urlencoded"},
                    )
                    urllib.request.urlopen(req)
                except Exception:
                    pass
            if os.path.exists(TOKEN_PATH):
                os.remove(TOKEN_PATH)
            print(json.dumps({"status": "revoked"}))
            return
        oauth_flow()
        print("Authorized")
        return

    if tool not in TOOLS:
        fail(f"Unknown tool '{tool}'. Run gws.py --help for list.")

    # Parse JSON args
    if len(sys.argv) >= 3 and sys.argv[2] != "-":
        raw = " ".join(sys.argv[2:])
    elif not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
    else:
        raw = "{}"

    try:
        args = json.loads(raw)
    except json.JSONDecodeError as e:
        fail(f"Invalid JSON: {e}")

    try:
        token = ensure_token()
        result = TOOLS[tool](token, args)
        if isinstance(result, (dict, list)):
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(result)
    except ApiError as e:
        if e.code == 401:
            print("Token rejected, re-authenticating...", file=sys.stderr)
            try:
                creds = oauth_flow()
                result = TOOLS[tool](creds["token"], args)
                if isinstance(result, (dict, list)):
                    print(json.dumps(result, ensure_ascii=False, indent=2))
                else:
                    print(result)
            except ApiError as e2:
                fail(str(e2))
        else:
            fail(str(e))


if __name__ == "__main__":
    main()
