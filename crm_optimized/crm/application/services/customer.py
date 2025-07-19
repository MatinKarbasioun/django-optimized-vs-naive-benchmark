from typing import Optional

from django.db.models import QuerySet
from kink import inject

from crm.application.schemas import Customer
from crm.application.handlers.customer_serach import CustomerSearchHandler
from crm.application.schemas import CustomerSearchQuery
from crm.domain.entities import Customer
from crm.domain.repositories import ICustomerRepository, IAddressRepository, ICustomerRelationshipRepository
from shared.utils import AsyncAtomicContextManager


@inject
class CustomerService:
    def __init__(
            self,
            search_handler: CustomerSearchHandler,
            customer_repository: ICustomerRepository,
            address_repository: IAddressRepository,
            relationship_repository: ICustomerRelationshipRepository
    ):
        self._customer_repo = customer_repository
        self._address_repo = address_repository
        self._relationship_repo = relationship_repository
        self._search_handler = search_handler

    async def create_customer(self, customer: Customer):
        async with AsyncAtomicContextManager():
            if customer.address:
                await self._address_repo.add(customer.address)

            await self._customer_repo.add(customer)
            await self._relationship_repo.add(customer.id, customer.relationship)


    async def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        return await self._customer_repo.find_by_id(customer_id)

    async def search_customers(self, query: CustomerSearchQuery) -> QuerySet:
        return await self._search_handler.handle(query)
