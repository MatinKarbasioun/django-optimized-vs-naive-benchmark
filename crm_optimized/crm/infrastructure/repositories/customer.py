from typing import Optional

from django.core.cache import cache
from django.db.models import Q, QuerySet, Case, When

from crm.application.schemas.sorting import SortField, Ordering
from crm.application.utils import generate_cache_key
from crm.application.utils.app_settings import AppSettings
from crm.domain.entities import Customer
from crm.domain.repositories import ICustomerRepository
from crm.infrastructure.extensions import CustomerToModel, ModelToCustomer, ToPrefix, ToQuery
from crm.infrastructure.models import AppUserModel
from shared.utils import handle_db_operation


class CustomerRepository(ICustomerRepository):
    def __init__(self):
        self.__cache_key = AppSettings.APP_SETTINGS['cashing']['keys']['customer_cache']

    async def add(self, customer: Customer):
        model = customer @ CustomerToModel()
        await handle_db_operation(lambda: model.asave())
        customer.id = model.id
        customer.created = model.created
        customer.last_updated = model.last_updated

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
            'address', 'relationship'
        ).only(
            'id', 'first_name', 'last_name', 'gender', 'customer_id',
            'phone_number', 'created', 'birthday', 'address__street',
            'address__street_number', 'address__city',
            'address__city_code', 'address__country', 'relationship__points',
            'relationship__last_activity'
        )

        ordering_prefix = ordering @ ToPrefix()
        sorting_field = sorted_by @ ToQuery()
        ordering_field = f'{ordering_prefix}{sorting_field}'

        cached_key = generate_cache_key(self.__cache_key, queries, sorting_field, ordering_field)
        cached_pks = await cache.aget(cached_key)

        if cached_pks is not None:
            preserved_order = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(cached_pks)])
            return AppUserModel.objects.select_related('address', 'relationship').filter(
                pk__in=cached_pks
            ).order_by(preserved_order)

        if queries:
            queryset = queryset.filter(queries)

        queryset = queryset.order_by(f'{ordering_prefix}{sorting_field}')

        return queryset.cache(key=cached_key)
