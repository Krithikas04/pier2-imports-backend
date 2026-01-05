import re
from src.core.error.exceptions import ValidationException
from pydantic import BaseModel, Field, model_validator, field_validator
from typing import Optional


class CustomerOrderQueryParams(BaseModel):
    phone: Optional[str] = Field(None, description="Customer phone number")
    email: Optional[str] = Field(None, description="Customer email address")

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v.strip():
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, v):
                raise ValueError('Invalid email format')
            return v
        return None

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and v.strip():
            # Remove common phone formatting
            clean_phone = re.sub(r'[\s\-\(\)\+]', '', v)
            if not clean_phone.isdigit():
                raise ValueError('Phone number must contain only digits')
            if len(clean_phone) < 10 or len(clean_phone) > 15:
                raise ValueError('Phone number must be between 10-15 digits')
            return v
        return None

    @model_validator(mode="after")
    def at_least_one_required(self):
        if not self.phone and not self.email:
            raise ValidationException("Either phone or email must be provided")
        return self
