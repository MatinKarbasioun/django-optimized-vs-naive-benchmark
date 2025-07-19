from crm.application.schemas.sorting import SortField


class ToQuery:
    def __init__(self):
        self._map = {
            SortField.FIRST_NAME: 'first_name',
            SortField.LAST_NAME: 'last_name',
            SortField.CREATED: 'created',
            SortField.CUSTOMER_ID: 'customer_id',
            SortField.POINTS: 'customer_relationships__points',
            SortField.LAST_ACTIVITY: 'customer_relationships__last_activity',
            SortField.CITY: 'address__city',
            SortField.COUNTRY: 'address__country',
            SortField.FULL_NAME: ['first_name', 'last_name']

        }

    def __rmatmul__(self, sort_field: SortField):
        return self._map.get(sort_field, 'created')
