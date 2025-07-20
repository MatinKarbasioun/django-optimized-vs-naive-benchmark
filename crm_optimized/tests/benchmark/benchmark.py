import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db

VIEW_NAME = 'api-1.0.0:customers'

@pytest.mark.benchmark(group="Initial Load")
async def test_benchmark_initial_load(async_client, benchmark):
    url = reverse(VIEW_NAME)
    await benchmark.pedantic(async_client.get, args=(url,), iterations=1, rounds=100)


@pytest.mark.benchmark(group="Filtering")
async def test_benchmark_filtering(async_client, benchmark):
    url = reverse(VIEW_NAME) + '?first_name=John'
    await benchmark.pedantic(async_client.get, args=(url,), iterations=1, rounds=100)


@pytest.mark.benchmark(group="Sorting")
async def test_benchmark_sorting(async_client, benchmark):
    url = f"{reverse(VIEW_NAME)}?field=points&ordering=descending"
    await benchmark.pedantic(async_client.get, args=(url,), iterations=1, rounds=100)