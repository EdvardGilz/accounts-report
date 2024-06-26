from typing import NamedTuple

from .infrastructure.bucket import BucketService
from .infrastructure.database import NonRelationalDbService
from .infrastructure.mailing import MailingService


class ReportCreatorContainerType(NamedTuple):
    bucket_service: BucketService
    mailing_service: MailingService
    non_relational_db_service: NonRelationalDbService


class ReportAccountsRetrieverContainerType(NamedTuple):
    non_relational_db_service: NonRelationalDbService
