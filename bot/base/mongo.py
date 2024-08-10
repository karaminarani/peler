from typing import Any, Dict, List, Optional

from async_pymongo import AsyncClient

from bot.utils import config, logger

from .exception import ForceStopLoop


class Database:
    """
    A class to manage MongoDB connections and operations.

    Attributes:
        client (Optional[AsyncClient]): The MongoDB client instance.
        db (Optional[Any]): The database instance.

    Methods:
        connect() -> None:
            Establishes a connection to the MongoDB server.

        close() -> None:
            Closes the MongoDB connection.

        list_docs() -> List[str]:
            Lists all document IDs in the collection.

        get_doc(_id: int) -> Optional[Dict[str, Any]]:
            Retrieves a document by its ID.

        add_value(_id: int, key: str, value: Any) -> None:
            Adds a value to a document's list field.

        del_value(_id: int, key: str, value: Any) -> None:
            Removes a value from a document's list field.

        clear_value(_id: int, key: str) -> None:
            Clears a field in a document.

        del_doc(_id: int) -> None:
            Deletes a document by its ID.
    """

    def __init__(self) -> None:
        """Initializes the Database instance with no active connection."""
        self.client: Optional[AsyncClient] = None
        self.db: Optional[Any] = None

    async def connect(self) -> None:
        """Establishes a connection to the MongoDB server."""
        while not self.client:
            try:
                self.client = AsyncClient(config.MONGODB_URL)
                self.db = self.client["FSUB_DATABASE"]["COLLECTIONS"]
                logger.info("MongoDB: Connected")
            except Exception as exc:
                raise ForceStopLoop(str(exc))

    async def close(self) -> None:
        """Closes the MongoDB connection."""
        if self.client:
            await self.client.close()
            self.client = None
            self.db = None
            logger.info("MongoDB: Closed")
        else:
            logger.info("MongoDB: Already Closed")

    async def list_docs(self) -> List[int]:
        """Lists all document IDs in the collection.

        Returns:
            List[int]: A list of document IDs.
        """
        pipeline = [{"$project": {"_id": 1}}]
        cursor = self.db.aggregate(pipeline)
        return [document["_id"] async for document in cursor]

    async def get_doc(self, _id: int) -> Optional[Dict[str, Any]]:
        """Retrieves a document by its ID.

        Args:
            _id (int): The ID of the document.

        Returns:
            Optional[Dict[str, Any]]: The document, if found.
        """
        document = await self.db.find_one({"_id": _id})
        return document

    async def add_value(self, _id: int, key: str, value: Any) -> None:
        """Adds a value to a document's list field.

        Args:
            _id (int): The ID of the document.
            key (str): The field to which the value will be added.
            value (Any): The value to be added.
        """
        await self.db.update_one({"_id": _id}, {"$addToSet": {key: value}}, upsert=True)

    async def del_value(self, _id: int, key: str, value: Any) -> None:
        """Removes a value from a document's list field.

        Args:
            _id (int): The ID of the document.
            key (str): The field from which the value will be removed.
            value (Any): The value to be removed.
        """
        await self.db.update_one({"_id": _id}, {"$pull": {key: value}})

    async def clear_value(self, _id: int, key: str) -> None:
        """Clears a field in a document.

        Args:
            _id (int): The ID of the document.
            key (str): The field to be cleared.
        """
        await self.db.update_one({"_id": _id}, {"$unset": {key: ""}})

    async def del_doc(self, _id: int) -> None:
        """Deletes a document by its ID.

        Args:
            _id (int): The ID of the document.
        """
        await self.db.delete_one({"_id": _id})


database: Database = Database()
