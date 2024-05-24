from aws_cdk import aws_iam as iam
from aws_cdk import aws_servicecatalog as servicecatalog
from aws_cdk import aws_sns
from constructs import Construct

from cdk.catalog.products.governance_construct import GovernanceProductConstruct


class CiCdProduct(servicecatalog.ProductStack):
    CICD_PRODUCT_NAME = 'CI/CD IAM Role Product'
    CICD_PRODUCT_VERSION = '1.0.0'
    CICD_PRODUCT_DESCRIPTION = 'An IAM role for CI/CD pipelines'

    def __init__(
        self,
        scope: Construct,
        id: str,
        topic: aws_sns.Topic,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)
        self.product_description = CiCdProduct.CICD_PRODUCT_DESCRIPTION
        self.product_name = CiCdProduct.CICD_PRODUCT_NAME
        self.product_version = CiCdProduct.CICD_PRODUCT_VERSION

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

        self.governance_enabler = GovernanceProductConstruct(
            self,
            'GovernanceEnabler',
            topic,
            self.product_name,
            self.product_version,
        )
        self.governance_enabler.node.add_dependency(self.role)
