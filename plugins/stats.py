import datetime

from hydrogram import Client, filters
from hydrogram.helpers import ikb
from hydrogram.types import CallbackQuery, Message

from bot import (
    authorized_users_only,
    config,
    get_users,
    helper_buttons,
    helper_handlers,
    logger,
)

startup_date = datetime.datetime.now()


@Client.on_message(
    filters.private & filters.user(config.OWNER_ID) & filters.command("log")
)
async def log_handler(_, message: Message) -> None:
    await message.reply_document("logs.txt", quote=True)


@Client.on_message(filters.private & filters.command("users"))
@authorized_users_only
async def users_handler(_, message: Message) -> None:
    counting_message = await message.reply_text("<b>Counting...</b>", quote=True)

    try:
        all_users = await get_users()
        bot_users = [user for user in all_users if user not in helper_handlers.admins]

        msg_users = (
            "<b>Bot Users:</b>\n"
            f"  - <code>Users :</code> {len(bot_users)}\n"
            f"  - <code>Admins:</code> {len(helper_handlers.admins)}\n\n"
            f"<b>Total:</b> {len(all_users)} Users"
        )
        await counting_message.edit_text(msg_users)
    except Exception as exc:
        logger.error(f"Users: {exc}")
        await counting_message.edit_text("<b>An Error Occurred!</b>")


@Client.on_message(filters.private & filters.command("uptime"))
async def uptime_handler(_, message: Message) -> None:
    uptime_text = uptime_func()

    await message.reply_text(
        uptime_text, quote=True, reply_markup=ikb(helper_buttons.Uptime)
    )


@Client.on_callback_query(filters.regex(r"\buptime\b"))
async def uptime_handler_query(_, query: CallbackQuery) -> None:
    await query.message.edit_text("<b>Refreshing...</b>")

    uptime_text = uptime_func()
    await query.message.edit_text(uptime_text, reply_markup=ikb(helper_buttons.Uptime))


def uptime_func() -> str:
    total_seconds = (datetime.datetime.now() - startup_date).total_seconds()
    converted_str = convert_seconds(total_seconds)

    date_str = startup_date.strftime("%B %d, %Y at %I:%M %p")
    msg_text = (
        "<b>Bot Uptime:</b>\n"
        f"  - <code>Since:</code> {date_str}\n"
        f"  - <code>Total:</code> {converted_str}"
    )

    return msg_text


def convert_seconds(seconds: int) -> str:
    weeks, remainder = divmod(seconds, 7 * 24 * 60 * 60)
    days, remainder = divmod(remainder, 24 * 60 * 60)
    hours, remainder = divmod(remainder, 60 * 60)
    minutes, seconds = divmod(remainder, 60)

    result_converted = []
    if weeks > 0:
        result_converted.append(f"{int(weeks)} Week{'s' if weeks > 1 else ''}")
    if days > 0:
        result_converted.append(f"{int(days)} Day{'s' if days > 1 else ''}")
    if hours > 0:
        result_converted.append(f"{int(hours)} Hour{'s' if hours > 1 else ''}")
    if minutes > 0:
        result_converted.append(f"{int(minutes)} Minute{'s' if minutes > 1 else ''}")
    if seconds > 0:
        result_converted.append(f"{int(seconds)} Second{'s' if seconds > 1 else ''}")

    # Limit to two components, prioritizing larger units first
    return ", ".join(result_converted[:2])
