from lexica import Client as LexicaClient
from pyrogram import filters
from pyrogram.types import Message
import os
from Devine import app

async def getFile(message: Message):
    if not message.reply_to_message:
        return None
    if message.reply_to_message.photo:
        image = await message.reply_to_message.download()
        return image
    elif message.reply_to_message.document and message.reply_to_message.document.mime_type in ['image/png', 'image/jpg', 'image/jpeg']:
        image = await message.reply_to_message.download()
        return image
    else:
        return None

async def UpscaleImages(image: bytes) -> str:
    try:
        client = LexicaClient()
        content = client.upscale(image)
        
        upscaled_file_path = "upscaled.png"
        with open(upscaled_file_path, "wb") as output_file:
            output_file.write(content)
        
        return upscaled_file_path
    except Exception as e:
        raise Exception(f"Failed to upscale the image: {e}")
    
@app.on_message(filters.command("upscale"))
async def upscaleImages(_, message):
    file = await getFile(message)
    if file is None:
        return await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀɴ ɪᴍᴀɢᴇ.")
    
    msg = await message.reply("ᴜᴘsᴄᴀʟɪɴɢ...")

    with open(file, "rb") as f:
        imageBytes = f.read()
    os.remove(file)
    
    try:
        upscaledImage = await UpscaleImages(imageBytes)
        await message.reply_document(open(upscaledImage, "rb"))
        await msg.delete()
        os.remove(upscaledImage)
    except Exception as e:
        await msg.edit(f"Failed to upscale the image: {e}")
