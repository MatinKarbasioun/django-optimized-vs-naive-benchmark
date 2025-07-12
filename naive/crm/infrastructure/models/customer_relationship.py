from django.utils import timezone

from django.db import models

from . import AppUser
from .base import ExternalModel


class CustomerRelationship(ExternalModel):
    id = models.BigAutoField(primary_key=True)
    appuser = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    points = models.FloatField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(default=timezone.now)

    class Meta(ExternalModel.Meta):
        table_name = 'customer_relationship'

    def __str__(self):
        return {f"{self.appuser.first_name} {self.appuser.last_name} with points: {self.points}" }