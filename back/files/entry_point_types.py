from typing import NamedTuple

from .infrastructure.bucket import BucketService


class UppyFilesCreatorContainerType(NamedTuple):
    bucket_service: BucketService
