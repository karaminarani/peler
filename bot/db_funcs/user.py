from typing import List

from bot.base import database
from bot.utils import BOT_ID


async def add_user(user_id: int) -> None:
    """
    Adds a user ID to the list of bot users in the database.

    Args:
        user_id (int): The ID of the user to add.
    """
    await database.add_value(int(BOT_ID), "BOT_USERS", user_id)


async def del_user(user_id: int) -> None:
    """
    Removes a user ID from the list of bot users in the database.

    Args:
        user_id (int): The ID of the user to remove.
    """
    await database.del_value(int(BOT_ID), "BOT_USERS", user_id)


async def get_users() -> List[int]:
    """
    Retrieves the list of bot users from the database.

    Returns:
        List[int]: A list of user IDs that are associated with the bot.
                   Returns an empty list if no users are found or if the document does not exist.
    """
    doc = await database.get_doc(int(BOT_ID))
    if doc:
        return doc.get("BOT_USERS", [])
    else:
        return []
