import datetime
from dataclasses import dataclass
from typing import Optional

from .address import Address
from .relationship import CustomerRelationship
from .gender import Gender


@dataclass
class Customer:
    id: Optional[int]
    first_name: str
    last_name: str
    gender: Gender
    customer_id: str
    created: datetime
    birthday: datetime.date
    address: Optional[Address] = None
    relationship: Optional[CustomerRelationship] = None