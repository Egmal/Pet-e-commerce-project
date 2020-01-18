import os
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Product
from my_shop import settings


@receiver(pre_delete, sender=Product)
def delete_product_image(sender, instance, **kwargs):
    image = f'{settings.BASE_DIR}{settings.MEDIA_URL}{instance.image}'
    os.remove(image)
