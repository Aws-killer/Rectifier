import aiohttp
import asyncio
from itertools import chain


class VideoGenerator:
    def __init__(self):
        self.base_urls = [f"https://yakova-depthflow-{i}.hf.space" for i in range(10)]
        self.headers = {"accept": "application/json"}
        self.default_params = {
            "frame_rate": 30,
            "duration": 3,
            "quality": 1,
            "ssaa": 0.8,
            "raw": "false",
        }

    async def generate_video(self, base_url, params):
        url = f"{base_url}/generate_video"

        async with aiohttp.ClientSession() as session:
            async with session.post(
                url, params=params, headers=self.headers
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    output_file = data.get("output_file")
                    return output_file
                else:
                    print(f"Request to {url} failed with status: {response.status}")
                    return None

    async def check_video_ready(self, base_url, output_file):
        url = f"{base_url}/download/{output_file}"

        async with aiohttp.ClientSession() as session:
            while True:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        video_content = await response.read()
                        if len(video_content) > 0:
                            return url
                        else:
                            print(
                                f"Video {output_file} is ready but the file size is zero, retrying in 10 seconds..."
                            )
                            await asyncio.sleep(10)
                    elif response.status == 404:
                        data = await response.json()
                        if data.get("detail") == "Video not found":
                            print(
                                f"Video {output_file} not ready yet, retrying in 10 seconds..."
                            )
                            await asyncio.sleep(120)
                        else:
                            print(f"Unexpected response for {output_file}: {data}")
                            return None
                    else:
                        print(f"Request to {url} failed with status: {response.status}")
                        return None

    async def process_image(self, base_url, image_link):
        params = self.default_params.copy()
        params["image_link"] = image_link

        output_file = await self.generate_video(base_url, params)
        if output_file:
            print(f"Generated video file id: {output_file} for image {image_link}")
            video_url = await self.check_video_ready(base_url, output_file)
            if video_url:
                print(
                    f"Video for {image_link} is ready and can be downloaded from: {video_url}"
                )
                return video_url
            else:
                print(f"Failed to get the video URL for {image_link}")
                return None
        else:
            print(f"Failed to generate the video for {image_link}")
            return None

    def flatten(self, nested_list):
        return list(chain.from_iterable(nested_list))

    def nest(self, flat_list, nested_dims):
        it = iter(flat_list)
        return [[next(it) for _ in inner_list] for inner_list in nested_dims]

    async def run(self, nested_image_links):
        flat_image_links = self.flatten(nested_image_links)
        tasks = []
        base_index = 0

        for image_link in flat_image_links:
            base_url = self.base_urls[base_index % len(self.base_urls)]
            tasks.append(self.process_image(base_url, image_link))
            base_index += 1

        flat_video_urls = await asyncio.gather(*tasks)
        nested_video_urls = self.nest(flat_video_urls, nested_image_links)
        return nested_video_urls


# # Example usage
# nested_image_links = [
#     [
#         "https://replicate.delivery/yhqm/mQId1rdf4Z3odCyB7cPsx1KwhHfdRc3w44eYAGNG9AQfV0dMB/out-0.png"
#     ],
#     [
#         "https://replicate.delivery/yhqm/mQId1rdf4Z3odCyB7cPsx1KwhHfdRc3w44eYAGNG9AQfV0dMB/out-1.png",
#         "https://replicate.delivery/yhqm/mQId1rdf4Z3odCyB7cPsx1KwhHfdRc3w44eYAGNG9AQfV0dMB/out-2.png",
#     ],
#     # Add more nested image links here
# ]

# loop = asyncio.get_event_loop()
# video_generator = VideoGenerator()
# nested_video_urls = loop.run_until_complete(video_generator.run(nested_image_links))

# print("Generated video URLs:", nested_video_urls)
