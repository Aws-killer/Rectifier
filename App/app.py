from fastapi import FastAPI, BackgroundTasks
from .Editor.editorRoutes import videditor_router
from App.utilis import WorkerClient, SERVER_STATE
import asyncio

app = FastAPI()
manager = WorkerClient()


@app.on_event("startup")
async def startup_event():
    if SERVER_STATE.MASTER:
        asyncio.create_task(manager.discover_node())
        await manager.get_all_nodes()
    response = await manager.register_worker()
    if not response:
        print("Error registering worker")


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(videditor_router)
