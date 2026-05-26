## 2024-05-18 - Caching Third-Party API Results
**Learning:** Repetitive and static third-party API queries (like fetching blueprint variants from Printify) can become significant network bottlenecks during bulk processing loops.
**Action:** Always memoize these operations using `@functools.lru_cache(maxsize=None)` to speed up execution and reduce unnecessary network calls.
