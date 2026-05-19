## 2025-05-24 - Memoize Printify Blueprint Variants
**Learning:** Calling the Printify API for static blueprint variants inside large loops creates a massive bottleneck due to network latency, causing the script to slow down significantly on large operations.
**Action:** Use Python's `@functools.lru_cache` to memoize invariant API requests such as blueprint lookups during bulk creations.
