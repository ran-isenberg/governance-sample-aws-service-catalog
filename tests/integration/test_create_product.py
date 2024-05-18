from datetime import datetime, timezone

import boto3

from tests.integration.utils import (
    RESOURCE_PROPERTIES,
    assert_crhelper_response,
    call_handle_product_event,
    create_product_body,
    create_sqs_records,
    mock_crhelper,
)
from tests.utils import generate_random_string


def test_create_product_success(mocker, table_name, portfolio_id):
    product_stack_id = f'arn:aws:cloudformation:us-east-1:123456789012:stack/SC-123456789012-pp-yuqxzldfdagkq/{generate_random_string(12)}'
    event = create_sqs_records(create_product_body('Create', product_stack_id, RESOURCE_PROPERTIES))
    crhelper_mock = mock_crhelper(mocker)
    call_handle_product_event(event)
    assert_crhelper_response(success=True, crhelper_mock=crhelper_mock)

    # check that product is in dynamoDB after create event
    dynamodb_table = boto3.resource('dynamodb').Table(table_name)
    response = dynamodb_table.get_item(
        Key={
            'portfolio_id': portfolio_id,
            'product_stack_id': product_stack_id,
        }
    )
    _assert_db_item(response['Item'], portfolio_id, product_stack_id)
    # delete entry
    response = dynamodb_table.delete_item(Key={'portfolio_id': portfolio_id, 'product_stack_id': product_stack_id})


def _assert_db_item(item: dict, portfolio_id: str, product_stack_id: str):
    assert item['version'] == RESOURCE_PROPERTIES['product_version']
    assert item['account_id'] == RESOURCE_PROPERTIES['account_id']
    assert item['consumer_name'] == RESOURCE_PROPERTIES['consumer_name']
    assert item['region'] == RESOURCE_PROPERTIES['region']
    assert item['portfolio_id'] == portfolio_id
    assert item['product_stack_id'] == product_stack_id
    assert item['created_at'] is not None
    now = int(datetime.now(timezone.utc).timestamp())
    assert now - int(item['created_at']) <= 60  # assume item was created in last minute, check that utc time calc is correct


def test_create_product_failure_empty_resource_props_body_input(mocker):
    event = create_sqs_records(create_product_body('Create', 'aaaa', {}))
    crhelper_mock = mock_crhelper(mocker)
    call_handle_product_event(event)
    assert_crhelper_response(success=False, crhelper_mock=crhelper_mock)
