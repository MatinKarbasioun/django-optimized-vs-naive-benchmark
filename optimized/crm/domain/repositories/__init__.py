__all__ = ["IAddressRepository", "ICustomerRepository", "ICustomerRelationshipRepository"]

from .relationship import ICustomerRelationshipRepository
from .customer import ICustomerRepository
from .address import IAddressRepository