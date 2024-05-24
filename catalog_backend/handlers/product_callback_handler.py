# pylint: disable=no-value-for-parameter,unused-argument
import json
from typing import Any, Dict

from aws_lambda_env_modeler import get_environment_variables, init_environment_variables
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.utilities.parser.models import SqsModel
from aws_lambda_powertools.utilities.typing import LambdaContext
from crhelper import CfnResource

from catalog_backend.handlers.models.env_vars import VisibilityEnvVars
from catalog_backend.handlers.utils.observability import logger, metrics, tracer
from catalog_backend.logic.product_lifecycle import delete_product, provision_product, update_product
from catalog_backend.models.input import ProductCreateEventModel, ProductDeleteEventModel, ProductUpdateEventModel

CFN_RESOURCE = CfnResource(json_logging=False, log_level='INFO', boto_level='CRITICAL', sleep_on_delete=0)


@init_environment_variables(model=VisibilityEnvVars)
@logger.inject_lambda_context()
@metrics.log_metrics
@tracer.capture_lambda_handler(capture_response=False)
def handle_product_event(event: Dict[str, Any], context: LambdaContext) -> None:
    logger.info('processing product SQS event', event=event)

    try:
        parsed_envelope = SqsModel.model_validate(event)
        # Batch size for the SQS integration is configured to size of 1 (CDK)
        for record in parsed_envelope.Records:
            record_body = json.loads(record.body)  # type: ignore
            logger.info('processing product SQS body', record_body=record_body)
            CFN_RESOURCE(record_body, context)
    except Exception as ex:
        logger.exception('failed to process product SQS event')
        CFN_RESOURCE.init_failure(ex)


@CFN_RESOURCE.create
def create_event(event: Dict[str, Any], context: LambdaContext) -> str:
    """
    Parses a product create request and calls the handler.
    Return an id that will be used for the resource PhysicalResourceId
    """
    logger.info('custom resource create flow', event=event)
    env_vars = get_environment_variables(model=VisibilityEnvVars)

    # parse product input as a create custom resource  request
    try:
        parsed_event = ProductCreateEventModel.model_validate(event)
        logger.append_keys(stack_id=parsed_event.stack_id, product=parsed_event.resource_properties)
        logger.info('parsed create product details')
        resource_id = provision_product(product_details=parsed_event, table_name=env_vars.TABLE_NAME, portfolio_id=env_vars.PORTFOLIO_ID)
        metrics.add_metric(name='CreatedProducts', unit=MetricUnit.Count, value=1)
        return resource_id
    except Exception:
        logger.exception('failed to process created product')
        metrics.add_metric(name='FailedCreatedProducts', unit=MetricUnit.Count, value=1)
        raise  # CFN_RESOURCE will fail the request


@CFN_RESOURCE.update
def update_event(event: Dict[str, Any], context: LambdaContext) -> None:
    """
    Parses a product update request and calls the handler.
    Return an id for the new PhysicalResourceId. CloudFormation will send
    a delete event with the old PhysicalResourceId when stack update completes.
    If the old PhysicalResourceId is returned CloudFormation won't call a delete request after the update.
    """
    logger.info('custom resource update flow', event=event)
    env_vars = get_environment_variables(model=VisibilityEnvVars)

    try:
        # parse product input as a delete custom resource  request
        parsed_event = ProductUpdateEventModel.model_validate(event)
        logger.append_keys(stack_id=parsed_event.stack_id, product=parsed_event.resource_properties, old_product=parsed_event.old_resource_properties)
        metrics.add_metric(name='UpdatedProducts', unit=MetricUnit.Count, value=1)
        logger.info('parsed update product details')
        update_product(product_details=parsed_event, table_name=env_vars.TABLE_NAME, portfolio_id=env_vars.PORTFOLIO_ID)
    except Exception:
        logger.exception('failed to process updated product')
        metrics.add_metric(name='FailedUpdatedProducts', unit=MetricUnit.Count, value=1)
        raise  # CFN_RESOURCE will fail the request


@CFN_RESOURCE.delete
def delete_event(event: Dict[str, Any], context: LambdaContext) -> None:
    """
    Parses a product delete request and calls the handler.
    Delete never returns anything. Should not fail if the underlying resources are already deleted. Desired state.
    """
    logger.info('custom resource delete flow', event=event)
    metrics.add_metric(name='DeletedProducts', unit=MetricUnit.Count, value=1)
    env_vars = get_environment_variables(model=VisibilityEnvVars)

    try:
        # parse product input as a delete custom resource  request
        parsed_event = ProductDeleteEventModel.model_validate(event)
        logger.append_keys(stack_id=parsed_event.stack_id, product=parsed_event.resource_properties)
        metrics.add_metric(name='DeleteProduct', unit=MetricUnit.Count, value=1)
        logger.info('parsed delete product details')
        delete_product(product_details=parsed_event, table_name=env_vars.TABLE_NAME, portfolio_id=env_vars.PORTFOLIO_ID)
    except Exception:
        logger.exception('failed to process deleted product')
        metrics.add_metric(name='FailedDeletedProducts', unit=MetricUnit.Count, value=1)
        raise  # CFN_RESOURCE will fail the request
