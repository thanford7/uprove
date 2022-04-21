from enum import Enum, auto

from django.core.files.uploadedfile import UploadedFile
from django.http import QueryDict
from django.utils import timezone
from rest_framework.views import APIView

from upapp.models import UserActivity, Activity
import upapp.security as security


def getFiles(request):
    if not request.data:
        return None

    files = {}
    for key, val in request.data.items():
        if isinstance(val, UploadedFile):
            files[key] = request.data.getlist(key)

    return files

class UproveAPIView(APIView):

    def initial(self, request, *args, **kwargs):
        requestData = request.data.dict() if isinstance(request.data, QueryDict) else request.data
        self.data = {**requestData, **request.query_params}
        self.files = getFiles(request)  # Django's dict method doesn't work for files - it drops all but the first uploaded file
        self.user = security.getSessionUser(request)
        self.isEmployer = self.user.isEmployer if self.user else False
        self.isCandidate = self.user.isCandidate if self.user else False
        self.isAdmin = self.user.isAdmin if self.user else False
        super().initial(request, *args, **kwargs)


# DO NOT MODIFY THESE. They are keys in upapp_activity table
class ActivityKey(Enum):
    CREATE_ACCOUNT = auto()
    SET_PASSWORD = auto()
    VIEW_PROJECT_SELECTION = auto()
    CANDIDATE_CREATE_PROJECT = auto()
    CANDIDATE_COMPLETE_PROJECT = auto()


def saveActivity(activityKey: ActivityKey, userId: int):
    UserActivity(
        activity=Activity.objects.get(key=activityKey.name),
        user_id=userId,
        timestamp=timezone.now()
    ).save()


def hasCompletedActivity(activityKey: ActivityKey, userId: int):
    activity = Activity.objects.get(key=activityKey.name)
    userActivities = UserActivity.objects.filter(user_id=userId, activity=activity)
    return bool(len(userActivities))
