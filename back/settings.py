import configparser
import logging
from datetime import datetime
from logging import basicConfig
from typing import Any

import boto3
import pytz

logger = logging.getLogger()
logger.setLevel(logging.INFO)
LOG_FORMAT = '[ %(levelname)s ] - %(asctime)-15s :: %(message)s'
basicConfig(format=LOG_FORMAT)

CONFIG_FILE = 'config.ini'
logger.debug('Parsing %s for %s', CONFIG_FILE, __name__)
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

_boto3: Any = boto3
boto3_session = _boto3.session.Session()

IS_MOCK = True if config.get('environment', 'mock') == 'yes' else False

TIME_ZONE = 'America/Mexico_City'
base_datetime = datetime.now(pytz.timezone(TIME_ZONE))

__all__ = [
    'config',
    'logger',
    'TIME_ZONE',
    'IS_MOCK',
]
