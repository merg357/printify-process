## 2026-09-23 - Printify N+1 Query Elimination

**Learning:** During bulk product creation, static data such as third-party API blueprint variants can cause severe N+1 network bottlenecks because the same identical network requests are made for every item in the batch.

**Action:** Whenever iterating over arrays to create objects that require supplementary third-party data, always apply `@functools.lru_cache(maxsize=None)` to the supplementary queries and ensure the return type is an immutable `tuple` instead of a mutable `list`.
