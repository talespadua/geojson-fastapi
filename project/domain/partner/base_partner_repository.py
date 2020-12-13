from abc import ABC, abstractmethod
from typing import List, Optional, Any

from project.domain.partner.model import PartnerModel


class BasePartnerRepository(ABC):
    @abstractmethod
    def insert_partner(self, partner: PartnerModel) -> Any:
        ...

    @abstractmethod
    def get_partner_by_id(self, partner_id: str) -> Optional[PartnerModel]:
        ...

    @abstractmethod
    def get_partners_by_point_intersection(
        self, long: float, lat: float
    ) -> List[PartnerModel]:
        ...
