## 2026-09-16 - Memoize Blueprint Variants
**Learning:** In batch API operations (e.g. creating many products using a few base blueprints), repeated queries for static blueprint configurations (variants) cause N+1 network bottlenecks and increase the risk of rate-limiting.
**Action:** Use Python's `@functools.lru_cache` to memoize repetitive, static external API responses. Ensure the return type is cast to an immutable structure (like `tuple`) to maintain thread safety and prevent downstream state mutations in cache-shared references.
