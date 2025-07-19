from django.http import JsonResponse
from django.views import View


class AppView(View):

    @classmethod
    def get(cls, request):
        return JsonResponse(
            {"status": "app is up and running",
             "docs": request.build_absolute_uri('/api/swagger')}
        )