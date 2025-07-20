import asyncio
import pytest
from ..fixtures import *
from django.urls import reverse, reverse_lazy
from django.core.cache import cache

VIEW_NAME = 'api-1.0.0:customers'


IN_MEMORY_CACHE = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}


pytestmark = [
    pytest.mark.django_db,
    pytest.mark.asyncio,
    pytest.mark.settings(CACHES=IN_MEMORY_CACHE)
]

async def test_search_query_is_cached(async_client, specific_users, mocker):

    url = reverse(VIEW_NAME)
    params = {"search": "Someone"}

    await cache.aclear()


    first_response = await async_client.get(url, params=params)
    assert first_response.status_code == 200
    assert len(first_response.json()['results']) == 1

    mocker.patch(
        'crm.models.AppUserModels.objects.all',
        side_effect=Exception("Database is down!")
    )

    second_response = await async_client.get(url, params=params)

    assert second_response.status_code == 200, "The second request should have been served from the cache"
    assert second_response.json() == first_response.json()