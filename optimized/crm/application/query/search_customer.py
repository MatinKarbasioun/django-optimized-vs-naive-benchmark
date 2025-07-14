from dataclasses import dataclass

from crm.domain.value_objects import SearchParams, PaginationParams, SortingParams


@dataclass(frozen=True)
class SearchCustomersQuery:
    criteria: SearchParams
    pagination: PaginationParams
    sorting: SortingParams