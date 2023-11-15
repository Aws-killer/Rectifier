from typing import List, Optional
from pydantic import BaseModel, HttpUrl


class LinkInfo(BaseModel):
    file_name: str
    link: HttpUrl


class EditorRequest(BaseModel):
    links: Optional[List[LinkInfo]]  # List of LinkInfo objects
    script: str


class TaskInfo(BaseModel):
    task_id: str
    progress: int
    completed_tasks: List[str]
