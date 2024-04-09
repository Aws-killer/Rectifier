from celery import Celery, chain
import os, shutil, subprocess
import uuid
from urllib.parse import urlparse
from subprocess import run
from App import celery_config, bot
from typing import List
from App.Editor.Schema import EditorRequest, LinkInfo, Assets, Constants
from celery.signals import worker_process_init
from asgiref.sync import async_to_sync
import json
import os
from pathlib import Path
from pydantic import BaseModel

class YouTubeUploadTask(BaseModel):
    filename: str
    title: str = "Default Title"
    description: str = "Default Description"
    category_id: str = "22"  # Default to a generic category, update as needed
    privacy: str = "private"
    tags: str = ""
    thumbnail: str = None



celery = Celery()
celery.config_from_object(celery_config)
# celery.conf.update(
#     # Other Celery configuration settings
#     CELERYD_LOG_LEVEL="DEBUG",  # Set log level to DEBUG for the worker
# )


@celery.task(name="CreateFile")
def create_json_file(assets: Assets, asset_dir: str):
    # Create the directory if it doesn't exist
    Path(asset_dir).mkdir(parents=True, exist_ok=True)
    
    # Define the file path
    file_path = Path(asset_dir) / "variables.json"

    # Serialize the Assets object to JSON
    json_data = assets.json()

    # Write JSON data to file
    with open(file_path, "w") as json_file:
        json_file.write(json_data)


@celery.task(name="Constants")
def create_constants_json_file(constants: Constants, asset_dir: str):
    filename = "Constants.json"
    if constants:
        json_string = json.dumps(constants.dict())
    else:
        json_string = json.dumps({})
    os.makedirs(asset_dir, exist_ok=True)
    with open(os.path.join(asset_dir, filename), "w") as f:
        f.write(json_string)


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


@celery.task(name="CopyRemotion")
def copy_remotion_app(src: str, dest: str):
    shutil.copytree(src, dest)

    # # create symbolic link to prevent multiple installs
    # source_dir = os.path.join(src, "node_module")
    # create_symlink(source_dir, target_dir=dest, symlink_name="node_module")


@celery.task(name="Unsilence")
def unsilence(directory: str):
    output_dir = os.path.join(directory, "out/video.mp4")
    shortered_dir = os.path.join(directory, "out/temp.mp4")
    os.system(f"pipx run unsilence {output_dir} {shortered_dir} -y")
    os.remove(output_dir)
    os.rename(shortered_dir, output_dir)


@celery.task(name="InstallDependency")
def install_dependencies(directory: str):
   
    os.chdir(directory)
    os.system("npm install typescript --save-dev")
    os.system("npm install --force")
    os.system("echo \"y\" | npx puppeteer browsers install chrome@stable")
    os.rename(f'{directory}/temp.js', f'{directory}/node_modules/@revideo/renderer/dist/main.js')





@celery.task(name="uploadTime")
def upload_video_to_youtube(task_data: dict):
    # Convert dict to Pydantic model
    task = YouTubeUploadTask(**task_data)

    # Build the command
    command = [
        '/srv/youtube/youtubeuploader',  # Adjust the path as needed
        '-filename', task.filename,
        '-title', task.title,
        '-description', task.description,
        '-categoryId', task.category_id,
        '-privacy', task.privacy,
        '-tags', task.tags
    ]

    if task.thumbnail:
        command.extend(['-thumbnail', task.thumbnail])

    # Execute the command
    result = run(command, capture_output=True, text=True)

    return result.stdout


@celery.task(name="DownloadAssets")
def download_assets(links: List[LinkInfo], temp_dir: str):
    public_dir = f"{temp_dir}"
    for link in links:
        file_link = link.link
        file_name = link.file_name
        download_with_wget(file_link, public_dir, file_name)


@celery.task(name="RenderFile")
def render_video(directory: str, output_directory: str):
    os.chdir(directory)
    os.system(f"npm run render")
    print("complete")


@celery.task(name="send")
def cleanup_temp_directory(
    video_folder_dir: str, output_dir: str, chat_id: int = -1002069945904
):
    os.makedirs(video_folder_dir, exist_ok=True)
    files = os.listdir(output_dir)

    # Filter out the MP4 files
    mp4_file = [f for f in files if f.endswith(".mp4")][0]
    shutil.copy(f'{output_dir}/{mp4_file}', f"{video_folder_dir}/project.mp4")
    echo = f"{video_folder_dir}/project.mp4"
    print(echo)

@celery.task(name="All")
def celery_task(video_task: EditorRequest):
    remotion_app_dir = os.path.join("/srv", "Motion")
    project_id = str(uuid.uuid4())
    video_folder_dir = f"/tmp/Videos/{project_id}"
    temp_dir = f"/tmp/{project_id}"
    output_dir = f"/tmp/{project_id}/output/"
    assets_dir = os.path.join(temp_dir, "src")

    # copy_remotion_app(remotion_app_dir, temp_dir),
    # install_dependencies(temp_dir),
    # create_constants_json_file(video_task.constants, assets_dir),
    # create_json_file(video_task.assets, assets_dir),
    # download_assets(video_task.links, temp_dir) if video_task.links else None,
    # render_video(temp_dir, output_dir),
    # unsilence(temp_dir),
    # await cleanup_temp_directory(temp_dir, output_dir),

    chain(
        copy_remotion_app.si(remotion_app_dir, temp_dir),
        install_dependencies.si(temp_dir),
        # create_constants_json_file.si(video_task.constants, assets_dir),
        create_json_file.si(video_task.assets, assets_dir),
        download_assets.si(video_task.links, temp_dir) if video_task.links else None,
        render_video.si(temp_dir, output_dir),
        cleanup_temp_directory.si(video_folder_dir, output_dir),
    ).apply_async(
        # link_error=handle_error
    )  # Link the tasks and handle errors


def handle_error(task_id, err, *args, **kwargs):
    print(f"Error in task {task_id}: {err}")
    # You can add additional error handling logic here
