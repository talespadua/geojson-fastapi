from random import uniform

from factory import Factory, SubFactory, List
from factory.faker import Faker
from factory.fuzzy import FuzzyText
from geojson_pydantic.geometries import MultiPolygon, Point

from project.domain.partner.model import PartnerModel


class CoverageAreaFactory(Factory):
    class Meta:
        model = MultiPolygon

    type = "MultiPolygon"
    coordinates = List(
        [
            [
                [
                    (uniform(-20.0000, -10.0000), uniform(-70.0000, -60.0000))
                    for _ in range(5)
                ]
            ]
        ]
    )


class AddressFactory(Factory):
    class Meta:
        model = Point

    type = "Point"
    coordinates = (uniform(-20.0000, -10.0000), uniform(-70.0000, -60.0000))


class PartnerFactory(Factory):
    class Meta:
        model = PartnerModel

    _id = FuzzyText(length=21)
    trading_name = Faker("name")
    owner_name = Faker("name")
    document = FuzzyText(length=15)
    coverageArea = SubFactory(CoverageAreaFactory)
    address = SubFactory(AddressFactory)
