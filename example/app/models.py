from django.db import models
from activation.models import Activation, Invitation
from activation.signals import activation_created
from activation.signals import invitation_created
from activation.signals import invitation_accepted
from django.dispatch import receiver


class Item(models.Model):
    #: content
    content = models.TextField()

    authors = models.ManyToManyField('auth.User', related_name='items')


@receiver(activation_created, sender=Activation, dispatch_uid='create_item_1')
def create_item_1(sender, activation, **kwargs):
    # Send an email or do something useful here.
    Item.objects.create(content=activation.key)


@receiver(invitation_created, sender=Invitation, dispatch_uid='create_item_2')
def create_item_2(sender, invitation, **kwargs):
    # Send an email or do something useful here.
    Item.objects.create(content=invitation.key)


@receiver(invitation_accepted, sender=Invitation, dispatch_uid='add_author')
def add_author(sender, invitation, user, **kwargs):
    if isinstance(invitation.to, Item):
        invitation.to.authors.add(user)
