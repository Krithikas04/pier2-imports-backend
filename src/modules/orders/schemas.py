from pydantic import BaseModel, Field, field_validator
from typing import Literal


class OrderAnalyticsQueryParams(BaseModel):
    order_by: Literal["asc", "desc"] = Field(..., description="Sort order: asc or desc")

    @field_validator('order_by')
    @classmethod
    def validate_order_by(cls, v: str) -> str:
        if v not in ["asc", "desc"]:
            raise ValueError('order_by must be either "asc" or "desc"')
        return v