from pydantic import BaseModel, Field
from typing import Literal


class SiteResponse(BaseModel):
    site_name:str = Field(min_length=1)
    utilization: float = Field(ge=0)
    status: Literal["NORMAL", "WARNING", "CRITICAL"]

class SummaryResponse(BaseModel):
    total_records: int
    valid_records: int
    invalid_records: int
    normal_count: int
    warning_count: int
    critical_count: int
