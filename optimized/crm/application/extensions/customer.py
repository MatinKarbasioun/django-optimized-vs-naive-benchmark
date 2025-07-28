from crm.application.schemas import CreateCustomerCommand
from crm.domain.entities import Customer, CustomerRelationship
from crm.domain.service import generate_customer_id
from .address import SchemToAddress


class SchemaToCustomer:
    def __rmatmul__(self, customer: CreateCustomerCommand) -> Customer:
        return Customer(
            id=None,
            first_name=customer.first_name,
            last_name=customer.last_name,
            gender=customer.gender,
            customer_id=generate_customer_id(),
            birthday=customer.birthday,
            address=customer.address @ SchemToAddress() if customer.address else None,
            relationship=CustomerRelationship.create(customer.initial_points),
            created=None,
            last_updated=None
        )
