from pyrogram import Client
from telethon import TelegramClient
from telethon.sessions import StringSession

import os


TELEGRAM_SESSION = os.environ.get("TELEGRAM_SESSION")
TELEGRAM_SESSION_PYROGRAM = os.environ.get("TELEGRAM_SESSION_PYROGRAM")

# bot: TelegramClient = TelegramClient(
#     StringSession(TELEGRAM_SESSION),
#     api_id=870972,
#     api_hash="ce2efaca02dfcd110941be6025e9ac0d",
# )


bot: Client = Client("mboneabot", session_string=TELEGRAM_SESSION_PYROGRAM, workers=5 ,workdir="/srv")
