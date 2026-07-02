## 2026-07-02 - N+1 Blueprint Variant Network Bottleneck
**Learning:** During iterative bulk product creation, repeatedly querying third-party APIs (like Printify) for static blueprint variants causes significant N+1 network bottlenecks.
**Action:** Always wrap static or infrequently changing third-party API queries in product creation loops with @functools.lru_cache(maxsize=None). Ensure the return data structure is explicitly cast to an immutable type (like tuple) to guarantee thread safety and prevent downstream state mutations.
