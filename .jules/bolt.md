## 2026-07-12 - Cache repetitive Printify API variant lookups
**Learning:** The bulk product creation loops query static blueprint variants on each iteration, causing an N+1 network bottleneck. Since Printify blueprint variants rarely change during a script's execution, caching these responses significantly speeds up operations.
**Action:** Use `@functools.lru_cache(maxsize=None)` for static 3rd-party API queries in loops, ensuring the return type is an immutable `tuple` (instead of `list`) to guarantee thread safety and prevent downstream state mutations while remaining JSON-serializable.
