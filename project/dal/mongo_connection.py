from pymongo import MongoClient, GEOSPHERE


class MongoConnection:
    def __init__(self, db_connection: str, db_name: str) -> None:
        mongodb_client = MongoClient(db_connection)
        self.database = mongodb_client[db_name]
        self.database.partners.create_index([("document", 1)], unique=True)
        # self.database.partners.create_index([("coverageArea", GEOSPHERE)])
        # self.database.partners.create_index([("address", GEOSPHERE)])
