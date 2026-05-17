# Model Selection & Benchmarking for Pipeline Tasks

## Core Lesson: Trivial Prompts Lie

A model that replies "OK" in 0.3s may take 30+ seconds on a real pipeline payload. **Always benchmark with production-sized inputs.**

### What went wrong (concrete example)

| Test | qwen3.5-plus | qwen3-coder-next |
|------|-------------|------------------|
| "Reply OK" | 2.90s | 0.36s |
| Scoring payload (~1500 tokens) | 30s+ (timeout) | 1.69s |
| Format compliance | Unknown (timed out) | Perfect |

qwen3.5-plus looked fine on a trivial test but was unusable on real payloads because of **reasoning token overhead** — it spent 127 reasoning tokens on "Reply with: OK". The `/no_think` prefix suppresses this partially, but for full scoring payloads the reasoning engine still burns time.

qwen3-coder-next had no reasoning overhead and returned structured output in 1.69s — making it 20x faster for the actual workload despite looking similar on trivial tests.

### Benchmarking Protocol

For any LLM-powered pipeline stage, run these tests **before** committing to a model:

```
1. CONNECTIVITY: Single trivial call (model responds, API key works)
2. FORMAT: System prompt + real payload → check output format compliance
3. LATENCY: 3× timed calls with production-sized payloads
4. TOKEN ECONOMICS: Track prompt_tokens vs completion_tokens vs reasoning_tokens
5. RATE LIMIT MATH: 
   - Latency-limited RPM = 60 / avg_seconds_per_call
   - Pipeline total = job_count × avg_seconds_per_call / 60
   - Is the pipeline bottlenecked by latency or by rate limits?
```

### Key Metrics to Measure

- **Latency per call** — average over 3+ calls with real payload size
- **Reasoning tokens** — if >10% of completion_tokens, the model is doing unnecessary CoT
- **Format compliance** — does output match the expected structured format?
- **Score consistency** — same input should give same score (±1)
- **RPM ceiling** — distinguish: rate-limit RPM (provider cap) vs actual RPM (latency-limited throughput)

### The Model Selection Matrix

| Model | Trivial Call | Real Payload | Reasoning Overhead | Format OK? | Verdict |
|-------|-------------|--------------|-------------------|------------|---------|
| qwen3.5-plus | 2.9s | 30s+ (timeout) | High (127 tok for "OK") | Untested | Slow for pipeline |
| qwen3-coder-plus | 1.17s | 4.23s | Low | Yes | Usable (64 min/913 jobs) |
| qwen3-coder-next | 0.36s | 1.69s | None | Yes | **Fastest — 26 min/913 jobs** |
| deepseek-chat (V3) | 0.6s | 5.2s | Low | Yes | Workable (79 min/913 jobs) |
| deepseek-v4-flash | 0.4s | 4.5s | Low | **No — empty output** | Broken for scoring |
| glm-5 (DashScope) | 4.0s | 23.2s | Moderate | Yes | Fallback only |

Note: `deepseek-v4-flash` returned empty content for structured scoring payloads — a format compliance issue that trivial testing missed. Always verify output format, not just latency.

### When to Reach for a Cascade

If the fastest model still gives unacceptable throughput, consider a **multi-provider fallback cascade**:

```
Primary: Fast cheap model (e.g. deepseek-chat, qwen3-coder-next)
  → ~0.5-1.7s per call → 8-26 min for 913 jobs
Fallback: Slower but reliable (e.g. qwen3-coder-plus)
  → ~4s per call → ~64 min for 913 jobs
Last resort: Quality model for retries (e.g. qwen3.5-plus)
  → Slow, use only when both faster models fail
```

The cascade is implemented at the provider level in `llm.py`:
- Try primary first
- On 429/503/timeout, fall to secondary
- On secondary failure, mark job as `score_error` and retry on next cron cycle

### /no_think Optimization for Qwen Models

Qwen models from DashScope default to chain-of-thought reasoning even for simple extraction tasks. The `/no_think` prefix suppresses this:

```python
if "qwen" in model and not message.startswith("/no_think"):
    message = f"/no_think\n{message}"
```

This is already handled by the LLMClient's `chat()` method. But be aware: it doesn't fully suppress reasoning on `qwen3.5-plus` for large payloads. The coder-series models (qwen3-coder-next, qwen3-coder-plus) have fundamentally less reasoning overhead.
