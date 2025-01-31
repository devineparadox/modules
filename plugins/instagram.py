import re
import requests
from pyrogram import filters
from Devine import app


EVENT_LOGS = -1001835308211

def is_instagram_url(url):
    return re.match(r"^(https?://)?(www\.)?(instagram\.com|instagr\.am)/.*$", url)

@app.on_message(filters.text)
async def auto_download_instagram_video(client, message):
    urls = re.findall(r"(https?://(?:www\.)?(?:instagram\.com|instagr\.am)/\S+)", message.text)
    
    if urls:
        url = urls[0]
        await process_instagram_video(message, url)

async def process_instagram_video(message, url):
    if not is_instagram_url(url):
        return await message.reply_text(
            "ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇᴅ ᴜʀʟ ɪs ɴᴏᴛ ᴀ ᴠᴀʟɪᴅ ɪɴsᴛᴀɢʀᴀᴍ ᴜʀʟ."
        )
    
    a = await message.reply_text("ᴘʀᴏᴄᴇssɪɴɢ...")
    api_url = f"https://insta-dl.hazex.workers.dev/?url={url}"

    response = requests.get(api_url)
    try:
        result = response.json()
        data = result["result"]
    except Exception as e:
        error_message = f"Error:\n{e}"
        try:
            await a.edit(error_message)
        except Exception:
            await message.reply_text(error_message)
        try:
            await app.send_message(EVENT_LOGS, error_message)
        except Exception as log_error:
            print(f"Failed to send log message: {log_error}")
        return
    
    if not result["error"]:
        video_url = data["url"]
        duration = data["duration"]
        quality = data["quality"]
        file_type = data["extension"]
        size = data["formattedSize"]
        caption = f"**ᴅᴜʀᴀᴛɪᴏɴ :** {duration}\n**ǫᴜᴀʟɪᴛʏ :** {quality}\n**ᴛʏᴘᴇ :** {file_type}\n**sɪᴢᴇ :** {size}"

        # Send video to the user
        await a.delete()
        await message.reply_video(video_url, caption=caption)

        # Forward video details to the log channel
        log_message = f"""
**#INSTAGRAM**

**ʟɪɴᴋ:** {url}
**ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ:** @{message.from_user.username} 
ɪᴅ: `{message.from_user.id}`
**ᴅᴜʀᴀᴛɪᴏɴ:** {duration}
**ǫᴜᴀʟɪᴛʏ:** {quality}
**Type:** {file_type}
**sɪᴢᴇ:** {size}
"""

        try:
            await app.send_video(
                EVENT_LOGS,
                video_url,
                caption=log_message
            )
        except Exception as log_error:
            print(f"Failed to forward log message with video: {log_error}")
    else:
        try:
            await a.edit("ғᴀɪʟᴇᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ʀᴇᴇʟ.")
        except Exception:
            await message.reply_text("ғᴀɪʟᴇᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ʀᴇᴇʟ.")
        try:
            await app.send_message(EVENT_LOGS, "Failed to download reel.")
        except Exception as log_error:
            print(f"Failed to send log message: {log_error}")

@app.on_message(filters.command(["ig", "instagram", "reel"]))
async def download_instagram_video(client, message):
    if len(message.command) < 2:
        await message.reply_text(
            "ᴘʀᴏᴠɪᴅᴇ ᴀɴ ɪɴsᴛᴀɢʀᴀᴍ ʟɪɴᴋ ᴀғᴛᴇʀ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ᴛʜᴇ ᴠɪᴅᴇᴏ."
        )
        return
    url = message.text.split()[1]
    await process_instagram_video(message, url)
