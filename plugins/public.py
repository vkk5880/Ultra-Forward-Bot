import re
import asyncio 
from .utils import STS
from database import db
from config import temp 
from translation import Translation
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait 
from pyrogram.errors.exceptions.not_acceptable_406 import ChannelPrivate as PrivateChat
from pyrogram.errors.exceptions.bad_request_400 import ChannelInvalid, ChatAdminRequired, UsernameInvalid, UsernameNotModified, ChannelPrivate
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

#===================Run Function===================#

@Client.on_message(filters.private & filters.command(["fwd", "forward"]))
async def run(bot, message):
    buttons = []
    btn_data = {}
    user_id = message.from_user.id
    _bot = await db.get_bot(user_id)
    if not _bot:
        return await message.reply("You Did Not Added Any Bot. Please Add A Bot Using /settings !")
    
    channels = await db.get_user_channels(user_id)
    if not channels:
        return await message.reply_text("Please Set A To Channel In /settings Before Forwarding")
    
    # Handle multiple channels selection
    if len(channels) > 1:
        for channel in channels:
            buttons.append([KeyboardButton(f"{channel['title']}")])
            btn_data[channel['title']] = channel['chat_id']
        buttons.append([KeyboardButton("cancel")]) 
        _toid = await bot.ask(
            message.chat.id, 
            Translation.TO_MSG.format(_bot['name'], _bot['username']), 
            reply_markup=ReplyKeyboardMarkup(buttons, one_time_keyboard=True, resize_keyboard=True)
        )
        if _toid.text.lower() == 'cancel' or _toid.text.startswith('/'):
            return await message.reply_text(Translation.CANCEL, reply_markup=ReplyKeyboardRemove())
        to_title = _toid.text
        toid = btn_data.get(to_title)
        if not toid:
            return await message.reply_text("Wrong Channel Choosen !", reply_markup=ReplyKeyboardRemove())
    else:
        toid = channels[0]['chat_id']
        to_title = channels[0]['title']
    
    # Get source chat information
    fromid = await bot.ask(message.chat.id, Translation.FROM_MSG, reply_markup=ReplyKeyboardRemove())
    if fromid.text and fromid.text.startswith('/'):
        return await message.reply(Translation.CANCEL)
    
    chat_id = None
    last_msg_id = None
    
    # Handle different input types
    if fromid.text and not fromid.forward_date:
        # Input is text (could be link or username/ID)
        input_text = fromid.text.strip()
        
        # Check if it's a link
        regex = re.compile(r"(https://)?(t\.me/|telegram\.me/|telegram\.dog/)(c/)?(\d+|[a-zA-Z_0-9]+)/(\d+)$")
        match = regex.match(input_text.replace("?single", ""))
        
        if match:
            # It's a link
            chat_id = match.group(4)
            last_msg_id = int(match.group(5))
            if chat_id.isnumeric():
                chat_id = int(("-100" + chat_id))
        else:
            # It's a username or ID
            try:
                if input_text.startswith('@'):
                    chat = await bot.get_chat(input_text)
                elif input_text.lstrip('-').isdigit():
                    chat = await bot.get_chat(int(input_text))
                else:
                    return await message.reply('Invalid input. Please provide channel link, username or ID')
                
                chat_id = chat.id
                title = chat.title
                # Ask for last message ID if not provided in link
                msg_id = await bot.ask(message.chat.id, "Please enter the last message ID to start forwarding from:")
                if msg_id.text.startswith('/'):
                    return await message.reply(Translation.CANCEL)
                last_msg_id = int(msg_id.text)
                
            except Exception as e:
                return await message.reply(f'Error getting chat: {e}')
    
    elif fromid.forward_from_chat and fromid.forward_from_chat.type in [enums.ChatType.CHANNEL]:
        # Forwarded message from channel
        last_msg_id = fromid.forward_from_message_id
        chat_id = fromid.forward_from_chat.username or fromid.forward_from_chat.id
        if last_msg_id is None:
            return await message.reply_text("This may be a forwarded message from a group sent by anonymous admin. Please send the last message link instead.")
    
    else:
        return await message.reply_text("Invalid input! Please provide a channel link, username, ID, or forward a message from the channel.")
    
    # Verify chat access
    try:
        chat = await bot.get_chat(chat_id)
        title = chat.title
    except (PrivateChat, ChannelPrivate, ChannelInvalid):
        title = "private" if fromid.text else fromid.forward_from_chat.title
    except (UsernameInvalid, UsernameNotModified):
        return await message.reply('Invalid username specified.')
    except Exception as e:
        return await message.reply(f'Error: {e}')
    
    # Get skip number
    skipno = await bot.ask(message.chat.id, Translation.SKIP_MSG)
    if skipno.text.startswith('/'):
        return await message.reply(Translation.CANCEL)
    
    forward_id = f"{user_id}-{skipno.id}"
    buttons = [[
        InlineKeyboardButton('Yes', callback_data=f"start_public_{forward_id}"),
        InlineKeyboardButton('No', callback_data="close_btn")
    ]]
    
    await message.reply_text(
        text=Translation.DOUBLE_CHECK.format(
            botname=_bot['name'],
            botuname=_bot['username'],
            from_chat=title,
            to_chat=to_title,
            skip=skipno.text
        ),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    
    STS(forward_id).store(chat_id, toid, int(skipno.text), int(last_msg_id))
