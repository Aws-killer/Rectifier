from celery import Celery, chain
import os, shutil, subprocess
import uuid, cgi
from urllib.parse import urlparse
import time
import requests
from App import celery_config, bot
from typing import List
from App.Editor.Schema import EditorRequest, LinkInfo
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


def create_symlink(source_dir, target_dir, symlink_name):
    source_path = os.path.join(source_dir, symlink_name)
    target_path = os.path.join(target_dir, symlink_name)

    try:
        os.symlink(source_path, target_path)
        print(f"Symlink '{symlink_name}' created successfully.")
    except FileExistsError:
        print(f"Symlink '{symlink_name}' already exists.")


def download_with_wget(link, download_dir, filename):
    subprocess.run(["aria2c", link, "-d", download_dir, "-o", filename])


@celery.task
def copy_remotion_app(src: str, dest: str):
    shutil.copytree(src, dest)

    # # create symbolic link to prevent multiple installs
    # source_dir = os.path.join(src, "node_module")
    # create_symlink(source_dir, target_dir=dest, symlink_name="node_module")


@celery.task
def install_dependencies(directory: str):
    os.chdir(directory)
    os.system("npm install")


@celery.task
def download_assets(links: List[LinkInfo], temp_dir: str):
    public_dir = f"{temp_dir}/public"
    for link in links:
        file_link = link.link
        file_name = link.file_name
        download_with_wget(file_link, public_dir, file_name)


@celery.task
def render_video(directory: str, output_directory: str):
    os.chdir(directory)
    os.system(f"npm run build --output {output_directory}")


@celery.task
def cleanup_temp_directory(
    temp_dir: str, output_dir: str, chat_id: int = -1002069945904
):
    try:
        bot.send_video(-1002069945904, video=output_dir, caption="Your video caption")
    finally:
        # Cleanup: Remove the temporary directory
        shutil.rmtree(temp_dir, ignore_errors=True)


@celery.task
def celery_task(video_task: EditorRequest):
    remotion_app_dir = os.path.join("/srv", "Remotion-app")
    project_id = str(uuid.uuid4())
    temp_dir = f"/tmp/{project_id}"
    output_dir = f"/tmp/{project_id}/out/video.mp4"

    chain(
        copy_remotion_app.si(remotion_app_dir, temp_dir),
        # install_dependencies.si(temp_dir),
        download_assets.si(video_task.links, temp_dir) if video_task.links else None,
        render_video.si(temp_dir, output_dir),
        cleanup_temp_directory.si(temp_dir, output_dir),
    ).apply_async(
        # link_error=handle_error
    )  # Link the tasks and handle errors


def handle_error(task_id, err, *args, **kwargs):
    print(f"Error in task {task_id}: {err}")
    # You can add additional error handling logic here
