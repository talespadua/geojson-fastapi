import uuid

from geojson_pydantic.geometries import MultiPolygon
from pydantic import BaseModel, Field

from project.domain.address.model import Address


class Partner(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    trading_name: str = Field(alias="tradingName")
    owner_name: str = Field(alias="ownerName")
    document: str
    coverageArea: MultiPolygon
    address: Address
