from rest_framework import serializers

from crm.infrastructure.models import AppUserModel
from crm.presentation.serializers.address import AddressSerializer
from crm.presentation.serializers.relationship import RelationshipSerializer


class CustomerSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    relationship = RelationshipSerializer(read_only=True)

    class Meta:
        model = AppUserModel
        fields = [
            'id', 'first_name', 'last_name', 'gender',
            'customer_id', 'phone_number', 'created', 'birthday',
            'address', 'relationship'
        ]