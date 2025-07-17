from kink import di
from crm.domain.repositories import ICustomerRepository
from crm.infrastructure.repositories.customer import CustomerRepository


class Bootstrap:
    def __init__(self):
        self.__define_models()

    @classmethod
    def __define_models(cls):
        di.factories[ICustomerRepository] = lambda di_container: CustomerRepository()