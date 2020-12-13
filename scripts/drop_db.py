import logging
from project.config import settings

from project.dal.mongo_connection import MongoConnection


def drop_db() -> None:
    connection = MongoConnection(
        db_connection=settings.DB_CONNECTION_STRING, db_name=settings.DB_NAME
    )

    connection.database.partners.drop()
    logging.info("partner database was dropped successfully")


if __name__ == "__main__":
    drop_db()
