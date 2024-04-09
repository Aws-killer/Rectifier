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
from App.Worker import celery_task
from celery.result import AsyncResult
import aiofiles, os, uuid, aiohttp, pprint, json

import os
videditor_router = APIRouter(tags=["vidEditor"])


@videditor_router.post("/create-video")
async def create_video(videoRequest: EditorRequest, background_task: BackgroundTasks):
    # background_task.add_task(celery_task, videoRequest)
    result = celery_task.delay(videoRequest)
    return {"task_id": "started"}


@videditor_router.get("/progress/{task_id}", response_model=TaskInfo)
async def progress(task_id: str):
    task_result = AsyncResult(
        task_id,
    )
    if not task_result.ready():
        progress = task_result.info.get("progress", 0)
        completed_tasks = task_result.info.get("completed_tasks", [])
        return {
            "task_id": task_id,
            "progress": progress,
            "completed_tasks": completed_tasks,
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )




@videditor_router.get("/videos/{task_id}/{video_name}")
async def serve_video(request: Request, task_id: str, video_name: str):
    video_directory = "/tmp/Videos"
    video_path = os.path.join(video_directory, task_id, video_name)
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
            # "content-disposition": f'inline; filename="{video_name}"',
        }

        content = read_file_range(video_path, start, end)
        return StreamingResponse(content, media_type="video/mp4", headers=headers)

    return FileResponse(video_path, media_type="video/mp4")

async def read_file_range(path, start, end):
    async with aiofiles.open(path, "rb") as file:
        await file.seek(start)
        while True:
            data = await file.read(1024 * 1024)  # read in chunks of 1MB
            if not data or await file.tell() > end:
                break
            yield data
