import asyncio
from pyrogram import Client, filters, enums
from config import LOG_CHANNEL, LOG_TEXT, API_ID, API_HASH, NEW_REQ_MODE
from plugins.database import db
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import schedule
import time

#Time set karne ke liye function
def set_time(client, message):
    if len(message.command) >= 2:
        time = message.command[1]
        # Time ko database mein save karein
        db.set_time(time)
        if message.chat.id:
            client.send_message(chat_id=message.chat.id, text="Time set successfully!")
    else:
        if message.chat.id:
            client.send_message(chat_id=message.chat.id, text="Invalid command. Please provide a time.")

#Channel set karne ke liye function
def set_channel(client, message):
    if len(message.command) >= 2:
        channel_id = message.command[1]
        # Channel ID ko database mein save karein
        db.set_channel(channel_id)
        if message.chat.id:
            client.send_message(chat_id=message.chat.id, text="Channel set successfully!")
    else:
        if message.chat.id:
            client.send_message(chat_id=message.chat.id, text="Invalid command. Please provide a channel ID.")

#Request accept karne ke liye function
def accept_requests():
    # Time aur channel ID ko database se get karein
    time = db.get_time()
    channel_id = db.get_channel()
    # Request accept karein
    client = Client("joinrequest", api_hash=API_HASH, api_id=API_ID)
    client.start()
    try:
        client.approve_all_chat_join_requests(channel_id)
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        client.stop()

#Schedule ko set karein
def schedule_accept_requests():
    time = db.get_time()
    if time:
        schedule.every().day.at(time).do(accept_requests)
    else:
        print("Time not set")

#Command handlers
@Client.on_message(filters.command('start'))
async def start_message(c,m):
    if not await db.is_user_exist(m.from_user.id):
        await db.add_user(m.from_user.id, m.from_user.first_name)
        await c.send_message(LOG_CHANNEL, LOG_TEXT.format(m.from_user.id, m.from_user.mention))
        await m.reply_photo(f"https://te.legra.ph/file/119729ea3cdce4fefb6a1.jpg", caption=f"<b>Hello {m.from_user.mention} 👋\n\nI Am Join Request Acceptor Bot. I Can Accept All Old Pending Join Request.\n\nFor All Pending Join Request Use - /accept</b>", reply_markup=InlineKeyboardMarkup( [[ InlineKeyboardButton('💝 sᴜʙsᴄʀɪʙᴇ ʏᴏᴜᴛᴜʙᴇ ᴄʜᴀɴɴᴇʟ', url='https://youtube.com/@Tech_VJ') ],[ InlineKeyboardButton("❣️ ᴅᴇᴠᴇʟᴏᴘᴇʀ", url='https://t.me/Kingvj01'), InlineKeyboardButton("🤖 ᴜᴘᴅᴀᴛᴇ", url='https://t.me/VJ_Botz') ]] ) )

@Client.on_message(filters.command('accept') & filters.private)
async def accept(client, message):
    show = await message.reply("**Please Wait.....**")
    user_data = await db.get_session(message.from_user.id)
    if user_data is None:
        await show.edit("**For Accepte Pending Request You Have To /login First.**")
        return
    try:
        acc = Client("joinrequest", session_string=user_data, api_hash=API_HASH, api_id=API_ID)
        await acc.connect()
    except:
        return await show.edit("**Your Login Session Expired. So /logout First Then Login Again By - /login**")
    show = await show.edit("**Now Forward A Message From Your Channel Or Group With Forward Tag\n\nMake Sure Your Logged In Account Is Admin In That Channel Or Group With Full Rights.**")
    vj = await client.listen(message.chat.id)
    if vj.forward_from_chat and not vj.forward_from_chat.type in [enums.ChatType.PRIVATE, enums.ChatType.BOT]:
        chat_id = vj.forward_from_chat.id
        try:
            info = await acc.get_chat(chat_id)
        except:
            await show.edit("**Error - Make Sure Your Logged In Account Is Admin In This Channel Or Group With Rights.**")
        else:
            return await message.reply("**Message Not Forwarded From Channel Or Group.**")
        await vj.delete()
        msg = await show.edit("**Accepting all join requests... Please wait until it's completed.**")
        try:
            while True:
                await acc.approve_all_chat_join_requests(chat_id)
                await asyncio.sleep(1)
                join_requests = [request async for request in acc.get_chat_join_requests(chat_id)]
                if not join_requests:
                    break
            await msg.edit("**Successfully accepted all join requests.**")
        except Exception as e:
            await msg.edit(f"**An error occurred:** {str(e)}")

@Client.on_message(filters.command('set_time'))
async def set_time(client, message):
    if len(message.command) >= 2:
        time = message.command[1]
        # Time ko database mein save karein
        db.set_time(time)
        client.send_message(chat_id=message.chat.id, text="Time set successfully!")
    else:
        await client.send_message(chat_id=message.chat.id, text="Invalid command. Please provide a time.")

@Client.on_message(filters.command('set_channel'))
async def set_channel(client, message):
    if len(message.command) >= 2:
        channel_id = message.command[1]
        # Channel ID ko database mein save karein
        db.set_channel(channel_id)
        client.send_message(chat_id=message.chat.id, text="Channel set successfully!")
    else:
        await client.send_message(chat_id=message.chat.id, text="Invalid command. Please provide a channel ID.")
        
def schedule_accept_requests():
    schedule.every().day.at(db.get_time()).do(accept_requests)

def accept_requests():
    # Time aur channel ID ko database se get karein
    time = db.get_time()
    channel_id = db.get_channel()
    # Request accept karein
    client = Client("joinrequest", api_hash=API_HASH, api_id=API_ID)
    client.start()
    client.approve_all_chat_join_requests(channel_id)
