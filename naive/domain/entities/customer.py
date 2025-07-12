import datetime
from dataclasses import dataclass
from typing import Optional

from domain.entities import Address, Gender, CustomerRelationship


@dataclass
class Customer:
    id: Optional[int]
    first_name: str
    last_name: str
    gender: Gender
    customer_id: str
    created: datetime
    address: Address
    birthday: datetime.date
    relationship: Optional[CustomerRelationship] = None