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
            'name': 'product_name',
            'version': '1.0',
            'account_id': '123456789012',
            'consumer_name': 'consumer_name',
            'region': 'us-east-1',
            'created_at': 1234567890,
        }
    )


def test_delete_product_success(mocker, table_name, portfolio_id):
    # add entry to dynamoDB
    product_stack_id = f'arn:aws:cloudformation:us-east-1:123456789012:stack/SC-123456789012-pp-yuqxzldfdagkq/{generate_random_string(12)}'
    _add_db_entry(table_name, portfolio_id, product_stack_id)
    # check that product is in dynamoDB after create event
    assert _check_db_entry_exists(table_name, portfolio_id, product_stack_id)

    # create delete event
    event = create_sqs_records(create_product_body('Delete', product_stack_id, RESOURCE_PROPERTIES))
    crhelper_mock = mock_crhelper(mocker)
    call_handle_product_event(event)
    assert_crhelper_response(success=True, crhelper_mock=crhelper_mock)

    # check that product is deleted from dynamoDB after delete event
    assert not _check_db_entry_exists(table_name, portfolio_id, product_stack_id)


def test_delete_product_failure_empty_resource_props_body_input(mocker):
    event = create_sqs_records(create_product_body('Delete', 'aaaa', {}))
    crhelper_mock = mock_crhelper(mocker)
    call_handle_product_event(event)
    assert_crhelper_response(success=False, crhelper_mock=crhelper_mock)
