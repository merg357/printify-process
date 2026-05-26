## 2026-04-25 - Initializing Bolt Journal
**Learning:** Found the need to memoize API calls using `@functools.lru_cache` on functions like `get_variants` in multiple files.
**Action:** Always add `import functools` and `@functools.lru_cache(maxsize=None)` to `get_variants` or similar static API query functions in Python.
