from typing import Annotated

from pydantic import BaseModel, Field, PositiveInt


class ProductEntry(BaseModel):
    portfolio_id: Annotated[str, Field(min_length=1, max_length=40)]  # primary key
    product_stack_id: Annotated[str, Field(min_length=1, max_length=200)]  # sort key
    name: Annotated[str, Field(min_length=1, max_length=40)]
    version: Annotated[str, Field(min_length=1, max_length=10)]
    account_id: Annotated[str, Field(min_length=1, max_length=40)]
    consumer_name: Annotated[str, Field(min_length=1, max_length=40)]
    region: Annotated[str, Field(min_length=1, max_length=20)]
    created_at: PositiveInt
