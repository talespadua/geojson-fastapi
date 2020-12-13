from typing import Tuple

import pytest
from requests.models import Response
from fastapi.testclient import TestClient

from project.api.main import app
from project.domain.partner.model import PartnerModel

client = TestClient(app)


class TestPartnerRoutes:
    @pytest.fixture()
    def partner_id(self, partner: PartnerModel) -> str:
        return "5fd53ee325a51f5b8631730a"

    @pytest.fixture()
    def get_partner_response(self, partner_id: str) -> Response:
        return client.get(f"/partners/{partner_id}/")

    @pytest.fixture()
    def insert_partner_response(self, partner_json: str) -> Response:
        return client.post("/partners/", data=partner_json)

    @pytest.fixture()
    def search_partner_response(self, location: Tuple[float, float]) -> Response:
        return client.get(f"/partners/search?long={location[0]}&lat={location[1]}")

    class TestGivenThereIsNoPartner:
        class TestWhenFetchingPartner:
            def test_should_return_returns_404(
                self, get_partner_response: Response
            ) -> None:
                assert get_partner_response.status_code == 404

        class TestWhenInsertingPartner:
            def test_partner_is_inserted(
                self, insert_partner_response: Response
            ) -> None:
                assert insert_partner_response.status_code == 201

        class TestWhenSearchingByLocation:
            @pytest.fixture()
            def location(self) -> Tuple[float, float]:
                return -46.57421, -21.785741

            def test_should_return_404(self, search_partner_response: Response) -> None:
                assert search_partner_response.status_code == 404

    class TestGivenThereIsPartners:
        class TestWhenInsertingNewPartner:
            @pytest.fixture()
            def partner_id(self, insert_partner_response: Response) -> str:
                return insert_partner_response.text.strip('"')

            def test_should_find_inserted_partner(
                self, get_partner_response: Response
            ) -> None:
                assert get_partner_response.status_code == 200

        class TestWhenInsertingExistingPartner:
            def test_should_raise_409(self, partner_json: str) -> None:
                response = client.post("/partners/", data=partner_json)
                assert response.status_code == 201

                response = client.post("/partners/", data=partner_json)
                assert response.status_code == 409

        class TestWhenSearchingForNearPartnerCoveringLocation:
            @pytest.fixture()
            def location(self) -> Tuple[float, float]:
                return 29.311523, 24.006326

            def test_should_return_partner(
                self,
                insert_partner_response: Response,
                search_partner_response: Response,
            ) -> None:
                assert insert_partner_response.status_code == 201
                assert search_partner_response.status_code == 200


# class TestThereIsOverlappingAreas:
#     def test_there_is_overlapping_areas(self) -> None:
#         from scripts.seed_db import seed_db
#         from project.dal import mongo_connection
#         from project.dal.partner_repository import PartnerRepository
#
#         repository = PartnerRepository(mongo_connection)
#
#         seed_db()
#         max_found = 0
#         coordinates = []
#         partners = mongo_connection.database.partners.find({})
#         dal = PartnerRepository(mongo_connection)
#
#         for p in partners:
#
#             near_partners = repository.get_partners_by_point_intersection(
#                 long=p["address"]["coordinates"][0],
#                 lat=p["address"]["coordinates"][1],
#             )
#
#             number_of_partners = len(near_partners)
#             if number_of_partners > max_found:
#                 max_found = number_of_partners
#                 parter_within = p
#                 coordinates = [
#                     p["address"]["coordinates"][0],
#                     p["address"]["coordinates"][1],
#                 ]
#
#         pass
