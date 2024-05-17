from aws_cdk import App
from aws_cdk.assertions import Template

from cdk.catalog.stack import ServiceStack


def test_synthesizes_properly():
    app = App()

    service_stack = ServiceStack(app, 'service-test')

    # Prepare the stack for assertions.
    template = Template.from_stack(service_stack)

    template.resource_count_is('AWS::DynamoDB::GlobalTable', 1)  # main db
    template.resource_count_is('AWS::ServiceCatalog::CloudFormationProduct', 2)  # two products
    template.resource_count_is('AWS::ServiceCatalog::Portfolio', 1)  # one portfolio
