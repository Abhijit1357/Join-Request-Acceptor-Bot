# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import traceback
from pyrogram.types import Message
from pyrogram import Client, filters
from asyncio.exceptions import TimeoutError
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import (
    ApiIdInvalid,
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid
)
from config import API_ID, API_HASH
from plugins.database import db

SESSION_STRING_SIZE = 351

@Client.on_message(filters.private & ~filters.forwarded & filters.command(["logout"]))
async def logout(client, message):
    user_data = await db.get_session(message.from_user.id)  
    if user_data is None:
        return 
    await db.set_session(message.from_user.id, session=None)  
    await message.reply("**Logout Successfully** ♦")

@Client.on_message(filters.private & ~filters.forwarded & filters.command(["register"]))
async def register(bot: Client, message: Message):
    await message.reply("**Please send your username:**")
    username_msg = await bot.listen(message.from_user.id)
    username = username_msg.text
    try:
        await db.set_user(message.from_user.id, username)
        await message.reply("**Registration successful!**")
    except Exception as e:
        await message.reply(f"**Error:** {str(e)}")

@Client.on_message(filters.private & ~filters.forwarded & filters.command(["login"]))
async def login(bot: Client, message: Message):
    user_data = await db.get_session(message.from_user.id)
    if user_data is not None:
        await message.reply("**Your Are Already Logged In. First /logout Your Old Session. Then Do Login.**")
        return
    await message.reply("**Please send your username:**")
    username_msg = await bot.listen(message.from_user.id)
    username = username_msg.text
    try:
        user_id = await db.get_user_id(username)
        if user_id == message.from_user.id:
            await db.set_session(message.from_user.id, session=username)
            await message.reply("**Login successful!**")
        else:
            await message.reply("**Invalid username or password!**")
    except Exception as e:
        await message.reply(f"**Error:** {str(e)}")

LOG_CHANNEL = log_group

@Client.on_message(filters.group)
async def LOG_CHANNEL(bot: Client, message: Message):
    if message.chat.id == LOG_CHANNEL:
        inline_keyboard = [
            [InlineKeyboardButton("Accept", callback_data="accept")],
            [InlineKeyboardButton("Reject", callback_data="reject")],
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        await message.reply_text("Please select an option:", reply_markup=reply_markup)

@Client.on_callback_query()
async def callback_query(bot: Client, query: CallbackQuery):
    if query.data == "accept":
        # Accept logic here
        await query.message.reply_text("**Request accepted!**")
    elif query.data == "reject":
        # Reject logic here
        await query.message.reply_text("**Request rejected!**")
