# Engineering Patterns from steipete's Codebases

Concrete implementation patterns from deep analysis of 10 repos. Reference these when implementing similar functionality. Use these patterns as starting points -- adapt, don't copy.

---

## 1. Streaming Dedup with Overlap Heuristics (summarize/streaming-merge.ts)

**Trigger:** Streaming APIs, WebSocket streams, SSE events where data might be resent or partially duplicated.

**Problem:** Streaming APIs resend partial chunks, causing duplicate text in output.

```typescript
function mergeStreamingChunk(existing: string, newChunk: string, maxOverlap: number = 4096): string {
  if (existing.endsWith(newChunk)) return existing;
  
  const overlapEnd = Math.min(maxOverlap, existing.length);
  for (let i = overlapEnd; i > 0; i--) {
    const tail = existing.slice(-i);
    if (newChunk.startsWith(tail)) {
      return existing + newChunk.slice(i);
    }
  }
  
  return existing + newChunk;
}
```

**Recognize this when:** You see duplicate content in streamed output, or an API that doesn't guarantee clean sequential chunks.

---

## 2. Exponential Priority Decay (poltergeist/priority-engine.ts)

**Trigger:** Build systems, task schedulers, background job queues where multiple things need attention simultaneously.

**Problem:** Which task to prioritize when many are pending?

```typescript
function computePriority(target: Target, recentChanges: FileChange[]): number {
  const now = Date.now();
  const ageMs = now - lastChange.timestamp;
  const recencyScore = Math.exp(-ageMs / 30_000); // 30s half-life
  const focusPct = recentChanges.filter(c => c.target === target.id).length / recentChanges.length;
  const focusMultiplier = 1.0 + focusPct; // 1.0x - 2.0x
  return recencyScore * focusMultiplier;
}
```

**Recognize this when:** You have a queue of tasks and need to decide which to do first based on recency and attention patterns, not just FIFO.

---

## 3. Stale Lock Detection with Heartbeats (poltergeist/state.ts)

**Trigger:** Any file-based locking, daemon management, build systems where processes can crash without cleanup.

**Problem:** Process crashes without cleaning up lock files, leaving resources permanently locked.

```typescript
async function isLockStale(lockPath: string): Promise<boolean> {
  const lock = await readLockFile(lockPath);
  if (!lock) return false;
  if (!await isProcessRunning(lock.pid)) return true;
  if (Date.now() - lock.lastHeartbeat > 5 * 60 * 1000) return true;
  return false;
}
```

**Recognize this when:** You see lock files that persist after a crash, or a system that says "resource busy" but nothing is using it.

---

## 4. Dynamic API Hash Resolution (spogo/connect_hash.go)

**Trigger:** APIs with obfuscated identifiers, versioned endpoints, anti-scraping measures.

**Problem:** GraphQL or internal APIs require hashes/tokens that change with each deploy.

```go
func (h *hashResolver) Hash(ctx context.Context, operation string) (string, error) {
  if hash, ok := h.hashes[operation]; ok { return hash, nil }
  html := h.fetchWebPlayerHTML(ctx)
  mainJS := pickWebPlayerBundle(html)
  hashMap := parseWebpackMaps(mainJS)
  h.hashes = hashMap
  return hashMap[operation], nil
}
```

**Recognize this when:** You need API parameters that change frequently and can't be hardcoded -- scrape the client that generates them.

---

## 5. Multi-Strategy Child Discovery (AXorcist/Element.swift)

**Trigger:** Tree traversal where node structure varies unpredictably (different app types, different versions).

**Problem:** Standard API returns nothing for some node types (Electron, web, hybrid apps).

```swift
func collectChildren(_ element: AXUIElement) -> [AXUIElement] {
  if let c = getAttribute(element, kAXChildrenAttribute) as? [AXUIElement] { return c }
  if let c = getAttribute(element, kAXVisibleChildrenAttribute) as? [AXUIElement] { return c }
  if let c = getAttribute(element, "AXSharedTextChildren") as? [AXUIElement] { return c }
  // ... 11 more strategies
  return []
}
```

**Recognize this when:** Your standard API call returns empty for some inputs but works for others -- different implementations need different discovery paths.

---

## 6. Atomic File Write with Retry (poltergeist/atomic-write.ts)

**Trigger:** Any file write where consistency matters, especially on Windows or multi-process scenarios.

**Problem:** Windows EBUSY errors when renaming files held by other processes.

