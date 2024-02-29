from pyrogram import Client
from telethon.sync import TelegramClient
from telethon.sessions import StringSession
from typing import List, Optional, Dict
from App.Utilis.Classes import ServerState
import os
import aiohttp
from pydantic import BaseModel


CHAT_ID = -1002069945904
TELEGRAM_SESSION = os.environ.get("TELEGRAM_SESSION", "None")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "None")
DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN", "None")
TELEGRAM_SESSION_PYROGRAM = os.environ.get("TELEGRAM_SESSION_PYROGRAM", "RANDOM_STRING")
MASTER_SERVER = os.environ.get("MASTER", 0).lower() in ["true", "1"]
SPACE_HOST = os.environ.get("SPACE_HOST", "RANDOM_STRING")


SERVER_STATE = ServerState(MASTER=MASTER_SERVER, SPACE_HOST=SPACE_HOST)


# bot: TelegramClient = TelegramClient(
#     StringSession(TELEGRAM_SESSION),
#     api_id=870972,
#     api_hash="ce2efaca02dfcd110941be6025e9ac0d",
# )


# bot: Client = Client("mboneabot", session_string=TELEGRAM_SESSION_PYROGRAM, workers=5 ,workdir="/srv")
