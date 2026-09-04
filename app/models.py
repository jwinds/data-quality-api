from typing import Any
from pydantic import BaseModel


class AllowedValuesRule(BaseModel):
    field: str
    allowed_values: list[Any]


class QualityCheckRequest(BaseModel):
    records: list[dict[str, Any]]
    allowed_values_rules: list[AllowedValuesRule] = []