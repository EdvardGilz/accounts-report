import decimal
import json
from typing import Any, List

from shared.types import MappingType


def _group_error_types(
    error_value: str,
    error_type_list: List[str],
    formated_error: MappingType
):
    for error_type in error_type_list:
        if error_type in formated_error:
            formated_error[error_type].append(error_value)
        else:
            formated_error[error_type] = [error_value]


def format_marshmallow_error_message(func: Any):
    def _get_formated_error(error_messages: MappingType):
        formated_error: MappingType = {}
        if isinstance(error_messages, str):
            return error_messages
        for error_value, error_type_list in error_messages.items():
            if not isinstance(error_type_list, dict):
                _group_error_types(
                    error_value,
                    error_type_list,
                    formated_error
                )
            else:
                parent_error_type_list: MappingType = error_type_list
                parent_error_value = error_value
                for child_error_value, child_error_type_list in (
                    parent_error_type_list.items()
                ):
                    _group_error_types(
                        f'{parent_error_value}-{child_error_value}',
                        child_error_type_list,
                        formated_error
                    )
        return formated_error

    def wrapper(*args: Any, **kwargs: Any):
        result = func(*args, **kwargs)
        if 'error' in result:
            result['error'] = _get_formated_error(result['error'])
        return result
    return wrapper


class DecimalEncoder(json.JSONEncoder):
    def default(self, o: Any):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def get_month_name(month_number: int):
    months_names = [
        'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio',
        'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ]
    return months_names[month_number-1]
