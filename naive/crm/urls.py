from django.urls import path, include
from rest_framework.routers import DefaultRouter

from crm.views.customer import CustomerViewSet

router = DefaultRouter()
router.register(r'v1/customers', CustomerViewSet, basename='customers')

urlpatterns = [
    path('api', include(router.urls)),
]
