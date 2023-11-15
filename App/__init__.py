from telethon.sync import TelegramClient
from telethon.sessions import StringSession
import os

TELEGRAM_SESSION = os.environ.get("TELEGRAM_SESSION")

bot: TelegramClient = TelegramClient(
    StringSession(TELEGRAM_SESSION),
)
