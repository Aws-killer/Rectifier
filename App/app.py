from fastapi import FastAPI, BackgroundTasks
from .Editor.editorRoutes import videditor_router
from App import SERVER_STATE
from App.Utilis.Classes import WorkerClient
import asyncio

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    manager = WorkerClient(node=SERVER_STATE)
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
