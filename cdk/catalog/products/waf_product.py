from aws_cdk import aws_servicecatalog as servicecatalog
from aws_cdk import aws_sns
from aws_cdk import aws_wafv2 as waf
from constructs import Construct

from cdk.catalog.products.governance_construct import GovernanceProductConstruct


class WafRulesProduct(servicecatalog.ProductStack):
    WAF_PRODUCT_NAME = 'WAF Rules Product'
    WAF_PRODUCT_VERSION = '1.0.0'
    WAF_PRODUCT_DESCRIPTION = 'Collection of WAF ACL rules for API Gateway'

    def __init__(
        self,
        scope: Construct,
        id: str,
        topic: aws_sns.Topic,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)
        self.id_ = id
        self.product_description = WafRulesProduct.WAF_PRODUCT_DESCRIPTION
        self.product_name = WafRulesProduct.WAF_PRODUCT_NAME
        self.product_version = WafRulesProduct.WAF_PRODUCT_VERSION
        self.acl = self._build_waf_rules()
        self.governance_enabler = GovernanceProductConstruct(
            self,
            'GovernanceEnabler',
            topic,
            self.product_name,
            self.product_version,
        )
        self.governance_enabler.node.add_dependency(self.acl)

    def _build_waf_rules(self) -> waf.CfnWebACL:
        # Create WAF WebACL with AWS Managed Rules
        acl = waf.CfnWebACL(
            self,
            'ProductApiGatewayWebAcl',
            scope='REGIONAL',  # Change to CLOUDFRONT if you're using edge-optimized API
            default_action=waf.CfnWebACL.DefaultActionProperty(allow={}),
            name=f'{self.id_}-Waf',
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
        return acl
