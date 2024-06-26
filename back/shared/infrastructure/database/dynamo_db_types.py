from typing import Any, TypedDict


class DynamoFilter(TypedDict):
    column: str
    value: Any
