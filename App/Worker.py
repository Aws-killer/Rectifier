from celery import Celery, chain
import os, shutil, subprocess
import uuid
import time
from App import celery_config, bot
from typing import List
from App.Editor.Schema import EditorRequest
from celery.signals import worker_process_init


celery = Celery()
celery.config_from_object(celery_config)
celery.conf.update(
    # Other Celery configuration settings
    CELERYD_LOG_LEVEL="DEBUG",  # Set log level to DEBUG for the worker
)


@worker_process_init.connect
def worker_process_init_handler(**kwargs):
    bot.start()


# Downloads list of links
# Script


def download_with_wget(link, download_dir):
    subprocess.run(["wget", "-P", download_dir, link])


@celery.task
def copy_remotion_app(src: str, dest: str):
    shutil.copytree(src, dest)


@celery.task
def install_dependencies(directory: str):
    os.chdir(directory)
    os.system("npm install")


@celery.task
def download_assets(links: List[str], temp_dir: str):
    for i, link in enumerate(links):
        download_dir = os.path.join(temp_dir, "public")
        download_with_wget(link, download_dir)


@celery.task
def render_video(directory: str, output_directory: str):
    os.chdir(directory)
    os.system(f"npm run build --output {output_directory}")


@celery.task
def cleanup_temp_directory(
    temp_dir: str, output_dir: str, chat_id: int = -1002069945904
):
    try:
        bot.send_video(chat_id, output_dir, caption="Your video caption")
    finally:
        # Cleanup: Remove the temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)


@celery.task
def celery_task(video_request):
    video_request = EditorRequest.parse_obj(video_request)
    remotion_app_dir = os.path.join("/srv", "Remotion-app")
    project_id = str(uuid.uuid4())
    temp_dir = f"/tmp/{project_id}"
    output_dir = f"/tmp/{project_id}/{project_id}.mp4"

    chain(
        copy_remotion_app.s(remotion_app_dir, temp_dir),
        install_dependencies.s(temp_dir),
        download_assets.s(video_request.links, temp_dir)
        if video_request.links
        else None,
        render_video.s(temp_dir, output_dir),
        cleanup_temp_directory.s(temp_dir, output_dir),
    ).apply_async(
        link_error=handle_error
    )  # Link the tasks and handle errors


def handle_error(task_id, err, *args, **kwargs):
    print(f"Error in task {task_id}: {err}")
    # You can add additional error handling logic here
