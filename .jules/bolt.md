## 2026-08-30 - Memoize variant API queries
**Learning:** In iterative product creation loops against third-party APIs (like Printify), fetching static blueprint variants repeatedly causes severe N+1 network bottlenecks. Caching these with `@functools.lru_cache` is effective, but requires converting mutable lists to immutable tuples to prevent shared-reference bugs in downstream payload construction.
**Action:** Always wrap static/infrequent external API queries inside loops with `@functools.lru_cache(maxsize=None)` and enforce immutable return types (e.g., `tuple`) for safety.
