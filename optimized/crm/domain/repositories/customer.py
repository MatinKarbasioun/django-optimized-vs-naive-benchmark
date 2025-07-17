from abc import ABC, abstractmethod
from typing import Optional, List

from django.db.models import Q, QuerySet

from crm.application.query import SortingSchema, Ordering, SortField
from crm.domain.entities import Customer


class ICustomerRepository(ABC):

    @abstractmethod
    async def find_by_id(self, user_id: int) -> Optional[Customer]:
        raise NotImplementedError()

    @abstractmethod
    async def find_by_customer_id(self, customer_id: str) -> Optional[Customer]:
        raise NotImplementedError

    @abstractmethod
    async def search(
            self,
            search_query: Q,
            sorting: Optional[SortField]=None,
            ordering: Optional[Ordering] = None
    ) -> QuerySet:
        raise NotImplementedError

    @abstractmethod
    async def add(self, customer: Customer) -> Customer:
        raise NotImplementedError

    @abstractmethod
    async def remove(self, customer_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def is_exist(self, customer_id: str) -> bool:
        raise NotImplementedError
