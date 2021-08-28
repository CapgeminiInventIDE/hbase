from typing import List, Optional

from pydantic import BaseModel


class Region(BaseModel):
    id: Optional[int]

    startKey: Optional[str]  # Base64 encoded?
    endKey: Optional[str]  # Base64 encoded?
    location: Optional[str]  # Base64 encoded(name):port ?
    name: str  # "<table_name>,,<id>.<something>." Unsure on structure of this


class TableInfo(BaseModel):
    name: str
    Region: List[Region]
