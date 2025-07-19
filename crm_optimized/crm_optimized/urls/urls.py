from django.contrib import admin
from django.urls import path
from ..api_v1 import api_v1
from ..app.view import app


NINJA_SWAGGER_SETTINGS = {
    "urls": [
        # Each entry is a new version in the dropdown
        {"name": "Version 1.0 (Latest)", "url": "/api/v1/schema.json"}
    ],
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/",api_v1.urls),
    path('', app, name="app"),
]
