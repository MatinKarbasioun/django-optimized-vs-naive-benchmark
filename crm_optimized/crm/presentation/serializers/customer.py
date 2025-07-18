from rest_framework import serializers

from crm.infrastructure.models import AppUserModel


class CustomerSerializer(serializers.ModelSerializer):
    city = serializers.CharField(source='address.city', read_only=True)
    country = serializers.CharField(source='address.country', read_only=True)
    points = serializers.IntegerField(source='relationship.points', read_only=True)

    class Meta:
        model = AppUserModel
        fields = [
            'id', 'first_name', 'last_name', 'gender',
            'customer_id', 'phone_number', 'created', 'birthday',
            'city', 'country', 'points'
        ]