## 2026-10-09 - Memoization of Printify Variants API

**Learning:** When creating products in bulk loops, repeatedly looking up variants for the same blueprint and provider causes unnecessary N+1 network bottlenecks.
**Action:** Always wrap static/infrequent third-party lookup queries (like Printify variants) with `@functools.lru_cache(maxsize=None)`. Cast the return type to an immutable `tuple` to ensure thread-safety and prevent unintended mutation of the shared cached references by downstream processes.
