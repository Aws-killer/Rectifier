import databases
import orm
import asyncio, os
import uuid, random
from pydub import AudioSegment
from .DescriptAPI import Speak
from .Vercel import AsyncImageGenerator
import aiohttp
from typing import List

database_url = "sqlite+aiosqlite:///srv/ok.db"
database = databases.Database(database_url)
models = orm.ModelRegistry(database=database)


class Project(orm.Model):
    tablename = "projects"
    start = 0
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "name": orm.String(max_length=10_000),
        "aspect_ratio": orm.Float(allow_null=True, default=0),
        "transcript": orm.JSON(allow_null=True, default=[]),
        "duration": orm.Integer(allow_null=True, default=0),
        "assets": orm.JSON(allow_null=True, default=[]),
        "links": orm.JSON(allow_null=True, default=[]),
        "constants": orm.JSON(allow_null=True, default={}),
    }

    """
        assets.extend(
        [
            {"type": "video", "sequence": video_sequence},
            {
                "type": "audio",
                "sequence": [
                    {
                        "type": "audio",
                        "name": "transcript.wav",
                        "start": trans_start,
                        "end": trans_end,
                        "props": {
                            "startFrom": trans_start * 30,
                            "endAt": trans_end * 30,
                            "volume": 5,
                        },
                    },
                ],
            },
            {
                "type": "background",
                "sequence": [
                    {
                        "type": "background",
                        "name": "background.mp3",
                        "start": trans_start,
                        "end": trans_end,
                        "props": {
                            "startFrom": trans_start * 30,
                            "endAt": trans_end * 30,
                            "volume": 0.4,
                        },
                    },
                ],
            },
        ]
    )

    
                {
                "type": "image",
                "name": file_name,
                "start": image["start"],
                "end": image["end"],
            }
"""

    async def get_all_scenes(self):
        return await Scene.objects.filter(project=self).all()

    async def generate_json(self):
        project_scenes: List[Scene] = await self.get_all_scenes()
        self.links = []
        self.assets = []
        image_assets = []
        video_assets = []
        audio_assets = []

        transitions = [
            "WaveRight_transparent.webm",
            "WaveLeft_transparent.webm",
            # "WaveBlue_transparent.webm",
            # "Wave_transparent.webm",
            # "Swirl_transparent.webm",
            # "Snow_transparent.webm",
            # "Likes_transparent.webm",
            # "Lightning_transparent.webm",
            # "Happy_transparent.webm",
            # "Fire_transparent.webm",
            # "CurlingWave_transparent.webm",
            # "Cloud_transparent.webm",
        ]

        self.links.append(
            {
                "file_name": "sfx_1.mp3",
                "link": "https://dm0qx8t0i9gc9.cloudfront.net/previews/audio/BsTwCwBHBjzwub4i4/camera-shutter-05_MJn9CZV__NWM.mp3?type=preview&origin=AUDIOBLOCKS&timestamp_ms=1715270679690&publicKey=kUhrS9sKVrQMTvByQMAGMM0jwRbJ4s31HTPVkfDGmwGhYqzmWJHsjIw5fZCkI7ba&organizationId=105711&apiVersion=2.0&stockItemId=2248&resolution=&endUserId=414d29f16694d76c58e7998200a8dcf6f28dc165&projectId=f734c6d7-e39d-4c1d-8f41-417f94cd37ce&searchId=4b01b35a-fafc-45fb-9f40-e98849cb71ac&searchPageId=f24f4c5b-9976-4fd3-9bac-d217d87c723d",
            }
        )
        for scene in project_scenes:
            _, file_name = os.path.split(scene.narration_path)
            self.duration += scene.narration_duration + 1  ## added one for spaces
            self.links.append({"file_name": file_name, "link": scene.narration_link})

            # narration
            audio_assets.append(
                {
                    "type": "audio",
                    "name": file_name,
                    "start": self.start,
                    "end": self.start + scene.narration_duration + 1,
                    "props": {
                        "startFrom": 0,
                        "endAt": scene.narration_duration * 30,
                        "volume": 5,
                    },
                }
            )

            ## images and transitions
            for image in scene.images:
                file_name = str(uuid.uuid4()) + ".png"
                self.links.append({"file_name": file_name, "link": image})
                image_assets.append(
                    {
                        "type": "image",
                        "name": file_name,
                        "start": self.start,
                        "end": self.start + scene.image_duration,
                    }
                )
                self.start = self.start + scene.image_duration

                ## transitions between images
                video_assets.append(
                    {
                        "type": "video",
                        "name": "Effects/" + random.choice(transitions),
                        "start": self.start - 1,
                        "end": self.start + 2,
                        "props": {
                            "startFrom": 1 * 30,
                            "endAt": 3 * 30,
                            "volume": 0,
                        },
                    }
                )

        self.assets.append({"type": "audio", "sequence": audio_assets})
        ## add the images to assets
        self.assets.append({"type": "image", "sequence": image_assets})
        self.assets.append(
            {"type": "video", "sequence": video_assets},
        )
        self.constants = {
            "duration": self.duration * 30,
            "height": 1920,
            "width": 1080,
        }

        await self.update(**self.__dict__)
        return {"links": self.links, "assets": self.assets, "constants": self.constants}

    async def generate_transcript(self):
        pass


