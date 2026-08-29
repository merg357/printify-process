## 2026-08-29 - Memoize Repeated Third-Party API Queries
**Learning:** The application loops over designs and repeatedly creates products for a fixed set of blueprints, causing N+1 network requests to Printify for variant IDs. Third-party catalog endpoints are often static during a session.
**Action:** Apply `@functools.lru_cache(maxsize=None)` to static API wrappers like `get_variants()`. Always cast the returned JSON list to a `tuple` to ensure thread safety and prevent downstream state mutations from shared references, relying on `json.dumps()` native tuple serialization.
