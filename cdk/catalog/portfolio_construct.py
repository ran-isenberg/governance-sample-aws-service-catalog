from aws_cdk import aws_servicecatalog as servicecatalog
from constructs import Construct

from cdk.catalog.products.cicd_product import CiCdProduct
from cdk.catalog.products.waf_product import WafRulesProduct


class PortfolioConstruct(Construct):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # create first product
        cicd_product = servicecatalog.CloudFormationProduct(
            self,
            'CiCdProduct',
            product_name='CI/CD IAM Role Product',
            owner='Platform engineering',
            product_versions=[
                servicecatalog.CloudFormationProductVersion(
                    cloud_formation_template=servicecatalog.CloudFormationTemplate.from_product_stack(CiCdProduct(self, 'CiCdProductStack')),
                    description='An IAM role for CI/CD pipelines',
                )
            ],
        )

        # create second product
        waf_product = servicecatalog.CloudFormationProduct(
            self,
            'WafProduct',
            product_name='Waf rules Product',
            owner='Platform engineering',
            product_versions=[
                servicecatalog.CloudFormationProductVersion(
                    cloud_formation_template=servicecatalog.CloudFormationTemplate.from_product_stack(WafRulesProduct(self, 'WafProductStack')),
                    description='Collection of WAF ACL rules for API Gateway',
                )
            ],
        )

        # Create a Service Catalog portfolio
        portfolio = servicecatalog.Portfolio(
            self,
            'GovernancePortfolio',
            display_name='Platform engineering Governance Portfolio',
            provider_name='Platform engineering',
        )

        # Add the products to the portfolio
        portfolio.add_product(cicd_product)
        portfolio.add_product(waf_product)
