from datetime import datetime, timezone

import boto3
from cachetools import TTLCache, cached
from mypy_boto3_dynamodb import DynamoDBServiceResource
from mypy_boto3_dynamodb.service_resource import Table
from pydantic import ValidationError

from catalog_backend.dal.db_handler import DalHandler
from catalog_backend.dal.models.db import ProductEntry
from catalog_backend.handlers.utils.observability import logger, tracer


class DynamoDalHandler(DalHandler):
    def __init__(self, table_name: str):
        self.table_name = table_name

    # cache dynamodb connection data for no longer than 5 minutes
    @cached(cache=TTLCache(maxsize=1, ttl=300))
    def _get_db_handler(self, table_name: str) -> Table:
        logger.info('opening connection to dynamodb table', table_name=table_name)
        dynamodb: DynamoDBServiceResource = boto3.resource('dynamodb')
        return dynamodb.Table(table_name)

    def _get_unix_time(self) -> int:
        return int(datetime.now(timezone.utc).timestamp())

    @tracer.capture_method(capture_response=False)
    def add_product_deployment(
        self,
        portfolio_id: str,
        product_stack_id: str,
        product_name: str,
        product_version: str,
        account_id: str,
        consumer_name: str,
        region: str,
    ) -> None:
        logger.info('trying to save product deployment')
        try:
            entry = ProductEntry(
                portfolio_id=portfolio_id,
                product_stack_id=product_stack_id,
                name=product_name,
                version=product_version,
                account_id=account_id,
                consumer_name=consumer_name,
                region=region,
                created_at=self._get_unix_time(),
            )
            table: Table = self._get_db_handler(self.table_name)
            table.put_item(Item=entry.model_dump())
        except ValidationError as exc:  # pragma: no cover
            logger.exception('failed to create product deployment')
            raise exc

        logger.info('finished create product deployment successfully')

    @tracer.capture_method(capture_response=False)
    def delete_product_deployment(
        self,
        portfolio_id: str,
        product_stack_id: str,
    ) -> None:
        logger.info('trying to delete product deployment')
        try:
            table: Table = self._get_db_handler(self.table_name)
            table.delete_item(Key={'portfolio_id': portfolio_id, 'product_stack_id': product_stack_id})
        except Exception as exc:
            logger.exception('failed to delete product deployment')
            raise exc
        logger.info('finished delete product deployment successfully')

    @tracer.capture_method(capture_response=False)
    def update_product_deployment(
        self,
        portfolio_id: str,
        product_stack_id: str,
        product_name: str,
        product_version: str,
        account_id: str,
        consumer_name: str,
        region: str,
    ) -> None:
        logger.info('trying to update product deployment')
        try:
            entry = ProductEntry(
                portfolio_id=portfolio_id,
                product_stack_id=product_stack_id,
                name=product_name,
                version=product_version,
                account_id=account_id,
                consumer_name=consumer_name,
                region=region,
                created_at=self._get_unix_time(),
            )
            table: Table = self._get_db_handler(self.table_name)
            # overwrite the entry if it exists
            table.put_item(Item=entry.model_dump())
        except ValidationError as exc:
            logger.exception('failed to update product deployment')
            raise exc
        logger.info('finished update product deployment successfully')
