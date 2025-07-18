
from crm.presentation.views.customer import customer_router
from shared.utils import CustomNinjaAPI, CustomSwagger

api_v1 = CustomNinjaAPI(
    title="Optimized CRM API",
    description='Optimized CRM API with Medium Performance',
    docs=CustomSwagger(),
    docs_url='swagger',
    version="1.0.0",
)

api_v1.add_router("/customers/", customer_router, tags=["Customers"])
