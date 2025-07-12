from drf_pydantic import BaseModel


class Address(BaseModel):
    street: str
    street_number: int
    city_code: int
    city: str
    country: str