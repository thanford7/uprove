from upapp.models import ProjectSkill


def setSkills(obj, skillIds):
    if obj.id:
        obj.skills.clear()

    for skill in ProjectSkill.objects.filter(id__in=skillIds):
        obj.skills.add(skill)