from typing import Any

import pytest
from geojson_pydantic.geometries import MultiPolygon, Point

from project.dal import mongo_connection
from project.domain.partner.model import PartnerModel


@pytest.fixture(scope="class", autouse=True)
def db_connection() -> Any:
    mongo_connection.database.partners.drop()
    yield
    mongo_connection.database.partners.drop()


@pytest.fixture()
def partner() -> PartnerModel:
    return PartnerModel(
        trading_name="Adega da Cerveja - Pinheiros",
        owner_name="Zé da Silva",
        document="1432132123891/0001",
        address=Point(coordinates=(-46.57421, -21.785741)),
        coverage_area=MultiPolygon(coordinates=[
            [[(30, 20), (45, 40), (10, 40), (30, 20)]],
            [[(15, 5), (40, 10), (10, 20), (5, 10), (15, 5)]],
        ])
    )
    # return PartnerModel.parse_obj({
    #     "tradingName": "Adega da Cerveja - Pinheiros",
    #     "ownerName": "Zé da Silva",
    #     "document": "1432132123891/0001",
    #     "coverageArea": {
    #         "type": "MultiPolygon",
    #         "coordinates": [
    #             [[[30, 20], [45, 40], [10, 40], [30, 20]]],
    #             [[[15, 5], [40, 10], [10, 20], [5, 10], [15, 5]]],
    #         ],
    #     },
    #     "address": {"type": "Point", "coordinates": [-46.57421, -21.785741]},
    # })

@pytest.fixture()
def partner_json() -> str:
    return """
        {
            "tradingName": "Adega da Cerveja - Pinheiros",
            "ownerName": "Z\u00e9 da Silva",
            "document": "1432132123891/0001",
            "coverageArea": {
                "coordinates": [
                    [[[30.0, 20.0], [45.0, 40.0], [10.0, 40.0], [30.0, 20.0]]],
                    [[[15.0, 5.0], [40.0, 10.0], [10.0, 20.0], [5.0, 10.0], [15.0, 5.0]]
                ]],
                "type": "MultiPolygon"
            },
            "address": {"coordinates": [-46.57421, -21.785741], "type": "Point"}}
    """
