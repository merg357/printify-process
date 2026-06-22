## 2026-06-22 - Printify API N+1 Bottleneck in Bulk Creation Loops
**Learning:** During bulk product creation, static third-party API queries (like fetching blueprint variants from Printify) cause an N+1 network bottleneck if left unmemoized in the creation loop.
**Action:** Always use Python's `@functools.lru_cache(maxsize=None)` to memoize infrequently changing third-party API queries within iterative loops. Remember to cast the returned JSON list to an immutable `tuple` to guarantee thread safety and prevent downstream state mutations from shared references.
