from django.db.models.signals import post_save
from django.dispatch import receiver

from crm.infrastructure.models.helper.search_vector import generate_app_user_search_vector
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
        users_with_vector = users_to_update.annotate(new_vector=generate_app_user_search_vector())
        for user in users_with_vector:
            AppUserModel.objects.filter(pk=user.pk).update(search_vector=user.new_vector)

        print(f"Updated search vector for {users_to_update.count()} user(s).")