from django.dispatch import Signal


# 'created' Signal fired when the activation key is created.
activation_created = Signal(providing_args=['activation'])

# An activation was used.
activation_used = Signal(providing_args=['activation'])

# An invitation was created.
invitation_created = Signal(providing_args=['invitation'])

# An invitation was accepted by an user.
invitation_accepted = Signal(providing_args=['invitation', 'user'])
