import hashlib
from typing import Optional
from django.db.models import Q


def generate_cache_key(
        queries: Q,
        sorted_by: Optional[str] = None,
        ordering: Optional[str] = None
        ) -> str:
    query_key = str(queries)
    sort_key = f"{sorted_by}:{ordering}" if sorted_by and ordering else ""
    raw_key = f"{query_key}:{sort_key}"
    return f"customer_search:{hashlib.md5(raw_key.encode('utf-8')).hexdigest()}"