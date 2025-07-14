from django.db import models
from django.utils import timezone

from crm.infrastructure.models import AddressModel
from shared.infrastructure.models.base import ExternalModel
from crm.domain.value_objects.gender import Gender


class AppUserModel(ExternalModel):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=128, null=False, blank=False, db_index=True)
    last_name = models.CharField(max_length=128, null=False, blank=False, db_index=True)
    gender = models.CharField(max_length=12, choices=Gender.get_genders(), default=Gender.UNDEFINED, db_index=True)
    customer_id = models.CharField(max_length=32, unique=True, db_index=True)
    phone_number = models.CharField(max_length=32, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(AddressModel, on_delete=models.CASCADE, null=True, blank=True, related_name='app_user')
    birthday = models.DateField(null=True, blank=True)
    last_updated = models.DateTimeField(default=timezone.now)

    class Meta(ExternalModel.Meta):
        db_table = 'app_user'
        verbose_name_plural = 'app_users'
        indexes = [
            models.Index(fields=['created', 'gender']),
            models.Index(fields=['first_name', 'last_name']),
            models.Index(fields=['birthday']),
        ]

    def __str__(self):
        return f'{self.first_name} {self.last_name} with customer id: {self.customer_id}'
