import aiohttp, asyncio

# from App import SERVER_STATE, Node, TELEGRAM_TOKEN, CHAT_ID, DISCORD_TOKEN, Task
import aiohttp, json
from typing import List, Optional, Dict
import asyncio
from pydantic import BaseModel
import sys


class Node(BaseModel):
    MASTER: bool
    SPACE_HOST: str

    def consistent_hash(self, value=None):
        # Use the hash() function to generate a hash value for the string
        if value:
            hash_value = hash(value)
        else:
            hash_value = hash(self.SPACE_HOST)
        # Ensure the hash value is non-negative
        if hash_value < 0:
            # If negative, convert to positive by adding the maximum integer value
            hash_value += sys.maxsize
        return str(hash_value)


class NodeTaskState(BaseModel):
    NODE: Node
    CHUNK: int
    COMPLETED: bool


class TaskMain(BaseModel):
    TASK_ID: str
    COMPLETED: bool = False
    NODES: Dict[str, NodeTaskState] = {}


class TaskRemote(BaseModel):
    base_url: str

    async def get_task(self, task_id: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/tasks/{task_id}.json") as resp:
                response = await resp.json()
                task = None
                if response:
                    task = Task(**response)
                return task

    async def delete_task(self, task: TaskMain):
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                f"{self.base_url}/tasks/{task.TASK_ID}.json"
            ) as resp:
                response = await resp.json()
                return response

    async def register_task(self, task: TaskMain):
        async with aiohttp.ClientSession() as session:
            json_task = task.json()
            async with session.put(
                f"{self.base_url}/tasks/{task.TASK_ID}.json",
                json=json.loads(json_task),
            ) as resp:
                response = await resp.json()
                return response

    async def mark_node_completed(self, task_id: str, node_id: str):

        # Construct the Firebase Realtime Database endpoint URL
        url = f"{self.base_url}/tasks/{task_id}/NODES/{node_id}.json"

        # Send a PATCH request to update the node's COMPLETED status to True
        async with aiohttp.ClientSession() as session:
            async with session.patch(url, json={"COMPLETED": True}) as response:
                if response.status == 200:
                    print(f"Node {node_id} marked as completed.")
                else:
                    print(
                        f"Failed to mark node {node_id} as completed. Status code: {response.status}"
                    )

    async def update_node_state(self, task: TaskMain, node: NodeTaskState):
        hashed = node.NODE.consistent_hash()
        async with aiohttp.ClientSession() as session:
            node.COMPLETED = True
            json_node = node.json()
            json_node["COMPLETED"] = True
            async with session.put(
                f"{self.base_url}/tasks/{task.TASK_ID}/NODES/{hashed}.json",
                json=json.loads(json_node),
            ) as resp:
                response = await resp.json()
                print(response, "Response")
                return response

    async def get_all_nodes(self, task_id: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/tasks/{task_id}.json") as resp:
                response = await resp.json()

                temp = Task(**response)
                return temp


class Task(TaskMain):
    DB: Optional[str] = "https://herokuserver-185316.firebaseio.com/"
    REMOTE: TaskRemote = TaskRemote(
        base_url="https://herokuserver-185316.firebaseio.com/"
    )

    async def get_remote_task(self) -> bool:
        self = await self.REMOTE.get_all_nodes(self.TASK_ID)
        return self

    async def _register_task(self) -> bool:
        resp = await self.REMOTE.register_task(TaskMain(**self.__dict__))
        return resp

    async def is_completed(self) -> bool:
        self = await self.REMOTE.get_all_nodes(self.TASK_ID)
        for node in self.NODES.values():
            if not node.COMPLETED:
                return False
        self.COMPLETED = True
        await self.REMOTE.delete_task(TaskMain(**self.__dict__))
        return True

    async def mark_node_completed(self, space_host: str):
        self = await self.REMOTE.get_all_nodes(self.TASK_ID)
        for node_id, node in self.NODES.items():
            if space_host == node_id:
                await self.REMOTE.mark_node_completed(self.TASK_ID, node_id)
                break

    def add_node(self, node: Node, CHUNK: int):
        new_node_state = NodeTaskState(NODE=node, CHUNK=CHUNK, COMPLETED=False)
        self.NODES[node.consistent_hash()] = new_node_state

    @classmethod
    async def _check_node_online(cls, space_host: str) -> bool:
        if not "https" in space_host:
            space_host = f"https://{space_host}"
        try:
            async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=10)
            ) as session:
                async with session.get(space_host) as response:
                    return response.status == 200
        except aiohttp.ClientError:
            return False


