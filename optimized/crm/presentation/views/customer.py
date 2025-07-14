import time
from django.db import connection
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from drf_spectacular.utils import extend_schema

from ..filtters import CustomerFilter
from ..serializers import CustomerSerializer
from ...infrastructure.models import AppUserModel



class CustomerViewSet(viewsets.List):

    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CustomerFilter
    ordering_fields = '__all__'
    search_fields = '__all__'

    def get_queryset(self):
        return AppUserModel.objects.select_related(
            'address', 'relationship'
        ).only(
            'id', 'first_name', 'last_name', 'gender', 'customer_id',
            'phone_number', 'created', 'birthday', 'last_updated',
            'address__street', 'address__street_number', 'address__city',
            'address__country', 'relationship__points', 'relationship__created',
            'relationship__last_activity'
        )

    @extend_schema(summary="List customers with filtering")
    def list(self, request, *args, **kwargs):
        start_time = time.time()
        queries_before = len(connection.queries)

        response = super().list(request, *args, **kwargs)

        # Add performance metrics
        execution_time = time.time() - start_time
        query_count = len(connection.queries) - queries_before

        if isinstance(response.data, dict) and 'results' in response.data:
            response.data['performance'] = {
                'execution_time': f"{execution_time:.3f}s",
                'query_count': query_count,
                'total_records': response.data.get('count', 0)
            }

        return response
