from typing import Optional

from django.db.models import Q

from crm.domain.entities import Customer
from crm.domain.repositories import ICustomerRepository
from crm.domain.value_objects import CustomerSearchOutput, SortingParams, PaginationParams, SearchParams
from crm.infrastructure.extensions import CustomerToModel, ModelToCustomer
from crm.infrastructure.models import AppUserModel
from shared.utils import handle_db_operation


class CustomerRepository(ICustomerRepository):

    def add(self, customer: Customer):
        model = customer @ CustomerToModel()
        handle_db_operation(lambda: model.save())
        customer.id = model.id

    def remove(self, customer_id: int) -> bool:
        result = handle_db_operation(lambda: AppUserModel.objects.get(id=customer_id).delete())
        return True if bool(result) else False

    def is_exist(self, customer_id: str) -> bool:
        return handle_db_operation(lambda: AppUserModel.objects.filter(customer_id=customer_id).exists())

    def find_by_id(self, customer_id: int) -> Optional[Customer]:
        return handle_db_operation(lambda: AppUserModel.objects.get(id=customer_id)) @ ModelToCustomer()

    def find_by_customer_id(self, customer_id: str) -> Optional[Customer]:
        return handle_db_operation(lambda: AppUserModel.objects.get(customer_id=customer_id)) @ ModelToCustomer()

    def search(
            self,
            criteria: SearchParams,
            pagination: PaginationParams,
            sorting: SortingParams
    ) -> CustomerSearchOutput:
        queryset = AppUserModel.objects.all()

        if criteria.query:
            queryset = queryset.filter(
                Q(first_name__icontains=criteria.query) |
                Q(last_name__icontains=criteria.query) |
                Q(customer_id__icontains=criteria.query) |
                Q(address__city__icontains=criteria.query)  # Causes join
            )

        if criteria.gender:
            queryset = queryset.filter(gender=criteria.gender.value)

        if criteria.city:
            queryset = queryset.filter(address__city__icontains=criteria.city)

        if criteria.country:
            queryset = queryset.filter(address__country__icontains=criteria.country)

        if criteria.min_points:
            queryset = queryset.filter(relationship__points__gte=criteria.min_points)

        if criteria.max_points:
            queryset = queryset.filter(relationship__points__lte=criteria.max_points)

        if criteria.has_relationship is not None:
            if criteria.has_relationship:
                queryset = queryset.filter(relationship__isnull=False)
            else:
                queryset = queryset.filter(relationship__isnull=True)

        if criteria.min_age or criteria.max_age:
            from datetime import date, timedelta
            today = date.today()

            if criteria.min_age:
                max_birth_date = today - timedelta(days=criteria.min_age * 365.25)
                queryset = queryset.filter(birthday__lte=max_birth_date)

            if criteria.max_age:
                min_birth_date = today - timedelta(days=criteria.max_age * 365.25)
                queryset = queryset.filter(birthday__gte=min_birth_date)

        sort_field = sorting.field

        match sort_field:
            case "points":
                sort_field = "relationship__points"

            case "last_activity":
                sort_field = "relationship__last_activity"

            case "city":
                sort_field = "address__city"

            case "country":
                sort_field = "address__country"


        if sorting.descending:
            sort_field = f"-{sort_field}"

        queryset = queryset.order_by(sort_field)

        total_count = queryset.count()

        offset = (pagination.page - 1) * pagination.per_page
        limit = pagination.per_page
        models = queryset[offset:offset + limit]

        customers = [model @ ModelToCustomer() for model in models]

        return CustomerSearchOutput(
            customers=customers,
            total_count=total_count,
            page=pagination.page,
            per_page=pagination.per_page
        )