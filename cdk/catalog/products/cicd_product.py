from aws_cdk import CfnParameter, aws_sns
from aws_cdk import aws_iam as iam
from aws_cdk import aws_servicecatalog as servicecatalog
from constructs import Construct

from cdk.catalog.products.governance_enabler import create_governance_enabler

CICD_PRODUCT_NAME = 'CI/CD IAM Role Product'
CICD_PRODUCT_VERSION = '1.0.0'
CICD_PRODUCT_DESCRIPTION = 'An IAM role for CI/CD pipelines'


class CiCdProduct(servicecatalog.ProductStack):
    def __init__(
        self,
        scope: Construct,
        id: str,
        product_name: str,
        product_version: str,
        topic: aws_sns.Topic,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        # Add a parameter for consumer_name
        consumer_name_param = CfnParameter(self, 'ConsumerName', type='String', description='Name of the team that deployed the product')

        # Create the IAM role within the product stack
        self.role = iam.Role(
            self,
            'CiCdRole',
            assumed_by=iam.ServicePrincipal('ec2.amazonaws.com'),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name('AWSCloudFormationFullAccess'),
                iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3FullAccess'),
            ],
        )

        self.governance_enabler = create_governance_enabler(self, topic, product_name, product_version, consumer_name_param.value_as_string)
        self.governance_enabler.node.add_dependency(self.role)

        # product_id = Token.as_string( self.governance_enabler.get_att_string('product_id'))
        # product_id_output = CfnOutput(scope, id='productId', value=product_id, description='The physical_resource_id generated for the product')
        # product_id_output.override_logical_id('productId')
