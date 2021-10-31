from http import HTTPStatus

from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
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

        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('')
        else:
            return Response(status=HTTPStatus.UNAUTHORIZED, data='Invalid username or password.')
