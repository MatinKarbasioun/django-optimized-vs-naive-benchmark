import redis

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from crm.infrastructure.models import AppUserModel, AddressModel


@receiver([post_save, post_delete], sender=AppUserModel)
@receiver([post_save, post_delete], sender=AddressModel)
def clear_customer_search_cache(self, sender, instance, **kwargs):
    redis_client = redis.from_url(self.__cache_url)
    for key in redis_client.scan_iter(f"{self.__key_prefix}*"):
        redis_client.delete(key)