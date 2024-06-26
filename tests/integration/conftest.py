import os

import pytest

from cdk.catalog.constants import (
    METRICS_DIMENSION_VALUE,
    METRICS_NAMESPACE,
    PORTFOLIO_ID_OUTPUT,
    POWER_TOOLS_LOG_LEVEL,
    POWERTOOLS_SERVICE_NAME,
    SERVICE_NAME,
    TABLE_NAME_OUTPUT,
)
from tests.utils import get_stack_output


@pytest.fixture(scope='module', autouse=True)
def init():
    os.environ[POWERTOOLS_SERVICE_NAME] = SERVICE_NAME
    os.environ['POWERTOOLS_METRICS_NAMESPACE'] = METRICS_NAMESPACE
    os.environ[POWER_TOOLS_LOG_LEVEL] = 'DEBUG'
    os.environ['METRICS_DIMENSION_KEY'] = METRICS_DIMENSION_VALUE
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'  # used for appconfig mocked boto calls
    os.environ['TABLE_NAME'] = get_stack_output(TABLE_NAME_OUTPUT)
    os.environ['PORTFOLIO_ID'] = get_stack_output(PORTFOLIO_ID_OUTPUT)


@pytest.fixture(scope='module', autouse=True)
def table_name():
    return os.environ['TABLE_NAME']


@pytest.fixture(scope='module', autouse=True)
def portfolio_id():
    return os.environ['PORTFOLIO_ID']
