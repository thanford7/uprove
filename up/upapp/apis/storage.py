from http import HTTPStatus

import boto3
from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from upapp import security
from upapp.models import User


class BaseStorageHandler:
    #  Prefixes for upload buckets
    #  Keep in sync with buckets created on DigitalOcean
    STORAGE_TYPE = None
    PERMISSION_LEVEL_READ = 'READ'
    PERMISSION_LEVEL_RW ='READ-WRITE'

    def __init__(self, user: User):
        if not user:
            raise PermissionError('You are not permitted to complete this action')

        self.folderKey = f'uploads-{self.STORAGE_TYPE}{"-test/" if settings.DEBUG else "/"}'
        self.user = user
        self.permissionLevel = self.PERMISSION_LEVEL_READ
        self.setPermissionLevel()
        session = boto3.session.Session()
        self.client = session.client(
            's3',
            region_name='nyc3',
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID if self.permissionLevel == self.PERMISSION_LEVEL_RW else settings.AWS_ACCESS_KEY_ID_READ_ONLY,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY if self.permissionLevel == self.PERMISSION_LEVEL_RW else settings.AWS_SECRET_ACCESS_KEY_READ_ONLY
        )
        self.folderContents = self.client.list_objects(Bucket='uprove-upload', Prefix=self.folderKey)['Contents']

    def setPermissionLevel(self):
        raise NotImplemented('Implement in subclass')

    def getAccessKeyId(self):
        return


class CanidateStorageHandler(BaseStorageHandler):
    STORAGE_TYPE = 'candidate'


class EmployerStorageHandler(BaseStorageHandler):
    STORAGE_TYPE = 'employer'


class ProjectStorageHandler(BaseStorageHandler):
    STORAGE_TYPE = 'project'

    def setPermissionLevel(self):
        if self.user.djangoUser.is_superuser:
            self.permissionLevel = self.PERMISSION_LEVEL_RW


class UserStorageView(APIView):
    # TODO: Add a permission class for upload
    permission_classes = [AllowAny]

    def get(self, request):
        if not (user := security.getSessionUser(request)):
            return Response(status=HTTPStatus.UNAUTHORIZED)
        storageHandler = ProjectStorageHandler(user)
        return Response(status=HTTPStatus.OK)
