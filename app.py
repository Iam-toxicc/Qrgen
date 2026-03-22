from pyrogram import Client
import config

app = Client(
    "Toxicqrbot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN
)
