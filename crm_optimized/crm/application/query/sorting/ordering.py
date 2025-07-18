from enum import Enum


class Ordering(str, Enum):
    ASCENDING = 'ascending'
    DESCENDING = 'descending'