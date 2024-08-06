from typing import Optional, Tuple

from bot.base import database
from bot.utils import BOT_ID


async def add_broadcast_data_id(chat_id: int, message_id: int) -> None:
    """
    Adds or updates broadcast data in the database.

    This function deletes any existing broadcast data and then adds new data
    with the provided chat ID and message ID.

    Args:
        chat_id (int): The ID of the chat where the message is sent.
        message_id (int): The ID of the message to broadcast.
    """
    await del_broadcast_data_id()

    broadcast_data = {"chat_id": chat_id, "message_id": message_id}
    await database.add_value(int(BOT_ID), "RESTART_IDS", broadcast_data)


async def del_broadcast_data_id() -> None:
    """
    Clears the broadcast data from the database.
    """
    await database.clear_value(int(BOT_ID), "RESTART_IDS")


async def get_broadcast_data_ids() -> Tuple[Optional[int], Optional[int]]:
    """
    Retrieves the broadcast data from the database.

    Returns:
        Tuple[Optional[int], Optional[int]]:
            A tuple containing the chat ID and message ID. Both values are
            `None` if no broadcast data is found.
    """
    doc = await database.get_doc(int(BOT_ID))

    if doc:
        data = doc.get("RESTART_IDS")
        if isinstance(data, list) and data:
            broadcast_data = data[0]
            chat_id = broadcast_data.get("chat_id")
            message_id = broadcast_data.get("message_id")
        else:
            chat_id, message_id = None, None
    else:
        chat_id, message_id = None, None

    return chat_id, message_id
