from typing import List

from django.http import HttpResponse
from kink import inject
from ninja import Query, Body
from ninja.constants import NOT_SET
from ninja.errors import ValidationError
from ninja_extra.pagination import paginate
from ninja_extra import api_controller, route

from crm.application.extensions.customer import SchemaToCustomer
from crm.application.filters import (
    CustomerFilter,
    AddressFilter,
    RelationshipFilter,
    SearchFilter
)
from crm.application.handlers import CustomerSearchHandler
from crm.application.schemas.customer import PaginatedCustomerResponse
from crm.application.schemas.sorting import SortingSchema
from crm.application.schemas import (
    Customer,
    CreateCustomerSuccessfully,
    CreateCustomerCommand,
    CustomerSearchQuery
)
from crm.application.services.customer import CustomerService
from shared.utils.api.paginator import CustomPagination



@api_controller("/customers", tags=["Customers"], auth=NOT_SET, permissions=[])
@inject
class CustomerController:
    def __init__(self, service: CustomerService):
        self._service = service

    @route.post('', response={200: CreateCustomerSuccessfully, 400: str})
    async def create_customer(self, command: CreateCustomerCommand = Body(...)):
        try:

            await self._service.create_customer(command @ SchemaToCustomer())
            return CreateCustomerSuccessfully(customer_id='test')

        except ValidationError as e:
            return HttpResponse(str(e), status=400)


    @route.get(
        '',
        response={200: PaginatedCustomerResponse},
        summary='search and filter customers',
        url_name="customers"
    )
    @paginate(CustomPagination, page_size=20)
    async def customers(
            self,
            sorting: Query[SortingSchema],
            search_filet: SearchFilter = Query(...),
            customer_filter: CustomerFilter = Query(...),
            address_filter: AddressFilter = Query(...),
            relationship_filter: RelationshipFilter = Query(...),
        ):
        query = search_filet.get_filter_expression() & \
                customer_filter.get_filter_expression() & \
                address_filter.get_filter_expression() & \
                relationship_filter.get_filter_expression()
        return await self._service.search_customers(CustomerSearchQuery(
            query=query,
            sorting=sorting,
        ))
