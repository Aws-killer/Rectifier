import os
import uuid
import tempfile
from PIL import Image
from io import BytesIO
from mimetypes import guess_extension
import subprocess
import requests
import asyncio
from itertools import chain


class VideoGenerator:
    def __init__(self):
        self.default_params = {
            "frame_rate": 30,
            "duration": 3,
            "quality": 1,
            "ssaa": 0.8,
            "raw": False,
        }
        self.video_directory = "/tmp/Video"
        self.ensure_video_directory()

    def ensure_video_directory(self):
        if not os.path.exists(self.video_directory):
            os.makedirs(self.video_directory)

    def download_image(self, image_url: str):
        temp_dir = tempfile.mkdtemp()
        response = requests.get(image_url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        image_format = image.format.lower()
        image_extension = guess_extension(f"image/{image_format}")
        if image_extension is None:
            raise ValueError("Cannot detect image file type.")
        image_path = os.path.join(temp_dir, f"image{image_extension}")
        with open(image_path, "wb") as image_file:
            image_file.write(response.content)
        return image_path, image.size

    def make_effect(self, image_link: str, filename: str, params):
        image_path, (width, height) = self.download_image(image_url=image_link)
        destination = os.path.join(self.video_directory, filename)
        command = [
            "depthflow",
            "input",
            "-i",
            image_path,
            "main",
            "-f",
            str(params["frame_rate"]),
            "-t",
            str(params["duration"]),
            "--width",
            str(width),
            "--height",
            str(height),
            "--quality",
            str(params["quality"]),
            "--ssaa",
            str(params["ssaa"]),
            "--benchmark",
        ]
        if params["raw"]:
            command.append("--raw")
        command.extend(["--output", destination])
        subprocess.run(command, check=True)
        return filename

    def process_image(self, image_link):
        filename = f"{str(uuid.uuid4())}.mp4"
        params = self.default_params.copy()
        try:
            video_filename = self.make_effect(image_link, filename, params)
            video_url = f"http://localhost:7860/download/{video_filename}"
            return video_url
        except Exception as e:
            print(f"Failed to generate video for {image_link}: {str(e)}")
            return None

    def flatten(self, nested_list):
        return list(chain.from_iterable(nested_list))

    def nest(self, flat_list, nested_dims):
        it = iter(flat_list)
        return [[next(it) for _ in inner_list] for inner_list in nested_dims]

    async def run(self, nested_image_links):
        flat_image_links = self.flatten(nested_image_links)
        flat_video_urls = []

        for image_link in flat_image_links:
            video_url = await asyncio.get_event_loop().run_in_executor(
                None, self.process_image, image_link
            )
            flat_video_urls.append(video_url)

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
# ]

# loop = asyncio.get_event_loop()
# video_generator = VideoGenerator()
# nested_video_urls = loop.run_until_complete(video_generator.run(nested_image_links))

# print("Generated video URLs:", nested_video_urls)
