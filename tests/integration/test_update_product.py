from datetime import datetime, timezone

import boto3

from tests.integration.utils import (
    NEW_RESOURCE_PROPERTIES,
    RESOURCE_PROPERTIES,
    assert_crhelper_response,
    call_handle_product_event,
    create_product_body,
    create_sqs_records,
    mock_crhelper,
)
from tests.utils import generate_random_string


def _check_db_entry_exists(table_name: str, portfolio_id: str, product_stack_id: str) -> bool:
    dynamodb_table = boto3.resource('dynamodb').Table(table_name)
    response = dynamodb_table.get_item(
        Key={
            'portfolio_id': portfolio_id,
            'product_stack_id': product_stack_id,
        }
    )
    return response.get('Item', None)


def _add_db_entry(table_name: str, portfolio_id: str, product_stack_id: str):
    dynamodb_table = boto3.resource('dynamodb').Table(table_name)
    dynamodb_table.put_item(
        Item={
            'portfolio_id': portfolio_id,
            'product_stack_id': product_stack_id,
            'name': RESOURCE_PROPERTIES['product_name'],
            'version': RESOURCE_PROPERTIES['product_version'],
            'account_id': RESOURCE_PROPERTIES['account_id'],
            'consumer_name': RESOURCE_PROPERTIES['consumer_name'],
            'region': RESOURCE_PROPERTIES['region'],
            'created_at': 1234567890,
        }
    )


def test_update_product_success(mocker, table_name, portfolio_id):
    # add entry to dynamoDB
    product_stack_id = f'arn:aws:cloudformation:us-east-1:123456789012:stack/SC-123456789012-pp-yuqxzldfdagkq/{generate_random_string(12)}'
    _add_db_entry(table_name, portfolio_id, product_stack_id)
    # check that product is in dynamoDB after create event
    assert _check_db_entry_exists(table_name, portfolio_id, product_stack_id)

    # create update event
    event = create_sqs_records(create_product_body('Update', product_stack_id, NEW_RESOURCE_PROPERTIES, RESOURCE_PROPERTIES))
    crhelper_mock = mock_crhelper(mocker)
    call_handle_product_event(event)
    assert_crhelper_response(success=True, crhelper_mock=crhelper_mock)

    dynamodb_table = boto3.resource('dynamodb').Table(table_name)
    response = dynamodb_table.get_item(
        Key={
            'portfolio_id': portfolio_id,
            'product_stack_id': product_stack_id,
        }
    )
    item = response['Item']
    assert item['version'] == NEW_RESOURCE_PROPERTIES['product_version']
    assert item['account_id'] == NEW_RESOURCE_PROPERTIES['account_id']
    assert item['consumer_name'] == NEW_RESOURCE_PROPERTIES['consumer_name']
    assert item['region'] == NEW_RESOURCE_PROPERTIES['region']
    assert item['portfolio_id'] == portfolio_id
    assert item['product_stack_id'] == product_stack_id
    assert item['created_at'] is not None
    now = int(datetime.now(timezone.utc).timestamp())
    assert now - int(item['created_at']) <= 60  # assume item was created in last minute, check that utc time calc is correct

    # delete entry
    response = dynamodb_table.delete_item(Key={'portfolio_id': portfolio_id, 'product_stack_id': product_stack_id})


def test_update_product_failure_empty_resource_props_body_input(mocker):
    event = create_sqs_records(create_product_body('Update', 'aaaaaa', NEW_RESOURCE_PROPERTIES, {}))
    crhelper_mock = mock_crhelper(mocker)
    call_handle_product_event(event)
    assert_crhelper_response(success=False, crhelper_mock=crhelper_mock)
