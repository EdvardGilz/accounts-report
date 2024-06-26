from settings import logger
from shared.types import ListMappingType, MappingType

from ...entry_point_types import UppyFilesCreatorContainerType


class UppyFilesCreator:
    def __init__(self, container: UppyFilesCreatorContainerType) -> None:
        self._bucket_service = container.bucket_service

    def _get_upload_parameters(self, event_data: MappingType):
        logger.info('get_upload_parameters')
        key = event_data.get('filename', '')

        return self._bucket_service.generate_presigned_post(key)

    def _create_multipart_upload(self, event_data: MappingType):
        logger.info('create_multipart_upload')
        key = event_data.get('filename', '')
        content_type = event_data.get('type', '')

        return self._bucket_service.create_multipart_upload(
            key=key,
            content_type=content_type,
        )

    def _sign_part_upload(self, event_data: MappingType):
        logger.info('sign_part_upload')
        key = event_data.get('key', '')
        part_number = int(event_data.get('partNumber', '0'))
        upload_id = event_data.get('uploadId', '')

        return self._bucket_service.generate_presigned_url(
            key=key,
            part_number=part_number,
            upload_id=upload_id,
        )

    def _complete_multipart_upload(self, event_data: MappingType):
        logger.info('complete_multipart_upload')
        key = event_data.get('key', '')
        upload_id = event_data.get('uploadId', '')
        parts: ListMappingType = event_data.get('body', {}).get('parts', [])

        return self._bucket_service.complete_multipart_upload(
            key=key,
            upload_id=upload_id,
            parts=parts,
        )

    def run(self, event: MappingType):
        stage_to_function = {
            'get_upload_parameters': self._get_upload_parameters,
            'create_multipart_upload': self._create_multipart_upload,
            'sign_part_upload': self._sign_part_upload,
            'complete_multipart_upload': self._complete_multipart_upload,
        }
        stage = event.get('stage', '')
        if stage in stage_to_function:
            return stage_to_function[stage](event.get('data', {}))
        return {'error': 'Invalid stage'}
