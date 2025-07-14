from datetime import date

from drf_pydantic import BaseModel
from pydantic import Field, field_validator

from crm.domain.value_objects import Gender
from .address import AddressRequestDto

class CustomerRequestDto(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100, description="Customer's first name")
    last_name: str = Field(..., min_length=1, max_length=100, description="Customer's last name")
    gender: Gender = Field(..., description="Customer's gender")
    phone_number: str = Field(..., min_length=10, max_length=20, description="Contact phone number")
    birthday: date = Field(..., description="Customer's date of birth")
    address: AddressRequestDto
    initial_points: int = Field(..., description="Customer initial points")

    @classmethod
    @field_validator('birthday')
    def validate_birthday(cls, v):
        if v >= date.today():
            raise ValueError('Birthday cannot be in the future')

        return v

    @classmethod
    @field_validator('phone_number')
    def validate_phone_number(cls, v):
        import re

        phone_pattern = r'^[\+]?[1-9][\d\s\-\(\)]{8,}$'
        if not re.match(phone_pattern, v):
            raise ValueError('Invalid phone number format')

        return v

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Matin",
                "last_name": "Karbasioun",
                "gender": "M",
                "phone_number": "+1-555-123-4567",
                "birthday": "1990-01-15",
                "address": {
                    "street": "Main Street",
                    "street_number": "123",
                    "city_code": "10001",
                    "city": "Linz",
                    "country": "Austria",
                },
                "initial_points": 100
            }
        }