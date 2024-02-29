import aiohttp, asyncio
from App import SERVER_STATE
import aiohttp, json
import asyncio


async def upload_file(file_path: str, node: str, chunk: int, task: str):
    master_node = SERVER_STATE.get_master()
    url = f"{master_node.SPACE_HOST}/uploadfile/?node={node}&chunk={chunk}&task={task}"
    async with aiohttp.ClientSession() as session:
        data = aiohttp.FormData()
        data.add_field("file", open(file_path, "rb"), content_type="video/mp4")
        async with session.post(url, data=data) as response:
            if response.status == 200:
                print("File uploaded successfully")
            else:
                print("Failed to upload file")
