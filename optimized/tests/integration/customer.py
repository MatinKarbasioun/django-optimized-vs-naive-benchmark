import asyncio
import pytest
from ..fixtures import *
from django.urls import reverse, reverse_lazy

VIEW_NAME = 'api-1.0.0:customers'


pytestmark = [pytest.mark.django_db, pytest.mark.asyncio]


async def test_pagination_is_working(async_client, specific_users):
    url = f"{reverse(VIEW_NAME)}?page_size=2"
    response = await async_client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert 'results' in data
    assert len(data['results']) == 2
    assert data['next'] is not None

async def test_view_url_exists(async_client):
    url = reverse(VIEW_NAME)
    response = await async_client.get(url)
    assert response.status_code == 200

@pytest.mark.parametrize("filter_param, filter_value, expected_count", [
    ("first_name", "Some", 1),
    ("last_name", "Two", 1),
    ("gender", "male", 2),
    ("birthday_after", "1999-01-01", 1),
    ("birthday_before", "1985-01-01", 1),
    ("customer_id", "CUST-003", 1),
    ("phone_number", "+444", 1),
])
async def test_customers_filters(async_client, specific_users, filter_param, filter_value, expected_count):
    url = f"{reverse(VIEW_NAME)}?{filter_param}={filter_value}"
    response = await async_client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert len(data['results']) == expected_count, f"Filter {filter_param}={filter_value} failed"

@pytest.mark.parametrize("filter_param, filter_value, expected_count", [
    ("min_points", "200", 1),
    ("max_points", "75", 1),
    ("active_from", "2023-05-01", 1),
    ("active_before", "2023-01-01", 1),
])
async def test_relationships_filters(async_client, specific_users, filter_param, filter_value, expected_count):
    url = f"{reverse(VIEW_NAME)}?{filter_param}={filter_value}"
    response = await async_client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert len(data['results']) == expected_count, f"Filter {filter_param}={filter_value} failed"

@pytest.mark.parametrize("filter_param, filter_value, expected_count", [
    ("city", "Someplace", 2),
    ("country", "Testland", 3),
    ("street", "Main", 2),
    ("city_code", "54321", 1),
    ("street_number", "1", 2),
    ("has_address", "true", 3),
    ("has_address", "false", 1),
])
async def test_address_filters(async_client, specific_users, filter_param, filter_value, expected_count):
    url = f"{reverse(VIEW_NAME)}?{filter_param}={filter_value}"
    response = await async_client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert len(data['results']) == expected_count, f"Filter {filter_param}={filter_value} failed"

@pytest.mark.parametrize("search_term, expected_count", [
    ("Someone", 1),
    ("Three", 1),
    ("Someplace", 2),
    ("Anotherone Second", 1),
    ("Main Street", 2),
    ("Thirdperson Testland", 1),
    ("One & 12345", 1),
    ("12345", 2),
    ("Main Street Testland", 2),
    ("Main Street One", 1)
])
async def test_search_filter(async_client, specific_users, search_term, expected_count):
    url = f"{reverse(VIEW_NAME)}?search={search_term}"
    response = await async_client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert len(data['results']) == expected_count, f"Search for '{search_term}' failed"


async def test_combined_filters(async_client, specific_users):
    url = f"{reverse(VIEW_NAME)}?city=Someplace&min_points=90&max_points=150"
    response = await async_client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert len(data['results']) == 1
    assert data['results'][0]['first_name'] == 'Someone'

@pytest.mark.parametrize("country, sort_by, ordering, expected_first_name", [
    ("Testland","first_name", "ascending", "Anotherone"),
    ("Testland","first_name", "descending", "Thirdperson"),
    ("Testland","last_name", "ascending","Someone"),
    ("Testland","last_name", "descending","Anotherone"),
    ("Testland","points", "ascending", "Thirdperson"),
    ("Testland","points", "descending", "Anotherone")
])
async def test_sorting(async_client, specific_users, country, sort_by, ordering, expected_first_name):
    url = f"{reverse(VIEW_NAME)}?country={country}&sort_by={sort_by}&ordering={ordering}"
    response = await async_client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert len(data['results']) == 3
    assert data['results'][0]['first_name'] == expected_first_name

async def test_search_vector_is_not_null_for_all_users(specific_users):
    # Act: Fetch all users from the database.
    all_users = [user async for user in AppUserModel.objects.all()]

    # Assert
    assert len(all_users) == 4 # Ensure we have the correct number of users to check
    for user in all_users:
        assert user.search_vector is not None, f"User {user.pk} has a NULL search_vector"

async def test_search_vector_on_user_creation():

    # Arrange
    address = await AddressModel.objects.acreate(city="VectorCity", street="Signal Street")
    user = await AppUserModel.objects.acreate(
        first_name="Vector", last_name="Test", address=address
    )

    #Act
    user_from_db = await AppUserModel.objects.aget(pk=user.pk)

    #Assert
    assert user_from_db.search_vector is not None