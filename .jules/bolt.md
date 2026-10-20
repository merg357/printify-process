## 2026-10-20 - Cache Remote Variant Blueprints in Loops
**Learning:** Inside product creation loops across multiple scripts, requesting Printify variants by blueprint is repeated continuously causing N+1 network calls, even though variant structures for identical blueprint-provider pairs rarely change mid-run.
**Action:** When repeatedly calling external APIs for static blueprint structures, use `@functools.lru_cache` and always cast list returns to immutable `tuple`s to prevent unintended modifications by caller processes.
