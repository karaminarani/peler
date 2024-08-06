import asyncio

from hydrogram import Client, errors, filters
from hydrogram.helpers import ikb
from hydrogram.types import CallbackQuery, Message

from bot import (
    add_broadcast_data_id,
    authorized_users_only,
    del_broadcast_data_id,
    del_user,
    get_users,
    helper_buttons,
    helper_handlers,
    logger,
)


class BroadcastManager:
    def __init__(self):
        self.is_running = False
        self.sent = 0
        self.failed = 0
        self.total = 0

    async def start_broadcast(
        self, client: Client, message: Message, broadcast_msg: Message
    ) -> None:
        if self.is_running:
            await message.reply_text(
                "<b>Currently, a broadcast is running. Check the status for details.</b>",
                quote=True,
            )
            return

        progress_msg = await message.reply_text(
            "<b>Broadcasting...</b>",
            quote=True,
            reply_markup=ikb(helper_buttons.Broadcast),
        )

        users, admins = await get_users(), helper_handlers.admins
        user_ids = [user for user in users if user not in admins]

        self.is_running, self.total = True, len(user_ids)
        logger.info("Broadcast: Starting...")

        chat_id, message_id = message.chat.id, progress_msg.id
        await add_broadcast_data_id(chat_id, message_id)

        for user_id in user_ids:
            if not self.is_running:
                break

            try:
                await broadcast_msg.copy(
                    user_id, protect_content=helper_handlers.protect_content
                )
                self.sent += 1
            except errors.FloodWait as fw:
                logger.warning(f"FloodWait: Sleep {fw.value}")
                await asyncio.sleep(fw.value)
            except errors.RPCError:
                await del_user(user_id)
                self.failed += 1

            if (self.sent + self.failed) % 250 == 0:
                await self.update_progress(progress_msg)

        await self.finalize_broadcast(message, progress_msg)

    async def update_progress(self, message: Message) -> None:
        await message.edit_text(
            "<b>Broadcast Status</b>:\n"
            f"  - <code>Sent  :</code> {self.sent} - {self.total}\n"
            f"  - <code>Failed:</code> {self.failed}",
            reply_markup=ikb(helper_buttons.Broadcast),
        )

    async def finalize_broadcast(self, message: Message, progress_msg: Message) -> None:
        status_msg = (
            "Broadcast Finished"
            if self.sent + self.failed == self.total
            else "Broadcast Stopped"
        )

        await message.reply_text(
            f"<b>{status_msg}</b>\n"
            f"  - <code>Sent  :</code> {self.sent} - {self.total}\n"
            f"  - <code>Failed:</code> {self.failed}",
            quote=True,
            reply_markup=ikb(helper_buttons.Close),
        )

        logger.info(status_msg)
        await del_broadcast_data_id()
        await progress_msg.delete()

        self.is_running, self.sent, self.failed, self.total = False, 0, 0, 0


broadcast_manager = BroadcastManager()


@Client.on_message(filters.command(["broadcast", "bc"]))
@authorized_users_only
async def broadcast_handler(client: Client, message: Message) -> None:
    broadcast_msg = message.reply_to_message

    if not broadcast_msg:
        if not broadcast_manager.is_running:
            await message.reply_text(
                "<b>Please reply to the message you want to broadcast!</b>",
                quote=True,
            )
        else:
            await message.reply_text(
                "<b>Broadcast Status</b>:\n"
                f"  - <code>Sent  :</code> {broadcast_manager.sent} - {broadcast_manager.total}\n"
                f"  - <code>Failed:</code> {broadcast_manager.failed}",
                quote=True,
                reply_markup=ikb(helper_buttons.Broadcast),
            )
        return

    await broadcast_manager.start_broadcast(client, message, broadcast_msg)


@Client.on_message(filters.command("stop"))
@authorized_users_only
async def stop_broadcast_handler(_, message: Message) -> None:
    if not broadcast_manager.is_running:
        await message.reply_text(
            "<b>No broadcast is currently running!</b>", quote=True
        )
        return

    broadcast_manager.is_running = False
    await message.reply_text("<b>Broadcast has been stopped!</b>", quote=True)


@Client.on_callback_query(filters.regex(r"\bbroadcast\b"))
async def broadcast_handler_query(_, query: CallbackQuery) -> None:
    await query.message.edit_text("<b>Refreshing...</b>")
    await broadcast_manager.update_progress(query.message)
