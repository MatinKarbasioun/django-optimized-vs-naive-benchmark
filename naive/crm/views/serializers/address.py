from rest_framework import serializers

from crm.models import AddressModel


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressModel
        fields = ['city', 'country', 'street', 'street_number', 'city_code']