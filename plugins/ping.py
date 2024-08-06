import time

from hydrogram import Client, filters
from hydrogram.helpers import ikb
from hydrogram.raw import functions
from hydrogram.types import CallbackQuery, Message

from bot import helper_buttons, logger


@Client.on_message(filters.private & filters.command("ping"))
async def ping_handler(client: Client, message: Message) -> None:
    try:
        latency = await ping_function(client)
        await message.reply_text(
            f"<b>Latency:</b> {latency}",
            quote=True,
            reply_markup=ikb(helper_buttons.Ping),
        )
    except Exception as exc:
        logger.error(f"Latency: {exc}")
        await message.reply_text("<b>An Error Occurred!</b>", quote=True)


@Client.on_callback_query(filters.regex(r"\bping\b"))
async def ping_handler_query(client: Client, query: CallbackQuery) -> None:
    await query.message.edit_text("<b>Refreshing...</b>")

    try:
        latency = await ping_function(client)
        await query.message.edit_text(
            f"<b>Latency:</b> {latency}", reply_markup=ikb(helper_buttons.Ping)
        )
    except Exception as exc:
        logger.error(f"Latency: {exc}")
        await query.message.edit_text(
            "<b>An Error Occurred!</b>", reply_markup=ikb(helper_buttons.Ping)
        )


async def ping_function(client: Client) -> str:
    try:
        start_time = time.time()
        await client.invoke(functions.Ping(ping_id=0))
        end_time = time.time()

        # Calculate latency in milliseconds
        latency_ms = (end_time - start_time) * 1000
        return f"{latency_ms:.2f} ms"
    except Exception as exc:
        logger.error(f"Latency: {exc}")
        return "<b>An Error Occurred!</b>"
