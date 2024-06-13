from typing import List, Optional
from pydantic import BaseModel, HttpUrl
from pydantic import validator


class GeneratorRequest(BaseModel):
    prompt: str
    grok: Optional[bool] = True
    batch_size: int = 4
    model: str = "llama3-70b-8192"


class GeneratorBulkRequest(BaseModel):
    stories: List[GeneratorRequest]
