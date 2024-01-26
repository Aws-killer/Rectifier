from fastapi import FastAPI, BackgroundTasks
from .Editor.editorRoutes import videditor_router
from App import bot

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await bot.start()


@app.on_event("shutdown")
async def shutdown_event():
    await bot.stop()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(videditor_router)
