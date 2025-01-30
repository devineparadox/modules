from typing import Callable

from pyrogram.enums import ChatMemberStatus
from pyrogram.types import Message

from config import OWNER_ID as GRADE1  # Ensure OWNER_ID is an integer
from Devine import app


def can_restrict(func: Callable) -> Callable:
    async def non_admin(_, message: Message):
        if message.from_user.id == GRADE1:  # Compare as an integer
            return await func(_, message)

        check = await app.get_chat_member(message.chat.id, message.from_user.id)
        if check.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR]:
            return await message.reply_text("You're not an admin.")

        admin = check.privileges
        if admin and admin.can_restrict_members:
            return await func(_, message)
        else:
            return await message.reply_text(
                "You don't have permissions to restrict users in this chat."
            )

    return non_admin
