from settings import IS_MOCK
from shared.infrastructure.mailing import SesService
from shared.mock import MockResponses
from shared.types import MappingType


class MailingService(SesService, MockResponses):
    def __init__(self):
        super().__init__()

    def send_report_email(
        self,
        recipient: str,
        user_name: str,
        movements_data: str,
    ):
        if IS_MOCK:
            self.print_mock_response()
            return

        self.send_email(
            subject='Accounts Report',
            recipient_list=[recipient],
            template_name='report_template.html',
            template_data={
                'user_name': user_name,
                'moviments': movements_data
            }
        )
