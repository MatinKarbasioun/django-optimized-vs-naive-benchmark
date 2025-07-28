from abc import ABC, abstractmethod
from typing import Optional

from crm.domain.entities import CustomerRelationship


class ICustomerRelationshipRepository(ABC):

    @abstractmethod
    async def add(self, customer_id: int, relationship: CustomerRelationship):
        raise NotImplementedError

    @abstractmethod
    async def find_by_customer_id(self, customer_id: int) -> Optional[CustomerRelationship]:
        raise NotImplementedError

