from django.db import models


class ExternalModel(models.Model):
    class Meta:
        managed = True
        abstract = True
