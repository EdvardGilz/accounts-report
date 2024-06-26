from typing import Any

from helpers.exceptions import exception_handler
from shared.types import MappingType

from .application.create import UppyFilesCreator
from .entry_point_types import UppyFilesCreatorContainerType
from .infrastructure.bucket import BucketService


def _get_uppy_files_creator_container():
    return UppyFilesCreatorContainerType(
        bucket_service=BucketService(),
    )


@exception_handler('create_uppy_files_handler')
def create_uppy_files_handler(event: MappingType, _: Any):
    '''
    # Test in local with:

    python aws_lambda_wrapper.py '{"stage": "get_upload_parameters", \
    "data": {"filename": "img_1.png", "metadata[name]": "img_1.png", \
    "metadata[type]": "image/png", "type": "image/png"}}' \
    --function create_uppy_files_handler

    python aws_lambda_wrapper.py '{"stage": "create_multipart_upload", \
    "data": {"filename": "img_1.png", "metadata[name]": "img_1.png", \
    "metadata[type]": "image/png", "type": "image/png"}}' \
    --function create_uppy_files_handler

    python aws_lambda_wrapper.py '{"stage": "sign_part_upload", "data": \
    {"uploadId": "SpYU_1A-", "partNumber": "2", \
    "key": "file_name.mp4"}}' --function create_uppy_files_handler

    python aws_lambda_wrapper.py '{"stage": "complete_multipart_upload", \
    "data": {"uploadId": "SpYU_1A-", "key": "file_name.mp4", \
    "body": {"parts": [{"PartNumber": 1, "ETag": \
    "60aa894dee15bd97b208a5683331471c"}, {"PartNumber": 2, \
    "ETag": "6fa055b69f9a4cc2efabce24d3adb315"}]}}}' \
    --function create_uppy_files_handler
    '''
    return UppyFilesCreator(
        container=_get_uppy_files_creator_container(),
    ).run(event)
