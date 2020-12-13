import logging
import os
import json

from project.config import settings

from project.dal.mongo_connection import MongoConnection


def seed_db() -> None:
    connection = MongoConnection(
        db_connection=settings.DB_CONNECTION_STRING, db_name=settings.DB_NAME
    )

    with open(f"{os.path.dirname(__file__)}/resources/pdvs.json", "r") as pdvs:
        pdvs_data = json.load(pdvs)
        connection.database.partners.insert_many(pdvs_data["pdvs"])

    logging.info("partner database was seeded successfully")


if __name__ == "__main__":
    seed_db()
