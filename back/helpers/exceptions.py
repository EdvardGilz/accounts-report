import traceback
from typing import Any, Dict, List

from settings import logger
from shared.types import MappingType


def _handle_exception(exception: Exception, reference: str):
    message = f'Error: {traceback.format_exc()}'
    logger.error(message, reference)

    raise exception


def exception_handler(reference: str):
    '''
    Handle exception and log
    '''
    custom_errors: MappingType = dict()

    def decorator(function: Any):
        def wrapper(*args: List[Any], **kwargs: Dict[str, Any]):
            try:
                return function(*args, **kwargs)
            except Exception as e:
                custom_errors['error'] = f' {e}'
                logger.error({'errorMessage': custom_errors})
                _handle_exception(e, reference)
        return wrapper

    return decorator
