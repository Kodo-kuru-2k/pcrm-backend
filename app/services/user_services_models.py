import enum
from typing import Optional

from pydantic import BaseModel, root_validator


class Quarter(enum.Enum):
    Q1 = "Q1"
    Q2 = "Q2"
    Q3 = "Q3"
    Q4 = "Q4"


class DateModel(BaseModel):
    year: int
    quarter: Quarter
    end_month: Optional[int] = None

    @root_validator
    def set_start_and_end_month(cls, values):
        if values["quarter"].name == Quarter.Q1.name:
            values["end_month"] = 6
        elif values["quarter"].name == Quarter.Q2.name:
            values["end_month"] = 9
        elif values["quarter"].name == Quarter.Q3.name:
            values["end_month"] = 12
        elif values["quarter"].name == Quarter.Q4.name:
            values["end_month"] = 3
        return values
