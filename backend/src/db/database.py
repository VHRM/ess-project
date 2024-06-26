from typing import List, Dict
from uuid import uuid4
from pymongo import MongoClient, errors
from pymongo.collection import Collection, IndexModel
from src.config.config import env
from logging import INFO, WARNING, getLogger

logger = getLogger('uvicorn')

class Database():

    ID_LENGTH = 8

    def __init__(self):
        self.db = None
        self.connect()


    def connect(self):
        try:
            mongo_connection = MongoClient(env.DB_URL)

            logger.setLevel(INFO)

            self.db = mongo_connection[env.DB_NAME]

            print("--------------------")
            logger.info("MongoDB connected!")
            logger.info(f"Server Version: {mongo_connection.server_info()['version']}")
            print("--------------------")


        except errors.ServerSelectionTimeoutError as err:

            mongo_connection = None
            logger.setLevel(WARNING)
            logger.info(f"MongoDB connection error! {err}")

    def close_connection(self):
        print("--------------------")
        logger.info("MongoDB connection closed!")
        print("--------------------")
        self.db.client.close()

    def get_db(self):
        return self.db


    def create_collection(
        self,
        name: str,
        indexes: List[IndexModel] = [],
        validation_schema: Dict = {}
    ) -> Collection:
        """
        Create a collection

        Parameters
        - name : str
            The name of the collection to create
        - indexes : List[IndexModel]
            The indexes to create in the collection
        - validation_schema : dict
            The validation schema used to validate data inserted into the
            collection. It should be a dictionary representing a JSON Schema

        Returns
        - pymongo.collection.Collection
            The created collection

        Raises
        - TypeError: If indexes is not a list of pymongo.IndexModel

        """

        collection_options = { "validator": { "$jsonSchema": validation_schema } }

        collection: Collection = self.db.create_collection(
            name,
            **collection_options
        )

        collection.create_indexes(indexes)

        logger.info(f"Collection {name} created!")

        return collection

    def drop_collection(self, name) -> bool:
        """
        Drop a collection

        Parameters
        - name : str
            The name of the collection to drop

        Returns
        - bool
            True if the collection was dropped successfully, False otherwise

        """

        if name in self.db.list_collection_names():
            self.db.drop_collection(name)
            logger.info(f"Collection {name} dropped!")
            return True

        return False

    def get_all_items(self, collection_name: str) -> list:
        """
        Get all items from a collection

        Parameters:
        - collection_name: str
            The name of the collection

        Returns:
        - list
            A list of all items in the collection

        """

        collection: Collection = self.db[collection_name]

        items = list(collection.find({}, {"_id": 0}))

        return items
    
    def get_items_by_field(self, collection_name: str, field: str, value: any) -> List[dict]:
        """
        Retrieve items from a collection by a specific field and value

        Parameters
        - collection_name: str
            The name of the collection to query
        - field: str
            The field name to filter by
        - value: Any
            The value to filter by

        Returns:
        - list:
            A list of items that match the field and value

        """
        collection: Collection = self.db[collection_name]

        items = list(collection.find({field: value}, {"_id": 0}))

        return items


    def get_item_by_id(self, collection_name: str, item_id: str) -> dict:
        """
        Retrieve an item by its ID from a collection

        Parameters:
        - collection_name: str
            The name of the collection where the item will be stored
        - item_id: str
            The ID of the item to retrieve

        Returns:
        - dict or None:
            The item if found, None otherwise

        """
        collection: Collection = self.db[collection_name]

        item = collection.find_one({"id": str(item_id)}, {"_id": 0})
        return item

    def insert_item(self, collection_name: str, item: dict) -> dict:
        """
        Insert an item into a collection

        Parameters:
        - collection_name: str
            The name of the collection where the item will be stored
        - item: dict
            The item to insert

        Returns:
        - dict:
            The inserted item

        """
        # TODO: test if this method works

        item["id"] = str(uuid4())[:self.ID_LENGTH]

        collection: Collection = self.db[collection_name]

        item_id = collection.insert_one(item).inserted_id
        return {
            "id": str(item_id),
            **item
        }

    def update_item(self, collection_name: str, item_id: str, item: dict) -> dict:
        """
        Update an item in a collection

        Parameters:
        - collection_name: str
            The name of the collection where the item is stored
        - item_id: str
            The ID of the item to update
        - item: dict
            New item data

        Returns:
        - dict:
            The updated item, or None if the item was not found

        """
        collection: Collection = self.db[collection_name]

        result = collection.update_one({"id": item_id}, {"$set": item})

        if result.matched_count == 0:
            raise ValueError(f"Item with id {item_id} not found in collection {collection_name}")

        updated_item = collection.find_one({"id": item_id})
        return updated_item

    def delete_item(self, collection_name: str, item_id: str) -> list:
        """
        Delete an item from a collection

        Parameters:
        - collection_name: str
            The name of the collection where the item is stored
        - item_id: str
            The ID of the item to delete

        Returns:
        - bool:
            True if the item was deleted successfully, False otherwise

        """
        collection: Collection = self.db[collection_name]

        result = collection.delete_one({"id": item_id})

        if result.deleted_count == 0:
            raise ValueError(f"Item with id {item_id} not found in collection {collection_name}")

        remaining_items = list(collection.find())
        return remaining_items
