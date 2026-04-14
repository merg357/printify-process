## 2024-06-25 - Memoize Static Third-Party API Responses
**Learning:** In bulk processing pipelines (like creating hundreds of products), fetching static provider data (e.g., variant IDs for a blueprint) inside loops creates massive network bottlenecks and risks rate-limiting.
**Action:** Use Python's `@functools.lru_cache(maxsize=None)` to memoize repetitive, static API queries (like `get_variants` from Printify) to eliminate redundant network requests and drastically speed up loops.
