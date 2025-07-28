import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db

VIEW_NAME = 'customers-list'

@pytest.mark.benchmark(group="Initial Load")
def test_benchmark_initial_load(client, benchmark):
    url = reverse(VIEW_NAME)
    benchmark.pedantic(client.get, args=(url,), iterations=1, rounds=100)


@pytest.mark.benchmark(group="Filtering")
def test_benchmark_filtering(client, benchmark):
    url = reverse(VIEW_NAME) + '?first_name=John'
    benchmark.pedantic(client.get, args=(url,), iterations=1, rounds=100)


@pytest.mark.benchmark(group="Sorting")
def test_benchmark_sorting(client, benchmark):
    url = f"{reverse(VIEW_NAME)}?ordering=-points"
    benchmark.pedantic(client.get, args=(url,), iterations=1, rounds=100)