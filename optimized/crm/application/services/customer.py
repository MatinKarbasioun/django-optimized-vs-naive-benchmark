from typing import Optional

from django.db.models import QuerySet
from kink import inject

from crm.application.dtos import PaginatedResult, CustomerSchema
from crm.application.handlers.customer_serach import CustomerSearchHandler
from crm.application.query import CustomerSearchQuery
from crm.domain.repositories import ICustomerRepository


@inject
class CustomerService:
    def __init__(
            self,
            search_handler: CustomerSearchHandler,
            customer_repository: ICustomerRepository):
        self._customer_repo = customer_repository
        self._search_handler = search_handler

    def get_customer_by_id(self, customer_id: int) -> Optional[CustomerSchema]:
        return self._customer_repo.find_by_id(customer_id)

    async def search_customers(self, query: CustomerSearchQuery) -> QuerySet:
        return await self._search_handler.handle(query)
