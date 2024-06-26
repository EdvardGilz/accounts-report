from typing import Any

import pandas as pd
from botocore.exceptions import ClientError
from settings import IS_MOCK
from shared.infrastructure.bucket import S3Service
from shared.messages_conts import EMPTY_FILE_MSG, FILE_ERROR_MSG
from shared.mock import MockResponses
from shared.types import MappingType


class BucketService(S3Service, MockResponses):
    def __init__(self) -> None:
        super().__init__()
        self._pd: Any = pd

    def get_file_data(self) -> MappingType:
        if IS_MOCK:
            return {
                'data': self._pd.DataFrame(
                    self._get_mock_response('_file_data')
                )
            }

        try:
            file_data = self.retrieve(
                bucket_name='uppy_files_bucket_name',
                object_name='account_file.csv'
            )
            df_file_data = self._pd.read_csv(file_data)
        except ClientError:
            return {'error': FILE_ERROR_MSG}
        except pd.errors.EmptyDataError:
            return {'error': EMPTY_FILE_MSG}

        return {'data': df_file_data}
