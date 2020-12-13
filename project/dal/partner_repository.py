from typing import Any, Optional, List

from project.dal.mongo_connection import MongoConnection
from project.domain.partner.base_partner_repository import BasePartnerRepository
from project.domain.partner.model import PartnerModel
from bson import ObjectId


class PartnerRepository(BasePartnerRepository):
    def __init__(self, connection: MongoConnection) -> None:
        self.connection = connection

    def insert_partner(self, partner: PartnerModel) -> Any:
        return self.connection.database.partners.insert_one(
            partner.dict(by_alias=True, exclude={"id"})
        )

    def get_partner_by_id(self, partner_id: str) -> Optional[PartnerModel]:
        partner = self.connection.database.partners.find_one(
            {"_id": ObjectId(partner_id)}
        )

        if partner:
            return PartnerModel.parse_obj(partner)
        return None

    def get_partners_by_point_intersection(
        self, long: float, lat: float
    ) -> List[PartnerModel]:
        partners = self.connection.database["partners"].find(
            {
                "coverageArea": {
                    "$geoIntersects": {
                        "$geometry": {"type": "Point", "coordinates": [long, lat]}
                    }
                }
            }
        )

        partner_models: List[PartnerModel] = []

        for partner in partners:
            partner_models.append(PartnerModel.parse_obj(partner))

        return partner_models
