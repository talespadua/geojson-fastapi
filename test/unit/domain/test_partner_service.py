from typing import cast, List, Dict, Any
from unittest.mock import MagicMock

import pytest
from geojson_pydantic.geometries import MultiPolygon, Point

from project.domain.partner.base_partner_repository import BasePartnerRepository
from project.domain.partner.model import PartnerModel
from project.domain.partner.partner_service import PartnerService
from test.helpers.factories.mongo_reponses_factory import InsertResponseFactory
from test.helpers.factories.partner_factory import PartnerFactory


class TestPartnerService:
    @pytest.fixture()
    def repository(self) -> BasePartnerRepository:
        repository = MagicMock()
        repository.insert_partner = MagicMock(
            return_value=InsertResponseFactory.build()
        )
        repository.get_partners_by_point_intersection = MagicMock(return_value=[])
        repository.get_partner_by_id = MagicMock(return_value=PartnerFactory.build())
        return cast(BasePartnerRepository, repository)

    @pytest.fixture()
    def partner_service(self, repository: BasePartnerRepository) -> PartnerService:
        return PartnerService(repository)

    def test_insert_partner(self, partner_service: PartnerService) -> None:
        response = partner_service.insert_partner(PartnerFactory())
        assert isinstance(response, str)

    def test_get_partner_by_id(self, partner_service: PartnerService) -> None:
        response = partner_service.get_partner_by_id("123456789")
        assert isinstance(response, PartnerModel)

    class TestGetNearestPartnerCoveringPoint:
        class TestGivenNoPartnerIsFound:
            def test_returns_none(self, partner_service: PartnerService) -> None:
                response = partner_service.get_nearest_partner_covering_point(
                    longitude=10.0, latitude=10.0
                )
                assert response is None

        class TestGivenValuesWhereFound:
            @pytest.fixture()
            def area_setup(self) -> Dict[str, Any]:
                response = {
                    "near": {
                        "name": "near",
                        "coverage_area": MultiPolygon(
                            coordinates=[
                                [
                                    [
                                        (-44.04982, -19.87743),
                                        (-44.04982, -19.89438),
                                        (-44.04758, -19.89438),
                                        (-44.04758, -19.87743),
                                        (-44.04982, -19.87743),
                                    ]
                                ]
                            ],
                            type="MultiPolygon",
                        ),
                        "address": Point(
                            coordinates=(-44.04925346374511, -19.89383034031159),
                            type="Point",
                        ),
                    },
                    "farther": {
                        "name": "farther",
                        "coverage_area": MultiPolygon(
                            coordinates=[
                                [
                                    [
                                        (-44.051098, -19.893265),
                                        (-44.038825, -19.8932653),
                                        (-44.0388250, -19.890480),
                                        (-44.051098, -19.890480),
                                        (-44.051098, -19.893265),
                                    ]
                                ]
                            ],
                            type="MultiPolygon",
                        ),
                        "address": Point(
                            coordinates=(-44.039876461029046, -19.891509947530643),
                            type="Point",
                        ),
                    },
                }
                return response

            @pytest.fixture()
            def repository(self, area_setup: Dict[str, Any]) -> BasePartnerRepository:
                repository = MagicMock()
                partners = PartnerFactory.build_batch(2)
                partners[0].coverage_area = area_setup["near"]["coverage_area"]
                partners[0].address = area_setup["near"]["address"]
                partners[0].trading_name = area_setup["near"]["name"]

                partners[1].coverage_area = area_setup["farther"]["coverage_area"]
                partners[1].address = area_setup["farther"]["address"]
                partners[1].trading_name = area_setup["farther"]["name"]

                repository.get_partners_by_point_intersection = MagicMock(
                    return_value=partners
                )
                return cast(BasePartnerRepository, repository)

            def test_find_partner_with_in_area_coverage(
                self, partner_service: PartnerService
            ) -> None:
                response = partner_service.get_nearest_partner_covering_point(
                    longitude=-44.0491247177124, latitude=-19.892821478063265
                )

                assert response is not None
                assert response.trading_name == "near"
