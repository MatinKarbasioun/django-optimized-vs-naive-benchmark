import datetime
from typing import Optional

from django.contrib.postgres.search import SearchQuery
from django.db.models import Q
from ninja import Field, FilterSchema

from crm.domain.value_objects import Gender



class SearchFilter(FilterSchema):
    search: Optional[str] = None

    @classmethod
    def filter_search(cls, value: str) -> Q:
        if not value:
            return Q()

        query = SearchQuery(value, search_type='websearch')
        return Q(search_vector=query)