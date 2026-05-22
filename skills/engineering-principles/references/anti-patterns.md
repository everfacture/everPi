# LLM Anti-Pattern Examples

Concrete wrong-vs-right examples demonstrating the four Karpathy principles. Use when reviewing your own proposed changes, or when a request triggers one of the four patterns. Each example shows what LLMs commonly do wrong and how to fix it.

---

## 1. Think Before Coding

### Example: Hidden Assumptions

**User Request:** "Add a feature to export user data"

**❌ Wrong — Silent Assumptions**

```python
def export_users(format='json'):
    users = User.query.all()
    if format == 'json':
        with open('users.json', 'w') as f:
            json.dump([u.to_dict() for u in users], f)
    elif format == 'csv':
        with open('users.csv', 'w') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'email', 'name'])
            writer.writeheader()
            writer.writerows([u.to_dict() for u in users])
    return f"Exported {len(users)} users"
```

**Problems:** Assumed ALL users (privacy? pagination?). Assumed file location. Assumed fields. Assumed CSV fieldnames match actual schema.

**✅ Right — Surface Assumptions**

```
Before implementing, I need to clarify:

1. Scope: Export all users or filtered subset? (privacy implications)
2. Format: Download in browser? Background job with email? API endpoint?
3. Fields: Which user fields? (some might be sensitive)
4. Volume: How many users typically? (affects approach)

Simplest approach: paginated JSON API endpoint.
What's your preference?
```

### Example: Multiple Interpretations

**User Request:** "Make the search faster"

**❌ Wrong — Pick Silently**

```python
# Adds caching, indexes, and async without asking which "faster" matters
@lru_cache(maxsize=1000)
async def search(query: str) -> List[Result]:
    # ... 200 lines of optimization code
```

**✅ Right — Present Interpretations**

```
"Make the search faster" could mean:

1. Faster response time (< 100ms instead of 500ms)
   → Database indexes, cache frequent queries. ~2 hours.
2. Handle more concurrent searches (throughput)
   → Async/await, connection pooling. ~4 hours.
3. Faster perceived speed (UX)
   → Partial results immediately, progressive loading. ~3 hours.

Current search ~500ms for typical queries. Which aspect matters most?
```

---

## 2. Simplicity First

### Example: Over-abstraction

**User Request:** "Add a function to calculate discount"

**❌ Wrong — Strategy Pattern for One Calculation**

```python
from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, amount: float) -> float: pass

class PercentageDiscount(DiscountStrategy): ...
class FixedDiscount(DiscountStrategy): ...

@dataclass
class DiscountConfig:
    strategy: DiscountStrategy
    min_purchase: float = 0.0
    max_discount: float = float('inf')

class DiscountCalculator:
    def __init__(self, config: DiscountConfig): ...
    def apply_discount(self, amount: float) -> float: ...
```

**30+ lines of setup for a single calculation.**

**✅ Right — One Function**

```python
def calculate_discount(amount: float, percent: float) -> float:
    """Calculate discount amount. percent should be 0-100."""
    return amount * (percent / 100)
```

**When to add complexity:** Only when you actually need multiple discount types. If that requirement comes later, refactor then.

### Example: Speculative Features

**User Request:** "Save user preferences to database"

**❌ Wrong — Caching, Validation, Merging, Notifications — All Unasked**

```python
class PreferenceManager:
    def __init__(self, db, cache=None, validator=None):
        self.db = db
        self.cache = cache or InMemoryCache()
        self.validator = validator or DefaultValidator()

    def save(self, user_id, prefs, merge=True, validate=True, notify=False):
        if validate: ...
        if merge: ...
        if notify: self.notify_preference_change(user_id, prefs)  # 30 more lines
```

**✅ Right — What Was Asked**

```python
def save_preferences(db, user_id: int, preferences: dict):
    db.execute(
        "UPDATE users SET preferences = ? WHERE id = ?",
        (json.dumps(preferences), user_id)
    )
```

**Add later when needed:** caching (when perf matters), validation (when bad data appears), merging (when requirement emerges).

---

## 3. Surgical Changes

### Example: Drive-by Refactoring

**User Request:** "Fix the bug where empty emails crash the validator"

**❌ Wrong — "Improved" Everything**

