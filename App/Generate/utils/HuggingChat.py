import aiohttp
import json
import re


class Hugging:
    def __init__(self):
        self.url = "https://p01--hugging--legal-stuff--a96n-7tyr.code.run/generate"
        self.headers = {
            "Authorization": "Bearer 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",
            "accept": "application/json",
            "content-type": "application/json",
        }

    async def chat(self, prompt: str):

        payload = {"prompt": prompt}

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.url, headers=self.headers, data=json.dumps(payload)
            ) as response:
                result = await response.text()
                print(result)
                return result
