from rest_framework.views import APIView

from upapp.models import ProjectSkill, User
import upapp.security as security


class UproveAPIView(APIView):

    def initial(self, request, *args, **kwargs):
        self.data = request.data
        self.user = security.getSessionUser(request)
        self.isEmployer = bool(self.user['employerId'])
        self.isCandidate = self.user['userTypeBits'] & User.USER_TYPE_CANDIDATE
        self.isAdmin = self.user['userTypeBits'] & User.USER_TYPE_ADMIN
        super().initial(request, *args, **kwargs)


def setSkills(obj, skillIds):
    isChanged = False
    if obj.id:
        oldSkillIds = {s.id for s in obj.skills.all()}
        diff = oldSkillIds.symmetric_difference(set(skillIds))
        isChanged = bool(len(diff))
        obj.skills.clear()

    for skill in ProjectSkill.objects.filter(id__in=skillIds):
        obj.skills.add(skill)

    return isChanged
