from typing import Any

from helpers.exceptions import exception_handler
from shared.types import MappingType

from .application.create import ReportCreator
from .application.retrieve import ResportAccountsRetriever
from .entry_point_types import (
    ReportAccountsRetrieverContainerType,
    ReportCreatorContainerType,
)
from .infrastructure.bucket import BucketService
from .infrastructure.database import NonRelationalDbService
from .infrastructure.mailing import MailingService


def _get_report_creator_container():
    return ReportCreatorContainerType(
        bucket_service=BucketService(),
        mailing_service=MailingService(),
        non_relational_db_service=NonRelationalDbService(),
    )


def _get_report_accounts_retriever_container():
    return ReportAccountsRetrieverContainerType(
        non_relational_db_service=NonRelationalDbService(),
    )


@exception_handler('create_report_handler')
def create_report_handler(event: MappingType, _: Any):
    '''
    # Test in local with:

    python aws_lambda_wrapper.py '{"email": "eduardo.michell94@gmail.com", \
    "user_name": "Eduardo Giles"}' \
    --function create_report_handler
    '''
    return ReportCreator(
        container=_get_report_creator_container(),
    ).run(event)


@exception_handler('retrieve_accounts_data_handler')
def retrieve_accounts_data_handler(event: MappingType, _: Any):
    '''
    # Test in local with:

    python aws_lambda_wrapper.py '{}' \
    --function retrieve_accounts_data_handler
    '''
    return ResportAccountsRetriever(
        container=_get_report_accounts_retriever_container(),
    ).run()
