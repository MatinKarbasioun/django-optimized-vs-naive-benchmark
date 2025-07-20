from datetime import date, timezone, datetime
import asyncio
import pytest_asyncio

from crm.domain.value_objects import Gender
from crm.infrastructure.models import AddressModel, AppUserModel, CustomerRelationshipModel


@pytest_asyncio.fixture(scope="module")
async def specific_users(django_db_setup, django_db_blocker):

    with django_db_blocker.unblock():
        address1 = await AddressModel.objects.acreate(
            street="Main Street", street_number="1", city="Someplace",
            city_code="12345", country="Testland"
        )
        address2 = await AddressModel.objects.acreate(
            street="Second Avenue", street_number="2", city="Anotherplace",
            city_code="54321", country="Testland"
        )

        # User 1
        user1 = await AppUserModel.objects.acreate(
            first_name="Someone", last_name="One", gender=Gender.FEMALE,
            birthday=date(2000, 1, 1), address=address1,
            customer_id="CUST-001", phone_number="+111111111"
        )
        await CustomerRelationshipModel.objects.acreate(
            appuser=user1, points=100, last_activity=datetime(2023, 1, 15, tzinfo=timezone.utc)
        )

        # User 2
        user2 = await AppUserModel.objects.acreate(
            first_name="Anotherone", last_name="Two", gender=Gender.MALE,
            birthday=date(1990, 5, 20), address=address2,
            customer_id="CUST-002", phone_number="+222222222"
        )
        await CustomerRelationshipModel.objects.acreate(
            appuser=user2, points=250, last_activity=datetime(2023, 6, 20, tzinfo=timezone.utc)
        )

        # User 3
        user3 = await AppUserModel.objects.acreate(
            first_name="Thirdperson", last_name="Three", gender=Gender.UNDEFINED,
            birthday=date(1980, 10, 25), address=address1,
            customer_id="CUST-003", phone_number="+333333333"
        )
        await CustomerRelationshipModel.objects.acreate(
            appuser=user3, points=50, last_activity=datetime(2022, 12, 1, tzinfo=timezone.utc)
        )

        # User 4
        await AppUserModel.objects.acreate(
            first_name="NoAddressPerson", last_name="Four", gender=Gender.MALE,
            birthday=date(1995, 2, 2), address=None,
            customer_id="CUST-004", phone_number="+444444444"
        )