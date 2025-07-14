from dataclasses import dataclass


@dataclass(frozen=True)
class PaginationParams:
    page: int = 1
    per_page: int = 50
