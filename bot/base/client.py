import asyncio

from hydrogram import Client, errors
from hydrogram.enums import ParseMode
from hydrogram.types import BotCommand, BotCommandScopeAllPrivateChats

from bot.utils import BOT_ID, config, logger

from .exception import ForceStopLoop
from .mongo import database

# Attempt to use uvloop for the event loop if available
try:
    import uvloop

    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    logger.info("Uvloop: Set Event Loop")
except ImportError:
    pass


class Bot(Client):
    """
    A class representing the Telegram bot.

    Methods:
        start() -> None:
            Starts the bot and connects to MongoDB.

        stop() -> None:
            Stops the bot and closes the MongoDB connection.

        bot_commands_setup() -> None:
            Sets up bot commands for users.
    """

    def __init__(self) -> None:
        """
        Initializes the Bot instance with required configurations.
        """
        super().__init__(
            name=str(BOT_ID),
            api_id=int(config.API_ID),
            api_hash=str(config.API_HASH),
            bot_token=str(config.BOT_TOKEN),
            plugins=dict(root="plugins"),
            workdir="./sessions/",
        )

    async def start(self) -> None:
        """
        Starts the bot, connecting to MongoDB and setting up commands.
        """
        logger.info("MongoDB: Connecting...")
        await database.connect()

        logger.info("Bot: Starting...")
        try:
            await super().start()
            logger.info("Bot: Started")
        except errors.RPCError as rpc:
            raise ForceStopLoop(str(rpc.MESSAGE))

        await self.bot_commands_setup()
        self.set_parse_mode(ParseMode.HTML)

    async def stop(self) -> None:
        """
        Stops the bot, closes the HTTP session and MongoDB connection.
        """
        logger.info("Bot: Stopping...")
        try:
            await super().stop()
        except Exception as exc:
            logger.error(str(exc))
        else:
            logger.info("Bot: Stopped")

        logger.info("MongoDB: Closing...")
        await database.close()

    async def bot_commands_setup(self) -> None:
        """
        Sets up the bot commands for user interaction.
        """
        await self.delete_bot_commands()
        try:
            await self.set_bot_commands(
                commands=[
                    BotCommand("start", "Start Bot"),
                    BotCommand("ping", "Server Latency"),
                    BotCommand("uptime", "Bot Uptime"),
                    BotCommand("privacy", "Privacy Policy"),
                ],
                scope=BotCommandScopeAllPrivateChats(),
            )
        except errors.RPCError:
            pass


# Instantiate the bot
bot: Bot = Bot()
