import datetime

from drf_pydantic import BaseModel

from .gender import Gender
from .address import Address


class User(BaseModel):
    customer_id: str
    first_name: str
    last_name: str
    gender: Gender
    created: datetime
    address: Address
    points: float
    last_activity: datetime