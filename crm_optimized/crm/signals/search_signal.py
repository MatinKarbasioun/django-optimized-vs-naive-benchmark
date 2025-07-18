from django.contrib.postgres.search import SearchVector
from django.db import models
from django.db.models import Value
from django.db.models.functions import Cast, Coalesce
from django.db.models.signals import post_save
from django.dispatch import receiver

from crm.infrastructure.models import AppUserModel, AddressModel, CustomerRelationshipModel


@receiver(post_save, sender=AppUserModel)
@receiver(post_save, sender=AddressModel)
@receiver(post_save, sender=CustomerRelationshipModel)
def update_search_vector_on_save(sender, instance, **kwargs):
    users_to_update = AppUserModel.objects.none()
    if sender == AppUserModel:
        users_to_update = AppUserModel.objects.filter(pk=instance.pk)
    elif sender == AddressModel:
        users_to_update = AppUserModel.objects.filter(address=instance)
    elif sender == CustomerRelationshipModel:
        users_to_update = AppUserModel.objects.filter(pk=instance.appuser.pk)

    if users_to_update.exists():
        vector = (
                SearchVector('first_name', weight='A') +
                SearchVector('last_name', weight='A') +
                SearchVector(Coalesce('customer_id', Value('')), weight='B') +
                SearchVector(Coalesce('phone_number', Value('')), weight='C') +
                SearchVector(Coalesce('address__street', Value('')), weight='D') +
                SearchVector(Coalesce('address__city', Value('')), weight='C') +
                SearchVector(Coalesce('address__country', Value('')), weight='C') +
                SearchVector(Coalesce('address__street_number', Value('')), weight='D') +
                SearchVector(
                    Cast(Coalesce('relationship__points', Value(0)), models.TextField()),
                    weight='D'
                ) +
                SearchVector(
                    Cast(Coalesce('relationship__last_activity', Value(None)), models.TextField()),
                     weight='D'
                )
        )

        users_with_vector = users_to_update.annotate(new_vector=vector)
        for user in users_with_vector:
            AppUserModel.objects.filter(pk=user.pk).update(search_vector=user.new_vector)

        print(f"Updated search vector for {users_to_update.count()} user(s).")