from fastapi import FastAPI, BackgroundTasks
from .Editor.editorRoutes import videditor_router
from App.utilis import WorkerClient, SERVER_STATE

app = FastAPI()
manager = WorkerClient()


@app.on_event("startup")
async def startup_event():
    response = await manager.register_worker()
    if not response:
        print("Error registering worker")
    await manager.get_all_nodes()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(videditor_router)
