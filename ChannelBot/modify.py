import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup
from pyrogram.errors.exceptions import FloodWait
import random
import re

# Import database interaction functions
from ChannelBot.database.channel_sql import (
    get_caption,
    get_position,
    get_buttons,
    get_webpage_preview,
    get_sticker,
    get_edit_mode,
)

# Import string_to_buttons function (assu ming it exists)
from ChannelBot.string_to_buttons import string_to_buttons

def get_readable_time(seconds):
    periods = [('d', 86400), ('h', 3600), ('m', 60), ('s', 1)]
    result = ''
    for period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            result += f'{int(period_value)}{period_name}'
    return result

def get_size(size):
    units = ("Bytes", "KB", "MB", "GB", "TB", "PB", "EB")
    i = 0
    while size >= 1016.44 and i < len(units):
        i += 1
        size /= 1016
    return f"{size:.2f} {units[i]}"

@Client.on_message(filters.channel & ~filters.forwarded)
async def modify(bot, msg: Message):
    if msg.media is not None:
       media = getattr(msg, msg.media.value)
    channel_id = msg.chat.id  # Get the channel ID
    caption = await get_caption(channel_id)
    try:
     if caption:
        edit_mode = await get_edit_mode(channel_id)
        buttons_data = await get_buttons(channel_id)

        # Handle button data if any
        buttons = None
        if buttons_data:
            buttons = await string_to_buttons(buttons_data)
        file_name = getattr(media, 'file_name', '')
        file_size = getattr(media, 'file_size', '')
        fcaption = getattr(msg, 'caption', '')
        
        mcap = caption.format(file_name=file_name, file_size=get_size(file_size), file_caption=fcaption)
                   
        position = await get_position(channel_id)
        if position == 'below':
            # Edit message with formatted caption and other parameters
            await msg.edit_text(
                mcap,
                reply_markup=InlineKeyboardMarkup(buttons) if buttons else None,
                disable_web_page_preview=not await get_webpage_preview(channel_id),
                parse_mode=enums.ParseMode.MARKDOWN,
            )
        else:
            # Edit message with formatted caption and other parameters
            await msg.edit_text(
                mcap,
                reply_markup=InlineKeyboardMarkup(buttons) if buttons else None,
                disable_web_page_preview=not await get_webpage_preview(channel_id),  
                parse_mode=enums.ParseMode.HTML,
            )
     sticker = await get_sticker(channel_id)       
     if sticker:
            await msg.reply_sticker(sticker)
            
    except FloodWait as gk:
        time = get_readable_time(gk.value)
        print(f"Flood wait encountered: {gk}")
        await asyncio.sleep(gk.value)  # Wait for the specified duration
        await modify(bot, msg)  # Retry the operation

