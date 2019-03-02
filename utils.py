import logging
from typing import Tuple, List, Optional

import instance
from backend import IBackend

FORMAT = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

Point = Tuple[int, int]
Points = List[Point]


def get_logger(name: str, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = logging.StreamHandler()
    handler.setFormatter(FORMAT)
    logger.addHandler(handler)

    return logger


def transform_path(inst: instance.Instance, starting_point: Tuple[int, int], path: list):
    if starting_point[0] == inst.x_min and starting_point[1] == inst.x_min:
        transformed_path = path
    elif starting_point[0] == inst.x_max and starting_point[1] == inst.y_max:
        transformed_path = path[::-1]
    elif starting_point[0] == inst.x_max and starting_point[1] == inst.y_min:
        transformed_path = [(x, -y) for (x, y) in path]
    else:
        transformed_path = [(-x, y) for (x, y) in path]

    translated_path = [(x + inst.x_min, y + inst.y_min) for (x, y) in transformed_path]

    return translated_path


def clamp(value: int, maximum: int):
    return max(0, min(maximum, value))


def points_around(point: Tuple[int, int], radius: int, x_max: int, y_max: int):
    around: List[Point] = []
    for y in range(-radius, radius + 1):
        for x in range(-radius + abs(y), radius - abs(y) + 1):
            around.append((clamp(point[0] + x, x_max), clamp(point[1] + y, y_max)))
    return around


def manhattan_distance(p1: Point, p2: Point):
    return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])


def closest_point(points: List[Point], target: Point) -> Optional[Point]:
    closest: Tuple[int, Point] = None

    for around in points:
        distance = manhattan_distance(around, target)
        if closest and distance >= closest[0]:
            continue

        closest = (distance, around)

    if closest is None:
        return None

    return closest[1]


def dump_garbage(bkend: IBackend, inst: instance.Instance):
    pass
