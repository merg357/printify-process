## 2026-09-21 - Printify API N+1 Bottleneck
**Learning:** Iterative bulk product creation loops query the same static Printify blueprint variants repeatedly, causing an N+1 network bottleneck.
**Action:** Use `@functools.lru_cache(maxsize=None)` to memoize static third-party API queries (like `get_variants`). Always cast the returned JSON lists to immutable `tuple`s to prevent unintended downstream mutations from shared cached references.
