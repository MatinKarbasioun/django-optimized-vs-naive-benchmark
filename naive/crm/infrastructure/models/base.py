from django.db import models


class ExternalModel(models.Model):
    class Meta:
        managed = False
        abstract = True
