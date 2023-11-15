from fastapi import FastAPI, BackgroundTasks
from .Editor.editorRoutes import videditor_router
from App import bot

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await bot.start()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(videditor_router)
