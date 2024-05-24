import pytest
from pydantic import ValidationError

from catalog_backend.handlers.models.env_vars import Observability, VisibilityEnvVars


def test_observability_valid():
    # Test a valid Observability instance
    obs = Observability(
        POWERTOOLS_SERVICE_NAME='MyService',
        LOG_LEVEL='DEBUG',
        POWERTOOLS_METRICS_NAMESPACE='MyNamespace',
    )
    assert obs.POWERTOOLS_SERVICE_NAME == 'MyService'
    assert obs.LOG_LEVEL == 'DEBUG'
    assert obs.POWERTOOLS_METRICS_NAMESPACE == 'MyNamespace'


def test_observability_invalid_power_tools_service_name():
    # Test invalid POWERTOOLS_SERVICE_NAME (too short)
    with pytest.raises(ValidationError):
        Observability(POWERTOOLS_SERVICE_NAME='', LOG_LEVEL='DEBUG')


def test_observability_invalid_log_level():
    # Test invalid LOG_LEVEL
    with pytest.raises(ValidationError):
        Observability(POWERTOOLS_SERVICE_NAME='MyService', LOG_LEVEL='NOT_A_LEVEL')


def test_visibility_env_vars_valid():
    # Test a valid GovernanceEnvVars instance
    gov = VisibilityEnvVars(
        POWERTOOLS_SERVICE_NAME='MyService',
        LOG_LEVEL='INFO',
        TABLE_NAME='MyTable',
        PORTFOLIO_ID='MyPortfolioId',
        POWERTOOLS_METRICS_NAMESPACE='MyNamespace',
    )
    assert gov.POWERTOOLS_SERVICE_NAME == 'MyService'
    assert gov.LOG_LEVEL == 'INFO'
    assert gov.TABLE_NAME == 'MyTable'
    assert gov.PORTFOLIO_ID == 'MyPortfolioId'
    assert gov.POWERTOOLS_METRICS_NAMESPACE == 'MyNamespace'


def test_visibility_env_vars_invalid_table_name():
    # Test invalid TABLE_NAME (too short)
    with pytest.raises(ValidationError):
        VisibilityEnvVars(POWERTOOLS_SERVICE_NAME='MyService', LOG_LEVEL='INFO', TABLE_NAME='', PORTFOLIO_ID='MyPortfolioId')


def test_visibility_env_vars_invalid_portfolio_id():
    # Test invalid PORTFOLIO_ID (too short)
    with pytest.raises(ValidationError):
        VisibilityEnvVars(POWERTOOLS_SERVICE_NAME='MyService', LOG_LEVEL='INFO', TABLE_NAME='MyTable', PORTFOLIO_ID='')


def test_visibility_env_vars_inherited_invalid_log_level():
    # Test inherited invalid LOG_LEVEL from Observability
    with pytest.raises(ValidationError):
        VisibilityEnvVars(POWERTOOLS_SERVICE_NAME='MyService', LOG_LEVEL='INVALID_LEVEL', TABLE_NAME='MyTable', PORTFOLIO_ID='MyPortfolioId')
