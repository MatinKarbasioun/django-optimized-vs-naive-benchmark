from abc import ABC, abstractmethod
from typing import List, Optional

from domain import Customer
from domain.value_objects import SearchParams, PaginationParams, SortingParams, CustomerSearchOutput


class ICustomerRepository(ABC):

    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[Customer]:
        raise NotImplementedError()

    @abstractmethod
    def find_by_customer_id(self, customer_id: str) -> Optional[Customer]:
        raise NotImplementedError

    @abstractmethod
    def search(
            self,
            criteria: SearchParams,
            pagination: PaginationParams,
            sorting: SortingParams
    ) -> CustomerSearchOutput:
        raise NotImplementedError

    @abstractmethod
    def add(self, customer: Customer) -> Customer:
        raise NotImplementedError

    @abstractmethod
    def remove(self, customer_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_exist(self, customer_id: str) -> bool:
        raise NotImplementedError
