from pyrogram import filters
from pyrogram.types import Message

from AnonXMusic import app
from AnonXMusic.misc import SUDOERS
from AnonXMusic.utils.database.play_counts import get_group_played, get_top_groups
from AnonXMusic.utils.decorators.language import language

@app.on_message(filters.command("check") & filters.group)
@language
async def check_group_played(client, message: Message, _):
    if len(message.command) != 2:
        return await message.reply_text(_["play_check_1"])
    
    try:
        chat_id = int(message.command[1])
    except ValueError:
        return await message.reply_text(_["play_check_2"])
        
    count = await get_group_played(chat_id)
    
    await message.reply_text(
        _["play_check_3"].format(
            chat_id=chat_id,
            count=count
        )
    )

@app.on_message(filters.command("topgroup"))
@language
async def top_groups_played(client, message: Message, _):
    top_groups = await get_top_groups(10)  # Get top 10 groups
    
    if not top_groups:
        return await message.reply_text(_["play_top_1"])
        
    text = _["play_top_2"] + "\n\n"
    for i, group in enumerate(top_groups, 1):
        try:
            chat = await app.get_chat(group["chat_id"])
            chat_title = chat.title
        except:
            chat_title = "Unknown Group"
            
        text += f"{i}. {chat_title} - {group['play_count']} plays\n"
    
    await message.reply_text(text)
