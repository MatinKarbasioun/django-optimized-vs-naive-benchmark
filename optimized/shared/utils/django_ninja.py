from django.http import HttpRequest, HttpResponse
from ninja import NinjaAPI, Swagger


class CustomNinjaAPI(NinjaAPI):
    apps_register = []

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        type(self).apps_register.append(self)


class CustomSwagger(Swagger):
    template_cdn = 'templates/swagger.html'
    default_settings = {
        'layout': 'StandaloneLayout',
        'deepLinking': True,
    }

    def render_page(
            self,
            request: HttpRequest,
            api: CustomNinjaAPI,
            **kwargs) -> HttpResponse:

        if 'urls' not in self.settings:
            self.settings['urls'] = [
                {
                    'url': obj.docs.get_openapi_url(obj, kwargs),
                    'name': obj.version,
                }
                for obj in api.apps_register
            ]
        return super().render_page(request=request, api=api, **kwargs)