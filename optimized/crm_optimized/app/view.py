from django.http import JsonResponse


async def app(request):
    return JsonResponse(
        {"status": "app is up and running",
         "docs": request.build_absolute_uri('/api/swagger')}
    )