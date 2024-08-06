from bot.base import database
from bot.utils import BOT_ID


async def add_force_text_msg(value: str) -> None:
    """
    Adds or updates the force text message in the database.

    Args:
        value (str): The force text message to set.
    """
    await database.add_value(int(BOT_ID), "FORCE_TEXT", value)


async def del_force_text_msg() -> None:
    """
    Clears the force text message from the database.
    """
    await database.clear_value(int(BOT_ID), "FORCE_TEXT")


async def get_force_text_msg() -> str:
    """
    Retrieves the current force text message from the database.

    Returns:
        str: The force text message. Defaults to an empty string if not set.
    """
    doc = await database.get_doc(int(BOT_ID))
    return doc.get("FORCE_TEXT", [""])[0] if doc else ""


async def update_force_text_msg(value: str) -> None:
    """
    Updates the force text message in the database.

    This function first deletes the existing force text message and then
    adds the new message.

    Args:
        value (str): The new force text message to set.
    """
    await del_force_text_msg()
    await add_force_text_msg(value)


async def add_start_text_msg(value: str) -> None:
    """
    Adds or updates the start text message in the database.

    Args:
        value (str): The start text message to set.
    """
    await database.add_value(int(BOT_ID), "START_TEXT", value)


async def del_start_text_msg() -> None:
    """
    Clears the start text message from the database.
    """
    await database.clear_value(int(BOT_ID), "START_TEXT")


async def get_start_text_msg() -> str:
    """
    Retrieves the current start text message from the database.

    Returns:
        str: The start text message. Defaults to an empty string if not set.
    """
    doc = await database.get_doc(int(BOT_ID))
    return doc.get("START_TEXT", [""])[0] if doc else ""


async def update_start_text_msg(value: str) -> None:
    """
    Updates the start text message in the database.

    This function first deletes the existing start text message and then
    adds the new message.

    Args:
        value (str): The new start text message to set.
    """
    await del_start_text_msg()
    await add_start_text_msg(value)
