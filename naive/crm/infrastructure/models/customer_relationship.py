from django.utils import timezone

from django.db import models

from shared.infrastructure.models.base import ExternalModel


class CustomerRelationship(ExternalModel):
    id = models.BigAutoField(primary_key=True)
    appuser = models.ForeignKey('AppUser', on_delete=models.CASCADE)
    points = models.IntegerField(default=0, null=False)
    created = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(default=timezone.now)

    class Meta(ExternalModel.Meta):
        db_table = 'customer_relationship'

    def __str__(self):
        return {f"{self.appuser.first_name} {self.appuser.last_name} with points: {self.points}" }