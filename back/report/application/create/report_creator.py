from decimal import Decimal
from typing import Any, List

import marshmallow_dataclass
import pandas as pd
from marshmallow import ValidationError
from settings import logger
from shared.messages_conts import (
    DATE_FORMAT_ERROR_MSG,
    DUPLICATED_IDS_ERROR_MSG,
    ID_COLUMN_FORMAT_ERROR_MSG,
    MISSING_COLUMNS_MSG,
    TRANSACTION_COLUMN_FORMAT_ERROR_MSG,
)
from shared.miscellaneous import format_marshmallow_error_message, get_month_name
from shared.types import MappingType

from ...domain.report_types import EventType
from ...entry_point_types import ReportCreatorContainerType

COLUMNS_NAMES = ['id', 'date', 'transaction']


class ReportCreator:
    def __init__(self, container: ReportCreatorContainerType) -> None:
        self._bucket_service = container.bucket_service
        self._mailing_service = container.mailing_service
        self._non_relational_db_service = container.non_relational_db_service
        self._marshmallow_dataclass: Any = marshmallow_dataclass
        self._pd: Any = pd
        self._event: EventType
        self._is_error: bool = False
        self._response: MappingType = {'report_sent': True}
        self._df_file_data: Any = self._pd.DataFrame()
        self._df_account_data: Any = self._pd.DataFrame()

    def _set_error_response(self, error_message: Any):
        self._is_error = True
        self._response['report_sent'] = False
        self._response['error'] = error_message
        logger.info(error_message)

    def _validate_inbound(self, event: MappingType):
        error: Any
        try:
            self._event: EventType = (
                self._marshmallow_dataclass
                .class_schema(EventType)()
                .load(event)
            )
        except ValidationError as error:
            self._set_error_response(error.normalized_messages())

    def _has_error(self, file_data: MappingType):
        if 'error' in file_data:
            self._set_error_response(file_data['error'])
            return True
        return False

    def _has_missing_columns(self):
        missing_columns = [
            col for col in COLUMNS_NAMES
            if col not in self._df_file_data.columns
        ]
        if missing_columns:
            self._set_error_response(
                MISSING_COLUMNS_MSG + ', '.join(missing_columns)
            )
            return True
        return False

    def _is_column_types_valid(self):
        if not self._pd.api.types.is_integer_dtype(self._df_file_data['id']):
            self._set_error_response(ID_COLUMN_FORMAT_ERROR_MSG)
            return False

        if not self._pd.api.types.is_numeric_dtype(
            self._df_file_data['transaction']
        ):
            self._set_error_response(TRANSACTION_COLUMN_FORMAT_ERROR_MSG)
            return False
        return True

    def _is_date_format_valid(self):
        try:
            self._pd.to_datetime(self._df_file_data['date'], format='%d/%m/%Y')
        except ValueError:
            self._set_error_response(DATE_FORMAT_ERROR_MSG)
            return False
        return True

    def _has_duplicate_ids(self):
        duplicate_ids = self._df_file_data[
            self._df_file_data.duplicated(subset='id', keep=False)
        ]
        unique_duplicated_ids = list(set(duplicate_ids["id"].tolist()))
        if not duplicate_ids.empty:
            self._set_error_response(
                DUPLICATED_IDS_ERROR_MSG +
                ', '.join(map(str, unique_duplicated_ids))
            )
            return True
        return False

    def _get_file_data(self):
        if self._is_error:
            return

        logger.info('Getting file data')
        file_data = self._bucket_service.get_file_data()

        if self._has_error(file_data):
            return

        self._df_file_data = file_data['data']
        if self._has_missing_columns():
            return

        if not self._is_column_types_valid():
            return

        if not self._is_date_format_valid():
            return

        if self._has_duplicate_ids():
            return

        self._df_file_data['transaction'] = (
            self._df_file_data['transaction'].apply(lambda x: Decimal(str(x)))
        )
        # TODO Replace hardcoded account_id in order to have more than 1 account
        self._df_file_data['account_id'] = 1

    def _store_account_data(self):
        if self._is_error:
            return

        logger.info('Storing account data')
        self._non_relational_db_service.create_accounts_data(
            self._df_file_data.to_dict('records')
        )

    def _get_account_data(self):
        if self._is_error:
            return

        logger.info('Getting account data')
        # TODO Replace hardcoded account_id in order to have more than 1 account
        accounts_data = (
            self._non_relational_db_service.retrieve_accounts_data(1)
        )
        self._df_account_data = self._pd.DataFrame(accounts_data)

    def _get_report_data(self) -> MappingType:
        negative_avg = self._df_account_data[
            self._df_account_data['transaction'] < 0
        ]['transaction'].mean()
        positive_avg = self._df_account_data[
            self._df_account_data['transaction'] > 0
        ]['transaction'].mean()
        self._df_account_data['date_column'] = (
            self._pd.to_datetime(
                self._df_account_data['date'],
                format='%d/%m/%Y'
            )
        )
        self._df_account_data['year_month'] = (
            self._df_account_data['date_column'].dt.to_period('M')
        )
        df_date_grouped = self._df_account_data.groupby('year_month')

        num_of_transaccions_for_months_str: List[str] = []
        for name, group in df_date_grouped:
            num_of_transaccions_for_months_str.append(
                f'<li>{get_month_name(name.month)} {name.year}: {len(group)}'
                '</li>'
            )

        return {
            'total_balance': round(
                sum(self._df_account_data['transaction']), 2
            ),
            'debit_avg': round(negative_avg, 2),
            'credit_avg': round(positive_avg, 2),
            'num_of_transaccions_for_months': (
                num_of_transaccions_for_months_str
            ),
        }

    @staticmethod
    def _get_formated_movements_content(report_data: MappingType):
        num_of_transactions = '<ul>'
        num_of_transactions += ''.join(
            report_data['num_of_transaccions_for_months']
        )
        num_of_transactions += '</ul>'

        return f'''
        <ul>
            <li>Balance Total: {report_data['total_balance']}</li>
            <li>Monto promedio de débito: {report_data['debit_avg']}</li>
            <li>Monto promedio de crédito: {report_data['credit_avg']}</li>
            <li>Número de transacciones por mes:</li>
            {num_of_transactions}
        </ul>
        '''

    def _send_report(self):
        if self._is_error:
            return

        report_data = self._get_report_data()
        report_content = self._get_formated_movements_content(report_data)

        logger.info('Sending report')
        self._mailing_service.send_report_email(
            recipient=self._event.email,
            user_name=self._event.user_name,
            movements_data=report_content,
        )

    @format_marshmallow_error_message
    def run(self, event: MappingType):
        self._validate_inbound(event)
        self._get_file_data()
        self._store_account_data()
        self._get_account_data()
        self._send_report()
        return self._response
