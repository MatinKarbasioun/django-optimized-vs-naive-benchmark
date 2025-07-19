from datetime import datetime
from dataclasses import dataclass
from typing import Optional



@dataclass
class CustomerRelationship:
    id: Optional[int]
    points: float
    created: Optional[datetime]
    last_activity: Optional[datetime]

    @classmethod
    def create(cls, initial_points=0):
        return cls(
            id=None,
            points=initial_points,
            created=None,
            last_activity=None
        )
