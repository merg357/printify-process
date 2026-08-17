## 2026-08-17 - Cache Immutability and Type Hints
**Learning:** When using @functools.lru_cache and altering the return type to an immutable `tuple` (instead of `list`) for safety, you must also explicitly update the type hints of downstream functions receiving this data to prevent static type checking errors.
**Action:** Before changing a return type for caching purposes, always verify and update downstream consumers' type hints (e.g., from `List[int]` to `tuple`).