```typescript
async function writeFileAtomic(filepath: string, content: string): Promise<void> {
  const tmpfile = path.join(dir, `.${basename}.${process.pid}.${randomHex()}.tmp`);
  await fs.writeFile(tmpfile, content);
  for (let retries = 0; retries < 10; retries++) {
    try {
      await fs.rename(tmpfile, filepath);
      return;
    } catch (e: any) {
      if (e.code === 'EBUSY' || e.code === 'ENOTEMPTY') {
        await sleep(50 * retries);
      } else throw e;
    }
  }
  throw new Error(`Failed atomic write after 10 retries`);
}
```

**Recognize this when:** File writes fail with EBUSY, ENOTEMPTY, or "file in use" -- especially on Windows.

---

## 7. Variadic AutoCall with Generics (spogo/auto.go)

**Trigger:** Retry/fallback logic duplicated across methods with different return signatures.

**Problem:** Same fallback pattern copied 20 times for methods returning 1, 2, 3 values.

```go
func autoCall[T any](c *autoClient, fn func(API) (T, error)) (T, error) {
  res, err := fn(c.primary)
  if err == nil || !c.shouldFallback(err) { return res, err }
  return fn(c.secondary)
}
```

**Recognize this when:** You catch the same error type and retry with a fallback in 3+ places. Extract to generic wrapper.

---

## 8. Multi-Source Config Aggregation (mcporter/config.ts)

**Trigger:** Systems that need configuration from multiple tool ecosystems or file locations.

**Problem:** Servers/configs defined across 10+ different config files in different formats.

```typescript
async function loadAllConfigs(): Promise<Map<string, ServerDefinition>> {
  const merged = new Map<string, ServerDefinition>();
  const sources = ['~/.claude/settings.json', '~/.cursor/mcp.json', '~/.mcporter/config.json'];
  for (const source of sources) {
    for (const [name, def] of await loadConfig(source)) {
      if (!merged.has(name)) merged.set(name, { ...def, source });
    }
  }
  return merged;
}
```

**Recognize this when:** Users ask "can it read from X?" and X is one of many tools they already use. Aggregate, don't duplicate.

---

## 9. DB Snapshot for Live Databases (sweet-cookie)

**Trigger:** Reading SQLite/database files that might be held open by another process.

**Problem:** Browser cookie databases are locked while the browser is running.

```typescript
async function extractCookies(browserPath: string): Promise<Cookie[]> {
  const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), 'cookies-'));
  await fs.copyFile(path.join(browserPath, 'Cookies'), path.join(tempDir, 'Cookies'));
  if (await fs.exists(dbPath + '-wal')) {
    await fs.copyFile(dbPath + '-wal', path.join(tempDir, 'Cookies-wal'));
  }
  const cookies = await readCookiesFromSnapshot(tempDir);
  await fs.rm(tempDir, { recursive: true });
  return cookies;
}
```

**Recognize this when:** You get "database is locked" or "file in use" reading a database that another process owns.

---

## 10. Permission Probing via Operation (peekaboo)

**Trigger:** Any system where permission/feature checks are unreliable -- test the actual operation instead.

**Problem:** Official permission APIs lie (return false even when granted, especially for CLI tools).

```swift
func hasScreenCapturePermission() -> Bool {
  if CGPreflightScreenCaptureAccess() { return true }
  // Real test: try the actual operation
  return SCShareableContent.current != nil
}
```

**Recognize this when:** A permission check fails but the operation actually works, or a feature flag is wrong. Test the thing, not the gatekeeper.

---

## 11. CFHash Cycle Detection (AXorcist)

**Trigger:** Tree/graph traversal where cycles are possible (accessibility trees, dependency graphs, DOM trees).

**Problem:** Cycles cause infinite loops. Depth limits are blunt and miss shallow cycles.

```swift
func traverseTree(_ element: AXUIElement, visited: inout Set<UInt>, depth: Int = 0) -> [Element] {
  guard depth < 50 else { return [] }
  let hash = CFHash(element)
  guard !visited.contains(hash) else { return [] }
  visited.insert(hash)
  return [Element(element)] + collectChildren(element).flatMap {
    traverseTree($0, visited: &visited, depth: depth + 1)
  }
}
```

**Recognize this when:** Tree traversal hangs or hits arbitrary depth limits. Hash-based cycle detection is O(1) and catches cycles at any depth.

---

## 12. Warning Aggregation with Dedup (spogo/cookies.go)

**Trigger:** Systems with multiple potential failure modes where users need concise error messages.

**Problem:** Too many individual errors overwhelm users. Single vague error is unhelpful.

```go
func compactWarnings(warnings []string) []string {
  out := slices.Compact(warnings)
  if len(out) > 3 { out = out[:3] }
  return out
}
```

**Recognize this when:** An operation can fail for 5+ different reasons and showing all of them is worse than showing none.
