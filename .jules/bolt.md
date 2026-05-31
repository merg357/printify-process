## 2026-05-31 - Printify Variants N+1 Network Bottleneck
**Learning:** During bulk product creation, the app makes repeated API calls to fetch variants for the same blueprints, causing an N+1 network bottleneck and risking API rate limits. Furthermore, returning mutable lists from cached functions can lead to unintended state mutation bugs.
**Action:** Use `@functools.lru_cache(maxsize=None)` to memoize third-party API queries like fetching blueprint variants, and explicitly cast the return type to an immutable structure like `tuple` to ensure thread safety and prevent downstream mutations.
