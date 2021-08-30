from typing import List, Optional

from pydantic import BaseModel, Field, validator

from ..utils import from_base64


class Cell(BaseModel):
    column: str
    timestamp: Optional[int]
    value: str = Field(..., alias="$")

    @validator("value")
    def _value_from_b64(cls, v):
        return from_base64(v)

    @validator("column")
    def _column_from_b64(cls, v):
        return from_base64(v)

    class Config:
        allow_population_by_field_name = True


class Row(BaseModel):
    key: str
    Cell: List[Cell]

    @validator("key")
    def _from_b64(cls, v):
        return from_base64(v)


class CellSet(BaseModel):
    Row: List[Row]
