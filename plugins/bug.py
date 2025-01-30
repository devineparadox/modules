from datetime import datetime
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from Devine import OWNER_ID as owner_id
from Devine import app as devine


def content(msg: Message) -> [None, str]:
    text_to_return = msg.text

    if text_to_return is None:
        return None
    if " " in text_to_return:
        try:
            return text_to_return.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None


@devine.on_message(filters.command("bug"))
async def bugs(_, msg: Message):
    if msg.chat.username:
        chat_username = f"@{msg.chat.username}"
    else:
        chat_username = "Private Group"
    chat_id = f"{msg.chat.id}"
        
    bugs = content(msg)
    user_id = msg.from_user.id
    mention = (
        "[" + msg.from_user.first_name + "](tg://user?id=" + str(msg.from_user.id) + ")"
    )
    datetimes_fmt = "%d-%m-%Y"
    datetimes = datetime.utcnow().strftime(datetimes_fmt)

    bug_report = f"""
**#BUG :**

**• ʙᴜɢ : ** {bugs}
**• ʀᴇᴩᴏʀᴛᴇᴅ ʙʏ : ** {mention}
**• ᴜsᴇʀ : ** {user_id}
**• ᴄʜᴀᴛ : ** {chat_username}
**• ᴄʜᴀᴛ ɪᴅ : ** {chat_id}
**• ᴇᴠᴇɴᴛ sᴛᴀᴍᴩ : **{datetimes}"""

    if msg.chat.type == "private":
        await msg.reply_text("ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ɪs ᴏɴʟʏ ғᴏʀ ɢʀᴏᴜᴩs.")
        return

    if user_id == owner_id:
        if bugs:
            await msg.reply_text(
                "this command is working.",
            )
            return
        else:
            await msg.reply_text("noob reporter!")
    elif user_id != owner_id:
        if bugs:
            await msg.reply_text(
                f"<b>ʙᴜɢ ʀᴇᴩᴏʀᴛ : {bugs}</b>",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close_data")]]
                ),
            )
            await devine.send_message(
                -1002436618749,  
                text=f"{bug_report}",
                reply_markup=InlineKeyboardMarkup(
                 [
                       [
                           InlineKeyboardButton("ᴠɪᴇᴡ ʙᴜɢ", url=f"{msg.link}")]
                   ]
               ),
           )
        else:
            await msg.reply_text(
                f"ɴᴏ ʙᴜɢ ᴛᴏ ʀᴇᴩᴏʀᴛ!",
            )


@devine.on_callback_query(filters.regex("close_data"))
async def close_send_message(_, query: CallbackQuery):
    is_admin = await devine.get_chat_member(query.message.chat.id, query.from_user.id)
    if not is_admin.privileges.can_delete_messages:
        await query.answer("ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ʀɪɢʜᴛs ᴛᴏ ᴄʟᴏsᴇ ᴛʜɪs.", show_alert=True)
    else:
        await query.message.delete()

__mod__ = "ʙᴜɢ"
__help__ = """
⟐ Commands :
• /bug <description> : Report a bug in the group and send it to the admins for review.

Example :
• /bug The bot is not responding to commands.

The bot admins will review your report and take appropriate action.
"""
