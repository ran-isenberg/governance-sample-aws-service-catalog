from aws_cdk import CfnParameter, CustomResource, RemovalPolicy, Stack, aws_sns
from constructs import Construct

from cdk.catalog.constants import CUSTOM_RESOURCE_TYPE


class GovernanceProductConstruct(Construct):
    def __init__(self, scope: Construct, id: str, topic: aws_sns.Topic, product_name: str, product_version: str) -> None:
        super().__init__(scope, id)
        # Add a parameter for consumer_name
        self.consumer_name_param = CfnParameter(
            self,
            id='ConsumerName',
            type='String',
            description='Name of the team that deployed the product',
            min_length=1,
        )
        self.consumer_name_param.override_logical_id('ConsumerName')  # this will be the parameter name in the CloudFormation template
        self.custom_resource = self._create_custom_resource(topic, product_name, product_version, self.consumer_name_param.value_as_string)

    def _create_custom_resource(self, topic: aws_sns.Topic, product_name: str, product_version: str, consumer_name: str) -> CustomResource:
        stack = Stack.of(self)
        cr_end_props = {
            'account_id': stack.account,
            'region': stack.region,
            'product_name': product_name,
            'product_version': product_version,
            'consumer_name': consumer_name,
        }
        custom_resource = CustomResource(
            self,
            'PlatformGovernanceCustomResource',
            service_token=topic.topic_arn,
            resource_type=CUSTOM_RESOURCE_TYPE,
            removal_policy=RemovalPolicy.DESTROY,
            properties=cr_end_props,
        )
        return custom_resource
