## 2024-05-20 - Caching Mutable Objects in Python
**Learning:** Returning mutable objects like lists from an `@lru_cache` decorated function can lead to unexpected downstream side effects if modified. Python standard library `json` seamlessly serializes `tuple` objects to JSON arrays.
**Action:** When adding `@functools.lru_cache` to API fetch functions returning lists (like Printify variants), cast the return type to an immutable `tuple` to ensure thread-safety and prevent regressions.
