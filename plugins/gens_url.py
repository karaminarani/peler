from hydrogram import Client, filters
from hydrogram.helpers import ikb
from hydrogram.types import Message

from bot import authorized_users_only, config, helper_handlers, logger, url_safe
from plugins import list_available_commands


@Client.on_message(
    filters.private & ~filters.me & ~filters.command(list_available_commands)
)
@authorized_users_only
async def generate_handler(client: Client, message: Message) -> None:
    # Check generate status
    if not helper_handlers.generate_status:
        return

    try:
        # Copy the message to the database chat
        database_chat_id = config.DATABASE_CHAT_ID
        message_db = await message.copy(database_chat_id)

        # Encode message ID
        encoded_data = url_safe.encode_data(
            f"id-{message_db.id * abs(database_chat_id)}"
        )
        encoded_data_url = f"https://t.me/{client.me.username}?start={encoded_data}"

        # Create a shareable URL
        share_encoded_data_url = f"https://t.me/share/url?url={encoded_data_url}"

        # Reply to the user with the generated URL
        await message.reply_text(
            encoded_data_url,
            quote=True,
            reply_markup=ikb([[("Share", share_encoded_data_url, "url")]]),
            disable_web_page_preview=True,
        )
    except Exception as exc:
        # Log the error and inform the user
        logger.error(f"Generator: {exc}")
        await message.reply_text("<b>An Error Occurred!</b>", quote=True)
