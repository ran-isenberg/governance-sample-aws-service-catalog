from typing import Annotated, Literal

from pydantic import BaseModel, Field


class Observability(BaseModel):
    POWERTOOLS_SERVICE_NAME: Annotated[str, Field(min_length=1)]
    LOG_LEVEL: Literal['DEBUG', 'INFO', 'ERROR', 'CRITICAL', 'WARNING', 'EXCEPTION']
    POWERTOOLS_METRICS_NAMESPACE: Annotated[str, Field(min_length=1)]


class VisibilityEnvVars(Observability):
    TABLE_NAME: Annotated[str, Field(min_length=1)]
    PORTFOLIO_ID: Annotated[str, Field(min_length=1)]
