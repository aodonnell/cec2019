import logging
from typing import Tuple, List

FORMAT = logging.Formatter('%(name)s - %(levelname)s - %(message)s')


def get_logger(name: str, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = logging.StreamHandler()
    handler.setFormatter(FORMAT)
    logger.addHandler(handler)

    return logger


def transform_path(instance, starting_x, starting_y, path: list):

    if starting_x == instance.x_min and starting_y == instance.x_min:
        transformed_path = path
    elif starting_x == instance.x_max and starting_y == instance.y_max:
         transformed_path = path.reverse()
    elif starting_x == instance.x_max and starting_y == instance.y_min:
         transformed_path = [(x, -y) for x, y in path]
    else:
         transformed_path = [(-x, y) for x, y in path]
    
    translated_path = [(x + instance.x_min, y + instance.y_min) for (x,y) in transformed_path]

    return translated_path


Point = Tuple[int, int]


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
