from django.db import models
from django.utils import timezone

from crm.infrastructure.models import Address
from crm.infrastructure.models.base import ExternalModel
from domain import Gender


class AppUser(ExternalModel):
    id = models.BigIntegerField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(choices=Gender.get_genders(), default=Gender.UNDEFINED)
    customer_id = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    birthday = models.DateField()
    last_updated = models.DateTimeField(default=timezone.now)

    class Meta(ExternalModel.Meta):
        table_name = 'app_user'

    def __str__(self):
        return f'{self.first_name} {self.last_name} with customer id: {self.customer_id}'
