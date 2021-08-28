from typing import List, Optional

from pydantic import BaseModel


class Region(BaseModel):
    name: str  # base64 encoded
    stores: Optional[int]
    storefiles: Optional[int]
    storefileSizeMB: Optional[int]
    storefileIndexSizeKB: Optional[int]
    readRequestsCount: Optional[int]
    writeRequestsCount: Optional[int]
    rootIndexSizeKB: Optional[int]
    totalStaticIndexSizeKB: Optional[int]
    totalStaticBloomSizeKB: Optional[int]
    totalCompactingKVs: Optional[int]
    currentCompactedKVs: Optional[int]
    memstoreSizeMB: Optional[int]


class LiveNode(BaseModel):
    name: str  # base64 encoded(name):port
    startCode: Optional[int]
    requests: Optional[int]
    heapSizeMB: Optional[int]
    maxHeapSizeMB: Optional[int]
    Region: List[Region]


class StorageClusterStatus(BaseModel):
    LiveNodes: List[LiveNode]
    DeadNodes: List[str]  # TODO: Unsure on what a DeadNode looks like
    regions: Optional[int]
    requests: Optional[int]
    averageLoad: Optional[float]
