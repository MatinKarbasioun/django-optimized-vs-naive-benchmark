import time
from typing import Any, Optional, List

from django.db import connection, models
from django.db.models import QuerySet
from ninja import Schema, Field
from ninja_extra.pagination import PageNumberPagination

from shared.schemas import PerformanceSchema


class CustomPagination(PageNumberPagination):
    class Input(Schema):
        page: int = Field(1, ge=1, description="The page number to retrieve.")
        page_size: int = Field(20, ge=1, le=100, description="The number of items per page.")

    class Output(Schema):
        next: Optional[str] = None
        previous: Optional[str] = None
        results: List[Any]
        performance: PerformanceSchema

    items_attribute: str = "results"

    async def apaginate_queryset(self, queryset: QuerySet, pagination: Any, **params: Any) -> Any:
        request = params.get("request")

        start_time = time.perf_counter()
        start_queries = len(connection.queries)

        page_size = pagination.page_size
        page_number = pagination.page
        offset = (page_number - 1) * page_size

        items_to_fetch = page_size + 1

        if isinstance(queryset, models.QuerySet):
            items = [item async for item in queryset[offset: offset + items_to_fetch]]
        else:
            items = queryset[offset: offset + items_to_fetch]

        has_next = len(items) > page_size

        if has_next:
            items = items[:page_size]

        performance_data = {
            "execution_time_s": round((time.perf_counter() - start_time), 3),
            "query_count": len(connection.queries) - start_queries
        }

        next_url = None
        if has_next:
            next_params = request.GET.copy()
            next_params['page'] = page_number + 1
            next_url = request.build_absolute_uri(f"{request.path}?{next_params.urlencode()}")

        previous_url = None
        if page_number > 1:
            prev_params = request.GET.copy()
            prev_params['page'] = page_number - 1
            previous_url = request.build_absolute_uri(f"{request.path}?{prev_params.urlencode()}")

        return {
            "next": next_url,
            "previous": previous_url,
            "results": items,
            "performance": performance_data,
        }