import logging
import re
from http import HTTPStatus
from json import dumps

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, views as viewsDjangoAuth
from django.contrib.auth.backends import ModelBackend, UserModel
from django.contrib.auth.views import PasswordResetConfirmView
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework.response import Response
from rest_framework.views import APIView

from upapp.apis import UproveAPIView, ActivityKey, saveActivity, hasCompletedActivity
from upapp.apis.user import UserView
from upapp.models import User
from upapp.modelSerializers import getSerializedUser

logger = logging.getLogger()


def logoutUser(request):
    logout(request)
    request.session['uproveUser'] = None


def setUproveUser(request, user):
    try:
        uproveUser = User.objects.select_related('djangoUser').prefetch_related('profile').get(djangoUser=user)
        request.session['uproveUser'] = getSerializedUser(uproveUser)
    except User.DoesNotExist:
        msg = 'No Uprove user exists for this Django user'
        logger.error(msg)
        messages.error(request, msg)
        return msg


def updateUproveUser(request):
    if userData := request.session['uproveUser']:
        uproveUser = User.objects.select_related('djangoUser').prefetch_related('profile').get(id=userData['id'])
        request.session['uproveUser'] = getSerializedUser(uproveUser)


def getLoginRedirectUrl(request):
    if not isinstance(request, WSGIRequest):
        pageRedirect = request.data.get('redirect')
        if pageRedirect and not re.match('^/[#]?$', pageRedirect):
            return pageRedirect
    pageRedirect = '/projects/'
    uproveUser = request.session['uproveUser']

    # Send user to the onboarding page if they are new
    if (
        uproveUser['userTypeBits'] & User.USER_TYPE_CANDIDATE
        and not hasCompletedActivity(ActivityKey.VIEW_PROJECT_SELECTION, uproveUser['id'])
    ):
        pageRedirect = '/candidateOnboard/'
        saveActivity(ActivityKey.VIEW_PROJECT_SELECTION, uproveUser['id'])
    elif uproveUser['isSuperUser']:
        pageRedirect = '/admin/'
    elif uproveUser['userTypeBits'] & User.USER_TYPE_CANDIDATE:
        pageRedirect = '/candidateDashboard/'
    elif uproveUser['userTypeBits'] & User.USER_TYPE_EMPLOYER:
        pageRedirect = '/employerDashboard/'

    return pageRedirect


class LoginPageView(viewsDjangoAuth.LoginView):

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        setUproveUser(self.request, user)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return getLoginRedirectUrl(self.request)


class LoginView(APIView):

    def post(self, request):
        logger.info('Hit login')
        email = request.data['email']
        password = request.data['password']
        if not email or not password:
            return Response(status=HTTPStatus.BAD_REQUEST)

        logger.info('About to authenticate')
        user = authenticate(username=email, password=password)
        return self.loginUser(request, user)

    @staticmethod
    def loginUser(request, user):
        if user is not None:
            login(request, user)
            if errorMsg := setUproveUser(request, user):
                return Response(status=HTTPStatus.UNAUTHORIZED, data=errorMsg)

            return Response(status=HTTPStatus.OK,
                            data={'pageRedirect': request.data.get('next') or getLoginRedirectUrl(request)})
        else:
            msg = 'Invalid username or password.'
            messages.error(request, msg)
            return Response(status=HTTPStatus.UNAUTHORIZED, data=msg)


class LogoutView(APIView):

    def post(self, request):
        logoutUser(request)
        return Response(status=HTTPStatus.OK, data={'pageRedirect': '/'})


class PasswordResetGenerateView(UproveAPIView):
    def post(self, request):
        UserView.sendPasswordResetEmail(request, self.data['email'], {
            'subject_template_name': 'email/resetPasswordEmailSubject.txt',
            'email_template_name': 'email/resetPasswordBody.html',
            'html_email_template_name': 'email/resetPassword.html',
            'extra_email_context': {
                'supportEmail': 'community@uprove.co',
                'isNew': False,
                'next': None
            }
        })
        return Response(status=HTTPStatus.OK, data=self.data['email'])


class PasswordResetView(PasswordResetConfirmView):
    """Render the page for the user to set password
    """

    def setup(self, *args, **kwargs):
        params = args[0].GET

        # Need to persist in session because Django redirects the URL
        if params:
            args[0].session['isNewUser'] = params.get('isnew') == 'True'
            args[0].session['next'] = params.get('next')
        super().setup(*args, **kwargs)

    def get_user(self, uidb64):
        # logoutUser(self.request)  # Logout the user if they were logged in when they made the request to reset
        user = super().get_user(uidb64)
        setUproveUser(self.request, user)
        return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sessionData = self.request.session
        isNewUser = sessionData.get('isNewUser')
        context['data'] = dumps({'isNew': isNewUser, 'next': sessionData.get('next')})

        # Remove session variables that are no longer needed
        if 'isNewUser' in sessionData:
            del sessionData['isNewUser']
        if 'next' in sessionData:
            del sessionData['next']

        if isNewUser:
            saveActivity(
                ActivityKey.CREATE_ACCOUNT,
                User.objects.select_related('djangoUser').get(djangoUser=self.user).id
            )
        return context


class SetPasswordView(APIView):
    """API to set password once user has submitted the form
    """

    def post(self, request):
        request.session['uproveUser'] = None
        uproveUserId = request.data['uproveUserId']
        newPassword = request.data['password']

        if not uproveUserId:
            return Response('The reset link you used may have expired. Use the \'reset password\' link from the Sign in form to get a new link.', status=HTTPStatus.UNAUTHORIZED)
        if not newPassword:
            return Response('Please provide a valid password', status=HTTPStatus.BAD_REQUEST)

        djangoUser = UserView.getUser(uproveUserId).djangoUser
        djangoUser.set_password(newPassword)
        djangoUser.save()

        return LoginView.loginUser(request, djangoUser)


class EmailAuthentication(ModelBackend):
    """Allow user authentication by either username or email
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            user = UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None
