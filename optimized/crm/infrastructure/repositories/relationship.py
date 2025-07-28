from typing import Optional

from crm.domain.entities import CustomerRelationship
from crm.domain.repositories import ICustomerRelationshipRepository
from crm.infrastructure.extensions import CustomerRelationshipToModel
from shared.utils import handle_db_operation


class CustomerRelationshipRepository(ICustomerRelationshipRepository):
    async def add(self, customer_id: int, relationship: CustomerRelationship):
        model = relationship @ CustomerRelationshipToModel(customer_id=customer_id)
        await handle_db_operation(lambda: model.asave())
        relationship.id = model.id
        relationship.created = model.created
        relationship.last_activity = model.last_activity

    async def find_by_customer_id(self, customer_id: int) -> Optional[CustomerRelationship]:
        raise NotImplementedError