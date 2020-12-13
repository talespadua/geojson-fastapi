from typing import Tuple

import pytest
from requests.models import Response
from fastapi.testclient import TestClient

from project.api.main import app

client = TestClient(app)


class TestPartnerRoutes:
    @pytest.fixture()
    def partner_id(self) -> str:
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
                return -44.014835357666016, -19.90638004921044

            def test_should_return_partner(
                self,
                insert_partner_response: Response,
                search_partner_response: Response,
            ) -> None:
                assert insert_partner_response.status_code == 201
                assert search_partner_response.status_code == 200
