import datetime
import re
from typing import Optional

from django.contrib.postgres.search import SearchQuery
from django.db.models import Q
from ninja import Field, FilterSchema

from crm.domain.value_objects import Gender



class SearchFilter(FilterSchema):
    search: Optional[str] = None

    def filter_search(self, value: str) -> Q:
        if not value:
            return Q()

        query = Q(search_vector=SearchQuery(value, search_type='websearch'))

        numeric_part = re.sub(r'\D', '', self.search)

        if numeric_part:
            numeric_query = (
                    Q(phone_number__icontains=numeric_part) |
                    Q(address__city_code__icontains=numeric_part) |
                    Q(address__street_number__icontains=numeric_part)
            )
            query |= numeric_query

        return query