from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from crm_naive.app.app import AppView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('crm.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('', AppView.as_view(), name='app'),
]
