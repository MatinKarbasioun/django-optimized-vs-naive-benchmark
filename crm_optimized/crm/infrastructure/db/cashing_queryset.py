import logging

from django.db import models
from django.core.cache import cache


logger = logging.getLogger(__name__)

class CachingQuerySet(models.QuerySet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cache_key = None
        self._cache_timeout = 300  # Default 15 minutes

    def _clone(self):
        clone = super()._clone()
        clone._cache_key = self._cache_key
        clone._cache_timeout = self._cache_timeout
        return clone

    def cache(self, key: str, timeout: int = 900):
        clone = self._clone()
        clone._cache_key = key
        clone._cache_timeout = timeout
        return clone

    async def __aiter__(self):
        if self._cache_key is None:
            async for item in super().__aiter__():
                yield item
            return

        logger.info(f"cash key: {self._cache_key}")
        results = []
        primary_keys = []
        async for item in super().__aiter__():
            results.append(item)
            primary_keys.append(item.pk)
            yield item

        await cache.aset(self._cache_key, primary_keys, timeout=self._cache_timeout)
        logger.info(f"cash hit {len(primary_keys)}.")