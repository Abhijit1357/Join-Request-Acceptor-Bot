import asyncio
from pyrogram import Client, filters, enums
from config import LOG_CHANNEL, API_ID, API_HASH, NEW_REQ_MODE
from plugins.database import db
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import schedule
import time

#Scheduled task
def accept_join_requests():
    # Get time and channel ID from database
    db = MongoClient(MONGO_URI)["bot_database"]
    settings_collection = db["settings"]
    time = settings_collection.find_one({"_id": "time"})["time"]
    channel_id = settings_collection.find_one({"_id": "channel"})["channel_id"]
    # Accept join requests in channel
    acc = Client("joinrequest", session_string=user_data, api_hash=API_HASH, api_id=API_ID)
    acc.start()
    acc.approve_all_chat_join_requests(channel_id)

Time setting feature
def set_time(update, context):
    time = context.args[0]
    # Save time to database
    db = MongoClient(MONGO_URI)["bot_database"]
    settings_collection = db["settings"]
    settings_collection.update_one({"_id": "time"}, {"$set": {"time": time}})
    context.bot.send_message(chat_id=update.effective_chat.id, text="Time set successfully!")
    schedule.every().day.at(time).do(accept_join_requests)  # Run scheduled task every day at specified time

Channel selection feature
def select_channel(update, context):
    channel_id = context.args[0]
    # Save channel ID to database
    db = MongoClient(MONGO_URI)["bot_database"]
    settings_collection = db["settings"]
    settings_collection.update_one({"_id": "channel"}, {"$set": {"channel_id": channel_id}})
    context.bot.send_message(chat_id=update.effective_chat.id, text="Channel selected successfully!")

Command to set time and channel
@Client.on_message(filters.command('set_time'))
async def set_time_command(client, message):
    if len(message.command) < 2:
        await message.reply("Please provide time in 24-hour format (e.g., 08:00)")
        return
    time = message.command[1]
    await set_time(message, client)
    await select_channel(message, client)

Command to select channel
@Client.on_message(filters.command('select_channel'))
async def select_channel_command(client, message):
    if len(message.command) < 2:
        await message.reply("Please provide channel ID")
        return
    channel_id = message.command[1]
    await select_channel(message, client)
