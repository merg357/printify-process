## 2024-04-23 - Memoizing Static Third-Party API Responses
**Learning:** The codebase performs repetitive third-party API queries (e.g., fetching blueprint variants from Printify) inside bulk processing loops. These responses are essentially static during a run, creating a significant network bottleneck.
**Action:** Use Python's `@functools.lru_cache(maxsize=None)` to memoize functions fetching static external data to prevent redundant network requests and drastically speed up bulk operations.
