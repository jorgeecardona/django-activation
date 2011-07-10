from django.db import models
from activation.models import ActivationKey
from activation.signals import activation_created
from django.dispatch import receiver


class Item(models.Model):
    #: content
    content = models.TextField()


@receiver(activation_created, sender=ActivationKey)
def create_item(sender, activation, **kwargs):
    Item.objects.create(content=activation.key)
