import re
import datetime
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

from Devine import app
from utils.error import capture_err
from utils.permissions import adminsOnly, member_permissions
from Devine.utils.keyboard import ikb
from Devine.utils.functions import check_format, extract_text_and_keyb, get_data_and_name
from Devine.utils.database import deleteall_filters, get_filter, get_filters_names, save_filter
from config import BANNED_USERS


__mod__ = "Filters"
__help__ = """/filters - List all filters in the chat.
/filter [FILTER_NAME] - Save a filter (reply to a message).

Supported filter types: Text, Animation, Photo, Document, Video, Video Notes, Audio, Voice.

To use multiple words in a filter, use `/filter Hey_there` to filter "Hey there".

/stop [FILTER_NAME] - Remove a specific filter.
/stopall - Delete all filters in a chat (permanently).

Supports markdown and HTML formatting. Use /markdownhelp to learn more.
"""


@app.on_message(filters.command("filter") & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_change_info")
async def save_filters(_, message: Message):
    try:
        if len(message.command) < 2:
            return await message.reply_text(
                "**Usage:**\nReply to a message with `/filter [FILTER_NAME] [CONTENT]` to set a new filter."
            )

        replied_message = message.reply_to_message or message
        data, name = await get_data_and_name(replied_message, message)

        if len(name) < 2:
            return await message.reply_text("**Filter name must be at least 2 characters long.**")

        if data == "error":
            return await message.reply_text(
                "**Usage:**\n`/filter [FILTER_NAME] [CONTENT]`\n"
                "`----------- OR -----------`\n"
                "Reply to a message with `/filter [FILTER_NAME]`."
            )

        _type, file_id = "text", None
        if replied_message.sticker:
            _type, file_id = "sticker", replied_message.sticker.file_id
        elif replied_message.animation:
            _type, file_id = "animation", replied_message.animation.file_id
        elif replied_message.photo:
            _type, file_id = "photo", replied_message.photo.file_id
        elif replied_message.document:
            _type, file_id = "document", replied_message.document.file_id
        elif replied_message.video:
            _type, file_id = "video", replied_message.video.file_id
        elif replied_message.video_note:
            _type, file_id = "video_note", replied_message.video_note.file_id
        elif replied_message.audio:
            _type, file_id = "audio", replied_message.audio.file_id
        elif replied_message.voice:
            _type, file_id = "voice", replied_message.voice.file_id

        data = await check_format(ikb, data) if data else None
        if not data:
            return await message.reply_text("**Invalid formatting. Check the help section.**")

        await save_filter(message.chat.id, name.replace("_", " "), {"type": _type, "data": data, "file_id": file_id})
        return await message.reply_text(f"**Saved filter `{name}`.**")

    except UnboundLocalError:
        return await message.reply_text("**Replied message is inaccessible. Try forwarding it instead.**")


@app.on_message(filters.command("filters") & ~filters.private & ~BANNED_USERS)
@capture_err
async def get_filters(_, message: Message):
    filters_list = await get_filters_names(message.chat.id)
    if not filters_list:
        return await message.reply_text("**No filters set in this chat.**")

    filters_list.sort()
    msg = f"**List of filters in {message.chat.title}:**\n" + "\n".join(f"- `{flt}`" for flt in filters_list)
    await message.reply_text(msg)


@app.on_message(
    filters.text
    & ~filters.private
    & ~filters.channel
    & ~filters.via_bot
    & ~filters.forwarded
    & ~BANNED_USERS,
    group=1,
)
@capture_err
async def filters_re(_, message: Message):
    text = message.text.lower().strip()
    if not text:
        return

    chat_id = message.chat.id
    list_of_filters = await get_filters_names(chat_id)
    for word in list_of_filters:
        pattern = rf"( |^|[^\w]){re.escape(word)}( |$|[^\w])"
        if re.search(pattern, text, flags=re.IGNORECASE):
            _filter = await get_filter(chat_id, word)
            data_type, data, file_id = _filter["type"], _filter["data"], _filter.get("file_id")
            keyb = None

            if data:
                replacements = {
                    "{app.mention}": app.mention,
                    "{GROUPNAME}": message.chat.title,
                    "{NAME}": message.from_user.mention,
                    "{ID}": f"`{message.from_user.id}`",
                    "{FIRSTNAME}": message.from_user.first_name,
                    "{SURNAME}": message.from_user.last_name or "None",
                    "{USERNAME}": message.from_user.username or "None",
                    "{DATE}": datetime.datetime.now().strftime("%Y-%m-%d"),
                    "{WEEKDAY}": datetime.datetime.now().strftime("%A"),
                    "{TIME}": datetime.datetime.now().strftime("%H:%M:%S UTC"),
                }
                for key, value in replacements.items():
                    data = data.replace(key, value)

                if re.findall(r".+\,.+", data):
                    keyboard = extract_text_and_keyb(ikb, data)
                    if keyboard:
                        data, keyb = keyboard

            if data_type == "text":
                await message.reply_text(text=data, reply_markup=keyb, disable_web_page_preview=True)
            elif file_id:
                media_methods = {
                    "sticker": message.reply_sticker,
                    "animation": message.reply_animation,
                    "photo": message.reply_photo,
                    "document": message.reply_document,
                    "video": message.reply_video,
                    "video_note": message.reply_video_note,
                    "audio": message.reply_audio,
                    "voice": message.reply_voice,
                }
                await media_methods.get(data_type, lambda **kwargs: None)(
                    file_id, caption=data, reply_markup=keyb
                )

            return  # Avoid filter spam


@app.on_message(filters.command("stopall") & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_change_info")
async def stop_all(_, message: Message):
    if not await get_filters_names(message.chat.id):
        return await message.reply_text("**No filters in this chat.**")

    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Yes, delete", callback_data="stop_yes"),
          InlineKeyboardButton("No, cancel", callback_data="stop_no")]]
    )
    await message.reply_text("**Are you sure you want to delete all filters in this chat?**", reply_markup=keyboard)


@app.on_callback_query(filters.regex("stop_(.*)") & ~BANNED_USERS)
async def stop_all_cb(_, cb: CallbackQuery):
    chat_id, user_id = cb.message.chat.id, cb.from_user.id
    if "can_change_info" not in await member_permissions(chat_id, user_id):
        return await cb.answer("**You don’t have the required permission.**", show_alert=True)

    if cb.data.split("_")[1] == "yes":
        await deleteall_filters(chat_id)
        return await cb.message.edit("**Successfully deleted all filters in this chat.**")

    await cb.message.delete()