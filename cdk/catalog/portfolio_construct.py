from typing import List

from aws_cdk import aws_servicecatalog as servicecatalog
from aws_cdk import aws_sns
from constructs import Construct

import cdk.catalog.constants as constants
from cdk.catalog.products.cicd_product import CICD_PRODUCT_DESCRIPTION, CICD_PRODUCT_NAME, CICD_PRODUCT_VERSION, CiCdProduct
from cdk.catalog.products.waf_product import WAF_PRODUCT_DESCRIPTION, WAF_PRODUCT_NAME, WAF_PRODUCT_VERSION, WafRulesProduct


class PortfolioConstruct(Construct):
    def __init__(self, scope: Construct, id: str, governance_topic: aws_sns.Topic, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        products = self._create_products(governance_topic)
        self.portfolio = self._create_portfolio(products)
        self._share_portfolio()

    def _create_portfolio(self, products: List[servicecatalog.CloudFormationProduct]) -> servicecatalog.Portfolio:
        # Create a Service Catalog portfolio
        portfolio = servicecatalog.Portfolio(
            self,
            constants.PORTFOLIO_ID,
            display_name='Platform engineering Governance Portfolio',
            provider_name='Platform engineering',
        )

        for product in products:
            portfolio.add_product(product)

        return portfolio

    def _create_products(self, governance_topic: aws_sns.Topic) -> List[servicecatalog.CloudFormationProduct]:
        # create first product
        cicd_product = servicecatalog.CloudFormationProduct(
            self,
            'CiCdProduct',
            product_name=CICD_PRODUCT_NAME,
            owner='Platform engineering',
            product_versions=[
                servicecatalog.CloudFormationProductVersion(
                    cloud_formation_template=servicecatalog.CloudFormationTemplate.from_product_stack(
                        CiCdProduct(self, 'CiCdProductStack', CICD_PRODUCT_NAME, CICD_PRODUCT_VERSION, governance_topic)
                    ),
                    description=CICD_PRODUCT_DESCRIPTION,
                    product_version_name=CICD_PRODUCT_VERSION,
                )
            ],
        )

        # create second product
        waf_product = servicecatalog.CloudFormationProduct(
            self,
            'WafProduct',
            product_name=WAF_PRODUCT_NAME,
            owner='Platform engineering',
            product_versions=[
                servicecatalog.CloudFormationProductVersion(
                    cloud_formation_template=servicecatalog.CloudFormationTemplate.from_product_stack(
                        WafRulesProduct(
                            self,
                            'WafProductStack',
                            WAF_PRODUCT_NAME,
                            WAF_PRODUCT_VERSION,
                            governance_topic,
                        )
                    ),
                    description=WAF_PRODUCT_DESCRIPTION,
                    product_version_name=WAF_PRODUCT_VERSION,
                )
            ],
        )

        return [cicd_product, waf_product]

    def _share_portfolio(self) -> None:
        # share with account numbers, ideally you would share across your organization
        # self.portfolio.share_with_account(account_number)
        return
