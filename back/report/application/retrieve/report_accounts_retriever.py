from settings import logger

from ...entry_point_types import ReportAccountsRetrieverContainerType


class ResportAccountsRetriever:
    def __init__(self, container: ReportAccountsRetrieverContainerType) -> None:
        self._non_relational_db_service = container.non_relational_db_service

    def _get_account_data(self):
        logger.info('Getting account data')
        # TODO Replace hardcoded account_id in order to have more than 1 account
        return self._non_relational_db_service.retrieve_accounts_data(1)

    def run(self):
        return self._get_account_data()
