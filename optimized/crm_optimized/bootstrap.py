from kink import di

from crm.application.handlers import CustomerSearchHandler
from crm.application.services.customer import CustomerService
from crm.application.utils.app_settings import AppSettings
from crm.domain.repositories import ICustomerRepository, IAddressRepository, ICustomerRelationshipRepository
from crm.infrastructure.repositories import *


class Bootstrap:
    def __init__(self):
        AppSettings()
        self.__define_repositories()
        self.__define_services()

    @classmethod
    def __define_repositories(cls):
        di.factories[ICustomerRepository] = lambda di_container: CustomerRepository()
        di.factories[IAddressRepository] = lambda di_container: AddressRepository()
        di.factories[ICustomerRelationshipRepository] = lambda di_container: CustomerRelationshipRepository()

    @classmethod
    def __define_services(cls):
        di.factories[CustomerService] = lambda di_container: CustomerService(search_handler=CustomerSearchHandler())