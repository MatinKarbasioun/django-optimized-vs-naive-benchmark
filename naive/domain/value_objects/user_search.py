from dataclasses import dataclass
from typing import List

from domain import Customer


@dataclass(frozen=True)
class CustomerSearchOutput:
    customers: List[Customer]
    total_count: int
    page: int
    per_page: int

    @property
    def total_pages(self) -> int:
        return (self.total_count + self.per_page - 1) // self.per_page

    @property
    def has_next(self) -> bool:
        return self.page < self.total_pages

    @property
    def has_previous(self) -> bool:
        return self.page > 1