class Scene(orm.Model):
    tts = Speak()
    tablename = "scenes"
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "project": orm.ForeignKey(Project),
        "images": orm.JSON(default=None),
        "narration": orm.String(max_length=10_000, allow_null=True, default=""),
        "image_prompts": orm.JSON(default=None),
        "narration_duration": orm.Float(allow_null=True, default=0),
        "image_duration": orm.Float(allow_null=True, default=0),
        "narration_path": orm.String(
            max_length=100,
            allow_null=True,
            default="",
        ),
        "narration_link": orm.String(max_length=10_000, allow_null=True, default=""),
    }

    async def generate_scene_data(self):
        # Run narrate() and generate_images() concurrently
        await asyncio.gather(self.narrate(), self.generate_images())
        self.calculate_durations()

    async def narrate(self):
        link, path = await self._retry_narration_generation()
        self.narration_path = path
        self.narration_link = link

    async def _retry_narration_generation(self):

        retry_count = 0
        while retry_count < 3:
            try:
                return await self.tts.say(text=self.narration)
            except Exception as e:
                print(f"Failed to generate narration: {e}")
                retry_count += 1
                await asyncio.sleep(1)  # Add delay before retrying

        print("Failed to generate narration after 3 attempts.")

    def calculate_durations(self):
        wav_file = AudioSegment.from_file(self.narration_path, format="wav")
        self.narration_duration = int(len(wav_file) / 1000)
        self.image_duration = self.narration_duration / len(self.image_prompts)

    async def generate_images(self):
        self.images = []
        async with aiohttp.ClientSession() as session:
            image_generator = AsyncImageGenerator(session)
            for payload in self.image_prompts:
                result = await image_generator.generate_image(payload)
                status = await image_generator.fetch_image_status(result["id"])
                self.images.extend(status["output"])


class Transition(orm.Model):
    tablename = "transitions"
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "name": orm.String(max_length=100),
        "file_path": orm.String(max_length=100),
    }


class BackgroundMusic(orm.Model):
    tablename = "background_music"
    registry = models
    fields = {
        "id": orm.Integer(primary_key=True),
        "name": orm.String(max_length=100),
        "file_path": orm.String(max_length=100),
    }


# class Testy(orm.Model):
#     tablename = "asd"
#     registry = models
#     fields = {
#         "id": orm.Integer(primary_key=True),
#         "duration": orm.Float(allow_null=True,default=None),
#         "area": orm.Float(allow_null=True,default=None),
#         "radius": orm.Float(allow_null=True,default=None),
#     }

#     def calculate_durations(self):
#         self.area = self.radius**2 * 3.14
#         pass


# # Create the tables
async def create_tables():
    datas = {
        "narration": "Welcome to a journey through some of history's strangest moments! Get ready to explore the bizarre, the unusual, and the downright weird.",
        "image_prompts": [
            "Vintage book opening, revealing strange facts, mixed media collage, curious and intriguing, mysterious, eccentric, macro lens, soft lighting, conceptual photography, cross-processed film, surreal, warm tones, textured paper."
        ],
    }

    await models._create_all(database_url)
    x = await Project.objects.create(name="avatar")
    scene = await Scene.objects.create(project=x)
    scene.narration = datas["narration"]
    scene.image_prompts = datas["image_prompts"]

    await scene.generate_scene_data()
    await scene.objects.update(**scene.__dict__)
    p = await x.get_all_scenes()
    print(p)
    print(scene.__dict__)


# asyncio.run(create_tables())
# # Run the function to create tables
# await create_tables()

# # Example usage:
# await Note.objects.create(text="Buy the groceries.", completed=False)
# note = await Note.objects.get(id=1)
# print(note)
