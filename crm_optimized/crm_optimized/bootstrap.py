from kink import di

from crm.application.utils.app_settings import AppSettings
from crm.domain.repositories import ICustomerRepository, IAddressRepository, ICustomerRelationshipRepository
from crm.infrastructure.repositories import CustomerRepository
from crm.infrastructure.repositories import *


class Bootstrap:
    def __init__(self):
        AppSettings()
        self.__define_models()

    @classmethod
    def __define_models(cls):
        di.factories[ICustomerRepository] = lambda di_container: CustomerRepository()
        di.factories[IAddressRepository] = lambda di_container: AddressRepository()
        di.factories[ICustomerRelationshipRepository] = lambda di_container: CustomerRelationshipRepository()