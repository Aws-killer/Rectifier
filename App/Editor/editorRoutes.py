from fastapi import APIRouter, HTTPException, status
from .Schema import EditorRequest, TaskInfo
from App.Worker import celery_task
from celery.result import AsyncResult

videditor_router = APIRouter(tags=["vidEditor"])


@videditor_router.post("/create-video")
async def create_video(videoRequest: EditorRequest):
    result = celery_task.delay(videoRequest.dict())
    return {"task_id": result.task_id}


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
