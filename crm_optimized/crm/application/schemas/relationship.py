from ninja import ModelSchema

from crm.infrastructure.models import CustomerRelationshipModel


class RelationshipSchema(ModelSchema):
    class Meta:
        model = CustomerRelationshipModel
        fields = ['points', 'last_activity']