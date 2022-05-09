from http import HTTPStatus
from json import dumps

from django.db.models import F, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from upapp import security
from upapp.modelSerializers import *
from upapp.apis.blog import BlogPostView
from upapp.apis.employer import EmployerView, JobPostingView
from upapp.apis.job import JobTemplateView
from upapp.apis.project import ProjectView
from upapp.apis.user import PreferencesView, UserJobApplicationView, UserView, UserProfileView, UserProjectView
from upapp.models import Role, Skill
from upapp.viewsAuth import getLoginRedirectUrl


def homepage(request):
    if security.getSessionUser(request):
        return redirect(getLoginRedirectUrl(request))
    return render(request, 'home.html', {'data': dumps({
        'roles': [getSerializedRole(r) for r in Role.objects.all()],
        'skills': [getSerializedSkill(s) for s in Skill.objects.all()]
    })})


def about(request):
    return render(request, 'about.html', context={})


def accountSettings(request, userId):
    if not security.isSelf(userId, request=request):
        return _getUnauthorizedPage(request)
    user = UserView.getUser(userId)
    serializedUser = {}
    if user:
        serializedUser = getSerializedUser(user)
    return render(request, 'accountSettings.html', {'data': dumps(serializedUser)})


def admin(request):
    if not security.isPermittedAdmin(request):
        return _getUnauthorizedPage(request)
    return render(request, 'admin.html', {'data': dumps({
        'projects': [getSerializedProject(p, isIncludeDetails=True, isAdmin=True) for p in ProjectView.getProjects(isIgnoreEmployerId=True)],
        'roles': [getSerializedRole(r) for r in Role.objects.all()],
        'skills': [getSerializedSkill(s) for s in Skill.objects.all()],
        'jobTemplates': [getSerializedJobTemplate(t) for t in JobTemplateView.getJobTemplates()],
        'companySizes': [{'id': s.id, 'companySize': s.companySize} for s in CompanySize.objects.all()],
    })})


def blog(request, blogId=None):
    isAdmin = security.isPermittedAdmin(request)
    data = {'blogTags': [getSerializedBlogTag(bt) for bt in BlogPostView.getBlogTags()]}
    if blogId:
        data['blog'] = getSerializedBlog(BlogPostView.getBlogPost(blogId))
        if not isAdmin and not data['blog']['isPublished']:
            return _getUnauthorizedPage(request)
    else:
        data['blogs'] = [getSerializedBlog(bp) for bp in BlogPostView.getBlogPosts(isPublishedOnly=not isAdmin)]
    if isAdmin:
        adminUsers = User.objects\
            .annotate(is_admin=F('userTypeBits').bitand(User.USER_TYPE_ADMIN))\
            .filter(djangoUser__is_active=True, is_admin__gt=0)
        data['authors'] = [{
            'id': user.id,
            'firstName': user.firstName,
            'lastName': user.lastName
        } for user in adminUsers]

    if blogId:
        return render(request, 'blogSingle.html', context={'data': dumps(data), 'title': data['blog']['title']})

    return render(request, 'blog.html', {'data': dumps(data)})


def candidateBoard(request):
    user = security.getSessionUser(request)
    if not user or not (user.isAdmin or user.isEmployer):
        return _getUnauthorizedPage(request)

    return render(request, 'candidateBoard.html', context={'data': dumps({
        'candidates': [{
            'id': candidate.id,
            'profileId': candidate.primaryProfile.id,
            'firstName': candidate.firstName,
            'lastName': candidate.lastName,
            'email': candidate.email,
            'appliedJobs': [
                j.employerJob.jobTitle
                for j in candidate.jobApplication.all()
                if j.employerJob.employer_id == user.employer_id
            ],
            'userProjects': [{
                'id': project.id,
                'projectTitle': project.customProject.project.title,
                'role': project.customProject.project.role.name,
                'roleId': project.customProject.project.role.id,
                'status': project.status,
                'skillLevelBit': project.customProject.skillLevelBit,
                'evaluationScorePct': project.evaluationScorePct,
                'skills': [getSerializedSkill(s) for s in project.customProject.skills.all()]
            } for project in candidate.userProject.all()
                if user.isAdmin or (project.status == UserProject.Status.COMPLETE.value and not project.isHidden)
            ]
        }
            for candidate
            in User.objects
                .select_related('djangoUser')
                .prefetch_related('profile', 'userProject', 'userProject__customProject', 'jobApplication', 'jobApplication__employerJob')
                .annotate(isCandidateF=F('userTypeBits').bitand(User.USER_TYPE_CANDIDATE))
                .annotate(isAdminF=F('userTypeBits').bitand(User.USER_TYPE_ADMIN))
                .filter(
                    djangoUser__is_active=True,
                    isDemo=False,
                    isCandidateF__gt=0,
                    isAdminF=0
                )
        ],
        'roles': [getSerializedRole(r) for r in Role.objects.all()],
        'skills': [getSerializedSkill(s) for s in Skill.objects.all()]
    })})


