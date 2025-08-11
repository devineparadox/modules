import io
from gtts import gTTS, gTTSError
from pyrogram import filters
from Devine import app

@app.on_message(filters.command("tts"))
async def text_to_speech(client, message):
    if len(message.command) < 2:
        return await message.reply_text(
            "Please provide some text to convert to speech.\nExample: `/tts Hello world!`"
        )

    text = message.text.split(None, 1)[1]

    # Optional: limit text length for gTTS stability
    if len(text) > 200:
        return await message.reply_text("⚠️ Text too long! Please keep it under 200 characters.")

    try:
        tts = gTTS(text=text, lang="hi")
        audio_data = io.BytesIO()
        tts.write_to_fp(audio_data)
        audio_data.seek(0)
        audio_data.name = "tts.mp3"

        await message.reply_audio(audio_data)

    except gTTSError as e:
        await message.reply_text(f"❌ Failed to generate speech: {e}")

__help__ = """
**ᴛᴇxᴛ ᴛᴏ sᴘᴇᴇᴄʜ ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅ**

ᴜsᴇ ᴛʜᴇ `/tts` ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴄᴏɴᴠᴇʀᴛ ᴛᴇxᴛ ɪɴᴛᴏ sᴘᴇᴇᴄʜ.

- `/tts <ᴛᴇxᴛ>`: ᴄᴏɴᴠᴇʀᴛs ᴛʜᴇ ɢɪᴠᴇɴ ᴛᴇxᴛ ᴛᴏ sᴘᴇᴇᴄʜ.

**ᴇxᴀᴍᴘʟᴇ :**
- `/tts Hello world !`

**ɴᴏᴛᴇ :**
ᴍᴀᴋᴇ sᴜʀᴇ ᴛᴏ ᴘʀᴏᴠɪᴅᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴀғᴛᴇʀ ᴛʜᴇ `/tts` ᴄᴏᴍᴍᴀɴᴅ.
"""

__mod__ = "ᴛᴛs"
