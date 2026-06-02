## 2026-06-02 - Printify API N+1 Queries Bottleneck
**Learning:** Repetitive Printify API variant queries in product creation loops cause a severe N+1 network bottleneck.
**Action:** Always use `@functools.lru_cache(maxsize=None)` to memoize these API queries. Ensure the cached function returns an immutable `tuple` to prevent downstream state mutations, and safely drop it into API JSON payloads since `json.dumps()` natively serializes tuples into JSON arrays.
