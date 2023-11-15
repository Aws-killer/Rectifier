from pyrogram import Client
import os

TELEGRAM_SESSION = os.environ.get("TELEGRAM_SESSION")


bot: Client = Client(
    "Editor", session_string=TELEGRAM_SESSION, workdir="/srv", workers=9
)
