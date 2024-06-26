import json
from typing import Any

from files.entry_point import create_uppy_files_handler
from helpers.entry_point import get_params
from report.entry_point import create_report_handler, retrieve_accounts_data_handler
from settings import logger

if __name__ == '__main__':
    # This main is for local testing purposes
    EVENT_PARAMS, CONTEXT, DEBUG, FUNCTION = get_params()
    EVENT = json.loads(EVENT_PARAMS)

    command_arguments: Any = {'event': EVENT, '_': CONTEXT}

    logger.info('Running %s', FUNCTION)

    functions = {
        'create_uppy_files_handler': lambda: print(json.dumps(
            create_uppy_files_handler(**command_arguments)
        )),
        'create_report_handler': lambda: print(json.dumps(
            create_report_handler(**command_arguments)
        )),
        'retrieve_accounts_data_handler': lambda: print(json.dumps(
            retrieve_accounts_data_handler(**command_arguments)
        )),
    }
    if FUNCTION:
        functions[FUNCTION]()
