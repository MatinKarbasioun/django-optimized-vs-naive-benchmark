from django.utils import timezone

from django.db import models

from shared.base import ExternalModel


class CustomerRelationshipModel(ExternalModel):
    id = models.BigAutoField(primary_key=True)
    appuser = models.OneToOneField('AppUserModel', on_delete=models.CASCADE, related_name='relationship')
    points = models.IntegerField(default=0, null=False)
    created = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        abstract = False
        db_table = 'customer_relationship'
        verbose_name_plural = 'relations'
        indexes = [
            models.Index(fields=['points', 'last_activity']),
        ]

    def __str__(self):
        return {f"{self.appuser.first_name} {self.appuser.last_name} with points: {self.points}" }