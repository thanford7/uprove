from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.urls import path, re_path

from upapp import views
from upapp import viewsAuth
from upapp.apis import blog, employer, lever, locations, project, sendEmail, storage, tag, teachable, training, user
from upapp.sitemaps import sitemaps

apiPath = 'api/v1/'

urlpatterns = [
    # Views
    path('', views.homepage, name='index'),
    path('admin/', views.admin, name='admin'),
    path('account-settings/<int:userId>/', views.accountSettings, name='accountSettings'),
    re_path('^blog/(?P<blogId>[0-9]+)?/?$', views.blog, name='blog'),
    path('candidate-board/', views.candidateBoard, name='candidateBoard'),
    re_path('^candidateDashboard/(?P<userId>[0-9]+)?/?$', views.candidateDashboard, name='candidateDashboard'),
    path('candidateOnboard/', views.candidateOnboard, name='candidateOnboard'),
    path('contact/', views.contact, name='contact'),
    path('courses/', views.courses, name='courses'),
    path('credits/', views.credits, name='credits'),
    re_path('^employerDashboard/(?P<employerId>[0-9]+)?/?$', views.employerDashboard, name='employerDashboard'),
    path('employers/', views.employers, name='employers'),
    path('errors/', views.errors, name='errors'),
    path('jobs/', views.jobs, name='jobs'),
    re_path('^job-posting/(?P<jobId>[0-9]+)/(?P<employerId>[0-9]+)?/?$', views.jobPosting, name='jobPosting'),
    path('login-page/', views.login, name='loginPage'),
    path('privacy/', views.privacy, name='privacy'),
    path('profile/<int:profileId>/', views.profile, name='profile'),
    path('project/<int:projectId>/', views.project, name='project'),
    re_path('^projects/$', views.projects, name='projects'),
    path('sign-up/', views.signUp, name='signUp'),
    re_path('^sign-up/employer/(?P<type>[a-z]+)?/?$', views.signUpEmployer, name='signUpEmployer'),
    path('terms-of-service/', views.termsOfService, name='termsOfService'),
    re_path('^user-project/(?P<userProjectId>[0-9]+)?/?$', views.userProject, name='userProject'),

    # Sales views
    path('mentor/', views.salesMentor, name="salesMentor"),

    # APIs
    re_path(apiPath + 'account-employer/(?P<employerId>[0-9]+)?/?$', employer.EmployerView.as_view()),
    re_path(apiPath + 'account-user/(?P<userId>[0-9]+)?/?$', user.UserView.as_view()),
    re_path(apiPath + 'blog/(?P<blogId>[0-9]+)?/?$', blog.BlogPostView.as_view()),
    re_path(apiPath + 'course/(?P<courseId>[0-9]+)?/?$', training.TrainingCourseView.as_view()),
    re_path(apiPath + 'job-posting/(?P<jobId>[0-9]+)?/?$', employer.JobPostingView.as_view()),
    re_path(apiPath + 'locations/$', locations.LocationView.as_view()),
    re_path(apiPath + 'organization/$', employer.OrganizationView.as_view()),
    re_path(apiPath + 'preferences/$', user.PreferencesView.as_view()),
    re_path(apiPath + 'project/(?P<projectId>[0-9]+)?/?$', project.ProjectView.as_view()),
    re_path(apiPath + 'project-role/(?P<roleId>[0-9]+)?/?$', project.RoleView.as_view()),
    re_path(apiPath + 'project-skill/(?P<skillId>[0-9]+)?/?$', project.SkillView.as_view()),
    re_path(apiPath + 'tag/$', tag.TagView.as_view()),
    re_path(apiPath + 'user-job-application/(?P<userJobApplicationId>[0-9]+)?/?$', user.UserJobApplicationView.as_view()),
    re_path(apiPath + 'user-job-rec/$', user.UserJobSuggestions.as_view()),
    re_path(apiPath + 'user-preferences/?$', user.UserPreferenceView.as_view()),
    re_path(apiPath + 'user-profile/$', user.UserProfileView.as_view()),
    re_path(apiPath + 'user-profile/content-item/$', user.UserProfileContentItemView.as_view()),
    re_path(apiPath + 'user-profile/section/$', user.UserProfileSectionView.as_view()),
    re_path(apiPath + 'user-profile/section/content-item/$', user.UserProfileSectionContentItemView.as_view()),
    re_path(apiPath + 'user-project/(?P<userProjectId>[0-9]+)?/?$', user.UserProjectView.as_view()),
    re_path(apiPath + 'user-project/status/?$', user.UserProjectStatusView.as_view()),
    re_path(apiPath + 'user-project-evaluation/$', employer.UserProjectEvaluationView.as_view()),
    re_path(apiPath + 'user-file/$', user.UserFileView.as_view()),
    re_path(apiPath + 'user-image/$', user.UserImageView.as_view()),
    re_path(apiPath + 'user-video/$', user.UserVideoView.as_view()),
    re_path(apiPath + 'waitlist/$', user.WaitlistView.as_view()),

    # Email
    path(apiPath + 'email/', sendEmail.EmailView.as_view()),

    # Authentication
    path(apiPath + 'login/', viewsAuth.LoginView.as_view()),
    path(apiPath + 'logout/', viewsAuth.LogoutView.as_view()),
    path(apiPath + 'setPassword/', viewsAuth.SetPasswordView.as_view()),
    re_path('password-reset-email/(?P<uidb64>[\S]+)?/(?P<token>[\S]+)?/$', viewsAuth.PasswordResetView.as_view(template_name='passwordReset.html'), name='passwordReset'),
    path(apiPath + 'password-reset-generate/', viewsAuth.PasswordResetGenerateView.as_view(), name='passwordResetSend'),
    path('password-reset-complete/', viewsAuth.LoginPageView.as_view(template_name='login.html'), name='password-reset-complete'),
    path('login/', viewsAuth.LoginPageView.as_view(template_name='login.html'), name='login'),

    # Lever
    re_path('^integrate/?$', lever.leverIntegrate, name='leverIntegrate'),

    re_path(f'^{apiPath}lever/logout/(?P<employerId>[0-9]+)?/?$', lever.LeverLogOut.as_view()),
    re_path(f'^{apiPath}lever/opportunities/(?P<employerId>[0-9]+)?/?$', lever.LeverOpportunities.as_view()),
    re_path(f'^{apiPath}lever/postings/(?P<employerId>[0-9]+)?/?$', lever.LeverPostings.as_view()),
    re_path(f'^{apiPath}lever/stages/(?P<employerId>[0-9]+)?/?$', lever.LeverStages.as_view()),
    re_path(f'^{apiPath}lever/users/(?P<employerId>[0-9]+)?/?$', lever.LeverUsers.as_view()),

    re_path(f'^{apiPath}lever/change/stage-change/(?P<employerId>[0-9]+)?/?$', lever.LeverChangeStage.as_view()),
    re_path(f'^{apiPath}lever/change/archive/(?P<employerId>[0-9]+)?/?$', lever.LeverArchive.as_view()),
    re_path(f'^{apiPath}lever/change/hire/(?P<employerId>[0-9]+)?/?$', lever.LeverHired.as_view()),
    re_path(f'^{apiPath}lever/change/delete/(?P<employerId>[0-9]+)?/?$', lever.LeverDeleted.as_view()),
    re_path(f'^{apiPath}lever/config/(?P<employerId>[0-9]+)?/?$', lever.LeverConfig.as_view()),

    # Teachable
    re_path(f'^{apiPath}teachable/enroll/?$', teachable.TeachableEnrolled.as_view()),
    re_path(f'^{apiPath}teachable/progress/?$', teachable.TeachableCourseProgress.as_view()),

    # Storage
    path(apiPath + 'user-storage/', storage.UserStorageView.as_view()),

    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
]

if settings.USE_LOCAL:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
