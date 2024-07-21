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


def tagger(
    narration: str, response_model: BaseModel, model: str = "mixtral-8x7b-32768"
):

    response: response_model = client.chat.completions.create(
        model=model,
        max_tokens=5000,
        response_model=response_model,
        messages=[
            {
                "role": "user",
                "content": f"Given the following narration {narration} extract the data in the correct form",
            },
        ],
    )
    return response


# x = tagger(
#     narration=""" In a quaint village nestled between rolling hills and emerald forests, there lived a young woman named Elara. With her radiant ruby eyes, sprinkled with freckles, and a smile that could light up the darkest night, she was the heart and soul of her village. Elara had short, chestnut hair that framed her face perfectly, and she always adorned herself with dark makeup that accentuated her striking features.

# Elara's days were spent wandering the lush meadows, picking wildflowers, and capturing the beauty of nature with her old, trusty camera. She had a gift for photography, a talent passed down from her mother, who had been the village's historian. Elara's photographs were more than just images; they were stories, each one capturing the essence of the moment and the soul of her subjects.

# One misty morning, as the soft light of dawn painted the sky in hues of pink and gold, Elara ventured into the forest, her camera slung over her shoulder. She had heard whispers of an ancient tree deep within the woods, a tree that was said to grant wishes to those who found it. Intrigued and driven by her insatiable curiosity, she set out on her journey.

# The forest was a mystical place, with towering trees and a carpet of moss that muffled her footsteps. As she walked, she could feel the magic in the air, a palpable energy that made her heart race with excitement. After hours of wandering, Elara stumbled upon a clearing, and there it stood—the ancient tree, its gnarled branches reaching out like welcoming arms.

# Elara approached the tree with reverence, her breath catching in her throat. She placed her hand on the rough bark and closed her eyes, making a silent wish. In that moment, the forest seemed to hold its breath, and a gentle breeze rustled the leaves, as if acknowledging her presence.

# When Elara opened her eyes, she saw a small, delicate flower blooming at the base of the tree, its petals shimmering with an ethereal light. She knelt down and carefully picked the flower, feeling a sense of peace wash over her. As she stood, she noticed a figure emerging from the shadows—a young man with kind eyes and a warm smile.

# He introduced himself as Aric, a wanderer and a storyteller. He had been searching for the ancient tree as well, drawn by the same legends that had brought Elara there. The two quickly became friends, sharing stories and dreams as they made their way back to the village.

# Days turned into weeks, and Elara and Aric grew inseparable. Together, they explored the beauty of their world, capturing moments with Elara's camera and weaving tales with Aric's words. Their bond blossomed into a deep and abiding love, one that was as timeless as the ancient tree that had brought them together.

# Years later, as they stood hand in hand beneath the tree's sprawling branches, they made a new wish—for a lifetime of adventures, love, and stories yet to be told. And as the wind whispered through the leaves, it seemed to carry their wishes to the heavens, sealing their fate with the magic of the forest.

# Elara and Aric's love story became a legend in their village, a tale of serendipity, dreams, and the enduring power of love. And though the years passed and the world changed, the ancient tree stood as a testament to their timeless bond, a symbol of hope and the beauty of wishes fulfilled.""",
#     response_model=YouTubeUploadTask,
# )


# print(x)
