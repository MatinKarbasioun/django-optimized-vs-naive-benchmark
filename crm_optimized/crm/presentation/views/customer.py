from typing import List

from django.http import HttpResponse
from ninja import Router, Query
from ninja.errors import ValidationError
from ninja.pagination import paginate

from crm.application.extensions.customer import SchemaToCustomer
from crm.application.filters import CustomerFilter, AddressFilter, RelationshipFilter, SearchFilter
from crm.application.handlers import CustomerSearchHandler
from crm.application.schemas.sorting import SortingSchema
from crm.application.schemas import Customer, CreateCustomerSuccessfully, CreateCustomerCommand, CustomerSearchQuery
from crm.application.services.customer import CustomerService
from shared.utils.api.paginator import CustomPagination

customer_router = Router()


@customer_router.post('', response={200: CreateCustomerSuccessfully, 400: str})
async def create_customer(request, command: CreateCustomerCommand):
    try:
        service = CustomerService(CustomerSearchHandler())
        await service.create_customer(command @ SchemaToCustomer())
        return CreateCustomerSuccessfully(customer_id='test')

    except ValidationError as e:
        return HttpResponse(str(e), status=400)



@customer_router.get('', response={200: List[Customer]}, summary='search and filter customers')
@paginate(CustomPagination, page_size=20)
async def customers(
        request,
        sorting: Query[SortingSchema],
        search_filet: SearchFilter = Query(...),
        customer_filter: CustomerFilter = Query(...),
        address_filter: AddressFilter = Query(...),
        relationship_filter: RelationshipFilter = Query(...),
    ):
    service = CustomerService(CustomerSearchHandler())
    query = search_filet.get_filter_expression() & \
            customer_filter.get_filter_expression() & \
            address_filter.get_filter_expression() & \
            relationship_filter.get_filter_expression()
    return await service.search_customers(CustomerSearchQuery(
        query=query,
        sorting=sorting,
    ))
