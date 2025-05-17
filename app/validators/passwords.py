import re
from pydantic_core import core_schema
from pydantic import GetCoreSchemaHandler


class PasswordStr(str):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler: GetCoreSchemaHandler):
        def validate(value: str) -> str:
            if not isinstance(value, str):
                raise TypeError("Password must be a string")

            if len(value) < 8:
                raise ValueError("Password must be at least 8 characters")
            if not re.search(r"[A-Z]", value):
                raise ValueError(
                    "Password must contain at least one uppercase letter")
            if not re.search(r"[a-z]", value):
                raise ValueError(
                    "Password must contain at least one lowercase letter")
            if not re.search(r"[0-9]", value):
                raise ValueError("Password must contain at least one digit")
            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
                raise ValueError(
                    "Password must contain at least one special character")

            return value

        return core_schema.no_info_after_validator_function(validate, core_schema.str_schema())
