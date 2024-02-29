import aiohttp, asyncio

# from App import SERVER_STATE, Node, TELEGRAM_TOKEN, CHAT_ID, DISCORD_TOKEN, Task
import aiohttp, json
from typing import List, Optional, Dict
import asyncio
from pydantic import BaseModel


class Node(BaseModel):
    MASTER: bool
    SPACE_HOST: str


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

    async def update_node_state(self, task: TaskMain, node: NodeTaskState):
        async with aiohttp.ClientSession() as session:
            json_node = node.json()
            async with session.put(
                f"{self.base_url}/tasks/{task.TASK_ID}/NODES/{node.NODE.SPACE_HOST}.json",
                json=json.loads(json_node),
            ) as resp:
                response = await resp.json()
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
        await self.REMOTE.register_task(TaskMain(**self.__dict__))
        return True

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
            if space_host in node_id:
                node.COMPLETED = True
                await self.REMOTE.update_node_state(TaskMain(**self.__dict__), node)
                break

    def add_node(self, node: Node, CHUNK: int):
        new_node_state = NodeTaskState(NODE=node, CHUNK=CHUNK, COMPLETED=False)
        self.NODES[node.SPACE_HOST] = new_node_state

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
