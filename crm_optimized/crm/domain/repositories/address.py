from abc import ABC, abstractmethod
from typing import Optional

from crm.domain.entities import Address


class IAddressRepository(ABC):

    @abstractmethod
    async def add(self, address: Address):
        raise NotImplementedError()

    @abstractmethod
    async def find_by_id(self, address_id: int) -> Optional[Address]:
        raise NotImplementedError()

