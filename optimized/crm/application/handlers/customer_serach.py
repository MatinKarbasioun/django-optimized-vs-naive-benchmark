import logging

from kink import inject

from crm.application.query.search_customer import SearchCustomersQuery
from crm.domain.repositories import ICustomerRepository
from crm.domain.exceptions import CustomerInvalidDataException
from crm.domain.value_objects import CustomerSearchOutput

logger = logging.getLogger(__name__)


@inject
class CustomerSearchHandler:

    def __init__(self, customer_repository: ICustomerRepository):
        self._customer_repository = customer_repository

    def handle(self, query: SearchCustomersQuery) -> CustomerSearchOutput:
        try:
            result = self._customer_repository.search(
                query.criteria,
                query.pagination,
                query.sorting
            )

            return result

        except Exception as e:
            msg = f'search customer raised error: {e}'
            logger.error(msg)
            raise CustomerInvalidDataException(msg)
