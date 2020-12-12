from pymongo import MongoClient


class MongoConnection:
    def __init__(self, db_connection: str, db_name: str) -> None:
        mongodb_client = MongoClient(db_connection)
        self.database = mongodb_client[db_name]
        self.database["partners"].create_index([("document", 1)], unique=True)
