from typing import Optional

from ninja import ModelSchema, Schema, Field
from crm.infrastructure.models import AddressModel


class AddressSchema(ModelSchema):
    class Meta:
        model = AddressModel
        fields = ['city', 'country', 'street', 'street_number', 'city_code']
