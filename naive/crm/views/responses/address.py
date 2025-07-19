from drf_pydantic import BaseModel
from pydantic import Field


class AddressDTO(BaseModel):
    street: str = Field(..., description="Street name")
    street_number: str = Field(..., description="Street number")
    city_code: str = Field(..., description="Postal/ZIP code")
    city: str = Field(..., description="City name")
    country: str = Field(..., description="Country name")

    class Config:
        schema_extra = {
            "example": {
                "street": "Main Street",
                "street_number": "123",
                "city_code": "10001",
                "city": "Linz",
                "country": "Austria",
            }
        }