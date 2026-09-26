## 2026-09-26 - N+1 Network Bottleneck in Bulk Product Creation
**Learning:** The bulk product creation loop repeatedly fetches static blueprint variants from Printify (an N+1 API request pattern), slowing down execution.
**Action:** Always memoize static or infrequently changing third-party API queries using `@functools.lru_cache(maxsize=None)` with an immutable `tuple` return type within iterative product creation loops.
