from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from app.models import Item
from activation.models import Activation, Invitation


class ActivationTestCase(TestCase):

    def setUp(self):
        # Create base user for tests.
        self.user = User.objects.create_user(
            username='pparamo', email='pparamo@rulfo.com', password='rulfo')
        settings.ACTIVATION_VALID_TIME = 7
        settings.INVITATION_VALID_TIME = 7

    def test_invite_user(self):
        " Invite an user to nothing in special."
        self.assertEqual(Item.objects.count(), 0)
        Invitation.objects.create_invitation(self.user, 'me@rulfo.com')
        self.assertEqual(Item.objects.count(), 1)

    def test_accept_invitation(self):
        " An user accepts an invitation on time. "

        # Create an item to invite
        item = Item.objects.create()
        self.assertEqual(item.authors.count(), 0)

        # Invite an user to an item.
        invitation = Invitation.objects.create_invitation(
            self.user, 'me@rulfo.com', item)
        self.assertEqual(Item.objects.count(), 2)

        # Accept invitation.
        invitation.accept(self.user)

        # Refresh item.
        item = Item.objects.get(id=item.id)
        self.assertEqual(item.authors.count(), 1)

    def test_accept_invalid_invitation(self):
        " Call the accept method must acept even if the time is passed."

        settings.INVITATION_VALID_TIME = 0

        # Create an item to invite
        item = Item.objects.create()
        self.assertEqual(item.authors.count(), 0)

        # Invite an user to an item.
        invitation = Invitation.objects.create_invitation(
            self.user, 'me@rulfo.com', item)
        self.assertEqual(Item.objects.count(), 2)

        # Accept invitation.
        invitation.accept(self.user)

    def test_get_invalid_invitation(self):
        " An user create an invitation and then want to accepted. "

        settings.INVITATION_VALID_TIME = 0

        # Create an item to invite
        item = Item.objects.create()
        self.assertEqual(item.authors.count(), 0)

        # Invite an user to an item.
        invitation = Invitation.objects.create_invitation(
            self.user, 'me@rulfo.com', item)
        self.assertEqual(Item.objects.count(), 2)

        # Accept invitation.
        self.assertRaises(
            ObjectDoesNotExist,
            Invitation.objects.get_valid, invitation.key)

    def test_create_activation_key(self):
        " Test the creation of the key."

        key = Activation.objects.create_activation(self.user)

        self.assertEqual(key.user, self.user)

        user = User.objects.get(id=self.user.id)
        self.assertFalse(user.is_active, "User must be inactive")

    def test_fire_created_signal(self):
        " Fire the signal of created activation key."
        self.assertEqual(Item.objects.count(), 0)
        Activation.objects.create_activation(self.user)
        self.assertEqual(Item.objects.count(), 1)

    def test_invalid_activation_key(self):
        " Get an invalidated activation key."

        settings.ACTIVATION_VALID_TIME = 0
        invitation = Activation.objects.create_activation(self.user)
        self.assertRaises(
            Activation.DoesNotExist, Activation.objects.get_valid,
            invitation.key)

    def test_activate_user(self):
        " Activate an user."

        key = Activation.objects.create_activation(self.user)
        key.activate()

        user = User.objects.get(id=self.user.id)
        self.assertTrue(user.is_active)
        self.assertEqual(Activation.objects.filter(id=key.id).count(), 1)
