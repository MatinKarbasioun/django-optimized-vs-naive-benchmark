import datetime
from typing import Optional

from ninja import Field, FilterSchema



class RelationshipFilter(FilterSchema):

    min_points: Optional[float] = Field(
        None, q='customer_relationships__points__gte',
        description="Users with at least this many points"
    )
    max_points: Optional[float] = Field(
        None, q='customer_relationships__points__lte',
        description="Users with at maximum this many points"
    )

    active_from: Optional[datetime.datetime] = Field(
        None,
        q='customer_relationships__last_activity__gte',
        description="Users active since this date"
    )

    active_before: Optional[datetime.datetime] = Field(
        None,
        q='customer_relationships__last_activity__gte',
        description="Users active since this date"
    )
