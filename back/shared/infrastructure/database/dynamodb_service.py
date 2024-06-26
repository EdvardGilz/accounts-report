import json
from typing import Any, List, Optional, Union

from boto3.dynamodb.conditions import Attr
from settings import boto3_session, config, logger
from shared.exceptions import UncontrolledExeption
from shared.miscellaneous import DecimalEncoder
from shared.types import MappingType

from .dynamo_db_types import DynamoFilter


class DynamoDbService:
    def __init__(self) -> None:
        self.dynamodb_resource = boto3_session.resource(
            service_name='dynamodb',
            region_name=config.get('dynamodb', 'region_name')
        )
        self._attr: Any = Attr

    def _get_table(self, table_name: str):
        return self.dynamodb_resource.Table(table_name)

    @staticmethod
    def _validate_response(response: Any) -> None:
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            logger.error('DynamoDB HTTPStatusCode Exception')
            raise UncontrolledExeption(response)

    @staticmethod
    def _decode_item(item: MappingType) -> MappingType:
        return json.loads(json.dumps(item, cls=DecimalEncoder))

    def _decode_items(self, items: List[MappingType]) -> List[MappingType]:
        items_decoded: List[MappingType] = []
        for item in items:
            items_decoded.append(self._decode_item(item))
        return items_decoded

    def _decode_response(
        self,
        response: Union[MappingType, List[MappingType]]
    ) -> Any:
        if isinstance(response, list):
            return self._decode_items(response)
        return self._decode_item(response)

    def populate_dynamo_filter(
        self,
        retrieve_colum_names_list: List[str],
        filter_list: List[DynamoFilter],
        union: bool = True,
    ):
        filters: MappingType = {
            'FilterExpression': None
        }

        if retrieve_colum_names_list:
            filters['ProjectionExpression'] = (
                ', '.join(retrieve_colum_names_list)
            )

        for filter_value in filter_list:
            logger.info(
                'Attr: %s, Value: %s',
                filter_value['column'], filter_value['value']
            )
            if not filters['FilterExpression']:
                filters['FilterExpression'] = (
                    self._attr(filter_value['column']).eq(
                        filter_value['value']))
            else:
                filters['FilterExpression'] = (
                    filters['FilterExpression'] |
                    self._attr(filter_value['column'])
                    .eq(filter_value['value'])
                ) if union else (
                    filters['FilterExpression'] &
                    self._attr(filter_value['column'])
                    .eq(filter_value['value'])
                )

        return filters

    def create_batch(
        self,
        table_name: str,
        items: List[MappingType],
    ) -> MappingType:
        _table_name = config.get('dynamodb', table_name)
        logger.info('Creating %s items in %s table', items, _table_name)
        table = self._get_table(table_name=_table_name)

        with table.batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item)

        return {'created': len(items)}

    def retrieve(
        self,
        table_name: str,
        query: MappingType,
    ) -> Any:
        _table_name = config.get('dynamodb', table_name)
        logger.info(
            'Searching in "%s" table with "%s" query', _table_name, query
        )
        table = self._get_table(table_name=_table_name)
        response = table.get_item(Key=query)
        self._validate_response(response=response)
        item = response.get('Item')
        if item:
            return self._decode_response(item)
        return {}

    def retrieve_all(
        self,
        table_name: str,
        filters: Optional[MappingType] = None
    ) -> List[Any]:
        _table_name = config.get('dynamodb', table_name)
        logger.info('Searching in %s table', _table_name)
        table = self._get_table(table_name=_table_name)

        if filters:
            logger.info('Filters %s', filters)
            response = table.scan(**filters)
        else:
            filters = {}
            response = table.scan()

        self._validate_response(response=response)
        items = response['Items']
        while 'LastEvaluatedKey' in response:
            filters['ExclusiveStartKey'] = (
                response['LastEvaluatedKey']
            )
            response = table.scan(**filters)
            self._validate_response(response=response)
            items.extend(response['Items'])
        if items:
            return self._decode_response(items)
        return []
