from ninja import ModelSchema
from typing import Optional

from crm.infrastructure.models import AppUserModel
from .relationship import RelationshipSchema
from .address import AddressSchema


class CustomerSchema(ModelSchema):
    address: Optional[AddressSchema] = None
    relationship: Optional[RelationshipSchema] = None

    class Meta:
        model = AppUserModel
        fields = [
            'id', 'first_name', 'last_name', 'gender',
            'customer_id', 'phone_number', 'created', 'birthday',
            'address'
        ]