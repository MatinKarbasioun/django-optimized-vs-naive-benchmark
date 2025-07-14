from datetime import datetime
from dataclasses import dataclass
from typing import Optional



@dataclass
class CustomerRelationship:
    id: Optional[int]
    points: float
    created: datetime
    last_activity: datetime

    @classmethod
    def create(cls, initial_points=0):
        return cls(
            id=None,
            points=initial_points,
            created=datetime.now(),
            last_activity=datetime.now()
        )
