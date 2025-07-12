from typing import Optional

from kink import inject

from crm.application.command import CreateCustomerCommand
from crm.application.handlers.customer_create import CustomerCreationHandler
from crm.application.handlers.customer_serach import CustomerSearchHandler
from crm.application.query.search_customer import SearchCustomersQuery
from domain import Customer
from domain.repositories import ICustomerRepository
from domain.value_objects import CustomerSearchOutput


@inject
class CustomerService:
    def __init__(
            self,
            creation_handler: CustomerCreationHandler,
            search_handler: CustomerSearchHandler,
            customer_repository: ICustomerRepository
                 ):
        self._creation_handler = creation_handler
        self._search_handler = search_handler
        self._customer_repository = customer_repository

    def create_customer(self, command: CreateCustomerCommand) -> Customer:
        return self._creation_handler.handle(command)

    def get_customer_by_id(self, customer_id: int) -> Optional[Customer]:
        return self._customer_repository.find_by_id(customer_id)

    def search_customers(self, query: SearchCustomersQuery) -> CustomerSearchOutput:
        return self._search_handler.handle(query)
