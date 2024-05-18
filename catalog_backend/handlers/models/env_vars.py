from typing import Annotated, Literal

from pydantic import BaseModel, Field


class Observability(BaseModel):
    POWERTOOLS_SERVICE_NAME: Annotated[str, Field(min_length=1)]
    LOG_LEVEL: Literal['DEBUG', 'INFO', 'ERROR', 'CRITICAL', 'WARNING', 'EXCEPTION']


class GovernanceEnvVars(Observability):
    TABLE_NAME: Annotated[str, Field(min_length=1)]
    PORTFOLIO_ID: Annotated[str, Field(min_length=1)]
