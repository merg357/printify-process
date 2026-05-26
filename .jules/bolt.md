## 2026-04-17 - Memoize Duplicate Printify API Calls
**Learning:** The codebase performs repeated API fetches for static third-party blueprint variants within loops across multiple scripts, causing measurable network bottlenecks.
**Action:** Use `@functools.lru_cache(maxsize=None)` on the API-fetching functions to cache the variant responses, thus skipping duplicate network requests when iterating over the same blueprints.
