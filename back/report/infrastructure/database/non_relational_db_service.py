from settings import IS_MOCK
from shared.infrastructure.database import DynamoDbService
from shared.mock import MockResponses
from shared.types import ListMappingType


class NonRelationalDbService(DynamoDbService, MockResponses):
    def __init__(self) -> None:
        super().__init__()

    def create_accounts_data(self, account_data: ListMappingType):
        if IS_MOCK:
            self.print_mock_response()
            return

        self.create_batch(
            table_name='accounts_table_name',
            items=account_data
        )

    def retrieve_accounts_data(self, account_id: int):
        if IS_MOCK:
            return self._get_mock_response('_account_data')

        return self.retrieve_all(
            table_name='accounts_table_name',
            filters=self.populate_dynamo_filter(
                retrieve_colum_names_list=[],
                filter_list=[
                    {'column': 'account_id', 'value': account_id}
                ]
            )
        )
