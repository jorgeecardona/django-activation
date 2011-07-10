from django.db import models
from django.conf import settings
from string import letters, digits
from random import choice
from datetime import datetime, timedelta
from activation import signals

KEY_LENGTH = getattr(settings, 'ACTIVATION_KEY_LENGTH', 80)
VALID_TIME = getattr(settings, 'ACTIVATION_VALID_TIME', 7)


class ActivationKeyManager(models.Manager):

    def _generate_key(self):
        return ''.join(choice(letters + digits) for i in range(KEY_LENGTH))

    def generate(self, user):
        " Generate an activation key to an user."

        key = self._generate_key()
        while self.filter(key=key).count() > 0:
            key = self._generate_key()

        # Create activation key.
        activation_key = self.create(user=user, key=key)

        # Deactivate user.
        user.is_active = False
        user.save()

        # Fire signal.
        signals.activation_created.send(
            sender=ActivationKey, activation=activation_key)
        return activation_key

    def get_valid(self, key):
        " Get a valid key."
        return self.get(
            key=key, creation_date__lt=datetime.now() - timedelta(VALID_TIME))


class ActivationKey(models.Model):

    #: User to activate.
    user = models.ForeignKey('auth.User', related_name='activation_keys')

    #: Key.
    key = models.CharField(max_length=KEY_LENGTH)

    #: Creation date.
    creation_date = models.DateTimeField(auto_now_add=True)

    #: Objects Manager.
    objects = ActivationKeyManager()

    def activate(self):
        " Activate the user."

        # Activate the user.
        self.user.is_active = True
        self.user.save()

        # Delete this activation key.
        AUTODELETE = getattr(settings, 'ACTIVATION_AUTODELETE', False)
        if AUTODELETE:
            self.delete()
