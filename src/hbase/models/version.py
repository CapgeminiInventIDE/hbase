from typing import Optional

from pydantic import BaseModel


class Version(BaseModel):
    Server: Optional[str] = ""
    Jersey: Optional[str] = ""
    OS: Optional[str] = ""
    REST: Optional[str] = ""
    JVM: Optional[str] = ""


class StorageClusterVersion(BaseModel):
    Version: Optional[str]
