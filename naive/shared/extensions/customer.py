import uuid
from datetime import datetime

from crm.application.command import CreateCustomerCommand
from domain import Customer, Address


class CommandToCustomer:
    def __init__(self, address: Address):
        self._address = address

    def __rmatmul__(self, customer_command: CreateCustomerCommand) -> Customer:
        return Customer(
            id=None,
            first_name=customer_command.first_name,
            last_name=customer_command.last_name,
            gender=customer_command.gender,
            customer_id=str(uuid.uuid4()),
            created=datetime.now(),
            address=self._address,
            birthday=customer_command.birthday
        )