from catalog_backend.dal import get_dal_handler
from catalog_backend.dal.db_handler import DalHandler
from catalog_backend.handlers.utils.observability import tracer
from catalog_backend.models.input import ProductCreateEventModel


# return the request_id of the product which will be used as the custom resource logical id
@tracer.capture_method(capture_response=False)
def provision_product(
    table_name: str,
    portfolio_id: str,
    product_details: ProductCreateEventModel,
) -> str:
    dal_handler: DalHandler = get_dal_handler(table_name)
    dal_handler.add_product_deployment(
        portfolio_id=portfolio_id,
        product_stack_id=product_details.stack_id,
        product_name=product_details.resource_properties.product_name,
        product_version=product_details.resource_properties.product_version,
        account_id=product_details.resource_properties.account_id,
        consumer_name=product_details.resource_properties.consumer_name,
        region=product_details.resource_properties.region,
    )
    return product_details.request_id
