## 2026-09-22 - N+1 Network Bottleneck in Bulk Product Creation
**Learning:** Static third-party API queries (like fetching blueprint variants) within iterative bulk operations cause severe N+1 network bottlenecks.
**Action:** Always memoize static API query results using `@functools.lru_cache(maxsize=None)` in iterative creation loops, and cast returned JSON arrays to immutable tuples to prevent shared state mutation.
