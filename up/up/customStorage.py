import logging

from django.core.files.storage import FileSystemStorage
from storages.backends.s3boto3 import S3Boto3Storage, S3ManifestStaticStorage

logger = logging.getLogger()


class S3ManifestStaticStorageWithLog(S3ManifestStaticStorage):
    def load_manifest(self):
        return super(S3ManifestStaticStorageWithLog, self).load_manifest()


class MediaStorage(S3Boto3Storage):
    location = 'media'


class OverwriteStorage(FileSystemStorage):

    def _save(self, name, content):
        self.delete(name)
        return super(OverwriteStorage, self)._save(name, content)

    def get_available_name(self, name, max_length=None):
        return name
