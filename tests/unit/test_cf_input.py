import pytest
from pydantic import ValidationError

from catalog_backend.models.input import ProductCreateEventModel, ProductDeleteEventModel, ProductModel, ProductUpdateEventModel


# Test cases for ProductModel
def test_product_model_valid():
    # Given: A set of valid product properties
    valid_product_data = {
        'product_name': 'TestProduct',
        'product_version': '1.0',
        'account_id': '123456789012',
        'consumer_name': 'TestConsumer',
        'region': 'us-west-2',
    }

    # When: Creating a ProductModel instance with valid properties
    product = ProductModel(**valid_product_data)

    # Then: The instance should be created successfully with the correct attributes
    assert product.product_name == 'TestProduct'
    assert product.product_version == '1.0'
    assert product.account_id == '123456789012'
    assert product.consumer_name == 'TestConsumer'
    assert product.region == 'us-west-2'


# Test invalid minimum length for all fields
@pytest.mark.parametrize(
    'field, value',
    [
        ('product_name', ''),
        ('product_version', ''),
        ('account_id', ''),
        ('consumer_name', ''),
        ('region', ''),
    ],
)
def test_product_model_invalid_min_length(field, value):
    # Given: A set of product properties with one field having invalid min length
    invalid_product_data = {
        'product_name': 'TestProduct',
        'product_version': '1.0',
        'account_id': '123456789012',
        'consumer_name': 'TestConsumer',
        'region': 'us-west-2',
    }
    invalid_product_data[field] = value

    # When/Then: Creating a ProductModel instance with invalid properties should raise a ValidationError
    with pytest.raises(ValidationError):
        ProductModel(**invalid_product_data)
        # Explanation: We expect a ValidationError because the field value does not meet the minimum length requirement.


# Test invalid maximum length for all fields
@pytest.mark.parametrize(
    'field, value',
    [
        ('product_name', 'T' * 41),  # 41 characters, max is 40
        ('product_version', 'V' * 11),  # 11 characters, max is 10
        ('account_id', 'A' * 41),  # 41 characters, max is 40
        ('consumer_name', 'C' * 41),  # 41 characters, max is 40
        ('region', 'R' * 21),  # 21 characters, max is 20
    ],
)
def test_product_model_invalid_max_length(field, value):
    # Given: A set of product properties with one field having invalid max length
    invalid_product_data = {
        'product_name': 'TestProduct',
        'product_version': '1.0',
        'account_id': '123456789012',
        'consumer_name': 'TestConsumer',
        'region': 'us-west-2',
    }
    invalid_product_data[field] = value

    # When/Then: Creating a ProductModel instance with invalid properties should raise a ValidationError
    with pytest.raises(ValidationError):
        ProductModel(**invalid_product_data)
        # Explanation: We expect a ValidationError because the field value exceeds the maximum length requirement.


def test_product_create_event_model_valid():
    # Given: A set of valid product create event properties
    valid_event_data = {
        'RequestType': 'Create',
        'ServiceToken': 'arn:aws:lambda:region:account-id:function:function-name',
        'ResponseURL': 'https://cloudformation-custom-resource-response-url.com',
        'StackId': 'arn:aws:cloudformation:region:account-id:stack/stack-name/guid',
        'RequestId': 'unique-request-id',
        'LogicalResourceId': 'PlatformGovernanceCustomResource',
        'ResourceType': 'Custom::Product',
        'ResourceProperties': {
            'product_name': 'TestProduct',
            'product_version': '1.0',
            'account_id': '123456789012',
            'consumer_name': 'TestConsumer',
            'region': 'us-west-2',
        },
    }

    # When: Creating a ProductCreateEventModel instance with valid properties
    event = ProductCreateEventModel(**valid_event_data)

    # Then: The instance should be created successfully with the correct attributes
    assert event.resource_properties.product_name == 'TestProduct'
    assert event.logical_resource_id == 'PlatformGovernanceCustomResource'


