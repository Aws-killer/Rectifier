import aiohttp, asyncio
from App import SERVER_STATE, Node
import aiohttp
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


class WorkerClient:
    base_url = SERVER_STATE.DB

    async def discover_node(self):
        if SERVER_STATE.MASTER:
            while True:
                await self.get_all_nodes()
                await asyncio.sleep(3)

    async def register_worker(self):
        async with aiohttp.ClientSession() as session:
            data = {
                "WORKER_ID": SERVER_STATE.SPACE_HOST,
                "MASTER": SERVER_STATE.MASTER,
                "HOST_NAME": SERVER_STATE.SPACE_HOST,
                "SPACE_HOST": f"https://{SERVER_STATE.SPACE_HOST}",
            }
            response = await self.get_node()
            if response != None:
                print(response, "Server Response", SERVER_STATE.SPACE_HOST)
                return response

            async with session.put(
                f"{self.base_url}/nodes/{SERVER_STATE.SPACE_HOST.replace('-', '_').replace('.', '_')}.json",
                json=data,
            ) as resp:
                return await resp.json()

    async def get_node(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/nodes/{SERVER_STATE.SPACE_HOST.replace('-', '_').replace('.', '_')}.json"
            ) as resp:
                response = await resp.json()
                return response

    async def delete_node(self):
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                f"{self.base_url}/nodes/{SERVER_STATE.SPACE_HOST.replace('-', '_').replace('.', '_')}.json"
            ) as resp:
                response = await resp.json()

    async def get_all_nodes(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/nodes.json") as resp:
                response = await resp.json()
                SERVER_STATE.NODES = [Node(**value) for value in response.values()]
                return SERVER_STATE.NODES
