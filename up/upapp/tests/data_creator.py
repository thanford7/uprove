import names

from upapp.models import *


def createUser(**kwargs):
    firstName = kwargs.get('firstName') or names.get_first_name()
    lastName = kwargs.get('lastName') or names.get_last_name()
    user = User(
        firstName=firstName,
        lastName=lastName,
        email=f'{firstName}_{lastName}@uprove.co',
        employer_id=kwargs.get('employerId')
    )

    if userTypeBits := kwargs.get('userTypeBits'):
        user.userTypeBits = userTypeBits