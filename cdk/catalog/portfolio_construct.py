from typing import List

from aws_cdk import CfnOutput, aws_sns
from aws_cdk import aws_lambda as _lambda
from aws_cdk import aws_servicecatalog as servicecatalog
from constructs import Construct

import cdk.catalog.constants as constants
from cdk.catalog.products.cicd_product import CiCdProduct
from cdk.catalog.products.waf_product import WafRulesProduct


class PortfolioConstruct(Construct):
    def __init__(self, scope: Construct, id: str, governance_topic: aws_sns.Topic, portfolio_lambda: _lambda.Function, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        products = self._create_products(governance_topic)
        self.portfolio = self._create_portfolio(products, portfolio_lambda)
        self._share_portfolio()

    def _create_portfolio(self, products: List[servicecatalog.CloudFormationProduct], portfolio_lambda: _lambda.Function) -> servicecatalog.Portfolio:
        # Create a Service Catalog portfolio
        portfolio = servicecatalog.Portfolio(
            self,
            constants.PORTFOLIO_ID,
            display_name='Platform engineering Governance Portfolio',
            provider_name='Platform engineering',
        )

        portfolio_lambda.add_environment(constants.PORTFOLIO_ID_ENV_VAR, portfolio.portfolio_id)

        CfnOutput(self, id=constants.PORTFOLIO_ID_OUTPUT, value=portfolio.portfolio_id).override_logical_id(constants.PORTFOLIO_ID_OUTPUT)

        for product in products:
            portfolio.add_product(product)

        return portfolio

    def _create_products(self, governance_topic: aws_sns.Topic) -> List[servicecatalog.CloudFormationProduct]:
        # create first product
        cicd_product = CiCdProduct(self, 'CiCdProductStack', governance_topic)
        cfn_cicd_product = servicecatalog.CloudFormationProduct(
            self,
            'CiCdProduct',
            product_name=cicd_product.product_name,
            owner='Platform engineering',
            product_versions=[
                servicecatalog.CloudFormationProductVersion(
                    cloud_formation_template=servicecatalog.CloudFormationTemplate.from_product_stack(cicd_product),
                    description=cicd_product.product_description,
                    product_version_name=cicd_product.product_version,
                )
            ],
        )

        # create second product
        waf_product = WafRulesProduct(self, 'WafProductStack', governance_topic)
        cfn_waf_product = servicecatalog.CloudFormationProduct(
            self,
            'WafProduct',
            product_name=waf_product.product_name,
            owner='Platform engineering',
            product_versions=[
                servicecatalog.CloudFormationProductVersion(
                    cloud_formation_template=servicecatalog.CloudFormationTemplate.from_product_stack(waf_product),
                    description=waf_product.product_description,
                    product_version_name=waf_product.product_version,
                )
            ],
        )

        return [cfn_cicd_product, cfn_waf_product]

    def _share_portfolio(self) -> None:
        # share with account numbers, ideally you would share across your organization
        # self.portfolio.share_with_account(account_number)
        return
