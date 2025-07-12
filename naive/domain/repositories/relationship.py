from abc import ABC, abstractmethod
from typing import Optional

from domain import CustomerRelationship


class ICustomerRelationshipRepository(ABC):

    @abstractmethod
    def find_by_customer_id(self, customer_id: int) -> Optional[CustomerRelationship]:
        pass

    @abstractmethod
    def add(self, relationship: CustomerRelationship) -> CustomerRelationship:
        pass