from dataclasses import dataclass
from typing import List

from crm.domain.entities.customer import Customer


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

    @classmethod
    def failed(cls):
        return CustomerSearchOutput(
            customers=[],
            total_count=0,
            page=0,
            per_page=0,
        )