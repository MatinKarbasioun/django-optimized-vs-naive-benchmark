from application.query.search_customer import SearchCustomersQuery
from domain.repositories import ICustomerRepository
from domain.value_objects import CustomerSearchOutput


class CustomerSearchHandler:

    def __init__(self, customer_repository: ICustomerRepository):
        self._customer_repository = customer_repository

    def handle(self, query: SearchCustomersQuery) -> CustomerSearchOutput:

        result = self._customer_repository.search(
            query.criteria,
            query.pagination,
            query.sorting
        )

        return result
