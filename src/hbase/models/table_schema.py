from typing import List, Optional

from pydantic import BaseModel


class Attribute(BaseModel):
    name: str
    value: str


class ColumnSchema(BaseModel):
    name: Optional[str]
    VERSIONS: Optional[int]
    EVICT_BLOCKS_ON_CLOSE: Optional[bool]
    NEW_VERSION_BEHAVIOR: Optional[bool]
    KEEP_DELETED_CELLS: Optional[bool]
    CACHE_DATA_ON_WRITE: Optional[bool]
    DATA_BLOCK_ENCODING: Optional[str]
    TTL: Optional[int]
    MIN_VERSIONS: Optional[int]
    REPLICATION_SCOPE: Optional[int]
    BLOOMFILTER: Optional[str]
    CACHE_INDEX_ON_WRITE: Optional[bool]
    IN_MEMORY: Optional[bool]
    CACHE_BLOOMS_ON_WRITE: Optional[bool]
    PREFETCH_BLOCKS_ON_OPEN: Optional[bool]
    COMPRESSION: Optional[str]
    LOCKCACHE: Optional[bool]
    BLOCKSIZE: Optional[int]


class TableSchema(BaseModel):
    name: Optional[str]
    ColumnSchema: List[ColumnSchema]
    IS_META: Optional[bool]
