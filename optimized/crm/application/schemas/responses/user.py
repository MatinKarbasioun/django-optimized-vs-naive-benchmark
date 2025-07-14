import datetime

from drf_pydantic import BaseModel

from .gender import Gender
from .address import AddressDTO


class UserDTO(BaseModel):
    customer_id: str
    first_name: str
    last_name: str
    gender: Gender
    created: datetime
    address: AddressDTO
    points: float
    last_activity: datetime