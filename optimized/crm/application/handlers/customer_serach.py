import logging

from django.db.models import QuerySet
from kink import inject

from crm.application.schemas import CustomerSearchQuery
from crm.domain.repositories import ICustomerRepository
from crm.domain.exceptions import CustomerInvalidDataException

logger = logging.getLogger(__name__)


@inject
class CustomerSearchHandler:

    def __init__(self, customer_repository: ICustomerRepository):
        self._customer_repository = customer_repository

    async def handle(self, query: CustomerSearchQuery) -> QuerySet:
        try:
            result = await self._customer_repository.search(
                query.query,
                query.sorting.sort_by,
                query.sorting.ordering
            )

            return result

        except Exception as e:
            msg = f'Search customer raised error: {e}'
            logger.error(msg)
            raise CustomerInvalidDataException(msg)
