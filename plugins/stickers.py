import asyncio
import os
import re
import shutil
import tempfile
import textwrap

from PIL import Image, ImageDraw, ImageFont
from pyrogram import Client, emoji, enums, filters
from pyrogram.errors import BadRequest, PeerIdInvalid, StickersetInvalid
from pyrogram.file_id import FileId
from pyrogram.raw.functions.messages import GetStickerSet, SendMedia
from pyrogram.raw.functions.stickers import (
    AddStickerToSet,
    CreateStickerSet,
    RemoveStickerFromSet,
)
from pyrogram.raw.types import (
    DocumentAttributeFilename,
    InputDocument,
    InputMediaUploadedDocument,
    InputStickerSetItem,
    InputStickerSetShortName,
)
from pyrogram.types import InlineKeyboardButton
from pyrogram.types import InlineKeyboardButton as IKB
from pyrogram.types import InlineKeyboardMarkup
from pyrogram.types import InlineKeyboardMarkup as IKM
from pyrogram.types import Message

from config import LOG as DATA_LOG
from Devine import app
from Devine.server import server


PREFIX_HANDLER = ["!", "/", "$"]


def get_emoji_regex():
    e_list = [
        getattr(emoji, e).encode("unicode-escape").decode("ASCII")
        for e in dir(emoji)
        if not e.startswith("_")
    ]
    e_sort = sorted([x for x in e_list if not x.startswith("*")], reverse=True)
    pattern_ = f"({'|'.join(e_sort)})"
    return re.compile(pattern_)


EMOJI_PATTERN = get_emoji_regex()
SUPPORTED_TYPES = ["jpeg", "png", "webp"]


@app.on_message(filters.command(["getsticker"], PREFIX_HANDLER), group=111)
async def getsticker_(self: Client, ctx: Message):
    if not ctx.reply_to_message:
        return await ctx.reply("ᴘʟᴇᴀsᴇ ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ.")
    sticker = ctx.reply_to_message.sticker
    if not sticker:
        return await ctx.reply("ᴏɴʟʏ sᴛɪᴄᴋᴇʀ ᴍᴇssᴀɢᴇs ᴀʀᴇ sᴜᴘᴘᴏʀᴛᴇᴅ.")
    if sticker.is_animated:
        return await ctx.reply("ᴀɴɪᴍᴀᴛᴇᴅ sᴛɪᴄᴋᴇʀs ᴀʀᴇ ɴᴏᴛ sᴜᴘᴘᴏʀᴛᴇᴅ.")
    with tempfile.TemporaryDirectory() as tempdir:
        path = os.path.join(tempdir, "getsticker")
    sticker_file = await self.download_media(
        message=ctx.reply_to_message,
        file_name=f"{path}/{sticker.set_name}.png",
    )
    await ctx.reply_to_message.reply_document(
        document=sticker_file,
        caption=f"<b>ᴇᴍᴏᴊɪ:</b> {sticker.emoji}\n"
        f"<b>sᴛɪᴄᴋᴇʀ ɪᴅ:</b> <code>{sticker.file_id}</code>\n\n",
    )
    shutil.rmtree(tempdir, ignore_errors=True)


@app.on_message(filters.command("getvidsticker"), group=222)
async def _vidstick(_, message):
    chat_id = message.chat.id
    replied = message.reply_to_message
    if replied and replied.sticker:
        if not replied.sticker.is_video:
            return await message.reply_text("ᴜsᴇ /getvidsticker ɪғ sᴛɪᴄᴋᴇʀ ɪs ɴᴏᴛ vɪᴅᴇᴏ.")
        file_id = replied.sticker.file_id
        new_file = await _.download_media(file_id, file_name="sticker.mp4")
        await _.send_animation(chat_id, new_file)
        os.remove(new_file)
    else:
        await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ vɪᴅᴇᴏ sᴛɪᴄᴋᴇʀ ᴛᴏ ᴜᴘʟᴏᴀᴅ ɪᴛ'ѕ ᴍᴘ4.")


