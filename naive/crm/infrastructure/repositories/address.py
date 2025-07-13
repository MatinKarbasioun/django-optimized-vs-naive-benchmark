from typing import Optional
from crm.domain import Address
from crm.domain.repositories import IAddressRepository
from crm.infrastructure.extensions import AddressToModel, ModelToAddress
from crm.infrastructure.models import AddressModel
from shared.utils import handle_db_operation


class AddressRepository(IAddressRepository):

    def add(self, address: Address):
        model = address @ AddressToModel()
        handle_db_operation(lambda: model.save())
        address.id = model.id

    def find_by_id(self, address_id: int) -> Optional[Address]:
        return handle_db_operation(lambda: AddressModel.objects.get(id=address_id)) @ ModelToAddress()
