from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant, ChatAdminRequired, InviteHashExpired
from Devine import app  
from config import OWNER_ID as BOT_OWNER_ID

@app.on_message(filters.command("unbanme"))
async def unbanme(client, message):
    try:
        if message.from_user.id != BOT_OWNER_ID:
            await message.reply_text("Only the bot owner can use this command.")
            return

        if len(message.command) < 2:
            await message.reply_text("Please provide the group ID.")
            return

        group_id = message.command[1]

        try:
            await client.unban_chat_member(group_id, message.from_user.id)

            try:
                member = await client.get_chat_member(group_id, message.from_user.id)
                if member.status == "member":
                    await message.reply_text(f"You've already been unbanned! Use this link to rejoin: {await get_group_link(client, group_id)}")
                    return
            except UserNotParticipant:
                pass  

            try:
                group_link = await get_group_link(client, group_id)
                await message.reply_text(f"You've been unbanned! Click here to rejoin: {group_link}")
            except InviteHashExpired:
                await message.reply_text("You've been unbanned, but I couldn't fetch the invite link.")
        except ChatAdminRequired:
            await message.reply_text("I lack the necessary permissions to unban users in that group.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")

async def get_group_link(client, group_id):
    chat = await client.get_chat(group_id)
    if chat.username:
        return f"https://t.me/{chat.username}"
    else:
        invite_link = await client.export_chat_invite_link(group_id)
        return invite_link

