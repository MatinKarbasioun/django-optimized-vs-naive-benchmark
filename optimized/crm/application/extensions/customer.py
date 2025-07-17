from crm.application.dtos.customer import CustomerResponse
from crm.domain.entities import Customer


class ToCustomerResponse:
    def __rmatmul__(self, customer: Customer) -> CustomerResponse:
        pass
