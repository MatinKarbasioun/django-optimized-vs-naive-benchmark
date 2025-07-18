from typing import Optional

from ninja import Field, Schema

from .fields import SortField
from .ordering import Ordering


class SortingSchema(Schema):
    sort_by: Optional[SortField] = Field(default=SortField.CREATED)
    ordering: Optional[Ordering] = Field(default=Ordering.DESCENDING)