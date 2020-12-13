from factory import Factory
from factory.fuzzy import FuzzyText
from pymongo.results import InsertOneResult


class InsertResponseFactory(Factory):
    class Meta:
        model = InsertOneResult

    inserted_id = FuzzyText(length=21)
    acknowledged = True
