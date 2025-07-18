from enum import Enum


class SortField(str, Enum):
    FULL_NAME = "full_name"
    FIRST_NAME = 'first_name'
    LAST_NAME = 'last_name'
    CREATED = 'created'
    CUSTOMER_ID = 'customer_id'
    CITY = 'city'
    COUNTRY = 'country'
    POINTS = 'points'
    LAST_ACTIVITY = 'last_activity'


    def __hash__(self):
        return hash(self.value)