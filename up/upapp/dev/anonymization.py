import os
import sys
from pathlib import Path

import django
import names

sys.path.append(Path(__file__).resolve().parent.parent.parent.as_posix())
os.environ['DJANGO_SETTINGS_MODULE'] = 'up.settings'
django.setup()

from django.conf import settings
from upapp.models import User

if 'app' in settings.DATABASES['default']['HOST']:
    raise ValueError('Cannot run this file on the prod database')

for user in User.objects.filter(isDemo=False):
    if user.isAdmin or user.firstName == 'Lever':
        continue

    user.firstName = names.get_first_name()
    user.middleName = None
    user.lastName = names.get_last_name()
    email = f'test-{user.firstName}-{user.lastName}@uprove.co'
    user.email = email
    user.save()

    djangoUser = user.djangoUser
    djangoUser.email = email
    djangoUser.set_password(os.getenv('DEV_DEFAULT_PWD'))
    djangoUser.save()



