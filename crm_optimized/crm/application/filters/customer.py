import datetime
from typing import Optional
from ninja import Field, FilterSchema
from crm.domain.value_objects import Gender



class CustomerFilter(FilterSchema):
    first_name: Optional[str] = Field(None, q='first_name__icontains')
    last_name: Optional[str] = Field(None, q='last_name__icontains')

    customer_id: Optional[str] = Field(None, q='customer_id__icontains')
    phone_number: Optional[str] = Field(None, q='phone_number__icontains')

    gender: Optional[Gender] = None

    # Birthday range
    birthday_after: Optional[datetime.date] = Field(None, q='birthday__gte')
    birthday_before: Optional[datetime.date] = Field(None, q='birthday__lte')

    created_after: Optional[datetime.datetime] = Field(None, q='created__gte')
    created_before: Optional[datetime.datetime] = Field(None, q='created__lte')

    last_update_after: Optional[datetime.datetime] = Field(None, q='last_update__gte')
    last_update__before: Optional[datetime.datetime] = Field(None, q='last_update_lte')