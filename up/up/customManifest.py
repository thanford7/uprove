import logging

from storages.backends.s3boto3 import S3ManifestStaticStorage

logger = logging.getLogger()


class S3ManifestStaticStorageWithLog(S3ManifestStaticStorage):
    def load_manifest(self):
        logger.info(self.read_manifest())
        return super(S3ManifestStaticStorageWithLog, self).load_manifest()