from django.contrib import admin
from django.urls import path
from ..api_v1 import api_v1
from ..api_v2 import api_v2
from ninja import Swagger


NINJA_SWAGGER_SETTINGS = {
    "urls": [
        # Each entry is a new version in the dropdown
        {"name": "Version 1.0 (Latest)", "url": "/api/v1/schema.json"},
        {"name": "Version 2.0 (Latest)", "url": "/api/v2/schema.json"},
    ],
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/",api_v1.urls),
    path("api/v2/",api_v2.urls)
]