def candidateDashboard(request, userId=None):
    user = security.getSessionUser(request)
    if not user:
        return _getUnauthorizedPage(request)

    userId = userId or user.id
    if not userId:
        return _getErrorPage(request, HTTPStatus.BAD_REQUEST, 'A user ID is required')

    if not security.isSelf(userId, request=request):
        return _getUnauthorizedPage(request)

    return render(request, 'candidateDashboard.html', context={'data': dumps({
        'user': getSerializedUser(UserView.getUser(userId), isIncludeAssets=True),
        'userProjects': [getSerializedUserProject(up) for up in UserProjectView.getUserProjects(userId=userId)],
        'jobApplications': [getSerializedJobApplication(ja, includeJob=True) for ja in UserJobApplicationView.getUserJobApplications(userId=userId)]
    })})


def candidateOnboard(request):
    user = security.getSessionUser(request)
    if not user:
        return _getUnauthorizedPage(request)

    if not user.id:
        return _getErrorPage(request, HTTPStatus.BAD_REQUEST, 'A user ID is required')

    return render(request, 'candidateOnboard.html', context={'data': dumps({
        'roles': [getSerializedRole(r) for r in Role.objects.all()],
        'skills': [getSerializedSkill(s) for s in Skill.objects.all()],
        **PreferencesView.getPreferenceOptions()
    })})


def candidateProject(request, userProjectId=None):
    user = security.getSessionUser(request)
    if not user or not (user.isAdmin or user.isEmployer):
        return _getUnauthorizedPage(request)

    if not userProjectId:
        return _getErrorPage(request, HTTPStatus.BAD_REQUEST, 'A user project ID is required')

    userProject = UserProjectView.getUserProjects(userProjectId=userProjectId)
    return render(request, 'candidateProject.html', context={'data': dumps({
        'user': getSerializedUser(UserView.getUser(userProject.user_id), isIncludeAssets=True),
        'userProject': getSerializedUserProject(userProject, employerId=None if user.isAdmin else user.employer_id),
        'projects': [getSerializedProject(
            userProject.customProject.project,
            isIncludeDetails=True,
            isAdmin=user.isAdmin,
            evaluationEmployerId=None if user.isAdmin else user.employer_id
        )],
    })})


def contact(request):
    return render(request, 'contact.html', context={})


def credits(request):
    return render(request, 'credits.html')


def employerDashboard(request, employerId=None):
    user = security.getSessionUser(request)
    if not user:
        return _getUnauthorizedPage(request)

    employerId = employerId or user.employer_id
    if not employerId:
        return _getErrorPage(request, HTTPStatus.BAD_REQUEST, 'An employer ID is required')

    if not (security.isPermittedEmployer(request, employerId) or security.isPermittedAdmin(request, user)):
        return _getUnauthorizedPage(request)

    return render(request, 'employerDashboard.html', context={'data': dumps({
        'employer': getSerializedEmployer(EmployerView.getEmployer(employerId), employerId=employerId),
        'projects': [getSerializedProject(p, isIncludeDetails=True, evaluationEmployerId=employerId) for p in ProjectView.getProjects(employerId=employerId)],
        'jobTemplates': [getSerializedJobTemplate(t) for t in JobTemplateView.getJobTemplates()],
        'roleLevels': [getSerializedRoleLevel(rl) for rl in RoleLevel.objects.select_related('role').all()],
        'users': [{
            'id': u.id,
            'firstName': u.firstName,
            'lastName': u.lastName,
            'email': u.email,
            'userTypeBits': u.userTypeBits,
            'leverUserKey': u.leverUserKey
        } for u in UserView.getUsers(filter=Q(employer_id=employerId))]
    })})


