from django.test import TestCase
from django.contrib.auth.models import User
from django.conf import settings
from app.models import Item
from activation.models import ActivationKey


class ActivationKeyTestCase(TestCase):

    def setUp(self):
        # Create base user for tests.
        self.user = User.objects.create_user(
            username='pparamo', email='pparamo@rulfo.com', password='rulfo')

    def test_create_activation_key(self):
        " Test the creation of the key."

        key = ActivationKey.objects.generate(self.user)

        self.assertEqual(key.user, self.user)

        user = User.objects.get(id=self.user.id)
        self.assertFalse(user.is_active, "User must be inactive")

    def test_fire_created_signal(self):
        " Fire the signal of created activation key."
        self.assertEqual(Item.objects.count(), 0)
        ActivationKey.objects.generate(self.user)
        self.assertEqual(Item.objects.count(), 1)

    def test_invalid_activation_key(self):
        " Get an invalidated activation key."

        settings.ACTIVATION_VALID_TIME = 0
        key = ActivationKey.objects.generate(self.user)
        self.assertRaises(
            ActivationKey.DoesNotExist, ActivationKey.objects.get_valid,
            key.key)
        settings.ACTIVATION_VALID_TIME = 7

    def test_activate_user(self):
        " Activate an user."

        key = ActivationKey.objects.generate(self.user)
        key.activate()

        user = User.objects.get(id=self.user.id)
        self.assertTrue(user.is_active)
        self.assertEqual(ActivationKey.objects.filter(id=key.id).count(), 1)

    def test_activate_user_with_autodelete(self):
        " Activate an user with autodelete"

        settings.ACTIVATION_AUTODELETE = True
        key = ActivationKey.objects.generate(self.user)
        key.activate()

        user = User.objects.get(id=self.user.id)
        self.assertTrue(user.is_active)
        self.assertEqual(ActivationKey.objects.filter(id=key.id).count(), 0)
        settings.ACTIVATION_AUTODELETE = False
