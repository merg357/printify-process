## 2026-09-04 - Cache Printify variants during bulk product creation
**Learning:** When generating multiple products in Printify (e.g. iterating over uploaded images and blueprint combos), `get_variants` requests the exact same third-party API variant JSON for the same blueprint and provider. In a loop, this causes an N+1 network bottleneck.
**Action:** Always use `@functools.lru_cache(maxsize=None)` with a `tuple` return type for static/rarely-changing Printify API lookup functions (`get_variants`) to prevent repeated external network calls during iterative loops.
