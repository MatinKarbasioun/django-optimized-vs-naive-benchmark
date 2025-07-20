import functools
from django.core.cache import cache
from django.http import HttpRequest
import hashlib

def cache_view(timeout: int, key_prefix: str):

    def decorator(func):
        @functools.wraps(func)
        async def wrapper(request: HttpRequest, *args, **kwargs):
            query_params = request.GET.urlencode()
            raw_key = f"{request.path}:{query_params}"
            cache_key = f"{key_prefix}:{hashlib.md5(raw_key.encode()).hexdigest()}"

            cached_response = await cache.aget(cache_key)
            if cached_response:
                return cached_response

            response_data = await func(request, *args, **kwargs)

            await cache.aset(cache_key, response_data, timeout)

            return response_data
        return wrapper
    return decorator
