from tests.integration.utils import call_handle_product_event, mock_crhelper


def test_create_product(mocker):
    create_product_event = (
        {
            'RequestType': 'Delete',
            'ServiceToken': 'arn:aws:sns:us-east-1:123456789012:ranisenberg-custom-PlatformCatalog-dev-GovernanceCatalogTopic',
            'ResponseURL': 'https://cloudformation-custom-resource-response-useast1.s3.amazonaws.com/arn%3Aaws%3Acloudformation%3Aus-east-1%3A123456789012%3Astack/SC-123456789012-pp-yuqxzldfdagkq/1dbb0a20-14e8-11ef-a95c-0eaa9ec0a8b1%7CPlatformGovernanceCustomResource%7C508d99b2-2cc8-4f4d-ba49-e2ee6103da31?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20240518T073027Z&X-Amz-SignedHeaders=host&X-Amz-Expires=7200&X-Amz-Credential=AIBXN%2F20240518%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=dtretreter01bf04ec386468df9c2f2573419fc7559',
            'StackId': 'arn:aws:cloudformation:us-east-1:123456789012:stack/SC-123456789012-pp-yuqxzldfdagkq/1dbb0a20-14e8-11ef-a95c-0eaa9ec0a8b1',
            'RequestId': '508d99b2-2cc8-4f4d-ba49-e2ee6103da31',
            'LogicalResourceId': 'PlatformGovernanceCustomResource',
            'PhysicalResourceId': 'SC-123456789012-pp-yuqxzldfdagkq-PlatformGovernanceCustomResource-1HCS9DZKVQHAB',
            'ResourceType': 'Custom::GovernanceDeploymentStatus',
            'ResourceProperties': {
                'ServiceToken': 'arn:aws:sns:us-east-1:123456789012:ranisenberg-custom-PlatformCatalog-dev-GovernanceCatalogTopic',
                'product_version': '1.0.0',
                'account_id': '123456789012',
                'consumer_name': 'Ran isenberg',
                'region': 'us-east-1',
                'product_name': 'CI/CD IAM Role Product',
            },
        },
    )
    crhelper_mock = mock_crhelper(mocker)
    call_handle_product_event(create_product_event)
    assert crhelper_mock.call_count == 2