@app.on_message(filters.command("getvideo"), group=333)
async def _vidstick(_, message):
    chat_id = message.chat.id
    replied = message.reply_to_message
    if replied and replied.animation:
        file_id = replied.animation.file_id
        new_file = await _.download_media(file_id, file_name="video.mp4")
        print(new_file)
        await _.send_video(chat_id, video=open(new_file, "rb"))
        os.remove(new_file)
    else:
        await message.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ ɢɪғ ғᴏʀ ᴍᴇ ᴛᴏ ɢᴇᴛ ɪᴛ'ѕ vɪᴅᴇᴏ.")


@app.on_message(filters.command("stickerid", PREFIX_HANDLER) & filters.reply, group=444)
async def getstickerid(_, ctx: Message):
    if ctx.reply_to_message.sticker:
        await ctx.reply(
            "ᴛʜᴇ ɪᴅ ᴏғ ᴛʜɪs sᴛɪᴄᴋᴇʀ ɪs : <code>{stickerid}</code>".format(
                stickerid=ctx.reply_to_message.sticker.file_id
            )
        )


@app.on_message(filters.command("delsticker", PREFIX_HANDLER) & filters.reply, group=555)
async def unkangs(self: Client, ctx: Message):
    if not ctx.from_user:
        return await ctx.reply("ʏᴏᴜ'ʀᴇ ᴀɴᴏɴʏᴍᴏᴜs, ᴜɴᴋᴀɴɢ ɪɴ ᴍʏ pm")
    if sticker := ctx.reply_to_message.sticker:
        if str(ctx.from_user.id) not in sticker.set_name:
            return await ctx.reply("ᴛʜɪs sᴛɪᴄᴋᴇʀ ɪs ɴᴏᴛ yᴏᴜʀ pᴀᴄᴋ, ᴅᴏɴ'ᴛ ᴅᴏ ɪᴛ..")
        pp = await ctx.reply("ᴀᴛᴛᴇᴍᴘᴛɪɴɢ...")
        try:
            decoded = FileId.decode(sticker.file_id)
            sticker = InputDocument(
                id=decoded.media_id,
                access_hash=decoded.access_hash,
                file_reference=decoded.file_reference,
            )
            await app.invoke(RemoveStickerFromSet(sticker=sticker))
            await pp.edit("sᴛɪᴄᴋᴇʀ sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴇᴍᴏᴠᴇᴅ ғʀᴏᴍ yᴏᴜʀ pᴀᴄᴋ.")
        except Exception as e:
            await pp.edit(f"ᴀɴ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ: {e}")
    else:
        await ctx.reply(f"ᴛᴏ ᴜɴᴋᴀɴɢ ᴀ sᴛɪᴄᴋᴇʀ, ʀᴇᴘʟʏ ᴛᴏ ᴛʜᴇ sᴛɪᴄᴋᴇʀ yᴏᴜ ᴡᴀɴᴛ ᴛᴏ ʀᴇᴍᴏᴠᴇ ғʀᴏᴍ ᴛʜᴇ sᴇᴛ.")

