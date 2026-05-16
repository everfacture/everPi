---
name: tinyfish-search
description: Web search via TinyFish Search API. Use for searching documentation, facts, or any web content. Lightweight, no browser required. Free tier available.
---

# TinyFish Search

Web search using the TinyFish Search API. Returns structured results (title, URL, snippet) ready for LLM consumption.

## Setup

Requires `TINYFISH_API_KEY` environment variable. Add to `~/.zprofile`:

```bash
export TINYFISH_API_KEY="your-api-key"
```

## Search

```bash
tinyfish-search.js "query"                              # Basic search
tinyfish-search.js "query" --location US --language en  # Geo-targeted
tinyfish-search.js "query" --page 2                      # Pagination (page 0-10)
tinyfish-search.js "query" --content                     # Raw JSON output
```

## Options

- `--location <code>` — Country code for geo-targeted results (e.g. US, GB, FR, DE)
- `--language <code>` — Language code (e.g. en, fr, de)
- `--page <num>` — Page number starting from 0 (max 10)
- `--content` — Output raw JSON instead of formatted text

## Search Operators

Use operators inside the query string:
- `python tutorial site:docs.python.org` — Limit to a domain
- `recipe ideas -site:facebook.com -site:youtube.com` — Exclude domains

## Output Format

```
--- Result 1 ---
Title: Page Title
Link: https://example.com/page
Site: example.com
Snippet: Description from search results

--- Result 2 ---
...

Total: 10 results
```

## When to Use

- Searching for documentation or API references
- Looking up facts or current information
- Any task requiring web search without interactive browsing

## Rate Limits

30 requests per minute on free tier. Does not use credits.
