## 2024-04-29 - [Memoize Printify Blueprint Variant Lookups]
**Learning:** [Discovered an N+1 network bottleneck in `printify_manager.py` where `create_product` continuously calls `get_variants` for the same blueprint and provider IDs in iterative loops (such as in `cmd_create`). This repeats identical API requests to Printify for static variant lists.]
**Action:** [Apply Python's `@functools.lru_cache(maxsize=None)` to functions like `get_variants` that query static or infrequently changing third-party APIs during iterative loops to prevent repetitive and expensive network calls.]
