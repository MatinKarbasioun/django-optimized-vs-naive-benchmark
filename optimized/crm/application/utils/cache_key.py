import hashlib
from typing import Optional
from django.db.models import Q


def generate_cache_key(
        key: str,
        queries: Q,
        sorted_by: Optional[str],
        ordering: Optional[str],
        ) -> str:
    query_key = str(queries)
    sort_key = f"{sorted_by}:{ordering}" if sorted_by and ordering else ""
    raw_key = f"{query_key}:{sort_key}"
    return f"{key}:{hashlib.md5(raw_key.encode('utf-8')).hexdigest()}"