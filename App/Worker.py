from celery import Celery, chain
import os, shutil, subprocess
import uuid, cgi
from urllib.parse import urlparse
import time
import requests
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


def download_with_wget(link, download_dir, filename):
    subprocess.run(["aria2c", link, "-d", download_dir, "-o", filename])


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
        # Make a request to the server to get the filename and format
        response = requests.head(link)

        # Extract filename and format from the Content-Disposition header, if available
        content_disposition = response.headers.get("Content-Disposition")
        if content_disposition and "filename" in content_disposition:
            _, params = cgi.parse_header(content_disposition)
            filename = params["filename"]
        else:
            # If Content-Disposition is not available, use the last part of the URL as the filename
            filename = os.path.basename(urlparse(link).path)
        public_dir = f"{temp_dir}/public"
        print(public_dir)
        # Use the extracted filename to save the file

        download_with_wget(link, public_dir, filename)


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
def celery_task(links, script=""):
    remotion_app_dir = os.path.join("/srv", "Remotion-app")
    project_id = str(uuid.uuid4())
    temp_dir = f"/tmp/{project_id}"
    output_dir = f"/tmp/{project_id}/out/video.mp4"

    chain(
        copy_remotion_app.si(remotion_app_dir, temp_dir),
        install_dependencies.si(temp_dir),
        download_assets.si(links, temp_dir) if links else None,
        render_video.si(temp_dir, output_dir),
        cleanup_temp_directory.si(temp_dir, output_dir),
    ).apply_async(
        # link_error=handle_error
    )  # Link the tasks and handle errors


def handle_error(task_id, err, *args, **kwargs):
    print(f"Error in task {task_id}: {err}")
    # You can add additional error handling logic here
