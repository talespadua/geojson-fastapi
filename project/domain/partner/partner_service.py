from project.libs.geometry import euclidean_distance
from typing import Optional, List, Tuple

from project.domain.partner.base_partner_repository import BasePartnerRepository
from project.domain.partner.model import PartnerModel


class PartnerService:
    def __init__(self, repository: BasePartnerRepository):
        self.repository = repository

    def insert_partner(self, partner: PartnerModel) -> str:
        insert_response = self.repository.insert_partner(partner)
        return str(insert_response.inserted_id)

    def get_partner_by_id(self, partner_id: str) -> Optional[PartnerModel]:
        return self.repository.get_partner_by_id(partner_id)

    def get_nearest_partner_covering_point(
        self, longitude: float, latitude: float
    ) -> Optional[PartnerModel]:
        partners_covering_area = self.repository.get_partners_by_point_intersection(
            long=longitude, lat=latitude
        )

        if len(partners_covering_area) == 0:
            return None

        return self._closest_partner(
            location=(longitude, latitude), partners=partners_covering_area
        )

    def _closest_partner(
        self, location: Tuple[float, float], partners: List[PartnerModel]
    ) -> PartnerModel:
        min_distance = 9999999999999.0
        closest_partner = partners[0]

        for partner in partners:
            distance = euclidean_distance(
                point_a=location,
                point_b=(
                    float(partner.address.coordinates[0]),
                    float(partner.address.coordinates[1]),
                ),
            )

            if distance < min_distance:
                min_distance = distance
                closest_partner = partner

            # if min_distance := distance < min_distance:
            #     closest_partner = partner

        return closest_partner
