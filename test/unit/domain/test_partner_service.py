from typing import cast
from unittest.mock import MagicMock

import pytest

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
        repository.get_partner_by_id = MagicMock(return_value=PartnerFactory.build())
        repository.get_nearest_partner_covering_point = MagicMock(
            return_value=PartnerFactory.build_batch(4)
        )
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
            @pytest.fixture()
            def repository(self) -> BasePartnerRepository:
                repository = MagicMock()
                repository.get_nearest_partner_covering_point = MagicMock(
                    return_value=[]
                )
                return cast(BasePartnerRepository, repository)

            def test_returns_none(self, partner_service: PartnerService) -> None:
                response = partner_service.get_nearest_partner_covering_point(
                    longitude=10.0, latitude=10.0
                )
                assert response is None

        class TestGivenValuesWhereFound:
            @pytest.fixture()
            def repository(self) -> BasePartnerRepository:
                repository = MagicMock()
                repository.get_nearest_partner_covering_point = MagicMock(
                    return_value=[]
                )
                return cast(BasePartnerRepository, repository)
