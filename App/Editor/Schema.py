from typing import List, Optional
from pydantic import BaseModel, HttpUrl


class EditorRequest(BaseModel):
    links: Optional[List[HttpUrl]]
    script: str


class TaskInfo(BaseModel):
    task_id: str
    progress: int
    completed_tasks: List[str]
