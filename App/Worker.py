from celery import Celery, chain
import os, shutil, subprocess
import uuid
from urllib.parse import urlparse
from subprocess import run
from App import celery_config, SERVER_STATE
from typing import List
from App.Editor.Schema import EditorRequest, LinkInfo, Assets, Constants
from celery.signals import worker_process_init
from asgiref.sync import async_to_sync
import json
import os
from pydantic import BaseModel
from App.Utilis.Functions import upload_file
from App.Utilis.Classes import Task, TelegramBot

import subprocess
from pydantic import BaseModel

tl_bot = TelegramBot()


async def concatenate_videos(input_dir):
    # Get a list of all the mp4 files in the input directory
    files = sorted([f for f in os.listdir(input_dir) if f.endswith(".mp4")])
    if len(files) > 1:
        # Generate the input file list for ffmpeg
        input_file_list = os.path.join(input_dir, "input.txt")
        with open(input_file_list, "w") as f:
            for file in files:
                f.write(f"file '{os.path.join(input_dir, file)}'\n")

        output_file = f"{input_dir}/final.mp4"
        # Run the ffmpeg command to concatenate the videos
        subprocess.run(
            [
                "ffmpeg",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                input_file_list,
                "-c",
                "copy",
                output_file,
            ]
        )
    else:
        output_file = os.path.join(input_dir, files[0])
    link = f"https://{SERVER_STATE.SPACE_HOST}/videos/{output_file.replace('/tmp/Video/', '')}"
    await tl_bot.send_message(link)
    # await tl_bot.send_message(
    #     f"https://{SERVER_STATE.SPACE_HOST}/videos/{output_file.replace('/tmp/Video/', '')}",
    # )

    return output_file


class YouTubeUploadTask(BaseModel):
    filename: str
    title: str = "Default Title"
    description: str = "Default Description"
    category_id: str = "22"  # Default to a generic category, update as needed
    privacy: str = "private"
    tags: str = ""
    thumbnail: str = None


def create_json_file(assets: List[Assets], asset_dir: str):
    for asset in assets:
        filename = f"{asset.type.capitalize()}Sequences.json"
        # Convert dictionary to JSON string
        json_string = json.dumps(asset.sequence)

        # Create directory if it doesn't exist
        os.makedirs(asset_dir, exist_ok=True)
        print(os.path.join(asset_dir, filename))
        # Write JSON string to file
        with open(os.path.join(asset_dir, filename), "w") as f:
            f.write(json_string)


def create_constants_json_file(constants: Constants, asset_dir: str):
    temp_dir = asset_dir.replace("src/HelloWorld/Assets", "")
    instrunction_file = os.path.join(temp_dir, "ServerInstructions.json")
    filename = "Constants.json"
    if constants:
        json_string = json.dumps(constants.dict())
    else:
        json_string = json.dumps({})
    os.makedirs(asset_dir, exist_ok=True)
    with open(instrunction_file, "w") as f:
        if constants.frames:
            f.write(json.dumps({"frames": constants.frames}))
        else:
            f.write(json.dumps({"frames": [0, constants.duration]}))

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


def copy_remotion_app(src: str, dest: str):
    shutil.copytree(src, dest)


def unsilence(directory: str):
    output_dir = os.path.join(directory, "out/video.mp4")
    shortered_dir = os.path.join(directory, "out/temp.mp4")
    os.system(f"pipx run unsilence {output_dir} {shortered_dir} -y")
    os.remove(output_dir)
    os.rename(shortered_dir, output_dir)


def install_dependencies(directory: str):
    os.chdir(directory)
    os.system(f"npm install")


def upload_video_to_youtube(task_data: dict):
    # Convert dict to Pydantic model
    task = YouTubeUploadTask(**task_data)

    # Build the command
    command = [
        "/srv/youtube/youtubeuploader",  # Adjust the path as needed
        "-filename",
        task.filename,
        "-title",
        task.title,
        "-description",
        task.description,
        "-categoryId",
        task.category_id,
        "-privacy",
        task.privacy,
        "-tags",
        task.tags,
    ]

    if task.thumbnail:
        command.extend(["-thumbnail", task.thumbnail])

    # Execute the command
    result = run(command, capture_output=True, text=True)

    return result.stdout


def delete_files(dir):
    files = os.listdir(dir)
    deleted_files = []
    for f in files:
        file_path = os.path.join(dir, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
            deleted_files.append(f)
    print("deleted files", deleted_files)
    return deleted_files


def download_assets(links: List[LinkInfo], temp_dir: str):
    public_dir = f"{temp_dir}/public"
    for link in links:
        file_link = link.link
        file_name = link.file_name
        download_with_wget(file_link, public_dir, file_name)


def render_video(directory: str, output_directory: str):
    os.chdir(directory)
    os.system(f"npm run build")
    print("complete")


async def cleanup_temp_directory(
    temp_dir: str,
    output_dir: str,
    video_task: EditorRequest,
    chat_id: int = -1002069945904,
):
    video_folder_dir = f"/tmp/Video/{video_task.constants.task}"

    if not SERVER_STATE.MASTER:
        await upload_file(
            output_dir,
            SERVER_STATE.SPACE_HOST,
            video_task.constants.chunk,
            video_task.constants.task,
        )
    else:

        os.makedirs(video_folder_dir, exist_ok=True)
        shutil.copy(output_dir, f"{video_folder_dir}/{video_task.constants.chunk}.mp4")

    try:
        pass

    except Exception as e:
        print(e)
    finally:
        remotion_app_dir = "/srv/Remotion-app"
        # use the cache

        if SERVER_STATE.MASTER:
            temp = Task(TASK_ID=video_task.constants.task)

            await temp.mark_node_completed(SERVER_STATE.SPACE_HOST)
            completed = await temp.is_completed()
            if completed:
                await concatenate_videos(video_folder_dir)
                print("completed")

        delete_files(f"{temp_dir}/public")
        SERVER_STATE.CACHED[temp_dir] = False

    return


async def celery_task(video_task: EditorRequest):
    remotion_app_dir = "/srv/Remotion-app"
    for temp_dir, busy in SERVER_STATE.CACHED.items():
        if not busy:
            break
    else:
        project_id = str(uuid.uuid4())
        temp_dir = f"/tmp/{project_id}"
        copy_remotion_app(remotion_app_dir, temp_dir)
        install_dependencies(temp_dir)

    output_dir = f"{temp_dir}/out/video.mp4"
    assets_dir = os.path.join(temp_dir, "src/HelloWorld/Assets")

    create_constants_json_file(video_task.constants, assets_dir)
    create_json_file(video_task.assets, assets_dir)
    download_assets(video_task.links, temp_dir)
    render_video(temp_dir, output_dir)
    # unsilence(temp_dir)

    # delete assets_dir
    shutil.rmtree(assets_dir)
    await cleanup_temp_directory(temp_dir, output_dir, video_task)


def handle_error(task_id, err, *args, **kwargs):
    print(f"Error in task {task_id}: {err}")
    # You can add additional error handling logic here
