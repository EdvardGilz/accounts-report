from botocore.exceptions import ClientError
from settings import boto3_session, config
from shared.types import ListMappingType


class BucketService:
    def __init__(self) -> None:
        self._s3 = boto3_session.client('s3')
        self._config = {
            'bucket_name': config.get('bucket', 'uppy_files_bucket_name'),
            'expiration_seconds': 300
        }

    def generate_presigned_post(self, key: str):
        try:
            response = self._s3.generate_presigned_post(
                Bucket=self._config['bucket_name'],
                Key=key,
                ExpiresIn=self._config['expiration_seconds'],
                Fields={'key': key},
            )

            return {
                'method': 'post',
                'url': response['url'],
                'fields': response['fields']
            }
        except ClientError as error:
            return {'error': str(error)}

    def create_multipart_upload(self, key: str, content_type: str):
        try:
            response = self._s3.create_multipart_upload(
                Bucket=self._config['bucket_name'],
                Key=key,
                ContentType=content_type,
                Expires=self._config['expiration_seconds']
            )
            return {'key': response['Key'], 'uploadId': response['UploadId']}
        except ClientError as error:
            return {'error': str(error)}

    def generate_presigned_url(
        self,
        key: str,
        upload_id: str,
        part_number: int
    ):
        try:
            url = self._s3.generate_presigned_url(
                'upload_part',
                ExpiresIn=self._config['expiration_seconds'],
                Params={
                    'Bucket': self._config['bucket_name'],
                    'Key': key,
                    'UploadId': upload_id,
                    'PartNumber': part_number,
                    'Body': '',
                }
            )

            return {'url': url}
        except ClientError as error:
            return {'error': str(error)}

    def complete_multipart_upload(
        self,
        key: str,
        upload_id: str,
        parts: ListMappingType
    ):
        try:
            response = self._s3.complete_multipart_upload(
                Bucket=self._config['bucket_name'],
                Key=key,
                UploadId=upload_id,
                MultipartUpload={
                    'Parts': parts
                }
            )

            return {'location': response['Location']}
        except ClientError as error:
            return {'error': str(error)}
