## 2024-05-23 - Memoizing Mutable Types
**Learning:** Using `lru_cache` to cache JSON response lists from an API is unsafe, because the list is mutable, which exposes cached state. Returning `tuple` instead creates an immutable sequence, while serializing cleanly to JSON.
**Action:** When caching API queries with `lru_cache`, ensure the return value is wrapped in a tuple or another immutable structure if it is to be passed downwards. Update matching typehints as appropriate.
