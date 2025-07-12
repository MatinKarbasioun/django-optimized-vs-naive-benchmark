from django.db import models

from crm.infrastructure.models.base import ExternalModel


class Address(ExternalModel):
    id = models.BigIntegerField(primary_key=True)
    street = models.CharField(max_length=100)
    street_number = models.CharField(max_length=100)
    city_code = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    class Meta(ExternalModel.Meta):
        table_name = 'address'


    def __str__(self):
        return f"{self.street}, {self.street_number}, {self.city_code}, {self.city}, {self.country}"