class ServerState(Node):
    CACHED: Optional[Dict[str, bool]] = {}
    TASKS: Optional[Dict[str, Task]] = {}
    NODES: Optional[list[Node]]

    async def _get_task(self, task_id: str):
        task = TaskRemote(base_url="https://herokuserver-185316.firebaseio.com/")
        return await task.get_task(task_id)

    def get_master(self) -> Optional[Node]:
        for node in self.NODES:
            if node.MASTER:
                return node
        return None


class WorkerClient:
    base_url = "https://herokuserver-185316.firebaseio.com/"
    SERVER_STATE: Node

    def __init__(self, node: Node):
        self.SERVER_STATE = node

    async def discover_node(self):
        if self.SERVER_STATE.MASTER:
            while True:
                try:
                    await self.get_all_nodes()
                except:
                    pass
                finally:
                    await asyncio.sleep(3)

    async def register_worker(self):
        async with aiohttp.ClientSession() as session:
            data = {
                "WORKER_ID": self.SERVER_STATE.SPACE_HOST,
                "MASTER": self.SERVER_STATE.MASTER,
                "HOST_NAME": self.SERVER_STATE.SPACE_HOST,
                "SPACE_HOST": f"https://{self.SERVER_STATE.SPACE_HOST}",
            }
            response = await self.get_node()
            if response != None:
                print(response, "Server Response", self.SERVER_STATE.SPACE_HOST)
                return response

            async with session.put(
                f"{self.base_url}/nodes/{self.SERVER_STATE.SPACE_HOST.replace('-', '_').replace('.', '_')}.json",
                json=data,
            ) as resp:
                return await resp.json()

    async def get_node(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}/nodes/{self.SERVER_STATE.SPACE_HOST.replace('-', '_').replace('.', '_')}.json"
            ) as resp:
                response = await resp.json()
                return response

    async def delete_node(self):
        async with aiohttp.ClientSession() as session:
            async with session.delete(
                f"{self.base_url}/nodes/{self.SERVER_STATE.SPACE_HOST.replace('-', '_').replace('.', '_')}.json"
            ) as resp:
                response = await resp.json()

    async def get_all_nodes(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/nodes.json") as resp:
                response = await resp.json()
                self.SERVER_STATE.NODES = [Node(**value) for value in response.values()]
                return self.SERVER_STATE.NODES


class TelegramBot:
    def __init__(self):
        self.url = f"https://botty.nofoxot593.workers.dev/"

    async def send_message(self, text):
        params = {"chat_id": "-1002069945904", "text": text}
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=params) as response:
                if response.status == 200:
                    print("Message sent successfully!")
                else:
                    print("Failed to send message:", await response.text())


# async def main():
#     test = ServerState(MASTER=False, SPACE_HOST="test_me")
#     new_task = Task(TASK_ID="new_task")
#     task_d = "new_task"
#     t = Node(MASTER=False, SPACE_HOST="sucky")
#     f = Node(MASTER=False, SPACE_HOST="sucfky")
#     new_task.add_node(CHUNK=0, node=t)
#     new_task.add_node(CHUNK=1, node=f)
#     test.TASKS["new_task"] = new_task
#     X = await new_task._register_task()
#     print(task_d)
#     task = await test._get_task(
#         task_id=task_d
#     )  # Fixed the method call by passing the task_id as a parameter
#     # await task.mark_node_completed(space_host=t.SPACE_HOST)
#     await task.mark_node_completed(space_host=f.SPACE_HOST)
#     x = await task.is_completed()
#     nw_task = Task(TASK_ID="new_task")
#     await nw_task.mark_node_completed(space_host=t.SPACE_HOST)
#     # nw_task.add_node(CHUNK=0, node=t)
#     print(x)


async def TestBot():
    bot = TelegramBot()
    await bot.send_message("Hello World")


if __name__ == "__main__":
    asyncio.run(TestBot())