def test_product_create_event_model_invalid_logical_resource_id():
    # Given: An invalid logical resource ID
    invalid_event_data = {
        'RequestType': 'Create',
        'ServiceToken': 'arn:aws:lambda:region:account-id:function:function-name',
        'ResponseURL': 'https://cloudformation-custom-resource-response-url.com',
        'StackId': 'arn:aws:cloudformation:region:account-id:stack/stack-name/guid',
        'RequestId': 'unique-request-id',
        'LogicalResourceId': 'InvalidResourceId',
        'ResourceType': 'Custom::Product',
        'ResourceProperties': {
            'product_name': 'TestProduct',
            'product_version': '1.0',
            'account_id': '123456789012',
            'consumer_name': 'TestConsumer',
            'region': 'us-west-2',
        },
    }

    # When/Then: Creating a ProductCreateEventModel instance with an invalid logical resource ID should raise a ValidationError
    with pytest.raises(ValidationError):
        ProductCreateEventModel(**invalid_event_data)
        # Explanation: We expect a ValidationError because 'LogicalResourceId' must be 'PlatformGovernanceCustomResource'.


def test_product_delete_event_model_valid():
    # Given: A set of valid product delete event properties
    valid_event_data = {
        'RequestType': 'Delete',
        'ServiceToken': 'arn:aws:lambda:region:account-id:function:function-name',
        'ResponseURL': 'https://cloudformation-custom-resource-response-url.com',
        'StackId': 'arn:aws:cloudformation:region:account-id:stack/stack-name/guid',
        'RequestId': 'unique-request-id',
        'LogicalResourceId': 'PlatformGovernanceCustomResource',
        'ResourceType': 'Custom::Product',
        'ResourceProperties': {
            'product_name': 'TestProduct',
            'product_version': '1.0',
            'account_id': '123456789012',
            'consumer_name': 'TestConsumer',
            'region': 'us-west-2',
        },
    }

    # When: Creating a ProductDeleteEventModel instance with valid properties
    event = ProductDeleteEventModel(**valid_event_data)

    # Then: The instance should be created successfully with the correct attributes
    assert event.resource_properties.product_name == 'TestProduct'
    assert event.logical_resource_id == 'PlatformGovernanceCustomResource'


def test_product_update_event_model_valid():
    # Given: A set of valid product update event properties
    valid_event_data = {
        'RequestType': 'Update',
        'ServiceToken': 'arn:aws:lambda:region:account-id:function:function-name',
        'ResponseURL': 'https://cloudformation-custom-resource-response-url.com',
        'StackId': 'arn:aws:cloudformation:region:account-id:stack/stack-name/guid',
        'RequestId': 'unique-request-id',
        'LogicalResourceId': 'PlatformGovernanceCustomResource',
        'ResourceType': 'Custom::Product',
        'ResourceProperties': {
            'product_name': 'TestProduct',
            'product_version': '1.0',
            'account_id': '123456789012',
            'consumer_name': 'TestConsumer',
            'region': 'us-west-2',
        },
        'OldResourceProperties': {
            'product_name': 'OldTestProduct',
            'product_version': '0.9',
            'account_id': '123456789012',
            'consumer_name': 'OldTestConsumer',
            'region': 'us-west-1',
        },
    }

    # When: Creating a ProductUpdateEventModel instance with valid properties
    event = ProductUpdateEventModel(**valid_event_data)

    # Then: The instance should be created successfully with the correct attributes
    assert event.resource_properties.product_name == 'TestProduct'
    assert event.old_resource_properties.product_name == 'OldTestProduct'
    assert event.logical_resource_id == 'PlatformGovernanceCustomResource'


def test_product_update_event_model_invalid_logical_resource_id():
    # Given: An invalid logical resource ID
    invalid_event_data = {
        'RequestType': 'Update',
        'ServiceToken': 'arn:aws:lambda:region:account-id:function:function-name',
        'ResponseURL': 'https://cloudformation-custom-resource-response-url.com',
        'StackId': 'arn:aws:cloudformation:region:account-id:stack/stack-name/guid',
        'RequestId': 'unique-request-id',
        'LogicalResourceId': 'InvalidResourceId',
        'ResourceType': 'Custom::Product',
        'ResourceProperties': {
            'product_name': 'TestProduct',
            'product_version': '1.0',
            'account_id': '123456789012',
            'consumer_name': 'TestConsumer',
            'region': 'us-west-2',
        },
        'OldResourceProperties': {
            'product_name': 'OldTestProduct',
            'product_version': '0.9',
            'account_id': '123456789012',
            'consumer_name': 'OldTestConsumer',
            'region': 'us-west-1',
        },
    }

    # When/Then: Creating a ProductUpdateEventModel instance with an invalid logical resource ID should raise a ValidationError
    with pytest.raises(ValidationError):
        ProductUpdateEventModel(**invalid_event_data)
        # Explanation: We expect a ValidationError because 'LogicalResourceId' must be 'PlatformGovernanceCustomResource'.
