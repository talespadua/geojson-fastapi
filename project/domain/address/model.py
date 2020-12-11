from geojson_pydantic.geometries import Point
from pydantic import BaseModel


class Address(BaseModel):
    type: Point
