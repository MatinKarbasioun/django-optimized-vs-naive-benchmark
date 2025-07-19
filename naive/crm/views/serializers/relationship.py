from rest_framework import serializers
from crm.models import CustomerRelationshipModel


class RelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerRelationshipModel
        fields = ['points','last_activity']