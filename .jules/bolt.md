## 2026-10-10 - Memoize Third-Party API Responses
**Learning:** In iterative operations like bulk product creation, third-party API calls (e.g., fetching blueprints) can silently create N+1 bottlenecks.
**Action:** Use `@functools.lru_cache(maxsize=None)` with immutable return types (like tuples) to cache repetitive network requests safely without risking downstream state mutation.
