from http import HTTPStatus

import boto3
from botocore.client import Config

from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


def getStorageSession():
    session = boto3.session.Session()
    client = session.client('s3',
                            region_name='nyc3',
                            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

    # List all buckets on your account.
    response = client.list_buckets()
    spaces = [space['Name'] for space in response['Buckets']]
    print("Spaces List: %s" % spaces)


class UserStorageView(APIView):
    # TODO: Add a permission class for upload
    permission_classes = [AllowAny]

    def get(self, request):
        getStorageSession()
        return Response(status=HTTPStatus.OK)
