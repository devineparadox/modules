from uuid import uuid4

import pyrogram
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Devine import app



@app.on_message(filters.command("pkang"))
async def _packkang(app, message):
    txt = await message.reply_text("ᴘʀᴏᴄᴇssɪɴɢ....")
    if not message.reply_to_message:
        await txt.edit("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ")
        return
    if not message.reply_to_message.sticker:
        await txt.edit("ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ")
        return
    
    # Check if the sticker is animated
    if message.reply_to_message.sticker.is_animated:
        # Process animated sticker
        if message.reply_to_message.sticker.is_video:
            return await txt.edit("ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴠɪᴅᴇᴏ sᴛɪᴄᴋᴇʀ.")
        
        # Get the pack name
        if len(message.command) < 2:
            pack_name = f"{message.from_user.first_name}_Animated"
        else:
            pack_name = message.text.split(maxsplit=1)[1]

        short_name = message.reply_to_message.sticker.set_name
        stickers = await app.invoke(
            pyrogram.raw.functions.messages.GetStickerSet(
                stickerset=pyrogram.raw.types.InputStickerSetShortName(
                    short_name=short_name
                ),
                hash=0,
            )
        )
        shits = stickers.documents
        sticks = []

        for i in shits:
            sex = pyrogram.raw.types.InputDocument(
                id=i.id, access_hash=i.access_hash, file_reference=i.file_reference
            )

            sticks.append(
                pyrogram.raw.types.InputStickerSetItem(
                    document=sex, emoji=i.attributes[1].alt
                )
            )

        try:
            bot_username = (await app.get_me()).username
            short_name = f"animated_sticker_pack_{str(uuid4()).replace('-', '')}_by_{bot_username}"
            user_id = await app.resolve_peer(message.from_user.id)
            
            # Create the animated sticker pack
            await app.invoke(
                pyrogram.raw.functions.stickers.CreateStickerSet(
                    user_id=user_id,
                    title=pack_name,
                    short_name=short_name,
                    stickers=sticks,
                )
            )
            await txt.edit(
                f"""ʏᴏᴜʀ ᴀɴɪᴍᴀᴛᴇᴅ sᴛɪᴄᴋᴇʀ ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ! ɪᴛ ᴡɪʟʟ ʙᴇ ʟɪɴᴋᴇᴅ ᴛᴏ ᴀ ᴘᴀᴄᴋ ɢɪᴠᴇ ᴇᴛᴇʀɴᴀʟ ʀᴇғᴇʀᴇɴᴄᴇ\n
• ᴛᴏᴛᴀʟ sᴛɪᴄᴋᴇʀ : {len(sticks)}""",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "ᴘᴀᴄᴋ", url=f"http://t.me/addstickers/{short_name}"
                            )
                        ]
                    ]
                ),
            )
        except Exception as e:
            await message.reply(str(e))
    else:
        # Process non-animated stickers (same as your original code)
        if message.reply_to_message.sticker.is_video:
            return await txt.edit("ʀᴇᴘʟʏ ᴛᴏ ᴀ ɴᴏɴ-ᴀɴɪᴍᴀᴛᴇᴅ sᴛɪᴄᴋᴇʀ.")
        
        # Get the pack name
        if len(message.command) < 2:
            pack_name = f"{message.from_user.first_name}"
        else:
            pack_name = message.text.split(maxsplit=1)[1]

        short_name = message.reply_to_message.sticker.set_name
        stickers = await app.invoke(
            pyrogram.raw.functions.messages.GetStickerSet(
                stickerset=pyrogram.raw.types.InputStickerSetShortName(
                    short_name=short_name
                ),
                hash=0,
            )
        )
        shits = stickers.documents
        sticks = []

        for i in shits:
            sex = pyrogram.raw.types.InputDocument(
                id=i.id, access_hash=i.access_hash, file_reference=i.file_reference
            )

            sticks.append(
                pyrogram.raw.types.InputStickerSetItem(
                    document=sex, emoji=i.attributes[1].alt
                )
            )

        try:
            bot_username = (await app.get_me()).username
            short_name = f"sticker_pack_{str(uuid4()).replace('-', '')}_by_{bot_username}"
            user_id = await app.resolve_peer(message.from_user.id)
            
            await app.invoke(
                pyrogram.raw.functions.stickers.CreateStickerSet(
                    user_id=user_id,
                    title=pack_name,
                    short_name=short_name,
                    stickers=sticks,
                )
            )
            await txt.edit(
                f"""ʏᴏᴜʀ sᴛɪᴄᴋᴇʀ ʜᴀs ʙᴇᴇɴ ᴀᴅᴅᴇᴅ! ғᴀsᴛ ᴜᴘᴅᴀᴛᴇ ʀᴇᴍᴏᴠᴇ ʏᴏᴜʀ ᴘᴀᴄᴋ & ᴀᴅᴅ ᴀɢᴀɪɴ\n
• ᴛᴏᴛᴀʟ sᴛɪᴄᴋᴇʀ : {len(sticks)}""",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                "ᴘᴀᴄᴋ", url=f"http://t.me/addstickers/{short_name}"
                            )
                        ]
                    ]
                ),
            )
        except Exception as e:
            await message.reply(str(e))
