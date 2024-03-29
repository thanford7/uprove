from upapp.utils.dataUtil import intOrNone
from upapp.models import User

#TODO: Improve security to update stored session user when user data changes
def getSessionUser(request):
    try:
        userDict = request.session['uproveUser']
        if not userDict:
            return None
        userObj = User.objects.select_related('djangoUser').get(id=userDict['id'])
        return userObj
    except (KeyError, AttributeError, User.DoesNotExist):
        return None


def isPermittedSessionUser(request=None, user=None):
    user = user or getSessionUser(request)
    if user:
        return user.isActive
    return False


def isPermittedAdmin(request=None, user=None):
    user = user or getSessionUser(request)
    if user:
        return user.isSuperUser and user.isActive
    return False


def isSelf(userId, request=None, user=None):
    user = user or getSessionUser(request)
    if user:
        return user.id == intOrNone(userId) and user.isActive
    return False


def isPermittedEmployer(request, employerId):
    if not employerId:
        return False
    if user := getSessionUser(request):
        return user.employer_id == intOrNone(employerId)
    return False
