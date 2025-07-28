
from crm.controller.customer import CustomerController
from shared.utils import CustomNinjaAPI, CustomSwagger

api_v1 = CustomNinjaAPI(
    title="Optimized CRM API",
    description='Optimized CRM API with Medium Performance',
    docs=CustomSwagger(),
    docs_url='swagger/',
    version="1.0.0",
)

api_v1.register_controllers(CustomerController)