@app.on_message(filters.command(["kang"], PREFIX_HANDLER), group=666)
async def kang_sticker(self: Client, ctx: Message):
    if not ctx.from_user:
        return await ctx.reply("ʏᴏᴜ'ʀᴇ ᴀɴᴏɴʏᴍᴏᴜs, ᴋᴀɴɢ ɪɴ ᴍʏ ᴘᴍ")
    prog_msg = await ctx.reply("ᴀᴛᴛᴇᴍᴘᴛɪɴɢ ᴛᴏ ᴋᴀɴɢ ᴛʜᴇ sᴛɪᴄᴋᴇʀ...")
    sticker_emoji = "⚡"
    packnum = 0
    packname_found = False
    resize = False
    animated = False
    videos = False
    convert = False
    reply = ctx.reply_to_message
    user = await self.resolve_peer(ctx.from_user.username or ctx.from_user.id)

    if reply and reply.media:
        if reply.photo:
            resize = True
        elif reply.animation:
            videos = True
            convert = True
        elif reply.video:
            convert = True
            videos = True
        elif reply.document:
            if "image" in reply.document.mime_type:
                resize = True
            elif reply.document.mime_type in (
                enums.MessageMediaType.VIDEO,
                enums.MessageMediaType.ANIMATION,
            ):
                videos = True
                convert = True
            elif "tgsticker" in reply.document.mime_type:
                animated = True
        elif reply.sticker:
            if not reply.sticker.file_name:
                return await prog_msg.edit("sᴛɪᴄᴋᴇʀ ʜᴀs ɴᴏ ғɪʟᴇ ɴᴀᴍᴇ.")
            if reply.sticker.emoji:
                sticker_emoji = reply.sticker.emoji
            animated = reply.sticker.is_animated
            videos = reply.sticker.is_video
            if videos:
                convert = False
            elif not reply.sticker.file_name.endswith(".tgs"):
                resize = True
        else:
            return await prog_msg.edit("ɪ ᴄᴀɴɴᴏᴛ ᴋᴀɴɢ ᴛʜɪs ᴛʏᴘᴇ.")

        pack_prefix = "anim" if animated else "vid" if videos else "a"
        packname = f"{pack_prefix}_{ctx.from_user.id}_by_{self.me.username}"

        if (
            len(ctx.command) > 1
            and ctx.command[1].isdigit()
            and int(ctx.command[1]) > 0
        ):
            packnum = ctx.command.pop(1)
            packname = f"{pack_prefix}{packnum}_{ctx.from_user.id}_by_{self.me.username}"
        if len(ctx.command) > 1:
            sticker_emoji = (
                "".join(set(EMOJI_PATTERN.findall("".join(ctx.command[1:]))))
                or sticker_emoji
            )
        filename = await self.download_media(ctx.reply_to_message)
        if not filename:
            await prog_msg.delete()
            return
    elif ctx.entities and len(ctx.entities) > 1:
        pack_prefix = "a"
        filename = "sticker.png"
        packname = f"c{ctx.from_user.id}_by_{self.me.username}"
        img_url = next(
            (
                ctx.text[y.offset : (y.offset + y.length)]
                for y in ctx.entities
                if y.type == "url"
            ),
            None,
        )

        if not img_url:
            await prog_msg.delete()
            return
        try:
            r = await server.get(img_url)
            if r.status_code == 200:
                with open(filename, mode="wb") as f:
                    f.write(r.read())
        except Exception as r_e:
            return await prog_msg.edit(f"{r_e.__class__.__name__} : {r_e}")
        if len(ctx.command) > 2:
            if ctx.command[2].isdigit() and int(ctx.command[2]) > 0:
                packnum = ctx.command.pop(2)
                packname = f"a{packnum}_{ctx.from_user.id}_by_{self.me.username}"
            if len(ctx.command) > 2:
                sticker_emoji = (
                    "".join(set(EMOJI_PATTERN.findall("".join(ctx.command[2:]))))
                    or sticker_emoji
                )
            resize = True
    else:
        return await prog_msg.edit("ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ ᴏʀ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴠᴀʟɪᴅ ɪᴍᴀɢᴇ ᴜʀʟ.")
    
    try:
        if resize:
            filename = resize_image(filename)
        elif convert:
            filename = await convert_video(filename)
            if filename is False:
                return await prog_msg.edit("ᴇʀʀᴏʀ ᴄᴏɴᴠᴇʀᴛɪɴɢ ᴠɪᴅᴇᴏ.")
        max_stickers = 50 if animated else 120
        while not packname_found:
            try:
                stickerset = await self.invoke(
                    GetStickerSet(
                        stickerset=InputStickerSetShortName(short_name=packname),
                        hash=0,
                    )
                )
                if stickerset.set.count >= max_stickers:
                    packnum += 1
                    packname = f"{pack_prefix}_{packnum}_{ctx.from_user.id}_by_{self.me.username}"
                else:
                    packname_found = True
            except StickersetInvalid:
                break
        file = await self.save_file(filename)
        media = await self.invoke(
            SendMedia(
                peer=(await self.resolve_peer(ctx.from_user.id)),  # Use user ID or another valid peer
                media=InputMediaUploadedDocument(
                    file=file,
                    mime_type=self.guess_mime_type(filename),
                    attributes=[DocumentAttributeFilename(file_name=filename)],
                ),
                message=f"#Sticker ᴋᴀɴɢ ʙʏ ᴜsᴇʀɪᴅ -> {ctx.from_user.id}",
                random_id=self.rnd_id(),
            ),
        )
        msg_ = media.updates[-1].message
        stkr_file = msg_.media.document
        if packname_found:
            await prog_msg.edit("ᴘᴀᴄᴋ ᴀʟʀᴇᴀᴅʏ ᴇxɪsᴛs, ᴀᴅᴅɪɴɢ sᴛɪᴄᴋᴇʀ...")
            await self.invoke(
                AddStickerToSet(
                    stickerset=InputStickerSetShortName(short_name=packname),
                    sticker=InputStickerSetItem(
                        document=InputDocument(
                            id=stkr_file.id,
                            access_hash=stkr_file.access_hash,
                            file_reference=stkr_file.file_reference,
                        ),
                        emoji=sticker_emoji,
                    ),
                )
            )
        else:
            await prog_msg.edit("ᴄʀᴇᴀᴛɪɴɢ ɴᴇᴡ sᴛɪᴄᴋᴇʀ ᴘᴀᴄᴋ...")
            stkr_title = f"{ctx.from_user.first_name}'s"
            if animated:
                stkr_title += "ᴀɴɪ-ᴘᴀᴄᴋ"
            elif videos:
                stkr_title += "ᴠɪᴅ-ᴘᴀᴄᴋ"
            if packnum != 0:
                stkr_title += f" ᴠ{packnum}"
            try:
                await self.invoke(
                    CreateStickerSet(
                        user_id=user,
                        title=stkr_title,
                        short_name=packname,
                        stickers=[
                            InputStickerSetItem(
                                document=InputDocument(
                                    id=stkr_file.id,
                                    access_hash=stkr_file.access_hash,
                                    file_reference=stkr_file.file_reference,
                                ),
                                emoji=sticker_emoji,
                            )
                        ],
                        animated=animated,
                        videos=videos,
                    )
                )
            except PeerIdInvalid:
                return await prog_msg.edit(
                    "sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʀᴇᴀᴛᴇ ᴛʜᴇ sᴛɪᴄᴋᴇʀ ᴘᴀᴄᴋ.",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    "ᴄʟɪᴄᴋ ʜᴇʀᴇ ᴛᴏ sᴛᴀʀᴛ",
                                    url=f"https://t.me/{self.me.username}?start",
                                )
                            ]
                        ]
                    ),
                )

    except BadRequest:
        return await prog_msg.edit("sᴛɪᴄᴋᴇʀ ᴘᴀᴄᴋ ɪs ғᴜʟʟ.")
    except Exception as all_e:
        await prog_msg.edit(f"{all_e.__class__.__name__} : {all_e}")
    else:
        markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="ᴠɪᴇᴡ ᴘᴀᴄᴋ",
                        url=f"https://t.me/addstickers/{packname}",
                    )
                ]
            ]
        )
        await prog_msg.edit(
            f"sᴛɪᴄᴋᴇʀ sᴜᴄᴄᴇssғᴜʟʟʏ ᴀᴅᴅᴇᴅ ᴛᴏ ᴛʜᴇ ᴘᴀᴄᴋ! {sticker_emoji}",
            reply_markup=markup,
        )
        try:
            os.remove(filename)
        except OSError:
            pass


