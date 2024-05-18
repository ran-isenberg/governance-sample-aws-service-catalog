from aws_cdk import CustomResource, RemovalPolicy, Stack, aws_sns


def create_governance_enabler(scope, topic: aws_sns.Topic, product_name: str, product_version: str, consumer_name: str) -> CustomResource:
    # custom resource
    stack = Stack.of(scope)
    cr_end_props = {
        'account_id': stack.account,
        'region': stack.region,
        'product_name': product_name,
        'product_version': product_version,
        'consumer_name': consumer_name,
    }
    custom_resource = CustomResource(
        scope,
        'PlatformGovernanceCustomResource',
        service_token=topic.topic_arn,
        resource_type='Custom::GovernanceDeploymentStatus',
        removal_policy=RemovalPolicy.DESTROY,
        properties=cr_end_props,
    )
    return custom_resource
