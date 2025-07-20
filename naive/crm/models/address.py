from django.db import models

from shared.infrastructure.models.base import ExternalModel


class AddressModel(ExternalModel):
    id = models.BigAutoField(primary_key=True)
    street = models.CharField(max_length=256, null=True, blank=True)
    street_number = models.CharField(max_length=256, null=True, blank=True)
    city_code = models.CharField(max_length=256)
    city = models.CharField(max_length=256)
    country = models.CharField(max_length=128)

    class Meta(ExternalModel.Meta):
        db_table = 'address'
        verbose_name_plural = 'addresses'


    def __str__(self):
        return f"{self.street}, {self.street_number}, {self.city_code}, {self.city}, {self.country}"

    def __repr__(self):
        return (f"{self._meta.db_table} {self.id} {self.street}, "
                f"{self.street_number}, {self.city_code}, {self.city}, {self.country}")