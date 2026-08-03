## 2026-08-03 - Immutable Returns for Safely Caching API Responses
**Learning:** When using `@functools.lru_cache` to memoize repeated 3rd-party API requests (like fetching Printify blueprint variants) within an iteration loop, returning mutable lists risks downstream mutation, which corrupts the shared cache.
**Action:** Cast JSON arrays to tuples before returning from cached API calls and ensure type hints (e.g., `tuple[int, ...]`) reflect the immutability. Since `json.dumps()` natively serializes tuples to JSON arrays, they are a safe drop-in replacement.
