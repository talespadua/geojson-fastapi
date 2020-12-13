from math import sqrt
from typing import Tuple


def euclidean_distance(
    point_a: Tuple[float, float], point_b: Tuple[float, float]
) -> float:
    return sqrt((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2)
