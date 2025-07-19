import datetime

from ninja import ModelSchema, Schema, Field
from typing import Optional

from crm.infrastructure.models import AppUserModel
from .relationship import RelationshipSchema
from .address import AddressSchema
from ...domain.value_objects import Gender


class Customer(ModelSchema):
    address: Optional[AddressSchema] = None
    relationship: Optional[RelationshipSchema] = None

    class Meta:
        model = AppUserModel
        fields = [
            'id', 'first_name', 'last_name', 'gender',
            'customer_id', 'phone_number', 'created', 'birthday',
            'address'
        ]




class CreateCustomerSuccessfully(Schema):
    customer_id: str


class CreateCustomerCommand(Schema):
    first_name: str
    last_name: str
    gender: Gender = Field(Gender.UNDEFINED)
    phone_number: str = Field(..., pattern=r'^\+?[1-9]\d{7,14}$')
    birthday: datetime.date = Field(..., examples=["2024-11-10"])
    address: Optional[AddressSchema] = Field(None)
    initial_points: Optional[int] = Field(default=0)


