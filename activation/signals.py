from django.dispatch import Signal

# 'created' Signal fired when the activation key is created.
activation_created = Signal(providing_args=['activation'])
