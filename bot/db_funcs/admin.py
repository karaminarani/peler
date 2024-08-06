from typing import List, Optional

from bot.base import database
from bot.utils import BOT_ID


async def add_admin(chat_id: int) -> None:
    """
    Adds a chat ID to the list of bot administrators.

    Args:
        chat_id (int): The chat ID to add as an administrator.
    """
    await database.add_value(int(BOT_ID), "BOT_ADMINS", chat_id)


async def del_admin(chat_id: int) -> None:
    """
    Removes a chat ID from the list of bot administrators.

    Args:
        chat_id (int): The chat ID to remove from the list of administrators.
    """
    await database.del_value(int(BOT_ID), "BOT_ADMINS", chat_id)


async def get_admins() -> List[int]:
    """
    Retrieves the list of bot administrators.

    Returns:
        List[int]: A list of chat IDs that are administrators.
    """
    doc: Optional[dict] = await database.get_doc(int(BOT_ID))
    # Ensure `BOT_ADMINS` exists in the document and is of the correct type
    return (
        doc.get("BOT_ADMINS", [])
        if doc and isinstance(doc.get("BOT_ADMINS"), list)
        else []
    )
