from dataclasses import dataclass
from datetime import date

from domain import Gender
from .address import CreateAddressCommand


@dataclass
class CreateCustomerCommand:
    first_name: str
    last_name: str
    gender: Gender
    customer_id: str
    phone_number: str
    birthday: date
    address: CreateAddressCommand
    initial_points: int = 0
