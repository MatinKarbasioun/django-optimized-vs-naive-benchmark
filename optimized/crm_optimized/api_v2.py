from ninja import NinjaAPI

from shared.utils import CustomNinjaAPI, CustomSwagger

api_v2 = CustomNinjaAPI(
    title="Optimized CRM API",
    description='Optimized CRM API with Medium Performance',
    docs=CustomSwagger(),
    docs_url='swagger',
    openapi_url='schema.json',
    version="2.0.0",
)