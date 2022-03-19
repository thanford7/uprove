from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.urls import path, re_path

from upapp import views
from upapp import viewsAuth
from upapp.apis import blog, employer, job, project, sendEmail, storage, tag, user
from upapp.sitemaps import sitemaps

apiPath = 'api/v1/'

urlpatterns = [
    # Views
    path('', views.homepage, name='index'),
    path('about/', views.about, name='about'),
    path('admin/', views.admin, name='admin'),
    path('account-settings/<int:userId>/', views.accountSettings, name='accountSettings'),
    re_path('^blog/(?P<blogId>[0-9]+)?/?$', views.blog, name='blog'),
    path('candidate-board/', views.candidateBoard, name='candidateBoard'),
    re_path('^candidateDashboard/(?P<userId>[0-9]+)?/?$', views.candidateDashboard, name='candidateDashboard'),
    path('candidateOnboard/', views.candidateOnboard, name='candidateOnboard'),
    re_path('^candidate-project/(?P<userProjectId>[0-9]+)?/?$', views.candidateProject, name='candidateProject'),
    path('contact/', views.contact, name='contact'),
    path('credits/', views.credits, name='credits'),
    re_path('^employerDashboard/(?P<employerId>[0-9]+)?/?$', views.employerDashboard, name='employerDashboard'),
    path('employers/', views.employers, name='employers'),
    path('errors/', views.errors, name='errors'),
    path('job-posting/<int:jobId>/', views.jobPosting, name='jobPosting'),
    path('login-page/', views.login, name='loginPage'),
    path('privacy/', views.privacy, name='privacy'),
    path('profile/<int:profileId>/', views.profile, name='profile'),
    path('profiles/<int:userId>/', views.profiles, name='profiles'),
    path('project/<int:projectId>/', views.project, name='project'),
    re_path('^projects/$', views.projects, name='projects'),
    path('sign-up/', views.signUp, name='signUp'),
    re_path('^sign-up/employer/(?P<type>[a-z]+)?/?$', views.signUpEmployer, name='signUpEmployer'),
    path('terms-of-service/', views.termsOfService, name='termsOfService'),

    # APIs
    re_path(apiPath + 'account-employer/(?P<employerId>[0-9]+)?/?$', employer.EmployerView.as_view()),
    re_path(apiPath + 'account-user/(?P<userId>[0-9]+)?/?$', user.UserView.as_view()),
    re_path(apiPath + 'blog/(?P<blogId>[0-9]+)?/?$', blog.BlogPostView.as_view()),
    re_path(apiPath + 'employer-custom-project/(?P<customProjectId>[0-9]+)?/?$', employer.EmployerCustomProject.as_view()),
    re_path(apiPath + 'job-posting/(?P<jobId>[0-9]+)?/?$', employer.JobPostingView.as_view()),
    re_path(apiPath + 'job-project-link/(?P<projectId>[0-9]+)?/?$', employer.JobProjectLinkView.as_view()),
    re_path(apiPath + 'job-template/(?P<templateId>[0-9]+)?/?$', job.JobTemplateView.as_view()),
    re_path(apiPath + 'organization/$', employer.OrganizationView.as_view()),
    re_path(apiPath + 'project/(?P<projectId>[0-9]+)?/?$', project.ProjectView.as_view()),
    re_path(apiPath + 'project-role/(?P<roleId>[0-9]+)?/?$', project.RoleView.as_view()),
    re_path(apiPath + 'project-skill/(?P<skillId>[0-9]+)?/?$', project.SkillView.as_view()),
    re_path(apiPath + 'tag/$', tag.TagView.as_view()),
    re_path(apiPath + 'user-job-application/(?P<userJobApplicationId>[0-9]+)?/?$', user.UserJobApplicationView.as_view()),
    re_path(apiPath + 'user-profile/$', user.UserProfileView.as_view()),
    re_path(apiPath + 'user-profile/content-item/$', user.UserProfileContentItemView.as_view()),
    re_path(apiPath + 'user-profile/section/$', user.UserProfileSectionView.as_view()),
    re_path(apiPath + 'user-profile/section/content-item/$', user.UserProfileSectionContentItemView.as_view()),
    re_path(apiPath + 'user-project/(?P<userProjectId>[0-9]+)?/?$', user.UserProjectView.as_view()),
    re_path(apiPath + 'user-project/status/?$', user.UserProjectStatusView.as_view()),
    re_path(apiPath + 'user-project-evaluation/$', employer.UserProjectEvaluationView.as_view()),
    re_path(apiPath + 'user-video/$', user.UserVideoView.as_view()),

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

    # Storage
    path(apiPath + 'user-storage/', storage.UserStorageView.as_view()),

    # Sitemap
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
]

if settings.USE_LOCAL:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
