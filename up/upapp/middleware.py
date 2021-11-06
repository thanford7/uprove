import logging
from hashlib import md5
from threading import local

from django.conf import settings
from django.contrib.auth import logout

from upapp.models import User

PASSWORD_HASH_KEY = getattr(settings, 'PASSWORD_SESSION_PASSWORD_HASH_KEY', 'password_session_password_hash_key')

_threadlocals = local()
logger = logging.getLogger()


def getPasswordHash(user):
    """Returns a string of crypted password hash"""
    password = user.password or ''
    return md5(
        md5(password.encode()).hexdigest().encode() + settings.SECRET_KEY.encode()
    ).hexdigest()


def setResponseAttribute(attrName, val):
    if val is None and hasattr(_threadlocals, attrName):
        delattr(_threadlocals, attrName)
    else:
        setattr(_threadlocals, attrName, val)


class UserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        uproveUser = setUproveUser(request)

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        # If user is logging in, user won't be set until response is returned
        if not uproveUser:
            setUproveUser(request)

        return response

def setUproveUser(request):
    try:
        uproveUser = None
        if request.user.is_authenticated:
            try:
                uproveUser = User.objects.get(djangoUser=request.user)
            except User.DoesNotExist:
                logger.error('No Uprove user exists for this Django user')
    except Exception:
        logger.error('Unable to load Uprove user')
        uproveUser = None

    if uproveUser:
        setResponseAttribute('uproveUser', uproveUser)

    return uproveUser