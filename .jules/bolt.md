## 2026-06-28 - N+1 Network Bottlenecks in Printify API Loops
**Learning:** When fetching third-party API configurations inside iterative product generation loops, failing to cache static data (like print provider variants) results in an N+1 performance bottleneck. Returning mutable structures (like lists) from cached API responses can lead to unsafe memory references across iterations.
**Action:** Always wrap static/infrequent external API fetching functions with `@functools.lru_cache(maxsize=None)` and ensure the return value is cast to an immutable `tuple` to guarantee thread safety.
