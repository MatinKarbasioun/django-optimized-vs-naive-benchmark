import datetime
from dataclasses import dataclass
from typing import Optional

from crm.domain.value_objects.gender import Gender
from .address import Address
from .relationship import CustomerRelationship


@dataclass
class Customer:
    id: Optional[int]
    first_name: str
    last_name: str
    gender: Gender
    customer_id: str
    birthday: datetime.date
    address: Optional[Address]
    relationship: Optional[CustomerRelationship]
    created: Optional[datetime]
    last_updated: Optional[datetime.datetime]
