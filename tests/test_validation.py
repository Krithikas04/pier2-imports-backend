import pytest
from pydantic import ValidationError
from src.modules.customer.schemas import CustomerOrderQueryParams
from src.core.error.exceptions import ValidationException


class TestCustomerOrderQueryParams:
    
    def test_valid_email_only(self):
        query = CustomerOrderQueryParams(email="test@example.com")
        assert query.email == "test@example.com"
        assert query.phone is None

    def test_valid_phone_only(self):
        query = CustomerOrderQueryParams(phone="1234567890")
        assert query.phone == "1234567890"
        assert query.email is None

    def test_valid_both_email_and_phone(self):
        query = CustomerOrderQueryParams(email="test@example.com", phone="1234567890")
        assert query.email == "test@example.com"
        assert query.phone == "1234567890"

    def test_invalid_email_format(self):
        with pytest.raises(ValidationError, match="Invalid email format"):
            CustomerOrderQueryParams(email="invalid-email")

    def test_invalid_phone_format(self):
        with pytest.raises(ValidationError, match="Phone number must contain only digits"):
            CustomerOrderQueryParams(phone="123abc4567890")

    def test_phone_too_short(self):
        with pytest.raises(ValidationError, match="Phone number must be between 10-15 digits"):
            CustomerOrderQueryParams(phone="123456789")

    def test_phone_too_long(self):
        with pytest.raises(ValidationError, match="Phone number must be between 10-15 digits"):
            CustomerOrderQueryParams(phone="1234567890123456")

    def test_phone_with_formatting_accepted(self):
        query = CustomerOrderQueryParams(phone="+1 (234) 567-8900")
        assert query.phone == "+1 (234) 567-8900"

    def test_neither_email_nor_phone_provided(self):
        with pytest.raises(ValidationException, match="Either phone or email must be provided"):
            CustomerOrderQueryParams()

    def test_empty_email_and_phone(self):
        with pytest.raises(ValidationException, match="Either phone or email must be provided"):
            CustomerOrderQueryParams(email="", phone="")

    def test_valid_international_phone(self):
        query = CustomerOrderQueryParams(phone="12345678901")
        assert query.phone == "12345678901"

    def test_email_max_length(self):
        long_email = "a" * 90 + "@test.com"
        query = CustomerOrderQueryParams(email=long_email)
        assert query.email == long_email