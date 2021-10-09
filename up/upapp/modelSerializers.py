from datetime import datetime

import six
from rest_framework import serializers
from models import *


# See link for explanation of meta class mixin
# https://github.com/encode/django-rest-framework/issues/4482
@six.add_metaclass(serializers.SerializerMetaclass)
class AuditSerializerMixin:
    createdDateTime = serializers.DateTimeField(initial=datetime.now())
    modifiedDateTime = serializers.DateTimeField(default=datetime.now(), initial=datetime.now())


class UserSerializer(AuditSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserProfileSerializer(AuditSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        depth = 1


class UserProfileSectionSerializer(AuditSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = UserProfileSection
        fields = '__all__'
        depth = 1


class UserProfileSectionItemSerializer(AuditSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = UserProfileSectionItem
        fields = '__all__'
        depth = 1


class UserEducationSerializer(AuditSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = UserEducation
        fields = '__all__'
        depth = 1


class UserContentItemSerializer(AuditSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = UserContentItem
        fields = '__all__'
        depth = 1


class UserContentItemSectionSerializer(AuditSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = UserContentItemSection
        fields = '__all__'
        depth = 1


class UserVideoSerializer(AuditSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = UserVideo
        fields = '__all__'
        depth = 1


class UserFileSerializer(AuditSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = UserFile
        fields = '__all__'
        depth = 1


class UserImageSerializer(AuditSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = '__all__'
        depth = 1


class UserTagSerializer(AuditSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = UserTag
        fields = '__all__'
        depth = 1


class OrganizationSerializer(AuditSerializerMixin, serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'
        depth = 1