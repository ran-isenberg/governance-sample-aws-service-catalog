from aws_cdk import Aspects, Stack, Tags
from cdk_nag import AwsSolutionsChecks, NagSuppressions
from constructs import Construct

from cdk.catalog.constants import OWNER_TAG, SERVICE_NAME, SERVICE_NAME_TAG
from cdk.catalog.observability_construct import ObservabilityConstruct
from cdk.catalog.portfolio_construct import PortfolioConstruct
from cdk.catalog.utils import get_construct_name, get_username
from cdk.catalog.visibility_construct import VisibilityConstruct


class ServiceStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        self._add_stack_tags()
        self.governance = VisibilityConstruct(self, get_construct_name(stack_prefix=id, construct_name='Governance'))
        self.portfolio = PortfolioConstruct(
            self, get_construct_name(stack_prefix=id, construct_name='Portfolio'), self.governance.sns_topic, self.governance.governance_lambda
        )
        self.observability = ObservabilityConstruct(
            self,
            get_construct_name(stack_prefix=id, construct_name='Observability'),
            db=self.governance.api_db.db,
            functions=[self.governance.governance_lambda],
            visibility_queue=self.governance.queue,
            visibility_topic=self.governance.sns_topic,
        )

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
                {'id': 'AwsSolutions-IAM5', 'reason': 'wild card is creating by CDK for X-ray tracing and CW logs'},
                {'id': 'AwsSolutions-IAM4', 'reason': 'log retention role created by CDK'},
            ],
        )
