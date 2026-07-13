## 2026-07-13 - Printify API N+1 Bottleneck
**Learning:** During bulk operations, querying static resources like blueprint variants repeatedly inside the creation loop causes an N+1 API bottleneck. Returning a list from a cached function can lead to downstream state mutation bugs.
**Action:** Always wrap static/infrequently changing API calls in loops with @functools.lru_cache(maxsize=None) and return an immutable tuple instead of a list.
