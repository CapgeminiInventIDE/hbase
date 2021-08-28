from typing import List

from pydantic import BaseModel


class TableListItem(BaseModel):
    name: str


class TableList(BaseModel):
    table: List[TableListItem]
