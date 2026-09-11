## 2026-09-11 - Cache Printify Variants API

**Learning:** Repeated identical queries to the Printify `variants.json` API during bulk product creation cause unnecessary network latency and N+1 bottlenecks.
**Action:** Use Python's `@functools.lru_cache(maxsize=None)` to memoize static Printify blueprints API requests. Return a `tuple` instead of a `list` to prevent downstream mutation issues and ensure cache safety, while using Python's built-in `json.dumps()` array serialization compatibility for tuples.
