from aws_cdk import Aspects, Stack, Tags
from cdk_nag import AwsSolutionsChecks, NagSuppressions
from constructs import Construct

from cdk.catalog.constants import OWNER_TAG, SERVICE_NAME, SERVICE_NAME_TAG
from cdk.catalog.governance_construct import GovernanceConstruct
from cdk.catalog.portfolio_construct import PortfolioConstruct
from cdk.catalog.utils import get_construct_name, get_username


class ServiceStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self._add_stack_tags()
        self.api = GovernanceConstruct(self, get_construct_name(stack_prefix=id, construct_name='Governance'))
        self.portfolio = PortfolioConstruct(self, get_construct_name(stack_prefix=id, construct_name='Portfolio'))

        # add security check
        self._add_security_tests()

    def _add_stack_tags(self) -> None:
        # best practice to help identify resources in the console
        Tags.of(self).add(SERVICE_NAME_TAG, SERVICE_NAME)
        Tags.of(self).add(OWNER_TAG, get_username())

    def _add_security_tests(self) -> None:
        Aspects.of(self).add(AwsSolutionsChecks(verbose=True))
        # Suppress a specific rule for this resource
        NagSuppressions.add_stack_suppressions(
            self,
            [
                {'id': 'AwsSolutions-IAM4', 'reason': 'policy for cloudwatch logs.'},
                {'id': 'AwsSolutions-IAM5', 'reason': 'policy for cloudwatch logs.'},
                {'id': 'AwsSolutions-APIG2', 'reason': 'lambda does input validation'},
                {'id': 'AwsSolutions-APIG1', 'reason': 'not mandatory in a sample template'},
                {'id': 'AwsSolutions-APIG3', 'reason': 'not mandatory in a sample template'},
                {'id': 'AwsSolutions-APIG6', 'reason': 'not mandatory in a sample template'},
                {'id': 'AwsSolutions-APIG4', 'reason': 'authorization not mandatory in a sample template'},
                {'id': 'AwsSolutions-COG4', 'reason': 'not using cognito'},
                {'id': 'AwsSolutions-L1', 'reason': 'False positive'},
                {'id': 'AwsSolutions-SNS2', 'reason': 'ignored for now'},
                {'id': 'AwsSolutions-SNS3', 'reason': 'False positive'},
                {'id': 'AwsSolutions-SQS4', 'reason': 'False positive'},
            ],
        )