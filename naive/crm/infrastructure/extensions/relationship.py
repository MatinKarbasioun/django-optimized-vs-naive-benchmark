from crm.domain import CustomerRelationship
from crm.infrastructure.models import CustomerRelationshipModel


class CustomerRelationshipToModel:
    def __init__(self, customer_id: int):
        self._customer_id = customer_id

    def __rmatmul__(self, relationship: CustomerRelationship) -> CustomerRelationshipModel:
        return CustomerRelationshipModel(
            appuser=relationship.id,
            points=relationship.points
        )


class ModelToCustomerRelationship:
    def __rmatmul__(self, model: CustomerRelationshipModel | None) -> CustomerRelationship | None:
        return CustomerRelationship(
            id=model.id,
            points=model.points,
            created=model.created,
            last_activity=model.last_activity
        ) if model else None
