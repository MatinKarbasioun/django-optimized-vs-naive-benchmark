from typing import Optional

from crm.domain.entities import CustomerRelationship
from crm.domain.repositories import ICustomerRelationshipRepository
from crm.infrastructure.extensions import ModelToCustomerRelationship, CustomerRelationshipToModel
from crm.infrastructure.models import CustomerRelationshipModel
from shared.utils import handle_db_operation


class CustomerRelationshipRepository(ICustomerRelationshipRepository):

    def add(self, customer_id: int, relationship: CustomerRelationship):
        model = relationship @ CustomerRelationshipToModel(customer_id)
        handle_db_operation(lambda: model.save())
        relationship.id = model.id

    def find_by_customer_id(self, customer_id: int) -> Optional[CustomerRelationship]:
        return (handle_db_operation(lambda: CustomerRelationshipModel.objects.get(customer_id=customer_id)) @
                ModelToCustomerRelationship())
