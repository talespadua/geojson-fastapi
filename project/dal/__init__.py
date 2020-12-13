from project.dal.mongo_connection import MongoConnection
from project.config import settings


mongo_connection = MongoConnection(
    db_connection=settings.DB_CONNECTION_STRING, db_name=settings.DB_NAME
)
