import random
from telethon import events
from Gojo import tbot as devine

GIF = (
    "https://telegra.ph/file/ef94f2f61aa4d9394ef23.mp4",
    "https://telegra.ph/file/b82442bf9ebc32534f7a2.mp4",
    "https://telegra.ph/file/70d43e136125f9c120d2e.mp4",
    "https://telegra.ph/file/45354d3e42982f8de78f4.mp4",
    "https://telegra.ph/file/a22a0930f069686a0c4ef.mp4",
)

@devine.on(events.NewMessage(pattern="/wish ?(.*)$"))
async def wish(e):
    if e.is_reply:
        point = random.randint(1, 100)
        lol = await e.get_reply_message()
        fire = "https://telegra.ph/file/d6c2cd346255a33b3a023.mp4"
        caption = (
            f"**ʏᴏᴏ, {e.sender.first_name}!**\n"
            "ᴛᴏ sʜᴀʀᴇ ʏᴏᴜʀ ᴡɪsʜ, ᴜsᴇ ᴛʜᴇ ғᴏʀᴍᴀᴛ /wish 'ᴜʀ ᴡɪsʜ'\n"
            )
        await devine.send_message(
            e.chat_id,
            caption,
            link_preview=False,
            reply_to=lol,
            parse_mode="markdown",
        )
    elif e.pattern_match.group(1):
        point = random.randint(1, 100)
        wish_text = e.pattern_match.group(1)
        fire = random.choice(GIF)
        caption = (
            f"ʏᴏᴏ! {e.sender.first_name}, ʏᴏᴜʀ ᴡɪsʜ ʜᴀs ʙᴇᴇɴ ᴄᴀsᴛᴇᴅ\n\n"
            f"✨ ʏᴏᴜʀ ᴡɪꜱʜ : {wish_text}\n"
            f"[🫧]({fire}) ᴘᴏssɪʙɪʟɪᴛɪᴇs : {point}%\n"
            )
        await devine.send_message(
            e.chat_id,
            caption,
            reply_to=e,
            parse_mode="markdown",
        )
    else:
        await devine.send_message(
            e.chat_id,
            "sʜᴀʀᴇ ʏᴏᴜʀ ᴡɪsʜ ʙʏ ᴜsɪɴɢ ᴛʜᴇ ғᴏʀᴍᴀᴛ: /wish ʏᴏᴜʀ ᴡɪsʜ",
            reply_to=e,
        )
