from typing import Any

from botocore.exceptions import ClientError
from settings import logger


class UncontrolledExeption(Exception):
    def __init__(self, result: Any):
        self.result = result
        super().__init__(self.result)

    def __str__(self):
        return (f'Uncontrolled error {self.result}')


def email_exception_handler(wrapped_function: Any):
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            response = wrapped_function(*args, **kwargs)
        except ClientError as e:
            error_message: Any = e.response['Error']['Message']
            logger.error(error_message)
            raise Exception(error_message)
        else:
            message_id = response['MessageId']
            logger.info(f'Email sent! Message ID: {message_id}')
            return message_id
    return wrapper
