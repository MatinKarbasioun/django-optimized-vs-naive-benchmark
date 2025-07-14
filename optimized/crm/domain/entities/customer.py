import datetime
from dataclasses import dataclass
from typing import Optional

from crm.domain.value_objects.gender import Gender
from . import *


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