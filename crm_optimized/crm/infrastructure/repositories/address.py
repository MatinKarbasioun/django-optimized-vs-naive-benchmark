from typing import Optional

from crm.domain.entities import Address
from crm.domain.repositories import IAddressRepository
from crm.infrastructure.extensions import AddressToModel
from shared.utils import handle_db_operation


class AddressRepository(IAddressRepository):
    async def add(self, address: Address):
        model = address @ AddressToModel()
        await handle_db_operation(lambda: model.asave())
        address.id = model.id

    async def find_by_id(self, address_id: int) -> Optional[Address]:
        raise NotImplementedError