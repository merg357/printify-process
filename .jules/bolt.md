## 2026-10-02 - Memoize Printify Variant Queries
**Learning:** Iterative bulk product creation loops (e.g., cmd_create) suffer from N+1 network bottlenecks by repeatedly calling get_variants() to fetch static Printify variant IDs for the same blueprints.
**Action:** Apply @functools.lru_cache to memoize get_variants() responses. Cast the return type from a list to an immutable tuple to guarantee thread safety and prevent downstream mutation of the cached reference. json.dumps() natively handles serializing tuples to JSON arrays.
