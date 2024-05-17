from typing import Any

from aws_lambda_env_modeler import get_environment_variables, init_environment_variables
from aws_lambda_powertools.event_handler.openapi.params import Body
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.shared.types import Annotated
from aws_lambda_powertools.utilities.typing import LambdaContext

from catalog_backend.handlers.models.dynamic_configuration import MyConfiguration
from catalog_backend.handlers.models.env_vars import MyHandlerEnvVars
from catalog_backend.handlers.utils.dynamic_configuration import parse_configuration
from catalog_backend.handlers.utils.observability import logger, metrics, tracer
from catalog_backend.handlers.utils.rest_api_resolver import ORDERS_PATH, app
from catalog_backend.logic.create_order import create_order
from catalog_backend.models.input import CreateOrderRequest
from catalog_backend.models.output import CreateOrderOutput, InternalServerErrorOutput


@app.post(
    ORDERS_PATH,
    summary='Create an order',
    description='Create an order identified by the body payload',
    response_description='The created order',
    responses={
        200: {
            'description': 'The created order',
            'content': {'application/json': {'model': CreateOrderOutput}},
        },
        501: {
            'description': 'Internal server error',
            'content': {'application/json': {'model': InternalServerErrorOutput}},
        },
    },
    tags=['CRUD'],
)
def handle_create_order(create_input: Annotated[CreateOrderRequest, Body(embed=False, media_type='application/json')]) -> CreateOrderOutput:
    env_vars: MyHandlerEnvVars = get_environment_variables(model=MyHandlerEnvVars)
    logger.debug('environment variables', env_vars=env_vars.model_dump())
    logger.info('got create order request', order=create_input.model_dump())

    my_configuration = parse_configuration(model=MyConfiguration)
    logger.debug('fetched dynamic configuration', configuration=my_configuration.model_dump())

    metrics.add_metric(name='ValidCreateOrderEvents', unit=MetricUnit.Count, value=1)
    response: CreateOrderOutput = create_order(
        order_request=create_input,
        table_name=env_vars.TABLE_NAME,
        context=app.lambda_context,
    )

    logger.info('finished handling create order request')
    return response


@init_environment_variables(model=MyHandlerEnvVars)
@logger.inject_lambda_context(correlation_id_path=correlation_paths.API_GATEWAY_REST)
@metrics.log_metrics
@tracer.capture_lambda_handler(capture_response=False)
def lambda_handler(event: dict[str, Any], context: LambdaContext) -> dict[str, Any]:
    return app.resolve(event, context)
