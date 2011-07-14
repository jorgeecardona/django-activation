from django.db import models
from django.conf import settings
from string import letters, digits
from random import choice
from datetime import datetime, timedelta
from activation import signals
from django.contrib.contenttypes import generic
import logging


KEY_LENGTH = getattr(settings, 'ACTIVATION_KEY_LENGTH', 80)


def _generate_key(length):
    return ''.join(choice(letters + digits) for i in range(length))


class ActivationManager(models.Manager):

    def create_activation(self, user):
        " Creates an activation key to an user."

        key = _generate_key(KEY_LENGTH)
        while self.filter(key=key).count() > 0:
            key = _generate_key(KEY_LENGTH)

        # Create activation key.
        activation_key = self.create(user=user, key=key)

        # Deactivate user.
        user.is_active = False
        user.save()

        # Fire signal.
        signals.activation_created.send(
            sender=Activation, activation=activation_key)
        return activation_key

    def get_valid(self, key):
        " Get a valid key."
        VALID_TIME = getattr(settings, 'ACTIVATION_VALID_TIME', 7)
        return self.get(
            key=key, creation_date__gt=datetime.now() - timedelta(VALID_TIME))


class Activation(models.Model):

    #: User to activate.
    user = models.ForeignKey('auth.User', related_name='activations')

    #: Key.
    key = models.CharField(max_length=KEY_LENGTH)

    #: Creation date.
    creation_date = models.DateTimeField(auto_now_add=True)

    #: Objects Manager.
    objects = ActivationManager()

    def activate(self):
        " Activate the user."

        # Activate the user.
        self.user.is_active = True
        self.user.save()

        # Send the user_activated signal.
        signals.activation_used.send(sender=Activation, activation=self)


class InvitationManager(models.Manager):
    def create_invitation(self, host, email, to=None):
        " Creates a new invitation."

        if to is None:
            to = host

        key = _generate_key(KEY_LENGTH)
        while self.filter(key=key).count() > 0:
            key = _generate_key(KEY_LENGTH)

        # Create activation key.
        invitation = self.create(host=host, key=key, email=email, to=to)

        # Fire signal.
        signals.invitation_created.send_robust(
            sender=Invitation, invitation=invitation)
        return invitation

    def get_valid(self, key):
        " Get a valid invitation."
        VALID_TIME = getattr(settings, 'INVITATION_VALID_TIME', 7)
        return self.get(
            key=key, creation_date__gt=datetime.now() - timedelta(VALID_TIME))


class Invitation(models.Model):
    " An invitation is a way to let other users to be part of 'something'"

    #: Host member that invite the user (email).
    host = models.ForeignKey('auth.User', related_name='invitations')

    #: Email of the user to invite.
    email = models.EmailField()

    #: Invitation key.
    key = models.CharField(max_length=KEY_LENGTH)

    #: Creation date of the invitation.
    creation_date = models.DateTimeField(auto_now_add=True)

    #: An user is invited 'to' this, it could be a group, a site, or wathever
    #: you want.
    to_content_type = models.ForeignKey('contenttypes.ContentType')
    to_object_id = models.CharField(max_length=255)
    to = generic.GenericForeignKey('to_content_type', 'to_object_id')

    #: Objects Manager
    objects = InvitationManager()

    def accept(self, user):
        " An user must accept the invitation."

        # Send the invitation_accepted signal
        signals.invitation_accepted.send(
            sender=Invitation, invitation=self, user=user)
