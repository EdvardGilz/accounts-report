from typing import Any

import pytest
from report.entry_point import create_report_handler


@pytest.mark.parametrize(
    'email, user_name, expected_result',
    [
        (
            'eduardo.michell94@gmail.com', 'Eduardo Giles',
            {'report_sent': True}
        ),
        (
            '', 'Eduardo Giles',
            {'report_sent': False, 'error': {'required': ['email']}}
        ),
        (
            'eduardo.michell94@gmail.com', '',
            {'report_sent': False, 'error': {'required': ['user_name']}}
        ),
        (
            '', '',
            {
                'report_sent': False,
                'error': {'required': ['user_name', 'email']}
            }
        ),
        (
            None, None,
            {
                'report_sent': False,
                'error': {'required': ['user_name', 'email']}
            }
        ),
    ]
)
def test_create_report(
    email: str,
    user_name: str,
    expected_result: Any
):
    command_arguments: Any = dict(
        event={'email': email, 'user_name': user_name},
        _=None
    )

    assert create_report_handler(**command_arguments) == expected_result
