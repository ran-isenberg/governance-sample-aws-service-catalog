from functools import lru_cache

from catalog_backend.dal.db_handler import DalHandler
from catalog_backend.dal.dynamo_dal_handler import DynamoDalHandler


@lru_cache
def get_dal_handler(table_name: str) -> DalHandler:
    return DynamoDalHandler(table_name)
