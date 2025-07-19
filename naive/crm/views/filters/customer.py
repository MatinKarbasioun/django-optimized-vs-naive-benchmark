import datetime

import django_filters
from django_filters import BooleanFilter

from crm.models import AppUserModel
from shared.contract import Gender


class CustomerFilter(django_filters.FilterSet):
    first_name = django_filters.ChoiceFilter(field_name='first_name', lookup_expr='icontains')
    last_name = django_filters.ChoiceFilter(field_name='first_name', lookup_expr='icontains')
    gender = django_filters.ChoiceFilter(choices=Gender.choices())
    customer_id = django_filters.CharFilter(field_name='customer_id', lookup_expr='icontains')
    phone_number = django_filters.CharFilter(field_name='phone_number', lookup_expr='icontains')
    birthday = django_filters.IsoDateTimeFromToRangeFilter(
        field_name='birthday',
        help_text=str(datetime.datetime.now().date().isoformat())
    )
    created = django_filters.IsoDateTimeFromToRangeFilter(
        field_name='created',
        help_text=str(datetime.datetime.now().isoformat())
    )
    last_updated = django_filters.IsoDateTimeFromToRangeFilter(
        field_name='last_updated',
        help_text=str(datetime.datetime.now().isoformat())
    )
    country = django_filters.CharFilter(field_name='address__country', lookup_expr='icontains', help_text='Austria')
    city = django_filters.CharFilter(field_name='address__city', lookup_expr='icontains')
    city_code = django_filters.CharFilter(field_name='address__city_code', lookup_expr='icontains')
    street = django_filters.CharFilter(field_name='address__street', lookup_expr='icontains')
    street_number = django_filters.CharFilter(field_name='address__street_number', lookup_expr='icontains')
    has_address = BooleanFilter(field_name='address', method='filter_has_address')

    points = django_filters.NumericRangeFilter(field_name='relationship__points')
    class Meta:
        model = AppUserModel
        fields = ['street_number', 'street', 'city_code', 'country', 'city', 'points']

    @classmethod
    def filter_has_address(cls, queryset, name, value):
        if value is None:
            return queryset
        if value:
            return queryset.filter(addresss__isnull=False)
        return queryset.filter(addresss__isnull=True)