def employers(request):
    return render(request, 'employers.html')


def errors(request):
    return render(request, 'errors.html', context={})


def jobs(request):
    user = security.getSessionUser(request)
    if not user or not security.isPermittedSessionUser(user=user):
        return _getUnauthorizedPage(request)

    user = UserView.getUser(user.id)  # Refetch to get all related objects
    jobs = JobPostingView.getEmployerJobs(jobFilter=JobPostingView.getEmployerJobFilter())
    employers = Employer.objects.filter(isDemo=False)
    projects = [getSerializedProject(p, isIncludeDetails=True) for p in ProjectView.getProjects(isIgnoreEmployerId=True)]
    projectsByRoleId = JobPostingView.getProjectsByRoleIdMap()

    return render(request, 'jobs.html', context={'data': dumps({
        'jobs': [{
            **getSerializedEmployerJob(job),
            'projectIds': [p.id for p in projectsByRoleId[job.roleLevel.role_id]],
        } for job in jobs],
        'employers': {e.id: {
            'id': e.id,
            'companyName': e.companyName,
            'logo': e.logo.url if e.logo else None,
            'description': e.description,
            'glassDoorUrl': e.glassDoorUrl
        } for e in employers},
        'preferences': {
            'companySizes': [{'id': s.id, 'companySize': s.companySize} for s in user.preferenceCompanySizes.all()],
            'roles': [getSerializedRoleLevel(v) for v in user.preferenceRoles.all()],
            'remoteBits': user.preferenceRemoteBits,
            'states': [{'id': v.id, 'stateName': v.stateName} for v in user.preferenceState.all()],
            'countries': [{'id': v.id, 'countryName': v.countryName} for v in user.preferenceCountry.all()],
        },
        'states': [{'id': s.id, 'stateName': s.stateName} for s in State.objects.all()],
        'countries': [{'id': c.id, 'countryName': c.countryName} for c in Country.objects.filter(countryName__in=JobPostingView.permittedCountries)],
        'roleLevels': [getSerializedRoleLevel(r) for r in RoleLevel.objects.select_related('role').all()],
        'projects': projects,
        'companySizes': [{'id': s.id, 'companySize': s.companySize} for s in CompanySize.objects.all()],
    })})


def jobPosting(request, jobId):
    user = security.getSessionUser(request)
    if not user or not security.isPermittedSessionUser(user=user):
        return _getUnauthorizedPage(request)
    job = JobPostingView.getEmployerJobs(jobId=jobId, isIncludeDemo=True)
    projects = ProjectView.getProjects(employerId=job.employer_id, projectIds=[p.project_id for p in job.allowedProjects.all()])
    isEmployer = security.isPermittedEmployer(request, job.employer_id)
    user = security.getSessionUser(request)
    employerId = user.employer_id if isEmployer else None
    projectsByRoleId = JobPostingView.getProjectsByRoleIdMap()
    recommendedProjects = ProjectView.getProjects(
        projectIds=[p.id for p in projectsByRoleId[job.roleLevel.role_id]]
    ) if job.roleLevel else []

    data = {
        'job': {
            **getSerializedEmployerJob(job, employerId=employerId),
            'projects': [getSerializedProject(p, isIncludeDetails=True) for p in recommendedProjects],
        },
        'employer': getSerializedEmployer(EmployerView.getEmployer(job.employer_id), employerId=employerId),
        'projects': {p.id: getSerializedProject(p, isIncludeDetails=True, evaluationEmployerId=employerId) for p in projects},
        'roles': [getSerializedRole(r) for r in Role.objects.all()],
        'skills': [getSerializedSkill(s) for s in Skill.objects.all()]
    }
    if user and user.userTypeBits & User.USER_TYPE_CANDIDATE:
        allowedProjectIds = [ap.id for ap in job.allowedProjects.all()]
        data['userProjects'] = [
            getSerializedUserProject(up)
            for up in UserProjectView.getUserProjects(userId=user.id)
            if up.customProject_id in allowedProjectIds
        ]
    return render(request, 'jobPosting.html', context={'data': dumps(data)})


