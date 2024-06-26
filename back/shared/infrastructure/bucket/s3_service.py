from typing import Optional

from settings import boto3_session, config, logger


class S3Service:
    def __init__(self) -> None:
        self._boto3_client = boto3_session.client('s3')

    def retrieve(
        self,
        bucket_name: str,
        object_name: str,
    ) -> str:
        logger.info(f'Getting object {bucket_name}/{object_name}')
        return self._boto3_client.get_object(
            Bucket=config.get('bucket', bucket_name),
            Key=object_name
        )['Body']
