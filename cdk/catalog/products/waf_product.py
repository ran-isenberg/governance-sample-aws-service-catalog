from aws_cdk import CfnParameter, aws_sns
from aws_cdk import aws_servicecatalog as servicecatalog
from aws_cdk import aws_wafv2 as waf
from constructs import Construct

from cdk.catalog.products.governance_enabler import create_governance_enabler

WAF_PRODUCT_NAME = 'WAF Rules Product'
WAF_PRODUCT_VERSION = '1.0.0'
WAF_PRODUCT_DESCRIPTION = 'Collection of WAF ACL rules for API Gateway'


class WafRulesProduct(servicecatalog.ProductStack):
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

        consumer_name_param = CfnParameter(self, 'ConsumerName', type='String', description='Name of the team that deployed the product')

        # Create WAF WebACL with AWS Managed Rules
        self.acl = waf.CfnWebACL(
            self,
            'ProductApiGatewayWebAcl',
            scope='REGIONAL',  # Change to CLOUDFRONT if you're using edge-optimized API
            default_action=waf.CfnWebACL.DefaultActionProperty(allow={}),
            name=f'{id}-Waf',
            visibility_config=waf.CfnWebACL.VisibilityConfigProperty(
                sampled_requests_enabled=True, cloud_watch_metrics_enabled=True, metric_name='ProductApiGatewayWebAcl'
            ),
            rules=[
                waf.CfnWebACL.RuleProperty(
                    name='Product-AWSManagedRulesCommonRuleSet',
                    priority=0,
                    override_action={'none': {}},
                    statement=waf.CfnWebACL.StatementProperty(
                        managed_rule_group_statement=waf.CfnWebACL.ManagedRuleGroupStatementProperty(
                            name='AWSManagedRulesCommonRuleSet', vendor_name='AWS'
                        )
                    ),
                    visibility_config=waf.CfnWebACL.VisibilityConfigProperty(
                        sampled_requests_enabled=True,
                        cloud_watch_metrics_enabled=True,
                        metric_name='Product-AWSManagedRulesCommonRuleSet',
                    ),
                ),
                # Block Amazon IP reputation list managed rule group
                waf.CfnWebACL.RuleProperty(
                    name='Product-AWSManagedRulesAmazonIpReputationList',
                    priority=1,
                    override_action={'none': {}},
                    statement=waf.CfnWebACL.StatementProperty(
                        managed_rule_group_statement=waf.CfnWebACL.ManagedRuleGroupStatementProperty(
                            name='AWSManagedRulesAmazonIpReputationList', vendor_name='AWS'
                        )
                    ),
                    visibility_config=waf.CfnWebACL.VisibilityConfigProperty(
                        sampled_requests_enabled=True,
                        cloud_watch_metrics_enabled=True,
                        metric_name='Product-AWSManagedRulesAmazonIpReputationList',
                    ),
                ),
                # Block Anonymous IP list managed rule group
                waf.CfnWebACL.RuleProperty(
                    name='Product-AWSManagedRulesAnonymousIpList',
                    priority=2,
                    override_action={'none': {}},
                    statement=waf.CfnWebACL.StatementProperty(
                        managed_rule_group_statement=waf.CfnWebACL.ManagedRuleGroupStatementProperty(
                            name='AWSManagedRulesAnonymousIpList', vendor_name='AWS'
                        )
                    ),
                    visibility_config=waf.CfnWebACL.VisibilityConfigProperty(
                        sampled_requests_enabled=True,
                        cloud_watch_metrics_enabled=True,
                        metric_name='Product-AWSManagedRulesAnonymousIpList',
                    ),
                ),
                # rule for blocking known Bad Inputs
                waf.CfnWebACL.RuleProperty(
                    name='Product-AWSManagedRulesKnownBadInputsRuleSet',
                    priority=3,
                    override_action={'none': {}},
                    statement=waf.CfnWebACL.StatementProperty(
                        managed_rule_group_statement=waf.CfnWebACL.ManagedRuleGroupStatementProperty(
                            name='AWSManagedRulesKnownBadInputsRuleSet', vendor_name='AWS'
                        )
                    ),
                    visibility_config=waf.CfnWebACL.VisibilityConfigProperty(
                        sampled_requests_enabled=True,
                        cloud_watch_metrics_enabled=True,
                        metric_name='Product-AWSManagedRulesKnownBadInputsRuleSet',
                    ),
                ),
            ],
        )

        self.governance_enabler = create_governance_enabler(self, topic, product_name, product_version, consumer_name_param.value_as_string)
        self.governance_enabler.node.add_dependency(self.acl)
