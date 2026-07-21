## 2026-07-21 - Cache Repeated Printify API Calls
**Learning:** The bulk product creation loops query the identical blueprint variants from the Printify API for every single uploaded image, creating a severe N+1 network bottleneck.
**Action:** Always memoize static 3rd-party API lookups (like `get_variants`) using `@functools.lru_cache(maxsize=None)` and cast returns to immutable types like `tuple` to ensure thread-safety and prevent unintended mutations during iterative creation workflows.
