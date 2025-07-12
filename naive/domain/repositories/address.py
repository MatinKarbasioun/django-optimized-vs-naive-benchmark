from abc import ABC, abstractmethod
from typing import Optional

from domain import Address


class IAddressRepository(ABC):

    @abstractmethod
    def add(self, address: Address) -> Address:
        raise NotImplementedError()

    @abstractmethod
    def find_by_id(self, address_id: int) -> Optional[Address]:
        raise NotImplementedError()

