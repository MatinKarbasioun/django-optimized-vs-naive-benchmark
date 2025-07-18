import datetime
from typing import Optional

from django.contrib.postgres.search import SearchQuery
from django.db.models import Q
from ninja import Field, FilterSchema

from crm.domain.value_objects import Gender



class CustomerFilter(FilterSchema):
    search: Optional[str] = Field(
        None,
        q=[
            'first_name__icontains',
            'last_name__icontains',
            'customer_id__icontains',
            'phone_number__icontains',
            'address__street__icontains',
            'address__city__icontains',
            'address__country__icontains'
        ],
        expression_connector='OR',
        description="Search across name, customer ID, phone, address, city, and country"
    )

    first_name: Optional[str] = Field(None, q='first_name__icontains', description="Search by first name")
    last_name: Optional[str] = Field(None, q='last_name__icontains',description="Search by last name")

    customer_id: Optional[str] = Field(None, q='customer_id__icontains')
    phone_number: Optional[str] = Field(None, q='phone_number__icontains')

    gender: Optional[Gender] = None

    created_after: Optional[datetime.datetime] = Field(None, q='created__gte')
    created_before: Optional[datetime.datetime] = Field(None, q='created__lte')

    points_min: Optional[float] = Field(None, q='customer_relationships__points__gte')
    points_max: Optional[float] = Field(None, q='customer_relationships__points__lte')

    # Birthday range
    birthday_after: Optional[datetime.date] = Field(None, q='birthday__gte')
    birthday_before: Optional[datetime.date] = Field(None, q='birthday__lte')

    # Address filters
    country: Optional[str] = Field(None, q='address__country__icontains', description="e.g., Austria")
    city: Optional[str] = Field(None, q='address__city__icontains')
    city_code: Optional[str] = Field(None, q='address__city_code__icontains')
    street: Optional[str] = Field(None, q='address__street__icontains')
    street_number: Optional[str] = Field(None, q='address__street_number__icontains')

    # Activity filters
    has_relationship: Optional[bool] = None
    active_since: Optional[datetime.datetime] = Field(
        None,
        q='customer_relationships__last_activity__gte',
        description="Users active since this date"
    )

    min_points: Optional[int] = Field(
        None,
        q='customer_relationships__points__gte',
        description="Users with at least this many points"
    )

    location: Optional[str] = Field(
        None,
        q=['address__city__icontains', 'address__country__icontains'],
        description="Search by city or country"
    )

    @classmethod
    def filter_has_relationship(cls, value: bool) -> Q:
        return Q(customer_relationships__isnull=not value)

    @classmethod
    def filter_search(cls, value: str) -> Q:
        if not value:
            return Q()

        query = SearchQuery(value, search_type='websearch')
        return Q(search_vector=query)