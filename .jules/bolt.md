## 2024-05-30 - Printify API N+1 Network Bottleneck
**Learning:** Fetching blueprint variants in iterative product creation loops causes an N+1 network bottleneck, slowing down bulk scripts.
**Action:** Always memoize static or infrequently changing third-party API queries (like blueprint variants) using `@functools.lru_cache(maxsize=None)`. Ensure to return an immutable structure like a tuple to prevent shared reference mutations.
