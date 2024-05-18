from typing import Literal

from aws_lambda_powertools.utilities.parser.models import (
    CloudFormationCustomResourceCreateModel,
    CloudFormationCustomResourceDeleteModel,
    CloudFormationCustomResourceUpdateModel,
)
from pydantic import BaseModel, Field


class ProductModel(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=40, alias='product_name')
    product_version: str = Field(..., min_length=1, max_length=10, alias='product_version')
    account_id: str = Field(..., min_length=1, max_length=40, alias='account_id')
    consumer_name: str = Field(..., min_length=1, max_length=40, alias='consumer_name')
    region: str = Field(..., min_length=1, max_length=20, alias='region')


class ProductCreateEventModel(CloudFormationCustomResourceCreateModel):
    resource_properties: ProductModel = Field(..., alias='ResourceProperties')
    logical_resource_id: Literal['PlatformGovernanceCustomResource'] = Field(..., alias='LogicalResourceId')


class ProductDeleteEventModel(CloudFormationCustomResourceDeleteModel):
    resource_properties: ProductModel = Field(..., alias='ResourceProperties')
    logical_resource_id: Literal['PlatformGovernanceCustomResource'] = Field(..., alias='LogicalResourceId')


class ProductUpdateEventModel(CloudFormationCustomResourceUpdateModel):
    resource_properties: ProductModel = Field(..., alias='ResourceProperties')
    old_resource_properties: ProductModel = Field(..., alias='OldResourceProperties')
    logical_resource_id: Literal['PlatformGovernanceCustomResource'] = Field(..., alias='LogicalResourceId')
