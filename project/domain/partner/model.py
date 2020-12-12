import uuid
from typing import Any, Union, Generator, Optional

from bson import ObjectId
from geojson_pydantic.geometries import MultiPolygon, Point
from pydantic import BaseModel, Field


class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls) -> Generator[Union[ValueError, ObjectId], None, None]:
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> Union[ValueError, ObjectId]:
        if not ObjectId.is_valid(str(v)):
            return ValueError(f"Not a valid ObjectId: {v}")
        return ObjectId(str(v))


class PartnerModel(BaseModel):
    id: Optional[ObjectIdStr] = Field(default_factory=uuid.uuid4, alias="_id")
    trading_name: str = Field(alias="tradingName")
    owner_name: str = Field(alias="ownerName")
    document: str
    coverageArea: MultiPolygon
    address: Point

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: lambda x: str(x)}
        schema_extra = {
            "example": {
                "tradingName": "Adega da Cerveja - Pinheiros",
                "ownerName": "Zé da Silva",
                "document": "1432132123891/0001",
                "coverageArea": {
                    "type": "MultiPolygon",
                    "coordinates": [
                        [[[30, 20], [45, 40], [10, 40], [30, 20]]],
                        [[[15, 5], [40, 10], [10, 20], [5, 10], [15, 5]]],
                    ],
                },
                "address": {"type": "Point", "coordinates": [-46.57421, -21.785741]},
            }
        }
