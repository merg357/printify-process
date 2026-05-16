## 2025-04-06 - API Connection Pooling
**Learning:** Sequential API requests across a bulk management script (`printify_manager.py`) suffer significant latency overhead from repeated TCP and TLS handshakes.
**Action:** Always use `requests.Session()` instead of isolated `requests.get/post` calls when a script makes multiple consecutive calls to the same host domain to reuse connections and improve performance by ~2-3x.
