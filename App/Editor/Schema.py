from typing import List, Optional
from pydantic import BaseModel, HttpUrl
from pydantic import validator


class LinkInfo(BaseModel):
    file_name: str
    link: HttpUrl


class Assets(BaseModel):
    type: str
    sequence: List[dict]

    @validator("type")
    def valid_type(cls, v):
        if v not in ["video", "audio", "text", "image", "sfx", "background"]:
            raise ValueError("Invalid asset type")
        return v


class EditorRequest(BaseModel):
    links: Optional[List[LinkInfo]]  # List of LinkInfo objects
    assets: List[Assets]


class TaskInfo(BaseModel):
    task_id: str
    progress: int
    completed_tasks: List[str]
