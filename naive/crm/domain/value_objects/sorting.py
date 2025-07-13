from dataclasses import dataclass


@dataclass(frozen=True)
class SortingParams:
    field: str = "created"
    descending: bool = True

    ALLOWED_FIELDS = [
        "created", "first_name", "last_name", "birthday",
        "points", "last_activity", "city", "country"
    ]

    def __post_init__(self):
        if self.field not in self.ALLOWED_FIELDS:
            raise ValueError(f"Invalid sort field: {self.field}")