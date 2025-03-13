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
        client.send_message(chat_id=message.chat.id, text="Time set successfully!")
    else:
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
async def accept_requests():
    # Time aur channel ID ko database se get karein
    time = await db.get_time()
    channel_id = await db.get_channel()

    # Request accept karein
    client = Client("joinrequest", api_hash=API_HASH, api_id=API_ID)
    await client.start()
    try:
        await client.approve_all_chat_join_requests(channel_id)
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        await client.stop()

#Schedule ko set karein
async def schedule_accept_requests():
    time = await db.get_time()
    if time:
        schedule.every().day.at(time).do(accept_requests)
    else:
        print("Time not set")

#Command handlers
@Client.on_message(filters.command('start'))
async def start_message(client, message):
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
    await client.send_message(LOG_CHANNEL, LOG_TEXT.format(message.from_user.id, message.from_user.mention))
    await message.reply_photo(f"https://te.legra.ph/file/119729ea3cdce4fefb6a1.jpg", 
                                caption=f"<b>Hello {message.from_user.mention} 👋\n\nI Am Join Request Acceptor Bot. I Can Accept All Old Pending Join Request.\n\nFor All Pending Join Request Use - /accept</b>", 
                                reply_markup=InlineKeyboardMarkup([
                                    [
                                        InlineKeyboardButton('💝 sᴜʙsᴄʀɪʙᴇ ʏᴏᴜᴛᴜʙᴇ ᴄʜᴀɴɴᴇʟ', url='https://youtube.com/@Tech_VJ')
                                    ],
                                    [
                                        InlineKeyboardButton("❣️ ᴅᴇᴠᴇʟᴏᴘᴇʀ", url='https://t.me/Kingvj01'), 
                                        InlineKeyboardButton("🤖 ᴜᴘᴅᴀᴛᴇ", url='https://t.me/VJ_Botz')
                                    ]
                                ])
                             )
    
@Client.on_message(filters.command('accept') & filters.private)
async def accept(client, message):
    show = await message.reply("**Please Wait.....**")
    # user_data = await db.get_session(message.from_user.id)
    # if user_data is None:
    #     await show.edit("**For Accepte Pending Request You Have To /login First.**")
    #     return
    try:
        acc = Client("joinrequest", api_hash=API_HASH, api_id=API_ID)
        await acc.start()
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
        await db.set_time(time)
        await client.send_message(chat_id=message.chat.id, text="Time set successfully! Now set the channel ID using /set_channel command.")
    else:
        await client.send_message(chat_id=message.chat.id, text="Invalid command. Please provide a time.")

@Client.on_message(filters.command('set_channel'))
async def set_channel(client, message):
    if len(message.command) >= 2:
        channel_id = message.command[1]
        try:
            channel = await client.get_chat(channel_id)
            channel_name = channel.title
            channel_link = channel.username
            if await db.get_time() is None:
                await client.send_message(chat_id=message.chat.id, text="Please set the time first using /set_time command.")
                return
            if channel_link:
                await db.set_channel(channel_id)
                await client.send_message(chat_id=message.chat.id, text=f"Channel set successfully!\nChannel Name: {channel_name}\nChannel Link: @{channel_link}")
            else:
                await db.set_channel(channel_id)
                await client.send_message(chat_id=message.chat.id, text=f"Channel set successfully!\nChannel Name: {channel_name}")
        except Exception as e:
            await client.send_message(chat_id=message.chat.id, text=f"Error: {str(e)}")
    else:
        await client.send_message(chat_id=message.chat.id, text="Invalid command. Please provide a channel ID.")
        
async def schedule_accept_requests():
    schedule.every().day.at(await db.get_time()).do(accept_requests)

async def accept_requests():
    # Time aur channel ID ko database se get karein
    time = await db.get_time()
    channel_id = await db.get_channel()

    # Request accept karein
    client = Client("joinrequest", api_hash=API_HASH, api_id=API_ID)
    await client.start()

    # Channel list aur pending requests ko print karein
    print("Channel List:")
    channels = await client.get_chat(channel_id)
    print(channels.title)
    print("Pending Requests:")
    pending_requests = await client.get_chat_join_requests(channel_id)
    for request in pending_requests:
        print(request.user.username)

    # Pending requests ko accept karein
    await client.approve_all_chat_join_requests(channel_id)
    await client.stop()
    
@Client.on_message(filters.command('list') & filters.private)
async def list(client, message):
    channel_id = await db.get_channel()
    client = Client("joinrequest", api_hash=API_HASH, api_id=API_ID)
    await client.start()
    channels = await client.get_chat(channel_id)
    time = await db.get_time()
    channel_list = ""
    channel_count = 0
    pages = []
    channel_info = f"◈ ᴄhannel {channel_count + 1} : {channels.title}"
    if channels.username:
        channel_info += f" [{channels.username}]"
    pages.append(channel_info)
    await message.reply(f"{pages[0]}\nTime: {time}\nTotal Channels: {channel_count + 1}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Next", callback_data="next_page")]]))
    await client.stop()

@Client.on_callback_query(filters.regex("next_page"))
async def next_page(client, callback_query):
    pages = []  # yeh pages list mein aapke channels ki list hogi
    current_page = 0
    # yeh code pagination ke liye hai, lekin aapke paas sirf ek channel hai
    await callback_query.answer("No more pages", show_alert=True)
