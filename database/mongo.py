# Toxicqrbot Database

from motor.motor_asyncio import AsyncIOMotorClient
import config

mongo = AsyncIOMotorClient(config.MONGO_URL)
db = mongo.toxicqrbot
