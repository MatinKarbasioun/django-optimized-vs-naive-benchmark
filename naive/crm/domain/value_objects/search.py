from datetime import datetime
from dataclasses import dataclass
from typing import Optional

from crm.domain.entities import Gender


@dataclass(frozen=True)
class SearchParams:
    query: Optional[str] = None
    gender: Optional[Gender] = None
    city: Optional[str] = None
    country: Optional[str] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    min_points: Optional[int] = None
    max_points: Optional[int] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    has_relationship: Optional[bool] = None