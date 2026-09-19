## 2026-09-19 - Cache Safety with Mutable Returns
**Learning:** When using @functools.lru_cache to memoize API responses, returning mutable objects (like lists or dictionaries parsed from JSON) can cause dangerous downstream state mutations if a caller modifies the result.
**Action:** Always cast cached return values to immutable types (e.g., tuples instead of lists, or frozensets) to guarantee thread safety and prevent accidental cache poisoning.
