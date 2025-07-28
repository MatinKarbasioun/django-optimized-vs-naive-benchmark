from crm.application.schemas.sorting import SortField


class ToQuery:
    def __init__(self):
        self._map = {
            SortField.FIRST_NAME: 'first_name',
            SortField.LAST_NAME: 'last_name',
            SortField.CREATED: 'created',
            SortField.LAST_UPDATED: 'last_updated',
            SortField.CUSTOMER_ID: 'customer_id',
            SortField.POINTS: 'relationship__points',
            SortField.LAST_ACTIVITY: 'relationship__last_activity',
            SortField.CITY: 'address__city',
            SortField.COUNTRY: 'address__country'
        }

    def __rmatmul__(self, sort_field: SortField):
        return self._map.get(sort_field, 'created')
