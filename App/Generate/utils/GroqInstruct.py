import os
import instructor
from groq import Groq

from pydantic import BaseModel, Field

from typing import List, Dict
from pydantic import BaseModel


class Scene(BaseModel):
    narration: str
    image_prompts: List[str]


class VideoOutput(BaseModel):
    scenes: List[Scene]


client = Groq(api_key="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")

# By default, the patch function will patch the ChatCompletion.create and ChatCompletion.create methods to support the response_model parameter
client = instructor.from_groq(client, mode=instructor.Mode.JSON)


# Now, we can use the response_model parameter using only a base model
# rather than having to use the OpenAISchema class


def chatbot(prompt: str, model: str = "llama3-70b-8192"):

    response: VideoOutput = client.chat.completions.create(
        model=model,
        # model="gemma-7b-it",
        # model="llama2-70b-4096",
        # model="llama3-70b-8192",
        max_tokens=5000,
        response_model=VideoOutput,
        # kwargs={
        #     # "temperature": 1,
        #     "max_tokens": 5000,
        #     # "top_p": 1,
        #     "stream": False,
        #     "stop": None,
        # },
        messages=[
            # {
            #     "role": "system",
            #     "content": """""",
            # },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    return response.dict()
