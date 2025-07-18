from dataclasses import dataclass
from typing import Optional


@dataclass
class Address:
    id: Optional[int]
    street: str
    street_number: str
    city_code: str
    city: str
    country: str

