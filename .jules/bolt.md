## 2026-10-16 - Memoization of Printify API lookups
**Learning:** In bulk merchandise creation loops, static blueprint lookups via API cause severe N+1 bottlenecks.
**Action:** Always wrap static third-party API queries in loops with @functools.lru_cache(maxsize=None) and ensure they return immutable types (like tuples) to guarantee thread safety.
