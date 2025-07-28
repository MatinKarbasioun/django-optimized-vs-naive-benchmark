import datetime
from typing import Optional

from django.contrib.postgres.search import SearchQuery
from django.db.models import Q
from ninja import Field, FilterSchema

from crm.domain.value_objects import Gender



class AddressFilter(FilterSchema):
    country: Optional[str] = Field(None, q='address__country__icontains')
    city: Optional[str] = Field(None, q='address__city__icontains')
    city_code: Optional[str] = Field(None, q='address__city_code__icontains')
    street: Optional[str] = Field(None, q='address__street__icontains')
    street_number: Optional[str] = Field(None, q='address__street_number__icontains')
    has_address: Optional[bool] = None

    @classmethod
    def filter_has_address(cls, value: bool) -> Q:
        return Q(address__isnull=not value)

    @classmethod
    def filter_search(cls, value: str) -> Q:
        if not value:
            return Q()

        query = SearchQuery(value, search_type='websearch')
        return Q(search_vector=query)