from ninja import Router, Query
from ninja.pagination import paginate, PageNumberPagination

from crm.application.dtos import CustomerSchema
from crm.application.filtters import CustomerFilter
from crm.application.handlers import CustomerSearchHandler
from crm.application.query import CustomerSearchQuery
from crm.application.query.sorting.Sorting import SortingSchema
from crm.application.services.customer import CustomerService
from shared.utils.paginator import CustomPagination

customer_router = Router()


@customer_router.get('/customers', response=list[CustomerSchema])
@paginate(CustomPagination, page_size=20)
async def customers(request, sorting: Query[SortingSchema], filters: CustomerFilter = Query(...)):
    service = CustomerService(CustomerSearchHandler())
    return await service.search_customers(CustomerSearchQuery(
        query=filters.get_filter_expression(),
        sorting=sorting,
    ))