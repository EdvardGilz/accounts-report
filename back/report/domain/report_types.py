from dataclasses import field
from typing import Any

from marshmallow import pre_load, validate


class EventType:
    @pre_load
    def change_empty_string_to_none(self, data: Any, **_: Any):
        for key, value in data.items():
            data[key] = value if value != '' else None
        return data

    email: str = field(
        metadata={
            'required': True,
            'validate': validate.Email(error='invalid'),
            'error_messages': {'null': 'required', 'required': 'required'}
        }
    )
    user_name: str = field(
        metadata={
            'error_messages': {'null': 'required', 'required': 'required'}
        }
    )
