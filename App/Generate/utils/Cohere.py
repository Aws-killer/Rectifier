import os
import cohere.core
import instructor
import cohere
import instructor


from pydantic import BaseModel, Field

from typing import List, Dict
from pydantic import BaseModel


class Scene(BaseModel):
    narration: str
    image_prompts: List[str]


class VideoOutput(BaseModel):
    scenes: List[Scene]


# Patching the Cohere client with the instructor for enhanced capabilities
client = instructor.from_cohere(
    cohere.Client(
        os.environ.get(
            "COHERE_API",
        )
    ),
    # max_tokens=5000,
    model="command-r-plus",
)


# Now, we can use the response_model parameter using only a base model
# rather than having to use the OpenAISchema class


def chatbot(prompt: str, model: str = "command-r-plus"):

    response: VideoOutput = client.chat.completions.create(
        model=model,
        # max_tokens=5000,
        response_model=VideoOutput,
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    return response.dict()


def tagger(narration: str, response_model: BaseModel, model: str = "command-r-plus"):

    response: response_model = client.chat.completions.create(
        model=model,
        # max_tokens=5000,
        response_model=response_model,
        messages=[
            {
                "role": "user",
                "content": f"Given the following narration {narration} extract the data in the correct form the narration",
            },
        ],
    )
    return response