```diff
  def validate_user(user_data):
-     if not user_data.get('email'):
+     email = user_data.get('email', '').strip()
+     if not email:
          raise ValueError("Email required")
-     if '@' not in user_data['email']:
+     if '@' not in email or '.' not in email.split('@')[1]:
          raise ValueError("Invalid email")
-     if not user_data.get('username'):
+     username = user_data.get('username', '').strip()
+     if not username:
+         if len(username) < 3: raise ValueError("Username too short")
+         if not username.isalnum(): raise ValueError("Username must be alphanumeric")
```

**Problems:** "Improved" email validation. Added username validation nobody asked for. Changed comments.

**✅ Right — Only Fix the Bug**

```diff
  def validate_user(user_data):
      # Check email format
-     if not user_data.get('email'):
+     email = user_data.get('email', '')
+     if not email or not email.strip():
          raise ValueError("Email required")
      # Basic email validation
-     if '@' not in user_data['email']:
+     if '@' not in email:
          raise ValueError("Invalid email")
```

**Only changed:** lines that fix empty email handling.

### Example: Style Drift

**User Request:** "Add logging to the upload function"

**❌ Wrong — Reformats Everything**

```diff
- def upload_file(file_path, destination):
+ def upload_file(file_path: str, destination: str) -> bool:
+     """Upload file to destination with logging."""
+     logger.info(f"Uploading {file_path} to {destination}")
      try:
-         with open(file_path, 'rb') as f:
-             response = requests.post(destination, files={'file': f.read()})
+         with open(file_path, "rb") as f:  # ← double quotes now
+             data = f.read()
+         response = requests.post(destination, files={"file": data})
+         success = response.status_code == 200
```

**Problems:** Changed quote style. Added type hints. Added docstring. Reformatted whitespace. Changed return logic.

**✅ Right — Match Existing Style**

```diff
+ import logging
+ logger = logging.getLogger(__name__)
+
  def upload_file(file_path, destination):
+     logger.info(f'Starting upload: {file_path}')
      try:
-         print(f"Error: {e}")
+         logger.exception(f'Upload error: {file_path}')
```

**Matched:** Single quotes, no type hints, existing spacing. Only added logging lines.

---

## 4. Goal-Driven Execution

### Example: Vague vs. Verifiable

**User Request:** "Fix the authentication system"

**❌ Wrong — Vague Steps**

```
1. Review the code
2. Identify issues
3. Make improvements
4. Test the changes
```

No success criteria. No way to verify done.

**✅ Right — Verifiable Goals**

```
If issue is "users stay logged in after password change":

1. Write test: Change password → verify old session invalidated
   Verify: Test fails (reproduces bug)

2. Implement: Invalidate sessions on password change
   Verify: Test passes

3. Check edge cases: multiple active sessions, concurrent changes
   Verify: Additional tests pass

4. Verify no regression: existing auth tests still pass
   Verify: Full test suite green
```

### Example: Multi-Step with Verification

**User Request:** "Add rate limiting to the API"

**❌ Wrong — 300 Lines in One Commit, No Verification Steps**

Full rate limiting with Redis, multiple strategies, config system, monitoring — all at once.

**✅ Right — Incremental, Each Step Deployable**

```
1. Basic in-memory rate limiting (single endpoint)
   Verify: 100 requests → first 10 succeed, rest 429

2. Extract to middleware (all endpoints)
   Verify: Rate limits apply to /users and /posts; existing tests pass

3. Redis backend (multi-server)
   Verify: Rate limit persists across restarts; two instances share counter

4. Configuration (rates per endpoint)
   Verify: /search 10/min, /users 100/min; config parsed correctly

Each step independently verifiable and deployable.
```

---

## Anti-Pattern Summary

| Principle | Anti-Pattern | Fix |
|-----------|-------------|-----|
| Think Before Coding | Silently assumes format, fields, scope | List assumptions, ask |
| Simplicity First | Strategy pattern for single calculation | One function until complexity is needed |
| Surgical Changes | Reformats quotes, adds type hints during bug fix | Only change lines that fix the issue |
| Goal-Driven | "Review and improve" | "Write test for X → make it pass → verify no regressions" |

## Key Insight

The "overcomplicated" examples aren't obviously wrong — they follow design patterns and best practices. The problem is **timing**: they add complexity before it's needed.

- Makes code harder to understand
- Introduces more bugs
- Takes longer to implement
- Harder to test

**Good code solves today's problem simply, not tomorrow's problem prematurely.**
