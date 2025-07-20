import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db

VIEW_NAME = 'customers'

@pytest.mark.benchmark(group="Initial Load")
def test_benchmark_initial_load(async_client, benchmark):
    url = reverse(VIEW_NAME)
    benchmark.pedantic(async_client.get, args=(url,), iterations=1, rounds=100)


@pytest.mark.benchmark(group="Filtering")
def test_benchmark_filtering(async_client, benchmark):
    url = reverse(VIEW_NAME) + '?first_name=John'
    benchmark.pedantic(async_client.get, args=(url,), iterations=1, rounds=100)


@pytest.mark.benchmark(group="Sorting")
def test_benchmark_sorting(async_client, benchmark):
    url = f"{reverse(VIEW_NAME)}?field=points&ordering=descending"
    benchmark.pedantic(async_client.get, args=(url,), iterations=1, rounds=100)