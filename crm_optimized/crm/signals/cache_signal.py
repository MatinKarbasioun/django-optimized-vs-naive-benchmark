from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from crm.application.utils.app_settings import AppSettings
from crm.infrastructure.models import AppUserModel, AddressModel, CustomerRelationshipModel


@receiver([post_save, post_delete], sender=AppUserModel)
@receiver([post_save, post_delete], sender=AddressModel)
@receiver([post_save, post_delete], sender=CustomerRelationshipModel)
def clear_customer_search_cache(sender, instance, **kwargs):
    cache.delete_pattern(f'*{AppSettings.APP_SETTINGS["cashing"]["keys"]["customer_cache"]}*')
