# TODO: Implement your data models here
# Consider what data structures you'll need for:
# - Storing URL mappings
# - Tracking click counts
# - Managing URL metadata

import threading
from datetime import datetime

class URLStore:
    """Thread-safe in-memory store for URL mappings and analytics."""
    def __init__(self):
        self._lock = threading.Lock()
        self._data = {}  # short_code -> {"url": ..., "created_at": ..., "clicks": ...}

    def create(self, short_code: str, original_url: str):
        with self._lock:
            self._data[short_code] = {
                "url": original_url,
                "created_at": datetime.utcnow().isoformat(),
                "clicks": 0
            }

    def get(self, short_code: str):
        with self._lock:
            return self._data.get(short_code)

    def increment_clicks(self, short_code: str):
        with self._lock:
            if short_code in self._data:
                self._data[short_code]["clicks"] += 1

url_store = URLStore()
