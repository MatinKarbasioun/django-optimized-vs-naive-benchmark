from typing import Optional

from django.db.models import Q, QuerySet

from crm.application.query import SortField, Ordering
from crm.domain.entities import Customer
from crm.domain.repositories import ICustomerRepository
from crm.infrastructure.extensions import CustomerToModel, ModelToCustomer, ToPrefix, ToQuery
from crm.infrastructure.models import AppUserModel
from shared.utils import handle_db_operation


class CustomerRepository(ICustomerRepository):

    async def add(self, customer: Customer):
        model = customer @ CustomerToModel()
        await handle_db_operation(lambda: model.asave())
        customer.id = model.id

    async def remove(self, customer_id: int) -> bool:
        result = await handle_db_operation(lambda: AppUserModel.objects.get(id=customer_id).adelete())
        return True if bool(result) else False

    async def is_exist(self, customer_id: str) -> bool:
        return await handle_db_operation(lambda: AppUserModel.objects.filter(customer_id=customer_id).aexists())

    async def find_by_id(self, customer_id: int) -> Optional[Customer]:
        return await handle_db_operation(lambda: AppUserModel.objects.aget(id=customer_id)) @ ModelToCustomer()

    async def find_by_customer_id(self, customer_id: str) -> Optional[Customer]:
        return await handle_db_operation(lambda: AppUserModel.objects.aget(customer_id=customer_id)) @ ModelToCustomer()

    async def search(
            self,
            queries: Q,
            sorted_by: Optional[SortField] = None,
            ordering: Optional[Ordering] = None
    ) -> QuerySet:
        queryset = AppUserModel.objects.select_related(
            'address',
            'relationship'  # Use 'relationship' as defined in related_name
        ).all()

        if queries:
            queryset = queryset.filter(queries)


        ordering_prefix = ordering @ ToPrefix()
        sorting_field = sorted_by @ ToQuery()

        if sorted_by == SortField.FULL_NAME:

            sorting_fields = [f'{ordering_prefix}last_name', f'{ordering_prefix}first_name']
            queryset = queryset.order_by(*sorting_fields)
        else:
            queryset = queryset.order_by(f'{ordering_prefix}{sorting_field}')

        return queryset
