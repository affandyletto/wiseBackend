from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Element, Page, Proposal

@receiver(pre_delete, sender=Element)
def delete_file(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete()

@receiver(pre_delete, sender=Page)
def delete_file(sender, instance, **kwargs):
    if instance.bgImage:
        instance.bgImage.delete()

@receiver(pre_delete, sender=Proposal)
def delete_file(sender, instance, **kwargs):
    if instance.thumbnail:
        instance.thumbnail.delete()