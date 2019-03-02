import logging
from typing import Tuple

import dataclasses

FORMAT = logging.Formatter('%(name)s - %(levelname)s - %(message)s')


def get_logger(name: str, level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = logging.StreamHandler()
    handler.setFormatter(FORMAT)
    logger.addHandler(handler)

    return logger


Point = Tuple[int, int]


def clamp(value: int, maximum: int):
    return max(0, min(maximum, value))


def points_around(point: Tuple[int, int], radius: int, x_max: int, y_max: int):
    for y in range(-radius, radius + 1):
        for x in range(-radius + abs(y), radius - abs(y) + 1):
            # if x == 0 and y == 0:
            #     continue

            yield [(clamp(point[0] + x, x_max), clamp(point[1] + y, y_max))]
