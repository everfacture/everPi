# Skills

Skills the agent loads automatically. Install via `pi install`.

## tinyfish-search

Web search via the TinyFish API. Returns title, URL, snippet.

```bash
tinyfish-search.js "your query"
tinyfish-search.js "query" --location US --language en
tinyfish-search.js "query" --page 2
tinyfish-search.js "query" --content   # raw JSON output
```

Query supports search operators: `site:`, `-site:`, etc.

**Requires:** `TINYFISH_API_KEY`
**Rate limit:** 30 requests/min on free tier
**No credit cost**
