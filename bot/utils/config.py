import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Configuration class that reads environment variables to set various settings.
    """

    def __init__(self):
        self.API_ID: int = int(os.environ.get("API_ID", 2040))
        self.API_HASH: str = os.environ.get(
            "API_HASH", "b18441a1ff607e10a989891a5462e627"
        )
        self.BOT_TOKEN: str = os.environ.get("BOT_TOKEN", "")
        self.OWNER_ID: int = int(os.environ.get("OWNER_ID", 487936750))
        self.MONGODB_URL: str = os.environ.get(
            "MONGODB_URL", "mongodb://root:passwd@mongo"
        )
        self.DATABASE_CHAT_ID: int = int(os.environ.get("DATABASE_CHAT_ID", 0))
        self.OWNER_USERNAME: str = os.environ.get("OWNER_USERNAME", "IlhamTG")

        # Perform validation
        self._validate()

    def _validate(self):
        """
        Validate environment variables to ensure they are correct.
        """
        if not self.BOT_TOKEN:
            raise ValueError("BOT_TOKEN: Missed")


config: Config = Config()
