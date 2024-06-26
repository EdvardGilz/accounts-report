# pylint: disable=missing-module-docstring,missing-class-docstring
# pylint: disable=relative-beyond-top-level,missing-function-docstring
from decimal import Decimal
from typing import Any

from settings import logger
from typing_extensions import Literal

from ..types.common_types import ListMappingType

RESPONSES_LIST = Literal[
    '_file_data', '_account_data',
]


class MockResponses:
    @staticmethod
    def _file_data() -> ListMappingType:
        return [
            {'id': 0, 'date': '10/02/2024', 'transaction': 12.5},
            {'id': 1, 'date': '9/03/2024', 'transaction': -12.5},
            {'id': 2, 'date': '5/04/2024', 'transaction': 35.6},
            {'id': 3, 'date': '4/05/2024', 'transaction': -60.0},
            {'id': 4, 'date': '3/06/2024', 'transaction': -20.0},
            {'id': 5, 'date': '11/07/2024', 'transaction': 100.0}
        ]

    @staticmethod
    def _account_data() -> ListMappingType:
        return [
            {
                'id': 0,
                'date': '10/02/2024',
                'transaction': Decimal('12.5'),
                'account_id': 1
            },
            {
                'id': 1,
                'date': '9/02/2024',
                'transaction': Decimal('-12.5'),
                'account_id': 1
            }, {
                'id': 2,
                'date': '5/02/2024',
                'transaction': Decimal('35.6'),
                'account_id': 1
            }, {
                'id': 3,
                'date': '4/05/2024',
                'transaction': Decimal('-60.0'),
                'account_id': 1
            }, {
                'id': 4,
                'date': '3/06/2024',
                        'transaction': Decimal('-20.0'),
                'account_id': 1
            }, {
                'id': 5,
                'date': '11/07/2024',
                'transaction': Decimal('100.0'),
                'account_id': 1
            }
        ]

    def _get_mock_response(self, function_name: RESPONSES_LIST):
        self.print_mock_response()
        logger.info('Getting mock data')
        _function: Any = getattr(self, function_name, None)
        return _function()

    @staticmethod
    def print_mock_response():
        logger.info('<--- Mock request --->')
