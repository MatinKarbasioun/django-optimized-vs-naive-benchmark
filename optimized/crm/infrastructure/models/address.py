from django.db import models

from shared.infrastructure.models.base import ExternalModel


class AddressModel(ExternalModel):
    id = models.BigAutoField(primary_key=True)
    street = models.CharField(max_length=128)
    street_number = models.CharField(max_length=32)
    city_code = models.CharField(max_length=32, db_index=True)
    city = models.CharField(max_length=64, db_index=True)
    country = models.CharField(max_length=32, db_index=True)

    class Meta(ExternalModel.Meta):
        db_table = 'address'
        verbose_name_plural = 'addresses'
        indexes = [
            models.Index(fields=['city', 'country']),
        ]


    def __str__(self):
        return f"{self.street}, {self.street_number}, {self.city_code}, {self.city}, {self.country}"