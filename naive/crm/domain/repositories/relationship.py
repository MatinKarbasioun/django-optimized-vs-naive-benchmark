from abc import ABC, abstractmethod
from typing import Optional

from crm.domain import CustomerRelationship


class ICustomerRelationshipRepository(ABC):

    @abstractmethod
    def add(self, customer_id: int, relationship: CustomerRelationship):
        pass

    @abstractmethod
    def find_by_customer_id(self, customer_id: int) -> Optional[CustomerRelationship]:
        pass

