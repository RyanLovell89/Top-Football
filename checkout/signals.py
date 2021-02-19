from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import OrderLineItem


@receiver(post_save, sender=OrderLineItem)
def update_when_saved(sender, instance, created, **kwargs):

    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_when_deleted(sender, instance, **kwargs):

    instance.order.update_total()
