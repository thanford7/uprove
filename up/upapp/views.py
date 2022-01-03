from http import HTTPStatus
from json import dumps

from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render

from upapp import security
from upapp.modelSerializers import *
from upapp.apis.blog import BlogPostView
from upapp.apis.employer import EmployerView, JobPostingView
from upapp.apis.project import ProjectView
from upapp.apis.user import UserJobApplicationView, UserView, UserProfileView, UserProjectView
from upapp.models import ProjectFunction, ProjectSkill


# Create your views here.
def homepage(request):
    return render(request, 'home.html', {'data': dumps({
        'functions': [getSerializedProjectFunction(f) for f in ProjectFunction.objects.all()],
        'skills': [getSerializedProjectSkill(s) for s in ProjectSkill.objects.all()]
    })})


def about(request):
    return render(request, 'about.html', context={})


def accountSettings(request, userId):
    if not security.isSelf(request, userId):
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
        'projects': [getSerializedProject(p, isIncludeDetails=True) for p in ProjectView.getProjects(isIgnoreEmployerId=True)],
        # TODO: Lazy load employers and users since this will get long
        'employers': [getSerializedEmployer(e, isEmployer=True) for e in EmployerView.getEmployers()],
        'users': [getSerializedUser(u) for u in UserView.getUsers()],
        'functions': [getSerializedProjectFunction(f) for f in ProjectFunction.objects.all()],
        'skills': [getSerializedProjectSkill(s) for s in ProjectSkill.objects.all()]
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
        return render(request, 'blogSingle.html', {'data': dumps(data)})

    return render(request, 'blog.html', {'data': dumps(data)})


def candidateDashboard(request, userId=None):
    user = security.getSessionUser(request)
    if not user:
        return _getUnauthorizedPage(request)

    userId = userId or user['id']
    if not userId:
        return _getErrorPage(request, HTTPStatus.BAD_REQUEST, 'A user ID is required')

    if not security.isSelf(request, userId):
        return _getUnauthorizedPage(request)

    return render(request, 'candidateDashboard.html', context={'data': dumps({
        'user': getSerializedUser(UserView.getUser(userId), isIncludeAssets=True),
        'userProjects': [getSerializedUserProject(up) for up in UserProjectView.getUserProjects(userId=userId)],
        'jobApplications': [getSerializedJobApplication(ja, includeJob=True) for ja in UserJobApplicationView.getUserJobApplications(userId=userId)]
    })})


def contact(request):
    return render(request, 'contact.html', context={})


def employerDashboard(request, employerId=None):
    user = security.getSessionUser(request)
    if not user:
        return _getUnauthorizedPage(request)

    employerId = employerId or user['employerId']
    if not employerId:
        return _getErrorPage(request, HTTPStatus.BAD_REQUEST, 'An employer ID is required')

    if not security.isPermittedEmployer(request, employerId):
        return _getUnauthorizedPage(request)

    return render(request, 'employerDashboard.html', context={'data': dumps({
        'employer': getSerializedEmployer(EmployerView.getEmployer(employerId), isEmployer=True),
        'projects': [getSerializedProject(p, isIncludeDetails=True) for p in ProjectView.getProjects(employerId=employerId)],
    })})


def errors(request):
    return render(request, 'errors.html', context={})


def jobPosting(request, jobId):
    job = JobPostingView.getEmployerJobs(jobId=jobId)
    projects = ProjectView.getProjects(employerId=job.employer_id, projectIds=[p.project_id for p in job.allowedProjects.all()])
    isEmployer = security.isPermittedEmployer(request, job.employer_id)
    return render(request, 'jobPosting.html', context={'data': dumps({
        'job': getSerializedEmployerJob(job, isEmployer=isEmployer),
        'employer': getSerializedEmployer(EmployerView.getEmployer(job.employer_id), isEmployer=isEmployer),
        'projects': {p.id: getSerializedProject(p, isIncludeDetails=True) for p in projects},
        'functions': [getSerializedProjectFunction(f) for f in ProjectFunction.objects.all()],
        'skills': [getSerializedProjectSkill(s) for s in ProjectSkill.objects.all()]
    })})


def login(request):
    return render(request, 'login.html')


def privacy(request):
    return render(request, 'privacy.html', context={})


def profile(request, profileId):
    profile = UserProfileView.getUserProfile(profileId)
    return render(request, 'userProfile.html', context={'data': UserProfileView.serializeUserProfile(profile)})


def profiles(request, userId):
    userProfiles = UserView.getUserProfiles(userId)
    if len(profiles := userProfiles.profile.all()) == 1:
        return render(request, 'userProfile.html', context={'data': UserProfileView.serializeUserProfile(profiles[0])})
    return render(request, 'userProfiles.html', context={'data': None})  # TODO


def project(request, projectId):
    baseData = {
        'project': getSerializedProject(ProjectView.getProject(projectId), isIncludeDetails=security.isPermittedSessionUser(request)),
        'functions': [getSerializedProjectFunction(f) for f in ProjectFunction.objects.all()],
        'skills': [getSerializedProjectSkill(s) for s in ProjectSkill.objects.all()]
    }

    extraData = {}
    user = security.getSessionUser(request)
    if user and (employerId := user['employerId']):
        extraData['jobs'] = [getSerializedEmployerJob(j, isEmployer=False) for j in JobPostingView.getEmployerJobs(employerId=employerId)]

    if user and (user['userTypeBits'] & User.USER_TYPE_CANDIDATE):
        extraData['userProjects'] = [getSerializedUserProject(up) for up in UserProjectView.getUserProjects(userId=user['id'])]

    return render(request, 'project.html', context={'data': dumps({**baseData, **extraData})})


def projects(request):
    return render(request, 'projects.html', context={'data': dumps({
        'projects': [getSerializedProject(p) for p in ProjectView.getProjects()],
        'functions': [getSerializedProjectFunction(f) for f in ProjectFunction.objects.all()],
        'skills': [getSerializedProjectSkill(s) for s in ProjectSkill.objects.all()]
    })})


def termsOfService(request):
    return render(request, 'termsOfService.html', context={})


def _getUnauthorizedPage(request):
    # If the user is logged in, they are truly unauthorized
    if security.getSessionUser(request):
        return _getErrorPage(request, HTTPStatus.UNAUTHORIZED, 'You do not have permission to view this account')
    else:
        return HttpResponseRedirect(f'/login-page/?next={request.path}')


def _getErrorPage(request, errorStatus, errorMessage):
    return render(request, 'errors.html', {
        'data': dumps({'error': errorStatus, 'text': errorMessage})})
