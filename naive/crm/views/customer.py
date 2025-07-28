import time
from django.db import connection
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from drf_spectacular.utils import extend_schema

from crm.views.filters import CustomerFilter
from crm.views.serializers import CustomerSerializer
from crm.models import AppUserModel
from shared.utils import CustomPageNumberPagination


class CustomerViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    pagination_class = CustomPageNumberPagination
    filterset_class = CustomerFilter
    ordering_fields = '__all__'
    ordering = ['-created']
    search_fields = [
        'last_name', 'first_name', 'customer_id',
        'phone_number', 'birthday',
        'relationship__points', 'relationship__last_activity',
        'address__city_code', 'address__city', 'address__country',
        'address__street', 'address__street_number'
    ]

    def get_queryset(self):
        return AppUserModel.objects.all()

    @extend_schema(summary="List customers with filtering")
    def list(self, request, *args, **kwargs):
        start_time = time.perf_counter()
        start_queries = len(connection.queries)

        CustomerFilter(request.GET)
        response = super().list(request, *args, **kwargs)

        execution_time = round((time.perf_counter() - start_time), 3)
        query_count = len(connection.queries) - start_queries

        if isinstance(response.data, dict) and 'results' in response.data:
            response.data['performance'] = {
                'execution_time': f"{execution_time}s",
                'query_count': query_count,
                'total_records': response.data.get('count', 0)
            }

        return response