def resize_image(filename: str) -> str:
    im = Image.open(filename)
    maxsize = 512
    scale = maxsize / max(im.width, im.height)
    sizenew = (int(im.width * scale), int(im.height * scale))
    im = im.resize(sizenew, Image.NEAREST)
    downpath, f_name = os.path.split(filename)
    # not hardcoding png_image as "sticker.png"
    png_image = os.path.join(downpath, f"{f_name.split('.', 1)[0]}.png")
    im.save(png_image, "PNG")
    if png_image != filename:
        os.remove(filename)
    return png_image


async def convert_video(filename: str) -> str:
    downpath, f_name = os.path.split(filename)
    webm_video = os.path.join(downpath, f"{f_name.split('.', 1)[0]}.webm")
    cmd = [
        "ffmpeg",
        "-loglevel",
        "quiet",
        "-i",
        filename,
        "-t",
        "00:00:03",
        "-vf",
        "fps=30",
        "-c:v",
        "vp9",
        "-b:v:",
        "500k",
        "-preset",
        "ultrafast",
        "-s",
        "512x512",
        "-y",
        "-an",
        webm_video,
    ]

    proc = await asyncio.create_subprocess_exec(*cmd)
    # Wait for the subprocess to finish
    await proc.communicate()

    if webm_video != filename:
        os.remove(filename)
    return webm_video


