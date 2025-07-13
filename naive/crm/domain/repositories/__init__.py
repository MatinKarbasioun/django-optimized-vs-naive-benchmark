__all__ = ["IAddressRepository", "ICustomerRepository", "ICustomerRelationshipRepository"]

from .relationship import ICustomerRelationshipRepository
from .user import ICustomerRepository
from .address import IAddressRepository