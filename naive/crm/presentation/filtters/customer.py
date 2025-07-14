import datetime

import django_filters
from django.db import models

from crm.infrastructure.models import AppUserModel


class CustomerFilter(django_filters.FilterSet):
    gender = django_filters.ChoiceFilter(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    customer_id = django_filters.CharFilter(field_name='customer_id', lookup_expr='icontains')
    phone_number = django_filters.CharFilter(field_name='phone_number', lookup_expr='icontains')
    has_relationship = django_filters.BooleanFilter(field_name='relationship', method='filter_has_relationship')
    created = django_filters.IsoDateTimeFromToRangeFilter(
        field_name='created',
        help_text=str(datetime.datetime.now().isoformat())
    )
    points = django_filters.NumericRangeFilter(field_name='relationship__points')
    country = django_filters.CharFilter(field_name='address__country', lookup_expr='icontains', help_text='Austria')
    city = django_filters.CharFilter(field_name='address__city', lookup_expr='icontains')
    city_code = django_filters.CharFilter(field_name='address__city_code', lookup_expr='icontains')
    street = django_filters.CharFilter(field_name='address__street', lookup_expr='icontains')
    street_number = django_filters.CharFilter(field_name='address__street_num', lookup_expr='icontains')
    birthday = django_filters.IsoDateTimeFromToRangeFilter(
        field_name='birthday',
        help_text=str(datetime.datetime.now().date().isoformat())
    )

    class Meta:
        model = AppUserModel
        fields = ['street_number', 'street', 'city_code', 'country', 'city', 'has_relationship']

    @classmethod
    def filter_has_relationship(cls, queryset, name, value):
        if value is None:
            return queryset
        if value:
            return queryset.filter(relationship__isnull=False)
        return queryset.filter(relationship__isnull=True)