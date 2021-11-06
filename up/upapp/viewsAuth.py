from http import HTTPStatus

from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.backends import ModelBackend, UserModel
from django.db.models import Q
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        if not email or not password:
            return Response(status=HTTPStatus.BAD_REQUEST)

        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/projects/')  # TODO: Update to go to profile or business page depending on user
        else:
            return Response(status=HTTPStatus.UNAUTHORIZED, data='Invalid username or password.')


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
