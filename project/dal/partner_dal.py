from typing import Any, Optional

from project.dal.mongo_connection import MongoConnection
from project.domain.partner.model import PartnerModel
from bson import ObjectId


class PartnerDAL:
    def __init__(self, connection: MongoConnection) -> None:
        self.connection = connection

    def insert_partner(self, partner: PartnerModel) -> Any:
        return self.connection.database["partners"].insert_one(partner.dict())

    def get_partner_by_id(self, partner_id: str) -> Optional[PartnerModel]:
        partner = self.connection.database["partners"].find_one(
            {"_id": ObjectId(partner_id)}
        )

        if partner:
            return PartnerModel.parse_obj(partner)
        return None
