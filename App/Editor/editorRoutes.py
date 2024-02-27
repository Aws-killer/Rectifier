from fastapi import (
    APIRouter,
    HTTPException,
    status,
    BackgroundTasks,
    UploadFile,
    Query,
    Request,
)
from fastapi.responses import StreamingResponse, FileResponse
from .Schema import EditorRequest, TaskInfo
from App.Worker import celery_task, concatenate_videos
from celery.result import AsyncResult
import aiofiles, os, uuid, aiohttp, pprint, json
from App import SERVER_STATE, Task

videditor_router = APIRouter(tags=["vidEditor"])


@videditor_router.post("/create-video")
async def create_video(videoRequest: EditorRequest, background_task: BackgroundTasks):
    background_task.add_task(celery_task, videoRequest)
    return {"task_id": "started"}


@videditor_router.get("/videos/{task_id}/{video_name}")
async def serve_video(request: Request, task_id: str, video_name: str):
    video_directory = "/tmp/Video"
    video_path = os.path.join(video_directory, task_id, video_name)
    print(video_path)
    if not os.path.isfile(video_path):
        raise HTTPException(status=404, detail="Video not found")

    range_header = request.headers.get("Range", None)
    video_size = os.path.getsize(video_path)

    if range_header:
        start, end = range_header.strip().split("=")[1].split("-")
        start = int(start)
        end = video_size if end == "" else int(end)

        headers = {
            "Content-Range": f"bytes {start}-{end}/{video_size}",
            "Accept-Ranges": "bytes",
            "content-disposition": f'inline; filename="{video_name}"',
        }

        content = await read_file_range(video_path, start, end)
        return StreamingResponse(content, media_type="video/mp4", headers=headers)

    return FileResponse(video_path, media_type="video/mp4")


async def read_file_range(path, start, end):
    with open(path, "rb") as file:
        file.seek(start)
        while True:
            data = file.read(1024 * 1024)  # read in chunks of 1MB
            if not data or file.tell() > end:
                break
            yield data


@videditor_router.post("/create-chunks")
async def create_chunks(videoRequest: EditorRequest, background_task: BackgroundTasks):
    video_duration = videoRequest.constants.duration
    task_id = str(uuid.uuid4())
    new_task = Task(TASK_ID=task_id)

    active_nodes = [
        node
        for node in SERVER_STATE.NODES
        if await new_task._check_node_online(node.SPACE_HOST)
    ]
    if len(active_nodes) == 0:
        active_nodes.extend(SERVER_STATE.NODES)

    steps = int(video_duration / len(active_nodes))

    ranges = [[i, i + steps - 1] for i in range(0, video_duration, steps)]
    print(ranges)
    for i, node in enumerate(active_nodes):
        await new_task.add_node(node, i)

    SERVER_STATE.TASKS[task_id] = new_task

    async with aiohttp.ClientSession() as session:
        for i, node in enumerate(active_nodes):
            videoRequest.constants.task = task_id
            videoRequest.constants.chunk = i
            videoRequest.constants.frames = ranges[i]
            if node.MASTER:
                background_task.add_task(celery_task, videoRequest)
                continue
            data = videoRequest.json()
            # pprint.pprint(data)
            async with session.post(
                f"{node.SPACE_HOST}/create-video", json=json.loads(data)
            ) as response:
                if response.status != 200:
                    raise HTTPException(
                        status_code=response.status,
                        detail="Failed to post request to node",
                    )

    return {"task_id": "started"}


@videditor_router.post("/uploadfile/")
async def create_file(
    background_tasks: BackgroundTasks,
    file: UploadFile,
    node: str,
    chunk: int,
    task: str,
):

    chunk_directory = f"/tmp/Video/{task}"
    file_name = f"{chunk_directory}/{chunk}.mp4"
    # Create the directory if it does not exist
    os.makedirs(chunk_directory, exist_ok=True)

    try:
        async with aiofiles.open(file_name, "wb") as f:
            while contents := await file.read(1024 * 1):
                await f.write(contents)

    except Exception as e:
        return {
            "message": f"There was an error uploading the file, error message {str(e)}  "
        }
    finally:
        await file.close()
    running_task = SERVER_STATE.TASKS[task]
    running_task.mark_node_completed(node)
    if running_task.is_completed():
        background_tasks.add_task(concatenate_videos, chunk_directory)

    return {"message": "File uploaded successfully"}
