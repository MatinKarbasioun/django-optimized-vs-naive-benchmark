from drf_pydantic import BaseModel
from pydantic import Field


class AddressRequestDto(BaseModel):
    street: str = Field(..., min_length=1, max_length=255, description="Street name")
    street_number: str = Field(..., min_length=1, max_length=10, description="Street number")
    city_code: str = Field(..., min_length=1, max_length=10, description="Postal/ZIP code")
    city: str = Field(..., min_length=1, max_length=100, description="City name")
    country: str = Field(..., min_length=1, max_length=100, description="Country name")

    class Config:
        schema_extra = {
                "street": "Main Street",
                "street_number": "123",
                "city_code": "10001",
                "city": "Linz",
                "country": "Austria",
            }
