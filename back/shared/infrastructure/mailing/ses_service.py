import codecs
from typing import List, Optional, Union

from settings import boto3_session, config
from shared.exceptions import email_exception_handler
from shared.types import MappingType


class SesService:
    def __init__(self) -> None:
        self._ses_client = boto3_session.client(
            'ses',
            region_name=config.get('mailing', 'aws_ses_region')
        )

    @staticmethod
    def _get_html_template(template_name: str = '') -> str:
        template_path = f'resources/email_templates/{template_name}'
        with codecs.open(template_path, 'r') as html_file:
            html_text = html_file.read()
            return html_text

    @staticmethod
    def _replace_html_template_data(
        template_data: MappingType,
        html_text: Optional[str] = None,
    ) -> Union[str, None]:
        if not html_text:
            return
        for key, value in template_data.items():
            html_text = html_text.replace(f'{{{key}}}', f'{value}')
        return html_text

    @email_exception_handler
    def send_email(
        self,
        subject: str,
        recipient_list: List[str],
        bcc_list: List[str] = [],
        body_html: Optional[str] = None,
        body_text: Optional[str] = None,
        template_name: str = '',
        template_data: MappingType = {},
    ) -> str:
        if template_name:
            body_html = self._get_html_template(template_name)
        body_html = self._replace_html_template_data(
            template_data=template_data,
            html_text=body_html,
        )
        email_message: MappingType = {
            'Body': {},
            'Subject': {
                'Charset': config.get('mailing', 'aws_ses_charset'),
                'Data': subject
            },
        }
        if body_html:
            email_message['Body']['Html'] = {
                'Charset': config.get('mailing', 'aws_ses_charset'),
                'Data': body_html
            }
        if body_text:
            email_message['Body']['Text'] = {
                'Charset': config.get('mailing', 'aws_ses_charset'),
                'Data': body_text
            }
        destination = {
            'ToAddresses': recipient_list
        }
        if (bcc_list):
            destination['BccAddresses'] = bcc_list

        return self._ses_client.send_email(
            Destination=destination,
            Message=email_message,
            Source=config.get('mailing', 'aws_ses_sender'),
        )
