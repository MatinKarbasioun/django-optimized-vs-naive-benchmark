from django.db import models

from shared.infrastructure.models.base import ExternalModel


class Address(ExternalModel):
    id = models.BigIntegerField(primary_key=True)
    street = models.CharField(max_length=128)
    street_number = models.CharField(max_length=32)
    city_code = models.CharField(max_length=32)
    city = models.CharField(max_length=64)
    country = models.CharField(max_length=32)

    class Meta(ExternalModel.Meta):
        db_table = 'address'


    def __str__(self):
        return f"{self.street}, {self.street_number}, {self.city_code}, {self.city}, {self.country}"