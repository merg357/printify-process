## 2026-10-25 - Memoize Blueprint Variants
**Learning:** Found repetitive N+1 network requests querying for Printify variant IDs for the same static blueprints in loop iterations during bulk product creation across multiple files.
**Action:** Use Python's built-in `@functools.lru_cache(maxsize=None)` for the `get_variants` functions and convert returned variant lists to immutable tuples to prevent shared state side-effects while drastically reducing network calls.
