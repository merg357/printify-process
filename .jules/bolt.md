## 2026-09-13 - Cache Third-Party Variant Lookups
**Learning:** In bulk operations calling external Printify APIs (like fetching blueprint variants), static configuration calls can become severe N+1 bottlenecks within iterative creation loops.
**Action:** Use Python's `@functools.lru_cache(maxsize=None)` for static/infrequently changing API lookups to save ~150-300ms per duplicate loop. Always cast the returned mutable structures (e.g., lists) to immutables (like tuples) to guarantee thread safety and prevent downstream cache corruption.
