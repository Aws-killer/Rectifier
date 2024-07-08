from fastapi import APIRouter, HTTPException, status, BackgroundTasks, UploadFile, Query
from .Schema import GeneratorRequest, GeneratorBulkRequest
from .utils.GroqInstruct import chatbot, VideoOutput, Scene
from .utils.Cohere import chatbot as cohere_chat
from .utils.HuggingChat import Hugging
from .Story.Story import Story
import asyncio, pprint, json
from tqdm import tqdm
from .database.Model import models, database_url, Scene, Project, database
from .utils.RenderVideo import RenderVideo
from .Prompts.StoryGen import Prompt
from App.Editor.editorRoutes import celery_task, EditorRequest
import uuid


async def update_scene(model_scene):
    await model_scene.generate_scene_data()
    await model_scene.update(**model_scene.__dict__)


async def from_dict_generate(data: Story):
    generated_strory = data
    await generate_assets(generated_story=generated_strory)


async def generate_assets(generated_story: Story, batch_size=4):
    x = await Project.objects.create(name=str(uuid.uuid4()))

    # Assuming generated_story.scenes is a list of scenes
    scene_updates = []
    with tqdm(total=len(generated_story.scenes)) as pbar:
        for i in range(0, len(generated_story.scenes), batch_size):
            batch = generated_story.scenes[
                i : i + batch_size
            ]  # Get a batch of two story scenes
            batch_updates = []

            for story_scene in batch:
                model_scene = await Scene.objects.create(project=x)
                model_scene.image_prompts = story_scene.image_prompts
                model_scene.narration = story_scene.narration
                await model_scene.update(**model_scene.__dict__)
                batch_updates.append(
                    update_scene(model_scene)
                )  # Append update coroutine to batch_updates
            scene_updates.extend(batch_updates)  # Accumulate updates for later awaiting
            await asyncio.gather(
                *batch_updates
            )  # Await update coroutines for this batch
            pbar.update(len(batch))  # Increment progress bar by the size of the batch

    temp = await x.generate_json()
    # print(temp)

    # await renderr.render_video(temp)
    request = EditorRequest.model_validate(temp)
    await celery_task(video_task=request)


async def main(request: GeneratorRequest):
    topic = request.prompt
    batch_size = request.batch_size
    renderr = RenderVideo()
    huggChat = Hugging()
    if request.grok:
        message = cohere_chat(Prompt.format(topic=topic), model=request.model)

    else:
        temp = await huggChat.chat(
            Prompt.format(topic=topic)
            + f"Match your response to the following schema:  {VideoOutput.model_json_schema()} Make sure to return an instance of the JSON, not the schema itself, and nothing else."
        )
        message = temp
    generated_story = Story.from_dict(message["scenes"])

    print("Generated Story ✅")
    await generate_assets(generated_story=generated_story, batch_size=batch_size)


async def bulkGenerate(bulkRequest: GeneratorBulkRequest):
    tasks = []
    for request in bulkRequest.stories:
        tasks.append(main(request=request))

    await asyncio.gather(*tasks)


generator_router = APIRouter(tags=["video-Generator"])


@generator_router.post("/generate_video")
async def generate_video(
    videoRequest: GeneratorRequest, background_task: BackgroundTasks
):
    background_task.add_task(main, videoRequest)
    return {"task_id": "started"}


@generator_router.post("/generate_video_from_json")
async def generate_video_from_json(jsonReq: Story, background_task: BackgroundTasks):
    background_task.add_task(from_dict_generate, jsonReq)
    return {"task_id": "started"}


@generator_router.post("/generate_video_bulk")
async def generate_video_bulk(
    BulkvideoRequest: GeneratorBulkRequest, background_task: BackgroundTasks
):
    background_task.add_task(bulkGenerate, BulkvideoRequest)
    return {"task_id": "started"}
