from django.db import models
from django.utils import timezone

from crm.infrastructure.models import Address
from shared.infrastructure.models.base import ExternalModel
from domain import Gender


class AppUser(ExternalModel):
    id = models.BigIntegerField(primary_key=True)
    first_name = models.CharField(max_length=128, null=False, blank=False)
    last_name = models.CharField(max_length=128, null=False, blank=False)
    gender = models.CharField(max_length=12, choices=Gender.get_genders(), default=Gender.UNDEFINED)
    customer_id = models.CharField(max_length=32, unique=True)
    phone_number = models.CharField(max_length=32, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    birthday = models.DateField(null=True, blank=True)
    last_updated = models.DateTimeField(default=timezone.now)

    class Meta(ExternalModel.Meta):
        db_table = 'app_user'

    def __str__(self):
        return f'{self.first_name} {self.last_name} with customer id: {self.customer_id}'
