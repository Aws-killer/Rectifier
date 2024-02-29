import aiohttp, asyncio
from App import SERVER_STATE
import aiohttp, json
import asyncio, sys


def consistent_hash(string):

    # Use the hash() function to generate a hash value for the string
    hash_value = hash(string)
    # Ensure the hash value is non-negative
    if hash_value < 0:
        # If negative, convert to positive by adding the maximum integer value
        hash_value += sys.maxsize
    return hash_value


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
