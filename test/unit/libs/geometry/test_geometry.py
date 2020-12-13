from typing import Tuple

import pytest
from project.libs.geometry import euclidean_distance


@pytest.mark.parametrize(
    "point_a,point_b,expected_distance",
    [
        ((1.0, 0.0), (0.0, 0.0), 1.0),
        ((0.0, 0.0), (0.0, -4.0), 4.0),
        ((0.0, 0.0), (0.0, 4.0), 4.0),
    ],
)
def test_euclidean_distance(
    point_a: Tuple[float, float], point_b: Tuple[float, float], expected_distance: float
) -> None:
    assert euclidean_distance(point_a, point_b) == expected_distance
