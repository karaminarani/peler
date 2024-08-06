from bot.base import database
from bot.utils import BOT_ID


async def add_generate_status(value: bool) -> None:
    """
    Adds or updates the generate URL status in the database.

    Args:
        value (bool): The status to set for generating URLs.
    """
    await database.add_value(int(BOT_ID), "GENERATE_URL", value)


async def del_generate_status() -> None:
    """
    Clears the generate URL status from the database.
    """
    await database.clear_value(int(BOT_ID), "GENERATE_URL")


async def get_generate_status() -> bool:
    """
    Retrieves the current generate URL status from the database.

    Returns:
        bool: The current status of generate URLs.
    """
    doc = await database.get_doc(int(BOT_ID))
    # Assume default value of False if no status is found
    return doc.get("GENERATE_URL", [False])[0]


async def update_generate_status() -> None:
    """
    Toggles the generate URL status in the database.
    """
    current_generate_status = await get_generate_status()
    await del_generate_status()
    await add_generate_status(not current_generate_status)


async def add_protect_content(value: bool) -> None:
    """
    Adds or updates the protect content status in the database.

    Args:
        value (bool): The status to set for protecting content.
    """
    await database.add_value(int(BOT_ID), "PROTECT_CONTENT", value)


async def del_protect_content() -> None:
    """
    Clears the protect content status from the database.
    """
    await database.clear_value(int(BOT_ID), "PROTECT_CONTENT")


async def get_protect_content() -> bool:
    """
    Retrieves the current protect content status from the database.

    Returns:
        bool: The current status of protecting content.
    """
    doc = await database.get_doc(int(BOT_ID))
    # Assume default value of False if no status is found
    return doc.get("PROTECT_CONTENT", [False])[0]


async def update_protect_content() -> None:
    """
    Toggles the protect content status in the database.
    """
    current_protect_content_status = await get_protect_content()
    await del_protect_content()
    await add_protect_content(not current_protect_content_status)