def login(request):
    return render(request, 'login.html')


def salesMentor(request):
    return render(request, 'sales/sales-mentor.html')


def privacy(request):
    return render(request, 'privacy.html', context={})


def profile(request, profileId):
    profile = UserProfileView.getUserProfile(profileId)
    data = getSerializedUserProfile(profile, isOwner=security.isSelf(profile.user_id, request=request))
    return render(request, 'userProfile.html', context={'data': dumps(data)})


def project(request, projectId):
    user = security.getSessionUser(request)
    employerId = user.employer_id if user else None
    jobMapByRole = JobPostingView.getJobMapByRole()
    project = ProjectView.getProject(projectId)
    baseData = {
        'project': {
            **getSerializedProject(
                project,
                isIncludeDetails=security.isPermittedSessionUser(request),
                evaluationEmployerId=employerId
            ),
            'jobs': jobMapByRole[project.role.name.lower()]
        },
        'roles': [getSerializedRole(r) for r in Role.objects.all()],
        'skills': [getSerializedSkill(s) for s in Skill.objects.all()]
    }

    extraData = {}
    user = security.getSessionUser(request)
    if employerId:
        extraData['jobs'] = [getSerializedEmployerJob(j, employerId=employerId) for j in JobPostingView.getEmployerJobs(employerId=employerId)]

    if user and (user.userTypeBits & User.USER_TYPE_CANDIDATE):
        extraData['userProjects'] = [getSerializedUserProject(up) for up in UserProjectView.getUserProjects(userId=user.id)]

    return render(request, 'project.html', context={'data': dumps({**baseData, **extraData})})


def projects(request):
    jobMapByRole = JobPostingView.getJobMapByRole()

    return render(request, 'projects.html', context={'data': dumps({
        'projects': [{
            **getSerializedProject(p),
            'jobs': jobMapByRole[p.role_id]
        } for p in ProjectView.getProjects()],
        'roles': [getSerializedRole(r) for r in Role.objects.all()],
        'skills': [getSerializedSkill(s) for s in Skill.objects.all()]
    })})


def signUp(request):
    return render(request, 'signUp.html')


def signUpEmployer(request, type=None):
    return render(request, 'signUpEmployer.html', context={
        'data': dumps({'isStarter': type == 'prove'}),
        'isStarter': type == 'prove'
    })


def termsOfService(request):
    return render(request, 'termsOfService.html', context={})


def userProject(request, userProjectId=None):
    user = security.getSessionUser(request)
    if not user or not security.isPermittedSessionUser(user=user):
        return _getUnauthorizedPage(request)

    userProject = UserProjectView.getUserProjects(userProjectId=userProjectId)
    if not (security.isSelf(userProject.user_id, user=user) or user.isEmployer or user.isAdmin):
        return _getUnauthorizedPage(request)

    employerId = None if user.isAdmin else user.employer_id

    data = {
        'userProject': getSerializedUserProject(userProject, employerId=employerId, isIncludeEvaluation=True),
        'project': getSerializedProject(
            ProjectView.getProject(userProject.customProject.project_id),
            isIncludeDetails=True,
            isAdmin=user.isAdmin,
            evaluationEmployerId=employerId
        )
    }

    return render(request, 'userProject.html', context={
        'data': dumps(data),
    })


def _getUnauthorizedPage(request):
    # If the user is logged in, they are truly unauthorized
    if security.getSessionUser(request):
        return _getErrorPage(request, HTTPStatus.UNAUTHORIZED, 'You do not have permission to view this account')
    else:
        return HttpResponseRedirect(f'/login-page/?next={request.path}')


def _getErrorPage(request, errorStatus, errorMessage):
    return render(request, 'errors.html', {
        'data': dumps({'error': errorStatus, 'text': errorMessage})})
