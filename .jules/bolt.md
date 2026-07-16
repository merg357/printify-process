## 2026-07-16 - LRU Cache with Lists and Mutability
**Learning:** Using @functools.lru_cache on list-returning API calls risks mutability bugs and thread safety issues.
**Action:** Cast the return type to an immutable structure (tuple) when memoizing responses to guarantee safety.
