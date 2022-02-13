from upapp.models import User

def getSessionUser(request):
    try:
        return request.session['uproveUser']
    except KeyError:
        return None


def isPermittedSessionUser(request):
    if user := getSessionUser(request):
        userObj = User.objects.select_related('djangoUser').get(id=user['id'])
        return userObj.djangoUser.is_active
    return False


def isPermittedAdmin(request):
    if user := getSessionUser(request):
        return user['isSuperUser'] and user['isActive']
    return False


def isSelf(request, userId):
    if user := getSessionUser(request):
        return user['id'] == userId and user['isActive']
    return False


def isPermittedEmployer(request, employerId):
    if user := getSessionUser(request):
        return user['employerId'] == employerId
    return False
