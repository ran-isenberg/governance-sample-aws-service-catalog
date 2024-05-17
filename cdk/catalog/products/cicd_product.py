from aws_cdk import (
    aws_iam as iam,
)
from aws_cdk import aws_servicecatalog as servicecatalog
from constructs import Construct


class CiCdProduct(servicecatalog.ProductStack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create the IAM role within the product stack
        iam.Role(
            self,
            'CiCdRole',
            assumed_by=iam.ServicePrincipal('ec2.amazonaws.com'),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name('AmazonS3ReadOnlyAccess'),
                iam.ManagedPolicy.from_aws_managed_policy_name('AmazonEC2ContainerRegistryReadOnly'),
                iam.ManagedPolicy.from_aws_managed_policy_name('CloudWatchLogsFullAccess'),
                iam.ManagedPolicy.from_aws_managed_policy_name('AWSCodeBuildDeveloperAccess'),
                iam.ManagedPolicy.from_aws_managed_policy_name('AWSCodePipelineFullAccess'),
                iam.ManagedPolicy.from_aws_managed_policy_name('AWSCodeDeployFullAccess'),
                iam.ManagedPolicy.from_aws_managed_policy_name('IAMFullAccess'),
            ],
        )