@app.on_message(filters.command("mmf"), group=777)
async def handler(client, message):
    if not message.reply_to_message:
        await message.reply("ʀᴇᴘʟʏ ᴛᴏ ᴀɴ ɪᴍᴀɢᴇ ᴏʀ ᴀ sᴛɪᴄᴋᴇʀ ᴛᴏ ᴍᴇᴍɪғʏ ɪᴛ!")
        return

    reply_message = message.reply_to_message
    if not reply_message.media:
        await message.reply("ᴘʀᴏᴠɪᴅᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴘʟᴇᴀsᴇ.")
        return

    file = await client.download_media(reply_message)
    msg = await message.reply("ᴍᴇᴍɪғʏɪɴɢ ᴛʜɪs ɪᴍᴀɢᴇ! ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ.")

    text = message.text.split("/mmf ", maxsplit=1)[1].strip()
    if len(text) < 1:
        return await msg.edit("ʏᴏᴜ ᴍɪɢʜᴛ ᴡᴀɴᴛ ᴛᴏ ᴛʏᴇ `/mmf ᴛᴇxᴛ`")

    meme = await draw_text(file, text)
    await client.send_document(message.chat.id, document=meme)
    await msg.delete()
    os.remove(meme)


async def draw_text(image_path, text):
    img = Image.open(image_path)
    os.remove(image_path)
    i_width, i_height = img.size

    if os.name == "nt":
        fnt = "arial.ttf"
    else:
        fnt = "./resources/default.ttf"
    m_font = ImageFont.truetype(fnt, int((70 / 640) * i_width))

    if ";" in text:
        upper_text, lower_text = text.split(";")
    else:
        upper_text = text
        lower_text = ""

    draw = ImageDraw.Draw(img)
    current_h, pad = 10, 5

    if upper_text:
        for u_text in textwrap.wrap(upper_text, width=15):
            u_width, u_height = draw.textsize(u_text, font=m_font)

            draw.text(
                xy=(((i_width - u_width) / 2) - 2, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=(((i_width - u_width) / 2) + 2, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=((i_width - u_width) / 2, int(((current_h / 640) * i_width)) - 2),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=(((i_width - u_width) / 2), int(((current_h / 640) * i_width)) + 2),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=((i_width - u_width) / 2, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(255, 255, 255),
            )

            current_h += u_height + pad

    if lower_text:
        for l_text in textwrap.wrap(lower_text, width=15):
            u_width, u_height = draw.textsize(l_text, font=m_font)

            draw.text(
                xy=(
                    ((i_width - u_width) / 2) - 2,
                    i_height - u_height - int((20 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(
                    ((i_width - u_width) / 2) + 2,
                    i_height - u_height - int((20 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    (i_height - u_height - int((20 / 640) * i_width)) - 2,
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    (i_height - u_height - int((20 / 640) * i_width)) + 2,
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    i_height - u_height - int((20 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(255, 255, 255),
            )

            current_h += u_height + pad

    image_name = "memify.webp"
    webp_file = os.path.join(image_name)
    img.save(webp_file, "webp")
    return webp_file


@app.on_message(filters.command(["stickerinfo", "stinfo"]), group=888)
async def give_st_info(c: app, m: Message):
    if not m.reply_to_message:
        await m.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ")
        return
    elif not m.reply_to_message.sticker:
        await m.reply_text("ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ")
        return
    st_in = m.reply_to_message.sticker
    st_type = "ɴᴏʀᴍᴀʟ"
    if st_in.is_animated:
        st_type = "ᴀɴɪᴍᴀᴛᴇᴅ"
    elif st_in.is_video:
        st_type = "ᴠɪᴅᴇᴏ"
    st_to_gib = f"""[sᴛɪᴄᴋᴇʀ]({m.reply_to_message.link}) ɪɴғᴏ:

ғɪʟᴇ ɪᴅ : `{st_in.file_id}`

ғɪʟᴇ ɴᴀᴍᴇ : {st_in.file_name}
ғɪʟᴇ ɪᴅ : `{st_in.file_unique_id}`
ᴅᴀᴛᴇ ᴀɴᴅ ᴛɪᴍᴇ ᴏғ sᴛɪᴄᴋᴇʀ ᴄʀᴇᴀᴛᴇᴅ : `{st_in.date}`
sᴛɪᴄᴋᴇʀ ᴛʏᴘᴇ : `{st_type}`
ᴇᴍᴏᴊɪ : {st_in.emoji}
ᴘᴀᴄᴋ ɴᴀᴍᴇ : {st_in.set_name}
"""
    kb = IKM(
        [
            [
                IKB(
                    "sᴛɪᴄᴋᴇʀ ᴘᴀᴄᴋ",
                    url=f"https://t.me/addstickers/{st_in.set_name}",
                )
            ]
        ]
    )
    await m.reply_text(st_to_gib, reply_markup=kb)
    return

 

__mod__ = "sᴛɪᴄᴋᴇʀ" 
__help__ = """
✧ ᴜsᴇʀ ᴄᴏᴍᴍᴀɴᴅs
• /kang : ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ ᴏʀ ᴀɴʏ sᴜᴘᴘᴏʀᴛᴇᴅ ᴍᴇᴅɪᴀ.
• /pkang : ʀᴇᴘʟʏ ᴛᴏ ᴀ ɪᴍᴀɢᴇ ᴛʏᴘᴇ sᴛɪᴄᴋᴇʀ ᴛᴏ ɢᴇᴛ ғᴜʟʟ ᴘᴀᴄᴋ.
• /stickerinfo : ʀᴇᴘʟʏ ᴛᴏ ᴀɴʏ sᴛɪᴄᴋᴇʀ ᴛᴏ ɢᴇᴛ ɪᴛ's ɪɴғᴏ.
• /stickerid : ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ ᴍᴇssᴀɢᴇ ᴛᴏ ɢᴇᴛ ᴛʜᴇ sᴛɪᴄᴋᴇʀ ɪᴅ ᴀɴᴅ ᴇᴍᴏᴊɪ.
• /getsticker : ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ ᴍᴇssᴀɢᴇ ᴛᴏ ɢᴇᴛ ᴛʜᴇ sᴛɪᴄᴋᴇʀ ᴀs ᴀ ᴅᴏᴄᴜᴍᴇɴᴛ.
• /getvideo : ʀᴇᴘʟʏ ᴛᴏ ᴀ ɢɪғ ᴍᴇssᴀɢᴇ ᴛᴏ ɢᴇᴛ ᴛʜᴇ ɢɪғ ᴀs ᴀ vɪᴅᴇᴏ.
• /delsticker : ʀᴇᴘʟʏ ᴛᴏ ᴀ sᴛɪᴄᴋᴇʀ ᴄʀᴇᴀᴛᴇᴅ ʙʏ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ʀᴇᴍᴏᴠᴇ ɪᴛ ғʀᴏᴍ ʏᴏᴜʀ ᴘᴀᴄᴋ.
"""
