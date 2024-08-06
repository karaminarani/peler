from hydrogram import Client, errors, filters
from hydrogram.helpers import ikb
from hydrogram.types import Message

from bot import authorized_users_only, config, logger, url_safe


@Client.on_message(filters.private & filters.command("batch"))
@authorized_users_only
async def batch_handler(client: Client, message: Message) -> None:
    database_chat_id = config.DATABASE_CHAT_ID

    async def ask_for_message_id(ask_msg: str) -> int:
        """
        Ask the user to forward a message from the Database Channel and return the message ID.

        Args:
            ask_msg (str): The prompt message to display to the user.

        Returns:
            int: The ID of the forwarded message, or None if invalid or not received.
        """
        database_ch_link = f"tg://openmessage?chat_id={str(database_chat_id)[4:]}"
        chat_id, user_id = message.chat.id, message.from_user.id

        try:
            ask_message = await client.ask(
                chat_id=chat_id,
                text=f"<b>{ask_msg}:</b>\n  Forward a message from the Database Channel!\n\n<b>Timeout:</b> 45s",
                user_id=user_id,
                timeout=45,
                reply_markup=ikb([[("Database Channel", database_ch_link, "url")]]),
            )
        except errors.ListenerTimeout:
            await message.reply_text(
                "<b>Time limit exceeded! Process has been cancelled.</b>"
            )
            return None

        if (
            not ask_message.forward_from_chat
            or ask_message.forward_from_chat.id != database_chat_id
        ):
            await ask_message.reply_text(
                "<b>Invalid message! Please forward a message from the Database Channel.</b>",
                quote=True,
            )
            return None

        return ask_message.forward_from_message_id

    # Get the start and end message IDs
    first_message_id = await ask_for_message_id("Start")
    if first_message_id is None:
        return

    last_message_id = await ask_for_message_id("End")
    if last_message_id is None:
        return

    # Encode data
    try:
        first_id = first_message_id * abs(database_chat_id)
        last_id = last_message_id * abs(database_chat_id)
        encoded_data = url_safe.encode_data(f"id-{first_id}-{last_id}")
        encoded_data_url = f"https://t.me/{client.me.username}?start={encoded_data}"
        share_encoded_data_url = f"https://t.me/share?url={encoded_data_url}"

        # Send the response
        await message.reply_text(
            encoded_data_url,
            quote=True,
            reply_markup=ikb([[("Share", share_encoded_data_url, "url")]]),
            disable_web_page_preview=True,
        )
    except Exception as exc:
        logger.error(f"Batch: {exc}")
        await message.reply_text("<b>An Error Occurred!</b>", quote=True)
