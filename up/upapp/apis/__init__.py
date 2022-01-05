from upapp.models import ProjectSkill


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
