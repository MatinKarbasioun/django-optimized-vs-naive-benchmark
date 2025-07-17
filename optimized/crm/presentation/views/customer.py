from ninja import Schema, Router, Query
from ninja.pagination import paginate, PageNumberPagination

from crm.application.dtos import CustomerSchema
from crm.application.filtters import CustomerFilter
from crm.application.handlers import CustomerSearchHandler
from crm.application.query import CustomerSearchQuery
from crm.application.query.sorting.Sorting import SortingSchema
from crm.application.services.customer import CustomerService

customer_router = Router()
#
# class PerformanceSchema(Schema):
#     execution_time: str
#     query_count: int
#
#
# class AddressSchema(Schema):
#     street: Optional[str]
#     street_number: Optional[str]
#     city: Optional[str]
#     country: Optional[str]
#
#
# class RelationshipSchema(Schema):
#     points: Optional[int]
#     created: Optional[datetime]
#     last_activity: Optional[datetime]
#
#
# class PaginatedCustomerResponse(Schema):
#     count: int
#     items: List[CustomerSchema]
#     performance: PerformanceSchema


@customer_router.get('/customers', response=list[CustomerSchema])
@paginate(PageNumberPagination, page_size=50)
async def customers(request, sorting: Query[SortingSchema], filters: CustomerFilter = Query(...)):
    service = CustomerService(CustomerSearchHandler())
    return await service.search_customers(CustomerSearchQuery(
        query=filters.get_filter_expression(),
        sorting=sorting,
    ))