from typing import List, Optional
from pydantic import BaseModel, HttpUrl
from pydantic import validator


class LinkInfo(BaseModel):
    file_name: str
    link: HttpUrl


class Constants(BaseModel):
    duration: Optional[int]
    height: Optional[int]
    width: Optional[int]
    text: Optional[dict]




class Explanation(BaseModel):
    highlight: str
    narration: str
    duration: int
    audio: str

class Assets(BaseModel):
    code: str
    Explanation: List[Explanation]


class EditorRequest(BaseModel):
    links: Optional[List[LinkInfo]]  # List of LinkInfo objects
    assets: Assets
    constants: Optional[Constants]


class TaskInfo(BaseModel):
    task_id: str
    progress: int
    completed_tasks: List[str]
