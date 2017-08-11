from django.db.models.signals import post_save
from django.dispatch import receiver

from wishlist.wishlist.api.models import Item
from wishlist.wishlist.api.tasks import get_item_raw_data


@receiver(post_save, sender=Item)
def trigger_get_item_raw_data(instance, raw, created, **kwargs):
    if created or not instance.raw_data:
        get_item_raw_data.delay(instance.pk)
