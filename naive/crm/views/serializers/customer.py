from rest_framework import serializers

from crm.models import AppUserModel
from crm.views.serializers.address import AddressSerializer
from crm.views.serializers.relationship import RelationshipSerializer


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