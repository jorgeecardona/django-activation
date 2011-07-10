django-activation
=================

Simple way to add an activation step to the creation of your users.


Installation
------------


Usage
-----

First you need to add *activation* to your installed_apps in settings.py::

    INSTALLED_APPS = (
        ...
        'activation',
        ...
        )

Some configuration can be made with this parameters:

:ACTIVATION_KEY_LENGTH: Controls the length of the activation key.

:ACTIVATION_AUTODELETE: It controls the deletion of the activation key after
			is used by the user.

:ACTIVATION_VALID_TIME: Define a period in which the activation key is valid.

You must to define the function that send the email or whatever you want listening to the signal 'ActivationKey.created', like this::
    
